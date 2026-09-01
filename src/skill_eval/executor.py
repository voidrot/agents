"""Provider-neutral Pydantic AI execution in a controlled attempt workspace."""

# pyright: reportMissingImports=false
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path

from pydantic_ai import Agent
from pydantic_ai.exceptions import AgentRunError, ToolRetryError, UsageLimitExceeded
from pydantic_ai.usage import UsageLimits

from .harness import AttemptWorkspace, HarnessError, SkillSnapshot
from .providers import ResolvedModel
from .suites import CapabilityProfile, EvalCaseSpec


@dataclass(frozen=True)
class ExecutionRequest:
    """Everything that varies per model/case/condition/repetition attempt."""

    model: ResolvedModel
    case: EvalCaseSpec
    condition: str
    skill_snapshot: SkillSnapshot
    workspace: AttemptWorkspace
    profile: CapabilityProfile


@dataclass(frozen=True)
class ExecutionResult:
    """A normalized result suitable for persistence independent of provider wire format."""

    status: str
    transcript: str | None
    raw_messages_json: str | None
    input_tokens: int | None
    output_tokens: int | None
    tool_calls: int
    error: dict[str, str] | None = None


class ToolSandbox:
    """Filesystem-only tools that enforce an attempt's capability profile."""

    def __init__(self, workspace: AttemptWorkspace, profile: CapabilityProfile) -> None:
        self.workspace = workspace
        self.profile = profile
        self.tool_calls = 0

    def read_file(self, path: str) -> str:
        """Read a UTF-8 input or skill file by a virtual inputs/ or skill/ path."""
        self._take_tool_call()
        root, relative = self._read_root(path)
        target = self._contained_path(root, relative)
        if not target.is_file():
            raise HarnessError(f"readable file does not exist: {path}")
        if target.stat().st_size > self.profile.max_output_bytes:
            raise HarnessError(f"readable file exceeds profile limit: {path}")
        return target.read_text(encoding="utf-8")

    def write_output(self, path: str, content: str) -> str:
        """Write a UTF-8 output file by a relative path below the output directory."""
        self._take_tool_call()
        target = self._contained_path(self.workspace.output_directory, Path(path))
        encoded = content.encode("utf-8")
        previous_size = target.stat().st_size if target.is_file() else 0
        total_size = self._output_size() - previous_size + len(encoded)
        if total_size > self.profile.max_output_bytes:
            raise HarnessError(f"writing {path} exceeds the profile output limit")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(encoded)
        return f"wrote {len(encoded)} bytes to {target.relative_to(self.workspace.output_directory)}"

    def _take_tool_call(self) -> None:
        if self.tool_calls >= self.profile.max_tool_calls:
            raise HarnessError("attempt exceeded its tool-call profile limit")
        self.tool_calls += 1

    def _read_root(self, path: str) -> tuple[Path, Path]:
        virtual_path = Path(path)
        if virtual_path.is_absolute() or not virtual_path.parts:
            raise HarnessError("read paths must begin with inputs/ or skill/")
        root_name, *relative_parts = virtual_path.parts
        roots = {
            "inputs": self.workspace.input_directory,
            "skill": self.workspace.skill_directory,
        }
        try:
            root = roots[root_name]
        except KeyError as error:
            raise HarnessError(
                "read paths must begin with inputs/ or skill/"
            ) from error
        return root, Path(*relative_parts)

    @staticmethod
    def _contained_path(root: Path, relative: Path) -> Path:
        if relative.is_absolute() or ".." in relative.parts:
            raise HarnessError("filesystem paths must remain inside their virtual root")
        target = (root / relative).resolve()
        if not target.is_relative_to(root.resolve()):
            raise HarnessError("filesystem paths must remain inside their virtual root")
        return target

    def _output_size(self) -> int:
        return sum(
            path.stat().st_size
            for path in self.workspace.output_directory.rglob("*")
            if path.is_file() and not path.is_symlink()
        )


class PydanticAIExecutor:
    """Execute one portable attempt using a configured Pydantic AI model."""

    async def run(self, request: ExecutionRequest) -> ExecutionResult:
        sandbox = ToolSandbox(request.workspace, request.profile)
        agent = Agent(
            request.model.model,
            instructions=_instructions(request),
            retries=0,
        )

        @agent.tool_plain(name="read_file")
        def read_file(path: str) -> str:
            """Read an allowed input or skill resource."""
            return sandbox.read_file(path)

        @agent.tool_plain(name="write_output")
        def write_output(path: str, content: str) -> str:
            """Write a UTF-8 output file within this attempt's output directory."""
            return sandbox.write_output(path, content)

        usage_limits = UsageLimits(
            request_limit=max(1, request.profile.max_tool_calls + 1),
            tool_calls_limit=request.profile.max_tool_calls,
        )

        try:
            async with asyncio.timeout(request.profile.timeout_seconds):
                result = await agent.run(request.case.prompt, usage_limits=usage_limits)
        except TimeoutError:
            return _failure(
                "timeout", "attempt exceeded profile timeout", sandbox.tool_calls
            )
        except UsageLimitExceeded as error:
            return _failure("failed", str(error), sandbox.tool_calls)
        except (HarnessError, OSError, ValueError) as error:
            return _failure("failed", str(error), sandbox.tool_calls)
        except (AgentRunError, ToolRetryError) as error:
            return _failure(
                "failed", str(error), sandbox.tool_calls, type(error).__name__
            )

        usage = result.usage
        return ExecutionResult(
            status="succeeded",
            transcript=str(result.output),
            raw_messages_json=result.all_messages_json().decode("utf-8"),
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            tool_calls=sandbox.tool_calls,
        )


def _instructions(request: ExecutionRequest) -> str:
    shared = """You are executing one isolated skill evaluation. Work only through the supplied filesystem tools.
- Read declared fixtures as inputs/<relative path>.
- Read bundled skill resources as skill/<relative path> only when the condition permits skill access.
- Write all deliverables through write_output using output-relative paths.
- Do not claim an output exists unless you wrote it.
"""
    if request.condition == "without_skill":
        return f"{shared}\nNo skill instructions are available for this condition."
    if request.condition == "with_metadata_only":
        return (
            f"{shared}\nSkill metadata:\n"
            f"name: {request.skill_snapshot.skill.name}\n"
            f"description: {request.skill_snapshot.skill.description}"
        )
    if request.condition == "with_full_skill":
        return (
            f"{shared}\nSkill name: {request.skill_snapshot.skill.name}\n"
            f"Skill instructions:\n{request.skill_snapshot.skill.body}"
        )
    raise HarnessError(f"unknown evaluation condition: {request.condition}")


def _failure(
    status: str,
    message: str,
    tool_calls: int,
    error_type: str = "ExecutionError",
) -> ExecutionResult:
    return ExecutionResult(
        status=status,
        transcript=None,
        raw_messages_json=None,
        input_tokens=None,
        output_tokens=None,
        tool_calls=tool_calls,
        error={"type": error_type, "message": message},
    )

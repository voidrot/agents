"""Temporary-workspace skill-discovery checks for supported coding-agent CLIs."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from .skills import SkillDefinition
from .suites import ResolvedSuite

NativeRuntime = Literal["claude", "codex", "pi", "opencode"]


class NativeRouteError(RuntimeError):
    """Raised when a native runtime cannot be invoked."""


@dataclass(frozen=True)
class NativeRouteResult:
    case_id: str
    status: str
    output: str
    used_skill: bool


_LAYOUTS: dict[NativeRuntime, Path] = {
    "claude": Path(".claude/skills"),
    "codex": Path(".agents/skills"),
    "pi": Path(".pi/skills"),
    "opencode": Path(".opencode/skills"),
}


def run_native_route_check(
    *,
    runtime: NativeRuntime,
    skill: SkillDefinition,
    suite: ResolvedSuite,
    timeout_seconds: int = 120,
) -> list[NativeRouteResult]:
    """Run suite prompts in a disposable workspace using one runtime's discovery path."""
    executable = shutil.which(runtime)
    if executable is None:
        raise NativeRouteError(f"{runtime} executable was not found on PATH")
    with tempfile.TemporaryDirectory(
        prefix="skill-eval-native-"
    ) as temporary_directory:
        root = Path(temporary_directory)
        target = root / _LAYOUTS[runtime] / skill.name
        shutil.copytree(skill.directory, target, symlinks=False)
        results: list[NativeRouteResult] = []
        for case in suite.suite.cases:
            command = _command(runtime, executable, case.prompt)
            try:
                completed = subprocess.run(
                    command,
                    cwd=root,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    timeout=timeout_seconds,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                results.append(
                    NativeRouteResult(
                        case.id, "timeout", "native runtime timed out", False
                    )
                )
                continue
            output = completed.stdout[-20_000:]
            results.append(
                NativeRouteResult(
                    case.id,
                    "succeeded" if completed.returncode == 0 else "failed",
                    output,
                    _trace_uses_skill(output),
                )
            )
        return results


def _command(runtime: NativeRuntime, executable: str, prompt: str) -> list[str]:
    if runtime == "claude":
        return [executable, "-p", "--output-format", "stream-json", "--verbose", prompt]
    if runtime == "codex":
        return [executable, "exec", "--json", prompt]
    if runtime == "pi":
        return [executable, "-p", "--mode", "json", prompt]
    return [executable, "run", "--format", "json", prompt]


def _trace_uses_skill(output: str) -> bool:
    """Recognize trace markers for Skill invocation or SKILL.md access."""
    return '"Skill"' in output or "SKILL.md" in output

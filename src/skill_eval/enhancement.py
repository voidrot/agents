"""Opt-in, reviewable skill-revision proposals."""

# pyright: reportMissingImports=false
from __future__ import annotations

import tempfile
from dataclasses import dataclass
from difflib import unified_diff
from pathlib import Path

from pydantic import BaseModel, Field
from pydantic_ai import Agent

from .providers import ResolvedModel
from .skills import SkillValidationError, validate_skill


class EnhancementError(ValueError):
    """Raised when a candidate is unsafe or cannot be validated."""


class EnhancementProposal(BaseModel):
    """The only model-produced data accepted by the candidate workflow."""

    skill_md: str = Field(min_length=1)
    rationale: str = Field(min_length=1)


@dataclass(frozen=True)
class ProposedSkill:
    """A validated, reviewable model proposal; never an applied change."""

    skill_md: str
    rationale: str


async def propose_skill_revision(
    *, model: ResolvedModel, source_skill_md: str, failure_summary: str
) -> ProposedSkill:
    """Request a complete revised SKILL.md without granting filesystem tools."""
    agent = Agent(model.model, output_type=EnhancementProposal, retries=0)
    prompt = f"""Propose a complete replacement SKILL.md for the skill below.
Preserve valid YAML frontmatter and improve only the instructions needed to address
these evaluation findings. Do not mention this request or invent unavailable tools.

Evaluation findings:
{failure_summary or "No grader failures were recorded; improve clarity conservatively."}

Current SKILL.md:
{source_skill_md}
"""
    try:
        result = await agent.run(prompt)
    except Exception as error:
        raise EnhancementError(f"enhancer proposal failed: {error}") from error
    proposal = result.output
    try:
        _validate_skill_markdown(proposal.skill_md)
    except SkillValidationError as error:
        raise EnhancementError(
            f"enhancer proposed invalid SKILL.md: {error}"
        ) from error
    return ProposedSkill(skill_md=proposal.skill_md, rationale=proposal.rationale)


def skill_markdown_diff(source: str, candidate: str) -> str:
    """Render a reviewable, deterministic unified diff for candidate application."""
    return "".join(
        unified_diff(
            source.splitlines(keepends=True),
            candidate.splitlines(keepends=True),
            fromfile="SKILL.md (current)",
            tofile="SKILL.md (candidate)",
        )
    )


def apply_skill_markdown(*, skill_directory: Path, source: str, candidate: str) -> None:
    """Replace only an unchanged SKILL.md after the caller has confirmed the diff."""
    skill_file = skill_directory.expanduser().resolve() / "SKILL.md"
    if not skill_file.is_file():
        raise EnhancementError(f"SKILL.md not found in: {skill_file.parent}")
    if skill_file.read_text(encoding="utf-8") != source:
        raise EnhancementError(
            "current SKILL.md differs from the candidate's source; refusing to overwrite it"
        )
    _validate_skill_markdown(candidate)
    skill_file.write_text(candidate, encoding="utf-8")


def _validate_skill_markdown(content: str) -> None:
    """Validate a candidate in an isolated temporary directory."""
    with tempfile.TemporaryDirectory(prefix="skill-eval-candidate-") as directory:
        root = Path(directory)
        (root / "SKILL.md").write_text(content, encoding="utf-8")
        validate_skill(root, strict=False)

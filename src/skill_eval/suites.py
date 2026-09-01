"""Versioned, portable evaluation-suite and capability-profile contracts."""

# pyright: reportMissingImports=false, reportMissingModuleSource=false
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

ConditionName = Literal["without_skill", "with_metadata_only", "with_full_skill"]


def _default_conditions() -> list[ConditionName]:
    return ["without_skill", "with_full_skill"]


class SuiteError(ValueError):
    """Raised when an evaluation suite cannot be parsed safely."""


class AssertionSpec(BaseModel):
    """A deterministic assertion supported by the first evaluator milestone."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    type: Literal["file_exists", "contains"]
    path: Path
    text: str | None = None

    @field_validator("path")
    @classmethod
    def require_relative_output_path(cls, path: Path) -> Path:
        if path.is_absolute() or ".." in path.parts:
            raise ValueError(
                "assertion paths must remain relative to the attempt output directory"
            )
        return path

    @model_validator(mode="after")
    def validate_expected_text(self) -> AssertionSpec:
        if self.type == "contains" and not self.text:
            raise ValueError("contains assertions require non-empty text")
        if self.type == "file_exists" and self.text is not None:
            raise ValueError("file_exists assertions must not include text")
        return self


class EvalCaseSpec(BaseModel):
    """One immutable task prompt with fixtures and deterministic assertions."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    partition: Literal["train", "holdout"] = "holdout"
    prompt: str = Field(min_length=1)
    fixtures: list[Path] = Field(default_factory=list)
    assertions: list[AssertionSpec] = Field(default_factory=list)

    @field_validator("id")
    @classmethod
    def require_stable_case_id(cls, value: str) -> str:
        if value != value.strip() or any(character.isspace() for character in value):
            raise ValueError("case ids must be stable, non-whitespace identifiers")
        return value


class CapabilityProfile(BaseModel):
    """A controlled harness profile available to every executor and condition."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str
    allow_network: bool
    max_tool_calls: int = Field(ge=0)
    max_output_bytes: int = Field(gt=0)
    timeout_seconds: int = Field(gt=0)
    output_directory: Path


RESTRICTED_FILESYSTEM_V1 = CapabilityProfile(
    id="restricted-filesystem-v1",
    allow_network=False,
    max_tool_calls=12,
    max_output_bytes=1_000_000,
    timeout_seconds=120,
    output_directory=Path("output"),
)
_PROFILES = {RESTRICTED_FILESYSTEM_V1.id: RESTRICTED_FILESYSTEM_V1}


class EvalSuite(BaseModel):
    """The portable evaluation matrix, independent of provider transport."""

    model_config = ConfigDict(extra="forbid")

    schema_version: Literal[1] = 1
    capability_profile: str = RESTRICTED_FILESYSTEM_V1.id
    conditions: list[ConditionName] = Field(default_factory=_default_conditions)
    repetitions: int = Field(default=1, ge=1)
    seed: int = 42
    executors: list[str] = Field(min_length=1)
    grader: str | None = None
    cases: list[EvalCaseSpec] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_matrix(self) -> EvalSuite:
        if "without_skill" not in self.conditions:
            raise ValueError("conditions must include the without_skill baseline")
        if len(set(self.conditions)) != len(self.conditions):
            raise ValueError("conditions must not contain duplicates")
        case_ids = [case.id for case in self.cases]
        if len(set(case_ids)) != len(case_ids):
            raise ValueError("case ids must be unique within a suite")
        if len(set(self.executors)) != len(self.executors):
            raise ValueError("executor aliases must not contain duplicates")
        return self


@dataclass(frozen=True)
class ResolvedSuite:
    """A validated suite plus its source location and immutable content hash."""

    path: Path
    base_directory: Path
    suite: EvalSuite
    source_yaml: str
    sha256: str
    fixture_paths: dict[str, tuple[Path, ...]]


def resolve_capability_profile(profile_id: str) -> CapabilityProfile:
    """Return a built-in profile, rejecting unknown profiles before execution."""
    try:
        return _PROFILES[profile_id]
    except KeyError as error:
        raise SuiteError(f"unknown capability profile: {profile_id}") from error


def load_suite(path: Path) -> ResolvedSuite:
    """Load a YAML suite and resolve all declared fixtures within its directory."""
    suite_path = path.expanduser().resolve()
    if not suite_path.is_file():
        raise SuiteError(f"evaluation suite does not exist: {suite_path}")
    try:
        content = suite_path.read_text(encoding="utf-8")
        payload = yaml.safe_load(content)
    except (OSError, yaml.YAMLError) as error:
        raise SuiteError(
            f"could not read evaluation suite {suite_path}: {error}"
        ) from error
    if not isinstance(payload, dict):
        raise SuiteError("evaluation suite root must be a YAML mapping")

    try:
        suite = EvalSuite.model_validate(payload)
    except Exception as error:
        raise SuiteError(f"invalid evaluation suite {suite_path}: {error}") from error
    resolve_capability_profile(suite.capability_profile)

    base_directory = suite_path.parent
    fixture_paths = {
        case.id: tuple(
            _resolve_fixture(base_directory, fixture) for fixture in case.fixtures
        )
        for case in suite.cases
    }
    return ResolvedSuite(
        path=suite_path,
        base_directory=base_directory,
        suite=suite,
        source_yaml=content,
        sha256=hashlib.sha256(content.encode("utf-8")).hexdigest(),
        fixture_paths=fixture_paths,
    )


def _resolve_fixture(base_directory: Path, fixture: Path) -> Path:
    if fixture.is_absolute():
        raise SuiteError(f"fixture path must be relative: {fixture}")
    resolved = (base_directory / fixture).resolve()
    if not resolved.is_relative_to(base_directory):
        raise SuiteError(f"fixture path escapes the suite directory: {fixture}")
    if not resolved.exists():
        raise SuiteError(f"fixture does not exist: {fixture}")
    return resolved

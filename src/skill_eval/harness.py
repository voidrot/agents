"""Skill snapshots and isolated filesystem workspaces for portable attempts."""

# pyright: reportMissingImports=false
from __future__ import annotations

import hashlib
import shutil
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from .persistence import ExperimentRepository
from .skills import SkillDefinition, SkillValidationError, validate_skill
from .suites import CapabilityProfile, EvalCaseSpec, ResolvedSuite, load_suite


class HarnessError(RuntimeError):
    """Raised when a skill snapshot or isolated attempt workspace is unsafe."""


@dataclass(frozen=True)
class SkillSnapshot:
    """A deterministic inventory of a validated skill directory."""

    skill: SkillDefinition
    manifest: dict[str, str]
    sha256: str


@dataclass(frozen=True)
class ArtifactData:
    """A bounded output artifact captured before an isolated workspace is removed."""

    path: str
    content: bytes
    sha256: str
    media_type: str | None


@dataclass(frozen=True)
class AttemptWorkspace:
    """Paths that an executor may use within one isolated attempt."""

    root: Path
    skill_directory: Path
    input_directory: Path
    output_directory: Path


def snapshot_skill(skill_directory: Path) -> SkillSnapshot:
    """Validate and hash every regular file in a skill without following symlinks."""
    try:
        skill = validate_skill(skill_directory, strict=True)
    except SkillValidationError as error:
        raise HarnessError(str(error)) from error

    manifest: dict[str, str] = {}
    for path in sorted(skill.directory.rglob("*")):
        if not path.is_file():
            continue
        if path.is_symlink():
            raise HarnessError(
                f"skill contains unsupported symbolic link: {path.relative_to(skill.directory)}"
            )
        relative = path.relative_to(skill.directory).as_posix()
        manifest[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    if "SKILL.md" not in manifest:
        raise HarnessError("skill snapshot is missing SKILL.md")

    manifest_content = "".join(
        f"{path}\0{digest}\n" for path, digest in manifest.items()
    )
    return SkillSnapshot(
        skill=skill,
        manifest=manifest,
        sha256=hashlib.sha256(manifest_content.encode("utf-8")).hexdigest(),
    )


@contextmanager
def rehydrated_replay_sources(
    repository: ExperimentRepository,
    *,
    experiment_id: str,
    skill_snapshot_id: str,
) -> Iterator[tuple[ResolvedSuite, SkillSnapshot]]:
    """Materialize persisted replay inputs without reading mutable original paths."""
    experiment = repository.get_experiment(experiment_id)
    suite_yaml = experiment.get("suite_yaml")
    if not isinstance(suite_yaml, str):
        raise HarnessError("experiment predates persisted replay-suite snapshots")
    with tempfile.TemporaryDirectory(
        prefix="skill-eval-replay-"
    ) as temporary_directory:
        root = Path(temporary_directory)
        suite_file = root / "suite.yaml"
        suite_file.write_text(suite_yaml, encoding="utf-8")
        for artifact in repository.list_input_artifacts(experiment_id):
            _write_replay_file(root, str(artifact["path"]), bytes(artifact["content"]))
        skill_directory = root / "skill"
        resources = repository.list_skill_resources(skill_snapshot_id)
        if not resources:
            raise HarnessError("experiment predates persisted skill-resource snapshots")
        for resource in resources:
            _write_replay_file(
                skill_directory, str(resource["path"]), bytes(resource["content"])
            )
        yield load_suite(suite_file), snapshot_skill(skill_directory)


def _write_replay_file(root: Path, relative_path: str, content: bytes) -> None:
    target = (root / relative_path).resolve()
    if not target.is_relative_to(root.resolve()) or relative_path.startswith("/"):
        raise HarnessError(f"persisted replay path is unsafe: {relative_path}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


@contextmanager
def isolated_workspace(
    *,
    skill_snapshot: SkillSnapshot,
    suite: ResolvedSuite,
    case: EvalCaseSpec,
) -> Iterator[AttemptWorkspace]:
    """Yield a short-lived workspace containing copied skill and declared fixtures only."""
    with tempfile.TemporaryDirectory(prefix="skill-eval-") as temporary_directory:
        root = Path(temporary_directory)
        skill_directory = root / "skill"
        input_directory = root / "inputs"
        output_directory = root / "output"
        _copy_tree_without_links(skill_snapshot.skill.directory, skill_directory)
        input_directory.mkdir()
        output_directory.mkdir()
        for fixture in suite.fixture_paths[case.id]:
            relative = fixture.relative_to(suite.base_directory)
            _copy_path_without_links(fixture, input_directory / relative)
        yield AttemptWorkspace(
            root=root,
            skill_directory=skill_directory,
            input_directory=input_directory,
            output_directory=output_directory,
        )


def collect_artifacts(
    workspace: AttemptWorkspace,
    profile: CapabilityProfile,
) -> list[ArtifactData]:
    """Capture regular files below output, rejecting links and aggregate size overflow."""
    artifacts: list[ArtifactData] = []
    total_bytes = 0
    for path in sorted(workspace.output_directory.rglob("*")):
        if not path.is_file():
            continue
        if path.is_symlink():
            raise HarnessError(
                f"attempt output contains unsupported symbolic link: {path.name}"
            )
        content = path.read_bytes()
        total_bytes += len(content)
        if total_bytes > profile.max_output_bytes:
            raise HarnessError(
                f"attempt output exceeds {profile.max_output_bytes} byte profile limit"
            )
        relative = path.relative_to(workspace.output_directory).as_posix()
        artifacts.append(
            ArtifactData(
                path=relative,
                content=content,
                sha256=hashlib.sha256(content).hexdigest(),
                media_type=_media_type(path),
            )
        )
    return artifacts


def _copy_tree_without_links(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True)
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source)
        target = destination / relative
        if path.is_symlink():
            raise HarnessError(
                f"symbolic links are not allowed in an attempt workspace: {relative}"
            )
        if path.is_dir():
            target.mkdir(exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def _copy_path_without_links(source: Path, destination: Path) -> None:
    if source.is_symlink():
        raise HarnessError(f"fixture symbolic links are not supported: {source}")
    if source.is_dir():
        _copy_tree_without_links(source, destination)
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def _media_type(path: Path) -> str | None:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt", ".json", ".yaml", ".yml", ".csv"}:
        return "text/plain"
    return None

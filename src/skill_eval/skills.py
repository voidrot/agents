"""Skill validation, safe resource discovery, and deterministic packaging."""

from __future__ import annotations

import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml  # pyright: ignore[reportMissingModuleSource]


class SkillValidationError(ValueError):
    """Raised when a skill does not satisfy the portable skill contract."""


@dataclass(frozen=True)
class SkillDefinition:
    """Validated frontmatter and body of a skill directory."""

    directory: Path
    name: str
    description: str
    frontmatter: dict[str, Any]
    body: str


_FRONTMATTER_PATTERN = re.compile(
    r"\A---\s*\n(?P<yaml>.*?)\n---\s*\n?(?P<body>.*)\Z", re.DOTALL
)
_ALLOWED_FRONTMATTER = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}
_EXCLUDED_DIRECTORY_NAMES = {".git", "__pycache__", "node_modules"}
_ROOT_EXCLUDED_DIRECTORY_NAMES = {"evals"}
_EXCLUDED_FILE_NAMES = {".DS_Store"}


def validate_skill(skill_directory: Path, *, strict: bool = False) -> SkillDefinition:
    """Read and validate the required `SKILL.md` frontmatter."""
    directory = skill_directory.expanduser().resolve()
    if not directory.is_dir():
        raise SkillValidationError(f"skill directory does not exist: {directory}")

    skill_file = directory / "SKILL.md"
    if not skill_file.is_file():
        raise SkillValidationError(f"SKILL.md not found in: {directory}")

    try:
        content = skill_file.read_text(encoding="utf-8")
    except OSError as error:
        raise SkillValidationError(f"could not read {skill_file}: {error}") from error

    match = _FRONTMATTER_PATTERN.match(content)
    if match is None:
        raise SkillValidationError(
            "SKILL.md must start with YAML frontmatter delimited by ---"
        )

    try:
        frontmatter = yaml.safe_load(match.group("yaml"))
    except yaml.YAMLError as error:
        raise SkillValidationError(f"invalid YAML frontmatter: {error}") from error
    if not isinstance(frontmatter, dict):
        raise SkillValidationError("frontmatter must be a YAML mapping")

    unexpected = set(frontmatter) - _ALLOWED_FRONTMATTER
    if unexpected:
        names = ", ".join(sorted(unexpected))
        raise SkillValidationError(f"unexpected frontmatter field(s): {names}")

    name = _require_text(frontmatter, "name")
    description = _require_text(frontmatter, "description")
    _validate_name(name)
    _validate_description(description)
    _validate_compatibility(frontmatter.get("compatibility"))

    if strict:
        _validate_referenced_paths(directory, match.group("body"))

    return SkillDefinition(
        directory=directory,
        name=name,
        description=description,
        frontmatter=frontmatter,
        body=match.group("body"),
    )


def _require_text(frontmatter: dict[str, Any], key: str) -> str:
    value = frontmatter.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SkillValidationError(
            f"frontmatter field {key!r} must be a non-empty string"
        )
    return value.strip()


def _validate_name(name: str) -> None:
    if len(name) > 64:
        raise SkillValidationError("frontmatter name must be at most 64 characters")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise SkillValidationError("frontmatter name must use lowercase kebab-case")


def _validate_description(description: str) -> None:
    if len(description) > 1024:
        raise SkillValidationError(
            "frontmatter description must be at most 1024 characters"
        )
    if "<" in description or ">" in description:
        raise SkillValidationError(
            "frontmatter description must not contain angle brackets"
        )


def _validate_compatibility(value: Any) -> None:
    if value is not None and (not isinstance(value, str) or len(value) > 500):
        raise SkillValidationError(
            "frontmatter compatibility must be a string of at most 500 characters"
        )


def _validate_referenced_paths(directory: Path, body: str) -> None:
    """Reject inline relative links escaping the skill root in strict mode."""
    for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", body):
        if "://" in target or target.startswith("#"):
            continue
        target_path = (directory / target.split("#", maxsplit=1)[0]).resolve()
        if not target_path.is_relative_to(directory):
            raise SkillValidationError(f"skill reference escapes skill root: {target}")


def package_skill(skill_directory: Path, output_directory: Path | None = None) -> Path:
    """Create a deterministic `.skill` archive after validating the skill."""
    skill = validate_skill(skill_directory)
    output_directory = (output_directory or Path.cwd()).expanduser().resolve()
    output_directory.mkdir(parents=True, exist_ok=True)
    archive_path = output_directory / f"{skill.name}.skill"

    files = sorted(
        path
        for path in skill.directory.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and not _should_exclude(path, skill.directory)
    )
    try:
        with zipfile.ZipFile(
            archive_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as archive:
            for file_path in files:
                entry = zipfile.ZipInfo.from_file(
                    file_path, file_path.relative_to(skill.directory.parent)
                )
                entry.date_time = (1980, 1, 1, 0, 0, 0)
                archive.writestr(
                    entry, file_path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED
                )
    except OSError as error:
        raise SkillValidationError(f"could not package skill: {error}") from error
    return archive_path


def _should_exclude(path: Path, directory: Path) -> bool:
    relative = path.relative_to(directory)
    if path.name in _EXCLUDED_FILE_NAMES or path.suffix == ".pyc":
        return True
    if any(part in _EXCLUDED_DIRECTORY_NAMES for part in relative.parts):
        return True
    return bool(relative.parts and relative.parts[0] in _ROOT_EXCLUDED_DIRECTORY_NAMES)

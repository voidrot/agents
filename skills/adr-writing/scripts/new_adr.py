#!/usr/bin/env python3
"""Create a safe, Nygard-style Architecture Decision Record."""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

ADR_FILENAME = re.compile(r"^(\d{4})-.+\.md$")
MAX_SEQUENCE = 9999


def error(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 1


def find_repo_root(start: Path) -> Path | None:
    """Return the nearest ancestor identified as a Git repository."""
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def slugify(title: str) -> str:
    normalized = unicodedata.normalize("NFKD", title)
    ascii_title = normalized.encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", ascii_title)).strip("-")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the next non-overwriting Nygard-style ADR under docs/adrs."
    )
    parser.add_argument("--title", required=True, help="ADR title; used for its heading and filename slug")
    parser.add_argument(
        "--repo-root",
        type=Path,
        help="Repository root (default: discover from the current directory)",
    )
    return parser.parse_args()


def template(title: str) -> str:
    return f"""# {title}

## Status

Proposed

## Context

<!-- What forces, constraints, and alternatives make this decision necessary? -->

## Decision

<!-- What is being decided? -->

## Consequences

<!-- What becomes easier, harder, or required as a result? -->
"""


def main() -> int:
    args = parse_args()
    title = args.title.strip()
    if not title:
        return error("--title must not be empty")
    if len(title) > 160:
        return error("--title must be 160 characters or fewer")
    if any(ord(character) < 32 or ord(character) == 127 for character in title):
        return error("--title must not contain control characters or line breaks")

    slug = slugify(title)
    if not slug:
        return error("--title must produce a non-empty ASCII kebab-case slug")
    if len(slug) > 120:
        return error("--title produces a slug longer than 120 characters")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        return error("generated slug is not valid kebab-case")

    if args.repo_root is not None:
        repo_root = args.repo_root.expanduser().resolve()
        if not repo_root.is_dir():
            return error(f"--repo-root is not a directory: {repo_root}")
    else:
        repo_root = find_repo_root(Path.cwd().resolve())
        if repo_root is None:
            return error("could not discover a repository root; pass --repo-root")

    adr_directory = repo_root / "docs" / "adrs"
    try:
        resolved_directory = adr_directory.resolve()
        resolved_directory.relative_to(repo_root.resolve())
        resolved_directory.mkdir(parents=True, exist_ok=True)
    except (OSError, ValueError) as exc:
        return error(f"cannot use ADR directory {adr_directory}: {exc}")

    numbers = []
    try:
        for entry in resolved_directory.iterdir():
            match = ADR_FILENAME.match(entry.name)
            if entry.is_file() and match:
                numbers.append(int(match.group(1)))
    except OSError as exc:
        return error(f"cannot inspect ADR directory {resolved_directory}: {exc}")

    next_number = max(numbers, default=0) + 1
    if next_number > MAX_SEQUENCE:
        return error("ADR sequence is exhausted at 9999")

    output = resolved_directory / f"{next_number:04d}-{slug}.md"
    try:
        with output.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(template(title))
    except FileExistsError:
        return error(f"refusing to overwrite existing ADR: {output}")
    except OSError as exc:
        return error(f"cannot create ADR {output}: {exc}")

    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())

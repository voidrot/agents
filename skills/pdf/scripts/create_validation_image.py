#!/usr/bin/env python3
"""Overlay form-field bounding boxes on a rendered PDF page image."""

import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw  # pyright: ignore[reportMissingImports]


def create_validation_image(
    page_number: int,
    fields_json_path: Path,
    input_path: Path,
    output_path: Path,
) -> int:
    """Create a validation image and return the number of boxes drawn."""
    try:
        data = json.loads(fields_json_path.read_text(encoding="utf-8"))
        with Image.open(input_path) as image:
            draw = ImageDraw.Draw(image)
            box_count = 0
            for field in data["form_fields"]:
                if field["page_number"] != page_number:
                    continue
                draw.rectangle(field["entry_bounding_box"], outline="red", width=2)
                draw.rectangle(field["label_bounding_box"], outline="blue", width=2)
                box_count += 2
            image.save(output_path)
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
        raise ValueError(f"could not create validation image: {error}") from error
    return box_count


def main() -> int:
    if len(sys.argv) != 5:
        print(
            "Usage: create_validation_image.py PAGE FIELDS_JSON INPUT_IMAGE OUTPUT_IMAGE",
            file=sys.stderr,
        )
        return 2
    try:
        page_number = int(sys.argv[1])
    except ValueError:
        print(f"error: invalid page number: {sys.argv[1]}", file=sys.stderr)
        return 2
    try:
        box_count = create_validation_image(
            page_number,
            Path(sys.argv[2]),
            Path(sys.argv[3]),
            Path(sys.argv[4]),
        )
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"Created validation image at {sys.argv[4]} with {box_count} bounding boxes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""GitHub Action entrypoint for README Arcade."""

from __future__ import annotations

import os
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from render import render_assets


def optional_input(name: str) -> str | None:
    value = os.environ.get(name, "").strip()
    return value or None


def write_action_outputs(paths: list[Path]) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return

    light = next((path for path in paths if not path.stem.endswith("-dark")), None)
    dark = next((path for path in paths if path.stem.endswith("-dark")), None)
    with Path(output_file).open("a", encoding="utf-8") as handle:
        if light:
            handle.write(f"light-svg={light.as_posix()}\n")
        if dark:
            handle.write(f"dark-svg={dark.as_posix()}\n")


def main() -> None:
    user = optional_input("INPUT_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "README"
    seed = optional_input("INPUT_SEED") or datetime.now(UTC).date().isoformat()
    config = optional_input("INPUT_CONFIG") or "readme-arcade.config.json"
    out_dir = optional_input("INPUT_OUTPUT_DIR") or "dist"

    written = render_assets(
        config_path=Path(config),
        out_dir=Path(out_dir),
        user_override=user,
        mode_override=optional_input("INPUT_MODE"),
        speed_override=optional_input("INPUT_SPEED"),
        base_name_override=optional_input("INPUT_BASE_NAME"),
        seed_override=seed,
        token=optional_input("INPUT_GITHUB_TOKEN"),
    )
    for path in written:
        print(f"wrote {path}")
    write_action_outputs(written)


if __name__ == "__main__":
    main()

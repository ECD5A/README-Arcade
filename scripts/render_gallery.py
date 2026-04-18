#!/usr/bin/env python3
"""Render all built-in modes into dist/gallery."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from readme_arcade.config import load_config
from readme_arcade.github import fetch_calendar
from readme_arcade.modes import lifegrid, pacman, snake


GALLERY_MODES = {
    "lifegrid": lifegrid.render,
    "snake": snake.render,
    "pacman": pacman.render,
}


def main() -> None:
    config = load_config(Path("readme-arcade.config.json"))
    user = os.environ.get("README_ARCADE_USER") or str(config.get("user") or "README")
    calendar = fetch_calendar(user, os.environ.get("GITHUB_TOKEN"))
    out_dir = Path("dist") / "gallery"

    for mode_name, renderer in GALLERY_MODES.items():
        gallery_config = dict(config)
        gallery_config["output"] = dict(config.get("output", {}))
        gallery_config["output"]["baseName"] = mode_name
        written = renderer(user, gallery_config, calendar, out_dir)
        for path in written:
            print(f"wrote {path}")


if __name__ == "__main__":
    main()

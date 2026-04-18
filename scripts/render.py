#!/usr/bin/env python3
"""Render README Arcade SVG assets."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from readme_arcade.config import load_config
from readme_arcade.github import fetch_calendar
from readme_arcade.modes import defrag, lifegrid, matrix, snake


MODES = {
    "lifegrid": lifegrid.render,
    "snake": snake.render,
    "matrix": matrix.render,
    "defrag": defrag.render,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render README Arcade SVG assets.")
    parser.add_argument("--config", default="readme-arcade.config.json", help="Path to JSON config.")
    parser.add_argument("--out-dir", default="dist", help="Output directory.")
    parser.add_argument("--user", default=None, help="Override the configured GitHub user/login.")
    parser.add_argument("--mode", default=None, help="Override the configured mode.")
    parser.add_argument("--base-name", default=None, help="Override output base name.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(Path(args.config))
    user = args.user or os.environ.get("README_ARCADE_USER") or str(config.get("user") or "README")
    mode = args.mode or str(config.get("mode") or "lifegrid")
    if args.base_name:
        config.setdefault("output", {})["baseName"] = args.base_name

    renderer = MODES.get(mode)
    if not renderer:
        available = ", ".join(sorted(MODES))
        raise SystemExit(f"unknown mode {mode!r}; available modes: {available}")

    calendar = fetch_calendar(user, os.environ.get("GITHUB_TOKEN"))
    written = renderer(user, config, calendar, Path(args.out_dir))
    for path in written:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()

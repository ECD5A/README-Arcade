#!/usr/bin/env python3
"""Render README Arcade SVG assets."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from readme_arcade.config import SPEED_PRESETS, load_config, output_base_name
from readme_arcade.github import fetch_calendar
from readme_arcade.modes import defrag, lifegrid, matrix, snake


MODES = {
    "lifegrid": lifegrid.render,
    "snake": snake.render,
    "matrix": matrix.render,
    "defrag": defrag.render,
}


def render_assets(
    *,
    config_path: Path,
    out_dir: Path,
    user_override: str | None = None,
    mode_override: str | None = None,
    speed_override: str | None = None,
    base_name_override: str | None = None,
    seed_override: str | None = None,
    token: str | None = None,
) -> list[Path]:
    """Render one configured mode and return the generated SVG paths."""
    config = load_config(config_path)
    user = user_override or os.environ.get("README_ARCADE_USER") or str(config.get("user") or "README")
    mode = mode_override or str(config.get("mode") or "lifegrid")
    if speed_override:
        speed = speed_override.lower()
        if speed not in SPEED_PRESETS:
            available = ", ".join(SPEED_PRESETS)
            raise ValueError(f"unknown speed {speed!r}; available speeds: {available}")
        config["speed"] = speed
        for mode_name, duration in SPEED_PRESETS[speed].items():
            config.setdefault(mode_name, {})["duration"] = duration
    if base_name_override:
        config.setdefault("output", {})["baseName"] = base_name_override
    seed = seed_override or os.environ.get("README_ARCADE_SEED")
    if seed:
        config.setdefault("snake", {})["seed"] = seed
    output_base_name(config)

    renderer = MODES.get(mode)
    if not renderer:
        available = ", ".join(sorted(MODES))
        raise ValueError(f"unknown mode {mode!r}; available modes: {available}")

    calendar = fetch_calendar(user, token)
    return renderer(user, config, calendar, out_dir)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render README Arcade SVG assets.")
    parser.add_argument("--config", default="readme-arcade.config.json", help="Path to JSON config.")
    parser.add_argument("--out-dir", default="dist", help="Output directory.")
    parser.add_argument("--user", default=None, help="Override the configured GitHub user/login.")
    parser.add_argument("--mode", default=None, help="Override the configured mode.")
    parser.add_argument("--speed", default=None, help="Override the configured speed preset.")
    parser.add_argument("--base-name", default=None, help="Override output base name.")
    parser.add_argument("--seed", default=None, help="Override the animation route seed.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        written = render_assets(
            config_path=Path(args.config),
            out_dir=Path(args.out_dir),
            user_override=args.user,
            mode_override=args.mode,
            speed_override=args.speed,
            base_name_override=args.base_name,
            seed_override=args.seed,
            token=os.environ.get("GITHUB_TOKEN"),
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    for path in written:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()

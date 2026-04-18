"""Hashwave mode."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from readme_arcade.grid_svg import base_grid, layout, write_theme_svgs
from readme_arcade.modes.common import login_grid, stable_byte
from readme_arcade.themes import THEMES


WAVE_COLORS = {
    "dark": {
        "scan": "#facc15",
        "edge": "#58a6ff",
    },
    "light": {
        "scan": "#bf8700",
        "edge": "#0969da",
    },
}


def render_hash_frame(
    user: str,
    theme: dict[str, str],
    colors: dict[str, str],
    width: int,
    height: int,
    frame: int,
) -> list[list[str]]:
    grid = base_grid(theme, width, height)
    scan_x = (frame * 2) % (width + 10) - 5
    epoch = frame // 4

    for y in range(height):
        for x in range(width):
            digest = stable_byte(user, f"hashwave:{epoch}:{x}:{y}")
            wave = (digest + (x * 5) + (y * 11) + (frame * 3)) % 32
            level = 1 + ((wave // 8) % 4)

            if abs(x - scan_x) <= 1:
                grid[y][x] = colors["scan"] if (x + y + frame) % 3 == 0 else theme["level4"]
            elif abs(x - scan_x) == 2:
                grid[y][x] = colors["edge"]
            else:
                grid[y][x] = theme[f"level{level}"]

    return grid


def build_frames(user: str, options: dict[str, Any], theme_name: str) -> list[list[list[str]]]:
    theme = THEMES[theme_name]
    colors = WAVE_COLORS[theme_name]
    box = layout(options)
    width = box["width"]
    height = box["height"]
    frames = int(options.get("frames", 120))
    intro_frames = min(max(1, int(options.get("holdFrames", 12))), frames - 1)

    rendered: list[list[list[str]]] = [login_grid(user, width, height, theme, "hashwave-name") for _ in range(intro_frames)]
    for frame in range(frames - intro_frames):
        rendered.append(render_hash_frame(user, theme, colors, width, height, frame))

    return rendered


def render(user: str, config: dict[str, Any], calendar: dict | None, out_dir: Path) -> list[Path]:
    _ = calendar
    options = dict(config.get("hashwave", {}))
    options.setdefault("titleLeft", "HASHWAVE")
    options.setdefault("titleRight", "")
    options.setdefault("duration", "42s")
    options.setdefault("frames", 120)
    options.setdefault("holdFrames", 12)
    options.setdefault("width", 53)
    options.setdefault("height", 7)

    frames_by_theme = {
        "dark": build_frames(user, options, "dark"),
        "light": build_frames(user, options, "light"),
    }
    return write_theme_svgs(config, "hashwave", options, user, calendar, out_dir, frames_by_theme)

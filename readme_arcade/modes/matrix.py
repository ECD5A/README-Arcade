"""Matrix rain mode."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from readme_arcade.grid_svg import base_grid, layout, write_theme_svgs
from readme_arcade.modes.common import login_grid, stable_byte
from readme_arcade.themes import THEMES


def render_matrix_frame(user: str, theme: dict[str, str], width: int, height: int, frame: int) -> list[list[str]]:
    grid = base_grid(theme, width, height)

    for x in range(width):
        speed = 1 + (stable_byte(user, f"matrix-speed:{x}") % 3)
        span = height + 4 + (stable_byte(user, f"matrix-span:{x}") % 4)
        head = ((frame // speed) + stable_byte(user, f"matrix-offset:{x}")) % span
        head -= 2

        for trail in range(5):
            y = head - trail
            if 0 <= y < height:
                level = max(1, 4 - trail)
                grid[y][x] = theme[f"level{level}"]

    residue_tick = frame // 3
    for y in range(height):
        for x in range(width):
            if grid[y][x] != theme["level0"]:
                continue
            residue = stable_byte(user, f"matrix-residue:{residue_tick}:{x}:{y}")
            if residue < 56:
                grid[y][x] = theme["level1"]
            elif residue < 76:
                grid[y][x] = theme["level2"]

    return grid


def build_frames(user: str, options: dict[str, Any], theme_name: str) -> list[list[list[str]]]:
    theme = THEMES[theme_name]
    box = layout(options)
    width = box["width"]
    height = box["height"]
    frames = int(options.get("frames", 120))
    intro_frames = min(max(1, int(options.get("holdFrames", 12))), frames - 1)

    rendered: list[list[list[str]]] = [login_grid(user, width, height, theme, "matrix-name") for _ in range(intro_frames)]
    for frame in range(frames - intro_frames):
        rendered.append(render_matrix_frame(user, theme, width, height, frame))

    return rendered


def render(user: str, config: dict[str, Any], calendar: dict | None, out_dir: Path) -> list[Path]:
    _ = calendar
    options = dict(config.get("matrix", {}))
    options.setdefault("titleLeft", "MATRIX")
    options.setdefault("titleRight", "")
    options.setdefault("duration", "36s")
    options.setdefault("frames", 120)
    options.setdefault("holdFrames", 12)
    options.setdefault("width", 53)
    options.setdefault("height", 7)

    frames_by_theme = {
        "dark": build_frames(user, options, "dark"),
        "light": build_frames(user, options, "light"),
    }
    return write_theme_svgs(config, "matrix", options, user, calendar, out_dir, frames_by_theme)

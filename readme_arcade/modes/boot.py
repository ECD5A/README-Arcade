"""Boot sequence mode."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from readme_arcade.grid_svg import base_grid, layout, write_theme_svgs
from readme_arcade.modes.common import login_grid, stable_byte
from readme_arcade.themes import THEMES


BOOT_COLORS = {
    "dark": {
        "cursor": "#facc15",
        "ok": "#58a6ff",
        "warn": "#ff7b72",
    },
    "light": {
        "cursor": "#bf8700",
        "ok": "#0969da",
        "warn": "#cf222e",
    },
}


def render_boot_frame(
    user: str,
    theme: dict[str, str],
    colors: dict[str, str],
    width: int,
    height: int,
    frame: int,
    total_frames: int,
) -> list[list[str]]:
    grid = base_grid(theme, width, height)
    total_cells = width * height
    progress = min(total_cells, int(((frame + 1) / max(1, total_frames - 4)) * total_cells))
    scan_row = (frame // 5) % height

    for y in range(height):
        for x in range(width):
            index = (y * width) + x
            if index < progress:
                level = 1 + ((stable_byte(user, f"boot-map:{x}:{y}") + (frame // 6) + y) % 4)
                grid[y][x] = theme[f"level{level}"]
            elif stable_byte(user, f"boot-noise:{frame // 4}:{x}:{y}") < 18:
                grid[y][x] = theme["level1"]

    for x in range(width):
        if (x + frame) % 3 == 0:
            grid[scan_row][x] = theme["level4"]

    cursor_x = min(width - 1, progress % width)
    cursor_y = min(height - 1, progress // width)
    grid[cursor_y][cursor_x] = colors["cursor"]

    if frame % 16 in (12, 13, 14):
        grid[height - 1][width - 1] = colors["ok"]
    if frame % 29 == 0:
        grid[0][0] = colors["warn"]

    return grid


def build_frames(user: str, options: dict[str, Any], theme_name: str) -> list[list[list[str]]]:
    theme = THEMES[theme_name]
    colors = BOOT_COLORS[theme_name]
    box = layout(options)
    width = box["width"]
    height = box["height"]
    frames = int(options.get("frames", 108))
    intro_frames = min(max(1, int(options.get("holdFrames", 14))), frames - 1)
    run_frames = frames - intro_frames

    rendered: list[list[list[str]]] = [login_grid(user, width, height, theme, "boot-name") for _ in range(intro_frames)]
    for frame in range(run_frames):
        rendered.append(render_boot_frame(user, theme, colors, width, height, frame, run_frames))

    return rendered


def render(user: str, config: dict[str, Any], calendar: dict | None, out_dir: Path) -> list[Path]:
    _ = calendar
    options = dict(config.get("boot", {}))
    options.setdefault("titleLeft", "BOOT")
    options.setdefault("titleRight", "")
    options.setdefault("duration", "38s")
    options.setdefault("frames", 108)
    options.setdefault("holdFrames", 14)
    options.setdefault("width", 53)
    options.setdefault("height", 7)

    frames_by_theme = {
        "dark": build_frames(user, options, "dark"),
        "light": build_frames(user, options, "light"),
    }
    return write_theme_svgs(config, "boot", options, user, calendar, out_dir, frames_by_theme)

"""Pacman-style dot eater mode."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from readme_arcade.grid_svg import base_grid, calendar_levels, layout, serpentine_path, write_theme_svgs
from readme_arcade.themes import THEMES


def build_frames(user: str, options: dict[str, Any], calendar: dict | None, theme_name: str) -> list[list[list[str]]]:
    theme = THEMES[theme_name]
    box = layout(options)
    width = box["width"]
    height = box["height"]
    frames = int(options.get("frames", 96))
    path = serpentine_path(width, height)
    dot_grid = calendar_levels(calendar, width, height, user, theme)
    rendered: list[list[list[str]]] = []

    for frame in range(frames):
        grid = base_grid(theme, width, height)
        head_index = frame % len(path)
        eaten = set(path[: head_index + 1])

        for i, (x, y) in enumerate(path):
            if (x, y) in eaten:
                continue
            if i % 3 == 0:
                grid[y][x] = dot_grid[y][x]

        x, y = path[head_index]
        grid[y][x] = theme["level4"]

        # A two-cell wake makes the eater readable on a tiny contribution grid.
        for offset, color in ((1, theme["level3"]), (2, theme["level2"])):
            tx, ty = path[(head_index - offset) % len(path)]
            grid[ty][tx] = color

        # A blinking target keeps the board from looking like random noise.
        target_x, target_y = path[(head_index + 18) % len(path)]
        if frame % 4 < 2:
            grid[target_y][target_x] = theme["level3"]

        rendered.append(grid)

    return rendered


def render(user: str, config: dict[str, Any], calendar: dict | None, out_dir: Path) -> list[Path]:
    options = dict(config.get("pacman", {}))
    options.setdefault("titleLeft", "PACMAN TRACE")
    options.setdefault("titleRight", "DOT EATER")
    options.setdefault("duration", "34s")
    options.setdefault("frames", 96)
    options.setdefault("width", 53)
    options.setdefault("height", 7)

    frames_by_theme = {
        "dark": build_frames(user, options, calendar, "dark"),
        "light": build_frames(user, options, calendar, "light"),
    }
    return write_theme_svgs(config, "pacman", options, user, calendar, out_dir, frames_by_theme)

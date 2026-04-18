"""Snake mode."""

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
    snake_length = int(options.get("length", 18))
    hold_frames = int(options.get("holdFrames", 2))
    path = serpentine_path(width, height)
    calendar_grid = calendar_levels(calendar, width, height, user, theme)

    rendered: list[list[list[str]]] = []
    for frame in range(frames):
        grid = base_grid(theme, width, height)
        head_index = frame % len(path)
        food_index = (head_index + snake_length + 17) % len(path)
        fx, fy = path[food_index]
        grid[fy][fx] = theme["level3"]

        for offset in range(snake_length):
            x, y = path[(head_index - offset) % len(path)]
            if offset == 0:
                grid[y][x] = theme["level4"]
            elif offset < 4:
                grid[y][x] = theme["level3"]
            elif offset < 10:
                grid[y][x] = theme["level2"]
            else:
                grid[y][x] = theme["level1"]

        # Keep a faint contribution map behind the snake trail.
        if frame >= hold_frames:
            for y in range(height):
                for x in range(width):
                    if grid[y][x] == theme["level0"] and (x + y + frame) % 23 == 0:
                        grid[y][x] = calendar_grid[y][x]

        rendered.append(grid)

    return rendered


def render(user: str, config: dict[str, Any], calendar: dict | None, out_dir: Path) -> list[Path]:
    options = dict(config.get("snake", {}))
    options.setdefault("titleLeft", "SNAKE TRACE")
    options.setdefault("titleRight", "README ARCADE")
    options.setdefault("duration", "36s")
    options.setdefault("frames", 96)
    options.setdefault("width", 53)
    options.setdefault("height", 7)

    frames_by_theme = {
        "dark": build_frames(user, options, calendar, "dark"),
        "light": build_frames(user, options, calendar, "light"),
    }
    return write_theme_svgs(config, "snake", options, user, calendar, out_dir, frames_by_theme)

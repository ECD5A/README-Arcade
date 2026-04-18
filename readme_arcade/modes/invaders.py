"""Space Invaders-style mode."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from readme_arcade.grid_svg import base_grid, layout, write_theme_svgs
from readme_arcade.modes.lifegrid import FONT_5X7
from readme_arcade.themes import THEMES


Position = tuple[int, int]
Alien = tuple[int, int, int]


ARCADE_COLORS = {
    "dark": {
        "ship": "#58a6ff",
        "ship_shadow": "#1f6feb",
        "shot": "#facc15",
        "hit": "#ff7b72",
    },
    "light": {
        "ship": "#0969da",
        "ship_shadow": "#54aeff",
        "shot": "#bf8700",
        "hit": "#cf222e",
    },
}


def stable_byte(user: str, salt: str) -> int:
    return hashlib.sha256(f"{user}:{salt}".encode("utf-8")).digest()[0]


def name_grid(user: str, width: int, height: int, theme: dict[str, str]) -> list[list[str]]:
    grid = base_grid(theme, width, height)
    text = "".join(ch for ch in user.upper() if ch in FONT_5X7)[:8] or "README"
    text_width = (len(text) * 6) - 1
    if text_width > width:
        text = text[: max(1, (width + 1) // 6)]
        text_width = (len(text) * 6) - 1

    x0 = max(0, (width - text_width) // 2)
    y0 = max(0, (height - 7) // 2)
    for index, char in enumerate(text):
        glyph = FONT_5X7[char]
        gx = x0 + index * 6
        for y, row in enumerate(glyph):
            gy = y0 + y
            if gy >= height:
                continue
            for dx, value in enumerate(row):
                x = gx + dx
                if value == "1" and 0 <= x < width:
                    level = 1 + ((stable_byte(user, f"invaders-name:{index}:{dx}:{y}") + x + gy) % 4)
                    grid[gy][x] = theme[f"level{level}"]

    return grid


def build_aliens(user: str, width: int) -> list[Alien]:
    columns = max(5, min(9, (width - 8) // 5))
    start_x = max(2, (width - ((columns - 1) * 5 + 3)) // 2)
    aliens: list[Alien] = []

    for row_index, y in enumerate((0, 2)):
        for col in range(columns):
            x = start_x + col * 5
            level = 1 + ((stable_byte(user, f"alien:{row_index}:{col}") + row_index + col) % 4)
            aliens.append((x, y, level))

    return aliens


def alien_cells(alien: Alien, x_shift: int, width: int, height: int) -> list[Position]:
    x, y, _level = alien
    points = (
        (x + x_shift, y),
        (x + x_shift + 2, y),
        (x + x_shift, y + 1),
        (x + x_shift + 1, y + 1),
        (x + x_shift + 2, y + 1),
    )
    return [(px, py) for px, py in points if 0 <= px < width and 0 <= py < height]


def alien_order(aliens: list[Alien]) -> list[Alien]:
    return sorted(aliens, key=lambda item: (-item[1], item[0]))


def formation_shift(frame: int) -> int:
    return (-1, 0, 1, 1, 0, -1)[(frame // 8) % 6]


def paint_ship(grid: list[list[str]], colors: dict[str, str], x: int, width: int, height: int) -> None:
    y = height - 1
    for px in (x - 1, x, x + 1):
        if 0 <= px < width:
            grid[y][px] = colors["ship_shadow"]
    if 0 <= x < width:
        grid[y][x] = colors["ship"]
    if height > 1 and 0 <= x < width:
        grid[y - 1][x] = colors["ship"]


def paint_shot(grid: list[list[str]], colors: dict[str, str], x: int, y: int, width: int, height: int) -> None:
    if 0 <= x < width and 0 <= y < height:
        grid[y][x] = colors["shot"]


def paint_alien(
    grid: list[list[str]],
    theme: dict[str, str],
    colors: dict[str, str],
    alien: Alien,
    x_shift: int,
    flash: bool,
    width: int,
    height: int,
) -> None:
    _x, _y, level = alien
    for px, py in alien_cells(alien, x_shift, width, height):
        if flash:
            grid[py][px] = colors["hit"]
        else:
            cell_level = min(4, level + ((px + py) % 2))
            grid[py][px] = theme[f"level{cell_level}"]


def render_game_frame(
    user: str,
    theme: dict[str, str],
    colors: dict[str, str],
    width: int,
    height: int,
    aliens: list[Alien],
    targets: list[Alien],
    frame: int,
    shot_period: int,
) -> list[list[str]]:
    grid = base_grid(theme, width, height)
    killed_count = min(len(targets), frame // shot_period)
    current_target = targets[killed_count] if killed_count < len(targets) else None
    killed = set(targets[:killed_count])
    shift = formation_shift(frame)
    shot_frame = frame % shot_period

    for alien in aliens:
        if alien in killed:
            continue
        paint_alien(
            grid,
            theme,
            colors,
            alien,
            shift,
            flash=alien == current_target and shot_frame >= shot_period - 2,
            width=width,
            height=height,
        )

    if current_target is not None:
        target_x = current_target[0] + shift + 1
        target_y = current_target[1] + 1
        travel = max(1, height - 2 - target_y)
        progress = min(travel, round((shot_frame / max(1, shot_period - 1)) * travel))
        shot_y = max(0, height - 2 - progress)
        paint_shot(grid, colors, target_x, shot_y, width, height)
        ship_x = min(max(1, target_x + ((stable_byte(user, f"ship:{frame}") % 3) - 1)), width - 2)
    else:
        span = max(1, width - 4)
        sweep = frame % (span * 2)
        ship_x = 2 + (sweep if sweep < span else (span * 2) - sweep)

    paint_ship(grid, colors, ship_x, width, height)
    return grid


def build_frames(user: str, options: dict[str, Any], theme_name: str) -> list[list[list[str]]]:
    theme = THEMES[theme_name]
    colors = dict(ARCADE_COLORS[theme_name])
    box = layout(options)
    width = box["width"]
    height = box["height"]
    frames = int(options.get("frames", 120))
    intro_frames = min(max(1, int(options.get("holdFrames", 12))), frames - 1)
    shot_period = min(max(4, int(options.get("shotPeriod", 7))), 14)

    aliens = build_aliens(user, width)
    targets = alien_order(aliens)
    rendered: list[list[list[str]]] = [name_grid(user, width, height, theme) for _ in range(intro_frames)]

    for frame in range(frames - intro_frames):
        rendered.append(render_game_frame(user, theme, colors, width, height, aliens, targets, frame, shot_period))

    return rendered


def render(user: str, config: dict[str, Any], calendar: dict | None, out_dir: Path) -> list[Path]:
    _ = calendar
    options = dict(config.get("invaders", {}))
    options.setdefault("titleLeft", "INVADERS")
    options.setdefault("titleRight", "")
    options.setdefault("duration", "40s")
    options.setdefault("frames", 120)
    options.setdefault("holdFrames", 12)
    options.setdefault("shotPeriod", 7)
    options.setdefault("width", 53)
    options.setdefault("height", 7)

    frames_by_theme = {
        "dark": build_frames(user, options, "dark"),
        "light": build_frames(user, options, "light"),
    }
    return write_theme_svgs(config, "invaders", options, user, calendar, out_dir, frames_by_theme)

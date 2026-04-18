"""Snake mode."""

from __future__ import annotations

import hashlib
import random
from pathlib import Path
from typing import Any

from readme_arcade.github import counts_from_calendar
from readme_arcade.grid_svg import base_grid, layout, write_theme_svgs
from readme_arcade.modes.lifegrid import FONT_5X7
from readme_arcade.themes import THEMES


Position = tuple[int, int]


SNAKE_COLORS = {
    "dark": {
        "head": "#ff4d8d",
        "jaw": "#facc15",
        "body": "#58a6ff",
        "tail": "#1f6feb",
    },
    "light": {
        "head": "#d6336c",
        "jaw": "#ca8a04",
        "body": "#0969da",
        "tail": "#54aeff",
    },
}


FOOD_LEVELS = {
    1: "level1",
    2: "level2",
    3: "level3",
    4: "level4",
}


def stable_rng(user: str, salt: str = "") -> random.Random:
    digest = hashlib.sha256(f"{user}:{salt}".encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def stable_byte(user: str, salt: str) -> int:
    return hashlib.sha256(f"{user}:{salt}".encode("utf-8")).digest()[0]


def manhattan(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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
                    level = 1 + ((stable_byte(user, f"name:{index}:{dx}:{y}") + x + gy) % 4)
                    grid[gy][x] = theme[f"level{level}"]

    return grid


def initial_body(width: int, height: int, length: int) -> list[Position]:
    y = height // 2
    head_x = min(width - 3, max(length + 2, 9))
    return [(head_x - offset, y) for offset in range(length)]


def build_food(user: str, width: int, height: int, calendar: dict | None, blocked: set[Position]) -> dict[Position, int]:
    counts, _total = counts_from_calendar(calendar, width, height)
    food: dict[Position, int] = {}

    for y in range(height):
        for x in range(width):
            pos = (x, y)
            if pos in blocked:
                continue

            count = counts[y][x]
            roll = stable_byte(user, f"snake-food:{x}:{y}")
            if count <= 0 and roll > 116:
                continue

            if count >= 10:
                level = 4
            elif count >= 5:
                level = 3
            elif count >= 2:
                level = 2
            elif count == 1:
                level = 1
            elif roll < 46:
                level = 1
            elif roll < 82:
                level = 2
            elif roll < 106:
                level = 3
            else:
                level = 4

            food[pos] = level

    # Ensure enough dark food exists, so the "eat darkest first" behavior is visible.
    rng = stable_rng(user, "snake-dark-food")
    dark_cells = [pos for pos, level in food.items() if level == 1]
    attempts = 0
    while len(dark_cells) < 26 and attempts < width * height * 2:
        attempts += 1
        pos = (rng.randrange(0, width), rng.randrange(0, height))
        if pos in blocked:
            continue
        food[pos] = 1
        if pos not in dark_cells:
            dark_cells.append(pos)

    return food


def choose_target(user: str, head: Position, food: dict[Position, int], theme_name: str) -> Position | None:
    if not food:
        return None

    def darkness_priority(level: int) -> int:
        return level if theme_name == "dark" else 5 - level

    return min(
        food,
        key=lambda pos: (
            darkness_priority(food[pos]),
            manhattan(head, pos),
            stable_byte(user, f"target:{pos[0]}:{pos[1]}"),
        ),
    )


def choose_step(
    user: str,
    frame: int,
    head: Position,
    target: Position | None,
    body: list[Position],
    width: int,
    height: int,
) -> Position:
    if target is None:
        target = ((head[0] + 7) % width, (head[1] + 3) % height)

    current_dir = (head[0] - body[1][0], head[1] - body[1][1]) if len(body) > 1 else (1, 0)
    directions = [(1, 0), (0, 1), (0, -1), (-1, 0)]
    body_block = set(body[:-1])
    candidates: list[tuple[tuple[int, int, int, int], Position]] = []

    for dx, dy in directions:
        nx = head[0] + dx
        ny = head[1] + dy
        if not (0 <= nx < width and 0 <= ny < height):
            continue
        pos = (nx, ny)
        if pos in body_block:
            continue

        turn_penalty = 0 if (dx, dy) == current_dir else 1
        edge_penalty = 1 if nx in (0, width - 1) or ny in (0, height - 1) else 0
        wiggle = stable_byte(user, f"move:{frame}:{nx}:{ny}") % 3
        candidates.append(((manhattan(pos, target), turn_penalty, edge_penalty, wiggle), pos))

    if candidates:
        return min(candidates, key=lambda item: item[0])[1]

    # Last-resort fallback keeps the animation alive even if the snake boxes itself in.
    for dx, dy in directions:
        nx = head[0] + dx
        ny = head[1] + dy
        if 0 <= nx < width and 0 <= ny < height:
            return (nx, ny)

    return head


def render_game_frame(
    theme: dict[str, str],
    snake_colors: dict[str, str],
    width: int,
    height: int,
    body: list[Position],
    food: dict[Position, int],
) -> list[list[str]]:
    grid = base_grid(theme, width, height)

    for (x, y), level in food.items():
        grid[y][x] = theme[FOOD_LEVELS[level]]

    for offset, (x, y) in enumerate(reversed(body)):
        grid[y][x] = snake_colors["tail"]
        if offset > len(body) // 3:
            grid[y][x] = snake_colors["body"]

    if len(body) > 1:
        nx, ny = body[1]
        grid[ny][nx] = snake_colors["jaw"]

    hx, hy = body[0]
    grid[hy][hx] = snake_colors["head"]
    return grid


def build_frames(user: str, options: dict[str, Any], calendar: dict | None, theme_name: str) -> list[list[list[str]]]:
    theme = THEMES[theme_name]
    snake_colors = dict(SNAKE_COLORS[theme_name])
    if theme_name == "dark" and options.get("headColorDark"):
        snake_colors["head"] = str(options["headColorDark"])
    if theme_name == "light" and options.get("headColorLight"):
        snake_colors["head"] = str(options["headColorLight"])

    box = layout(options)
    width = box["width"]
    height = box["height"]
    frames = int(options.get("frames", 120))
    intro_frames = min(max(1, int(options.get("holdFrames", 12))), frames - 1)
    start_length = min(max(4, int(options.get("length", 6))), max(4, width - 4))
    max_length = max(start_length, int(options.get("maxLength", 7)))
    grow_per_food = max(0, int(options.get("growPerFood", 0)))

    body = initial_body(width, height, start_length)
    food = build_food(user, width, height, calendar, set(body))

    rendered: list[list[list[str]]] = [name_grid(user, width, height, theme) for _ in range(intro_frames)]
    growth = 0

    for frame in range(frames - intro_frames):
        head = body[0]
        target = choose_target(user, head, food, theme_name)
        next_head = choose_step(user, frame, head, target, body, width, height)
        body.insert(0, next_head)

        if next_head in food:
            del food[next_head]
            growth += grow_per_food

        if growth > 0 and len(body) <= max_length:
            growth -= 1
        else:
            body.pop()

        body = body[:max_length]
        rendered.append(render_game_frame(theme, snake_colors, width, height, body, food))

    return rendered


def render(user: str, config: dict[str, Any], calendar: dict | None, out_dir: Path) -> list[Path]:
    options = dict(config.get("snake", {}))
    options.setdefault("titleLeft", "SNAKE TRACE")
    options.setdefault("titleRight", "PINK HEAD // DARKEST FIRST")
    options.setdefault("duration", "40s")
    options.setdefault("frames", 120)
    options.setdefault("holdFrames", 12)
    options.setdefault("length", 6)
    options.setdefault("maxLength", 7)
    options.setdefault("growPerFood", 0)
    options.setdefault("width", 53)
    options.setdefault("height", 7)

    frames_by_theme = {
        "dark": build_frames(user, options, calendar, "dark"),
        "light": build_frames(user, options, calendar, "light"),
    }
    return write_theme_svgs(config, "snake", options, user, calendar, out_dir, frames_by_theme)

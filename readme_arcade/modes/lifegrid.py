"""Conway Lifegrid mode."""

from __future__ import annotations

import hashlib
import random
from html import escape
from pathlib import Path
from typing import Any

from readme_arcade.github import counts_from_calendar
from readme_arcade.themes import THEMES


FONT_5X7 = {
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01111", "10000", "10000", "10011", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "10010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "01010", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "01010", "00100", "00100", "00100", "01010", "10001"),
    "Y": ("10001", "01010", "00100", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
}


def stable_rng(user: str, salt: str = "") -> random.Random:
    digest = hashlib.sha256(f"{user}:{salt}".encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def empty_grid(width: int, height: int) -> list[list[int]]:
    return [[0 for _ in range(width)] for _ in range(height)]


def empty_counts(width: int, height: int) -> list[list[int]]:
    return [[0 for _ in range(width)] for _ in range(height)]


def density_value(name: str, sparse: int, balanced: int, dense: int) -> int:
    return {
        "sparse": sparse,
        "balanced": balanced,
        "dense": dense,
    }.get(name, balanced)


def stamp_name(grid: list[list[int]], counts: list[list[int]], user: str) -> None:
    height = len(grid)
    width = len(grid[0])
    text = "".join(ch for ch in user.upper() if ch in FONT_5X7)[:8]
    if not text:
        text = "README"

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
                    grid[gy][x] = 1
                    counts[gy][x] = max(counts[gy][x], 3)


def clean_name_grid(user: str, width: int, height: int) -> list[list[int]]:
    grid = empty_grid(width, height)
    counts = empty_counts(width, height)
    stamp_name(grid, counts, user)
    return grid


def inject_gliders(grid: list[list[int]], counts: list[list[int]], user: str, minimum: int = 4) -> None:
    height = len(grid)
    width = len(grid[0])
    if width < 4 or height < 3:
        return

    glider = ((1, 0), (2, 1), (0, 2), (1, 2), (2, 2))
    rng = stable_rng(user, "gliders")
    live = sum(sum(row) for row in grid)
    pieces = minimum if live < 80 else max(2, minimum // 2)

    for _ in range(pieces):
        x0 = rng.randrange(0, width - 3)
        y0 = rng.randrange(0, height - 2)
        for dx, dy in glider:
            x = (x0 + dx) % width
            y = (y0 + dy) % height
            grid[y][x] = 1
            counts[y][x] = max(counts[y][x], 2)


def inject_activity_stream(
    grid: list[list[int]],
    user: str,
    frame: int,
    enabled: bool,
    stream_every: int,
    stream_bursts: int,
) -> None:
    height = len(grid)
    width = len(grid[0])
    if not enabled or height < 3 or width < 5:
        return
    if frame < 6 or frame % max(1, stream_every):
        return

    rng = stable_rng(user, f"edge-stream:{frame}")
    for _ in range(max(0, stream_bursts)):
        side = rng.choice(("left", "right"))
        y = rng.randrange(1, height - 1)
        if side == "left":
            cells = ((0, y), (1, y + 1), (2, y - 1), (2, y), (2, y + 1))
        else:
            cells = (
                (width - 1, y),
                (width - 2, y + 1),
                (width - 3, y - 1),
                (width - 3, y),
                (width - 3, y + 1),
            )

        for x, cell_y in cells:
            if 0 <= x < width and 0 <= cell_y < height:
                grid[cell_y][x] = 1


def next_state(grid: list[list[int]]) -> list[list[int]]:
    height = len(grid)
    width = len(grid[0])
    nxt = empty_grid(width, height)

    for y in range(height):
        for x in range(width):
            neighbours = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx = (x + dx) % width
                    ny = (y + dy) % height
                    neighbours += grid[ny][nx]

            if grid[y][x]:
                nxt[y][x] = 1 if neighbours in (2, 3) else 0
            else:
                nxt[y][x] = 1 if neighbours == 3 else 0

    return nxt


def evolve(seed: list[list[int]], user: str, options: dict[str, Any]) -> list[list[list[int]]]:
    density = str(options.get("density", "balanced"))
    frames = int(options.get("frames", 96))
    stream_bursts = int(options.get("streamBursts", density_value(density, 2, 3, 4)))
    stream_every = int(options.get("streamEvery", 2))
    stream_enabled = bool(options.get("activityStream", True))
    rescue_minimum = density_value(density, 4, 6, 8)

    states = [[row[:] for row in seed]]
    for frame in range(1, frames):
        nxt = next_state(states[-1])
        inject_activity_stream(nxt, user, frame, stream_enabled, stream_every, stream_bursts)
        if frame > 10 and sum(sum(row) for row in nxt) < 8:
            counts = empty_counts(len(nxt[0]), len(nxt))
            inject_gliders(nxt, counts, f"{user}:{frame}", minimum=rescue_minimum)
        states.append(nxt)

    return states


def cell_fill(theme: dict[str, str], count: int, x: int, y: int, user: str) -> str:
    if count >= 10:
        return theme["level4"]
    if count >= 5:
        return theme["level3"]
    if count >= 2:
        return theme["level2"]
    if count == 1:
        return theme["level1"]

    digest = hashlib.sha256(f"{user}:{x}:{y}:accent".encode("utf-8")).digest()[0]
    if digest < 16:
        return theme["level4"]
    if digest < 48:
        return theme["level3"]
    if digest < 96:
        return theme["level2"]
    return theme["level1"]


def make_svg(
    states: list[list[list[int]]],
    counts: list[list[int]],
    user: str,
    options: dict[str, Any],
    theme_name: str,
) -> str:
    theme = THEMES[theme_name]
    width = int(options.get("width", 53))
    height = int(options.get("height", 7))
    cell = int(options.get("cellSize", 13))
    gap = int(options.get("gap", 4))
    radius = int(options.get("radius", 2))
    grid_width = width * cell + (width - 1) * gap
    grid_height = height * cell + (height - 1) * gap
    svg_width = max(int(options.get("canvasWidth", 960)), grid_width + 48)
    svg_height = max(int(options.get("canvasHeight", 190)), grid_height + 72)
    x0 = (svg_width - grid_width) // 2
    y0 = int(options.get("gridTop", 56))
    duration = str(options.get("duration", "42s"))
    hold_frames = int(options.get("holdFrames", 4))
    title_left = str(options.get("titleLeft", "CONWAY LIFEGRID"))
    title_right = str(options.get("titleRight", "B3/S23"))
    title = f"{user} README Arcade Lifegrid"

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" '
        'role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        (
            f'<desc id="desc">A {width} by {height} animated Conway Game of Life grid '
            f'started from the {escape(user)} mark and colored with GitHub-style contribution levels.</desc>'
        ),
        "<defs>",
        (
            '<pattern id="scanlines" width="6" height="6" patternUnits="userSpaceOnUse">'
            f'<path d="M0 0H6" stroke="{theme["scanline"]}" stroke-opacity="0.055"/>'
            "</pattern>"
        ),
        "</defs>",
        f'<rect width="{svg_width}" height="{svg_height}" rx="8" fill="{theme["bg"]}"/>',
        (
            f'<rect x="12" y="12" width="{svg_width - 24}" height="{svg_height - 24}" rx="8" '
            f'fill="{theme["panel"]}" stroke="{theme["border"]}" stroke-width="1"/>'
        ),
        f'<rect x="12" y="12" width="{svg_width - 24}" height="{svg_height - 24}" rx="8" fill="url(#scanlines)"/>',
    ]

    if title_left:
        lines.append(
            f'<text x="30" y="34" fill="{theme["muted"]}" '
            'font-family="ui-monospace, SFMono-Regular, Consolas, Liberation Mono, monospace" '
            f'font-size="12">{escape(title_left)}</text>'
        )
    if title_right:
        lines.append(
            f'<text x="{svg_width - 30}" y="34" text-anchor="end" fill="{theme["muted"]}" '
            'font-family="ui-monospace, SFMono-Regular, Consolas, Liberation Mono, monospace" '
            f'font-size="12">{escape(title_right)}</text>'
        )

    initial_state = states[0]
    animation_states = [initial_state] * max(0, hold_frames) + states

    for y in range(height):
        for x in range(width):
            px = x0 + x * (cell + gap)
            py = y0 + y * (cell + gap)
            count = counts[y][x]
            fill = cell_fill(theme, count, x, y, user)
            fill_values = ";".join(fill if state[y][x] else theme["level0"] for state in animation_states)
            lines.append(
                f'<rect x="{px}" y="{py}" width="{cell}" height="{cell}" rx="{radius}" '
                f'fill="{fill_values.split(";")[0]}">'
                f'<animate attributeName="fill" dur="{duration}" repeatCount="indefinite" '
                f'values="{fill_values}"/>'
                "</rect>"
            )

    lines.append("</svg>")
    return "\n".join(lines)


def render(user: str, config: dict[str, Any], calendar: dict | None, out_dir: Path) -> list[Path]:
    options = dict(config.get("lifegrid", {}))
    width = int(options.get("width", 53))
    height = int(options.get("height", 7))
    counts, _total = counts_from_calendar(calendar, width, height)
    seed = clean_name_grid(user, width, height)
    states = evolve(seed, user, options)
    out_dir.mkdir(parents=True, exist_ok=True)

    base_name = str(config.get("output", {}).get("baseName", "readme-arcade"))
    written: list[Path] = []
    for theme_name in ("dark", "light"):
        suffix = "-dark" if theme_name == "dark" else ""
        path = out_dir / f"{base_name}{suffix}.svg"
        path.write_text(make_svg(states, counts, user, options, theme_name), encoding="utf-8", newline="\n")
        written.append(path)

    return written

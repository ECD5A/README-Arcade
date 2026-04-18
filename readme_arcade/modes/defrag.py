"""Windows 98-style defrag mode."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from readme_arcade.grid_svg import base_grid, layout, write_theme_svgs
from readme_arcade.modes.common import login_grid, stable_byte
from readme_arcade.themes import THEMES


DEFRAG_COLORS = {
    "dark": {
        "scan": "#facc15",
        "move": "#58a6ff",
    },
    "light": {
        "scan": "#bf8700",
        "move": "#0969da",
    },
}


def build_disk(user: str, width: int, height: int, theme: dict[str, str]) -> tuple[list[str], list[str]]:
    total = width * height
    fragmented: list[str] = []

    for index in range(total):
        x = index % width
        y = index // width
        roll = stable_byte(user, f"defrag-cell:{x}:{y}")
        stripe = (x // 4) + (y * 3)
        open_lane = x % 13 == 0 or ((x + (y * 3)) % 19 == 0)
        if roll < 122 or open_lane:
            fragmented.append(theme["level0"])
            continue

        level = 1 + ((roll + stripe) % 4)
        fragmented.append(theme[f"level{level}"])

    blocks = [color for color in fragmented if color != theme["level0"]]
    ordered = sorted(
        blocks,
        key=lambda color: (
            0 if color == theme["level4"] else 1 if color == theme["level3"] else 2 if color == theme["level2"] else 3,
            stable_byte(user, f"defrag-order:{len(blocks)}:{color}"),
        ),
    )
    compacted = [theme["level0"]] * total
    write_index = 0
    for color in ordered:
        while write_index < total:
            x = write_index % width
            y = write_index // width
            spacer = x % 12 == 11 or (x + y) % 23 == 0
            if not spacer:
                break
            write_index += 1
        if write_index >= total:
            break
        compacted[write_index] = color
        write_index += 1

    return fragmented, compacted


def render_defrag_frame(
    user: str,
    theme: dict[str, str],
    colors: dict[str, str],
    width: int,
    height: int,
    fragmented: list[str],
    compacted: list[str],
    frame: int,
    total_frames: int,
) -> list[list[str]]:
    grid = base_grid(theme, width, height)
    total = width * height
    progress = min(1.0, frame / max(1, total_frames - 1))
    scan_index = min(total - 1, int(progress * (total - 1)))

    for index in range(total):
        x = index % width
        y = index // width
        settle = (index / total) * 0.72
        settle += (stable_byte(user, f"defrag-settle:{index}") / 255) * 0.26
        color = compacted[index] if progress >= settle else fragmented[index]

        if color == theme["level0"] and stable_byte(user, f"defrag-static:{frame // 8}:{index}") < 3:
            color = theme["level1"]

        grid[y][x] = color

    sx = scan_index % width
    sy = scan_index // width
    grid[sy][sx] = colors["scan"]

    move_index = (scan_index + 11 + (frame % 9)) % total
    mx = move_index % width
    my = move_index // width
    grid[my][mx] = colors["move"]

    return grid


def build_frames(user: str, options: dict[str, Any], theme_name: str) -> list[list[list[str]]]:
    theme = THEMES[theme_name]
    colors = DEFRAG_COLORS[theme_name]
    box = layout(options)
    width = box["width"]
    height = box["height"]
    frames = int(options.get("frames", 120))
    intro_frames = min(max(1, int(options.get("holdFrames", 12))), frames - 1)
    run_frames = frames - intro_frames
    fragmented, compacted = build_disk(user, width, height, theme)

    rendered: list[list[list[str]]] = [login_grid(user, width, height, theme, "defrag-name") for _ in range(intro_frames)]
    for frame in range(run_frames):
        rendered.append(render_defrag_frame(user, theme, colors, width, height, fragmented, compacted, frame, run_frames))

    return rendered


def render(user: str, config: dict[str, Any], calendar: dict | None, out_dir: Path) -> list[Path]:
    _ = calendar
    options = dict(config.get("defrag", {}))
    options.setdefault("titleLeft", "DEFRAG")
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
    return write_theme_svgs(config, "defrag", options, user, calendar, out_dir, frames_by_theme)

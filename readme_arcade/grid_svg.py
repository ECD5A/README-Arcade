"""Shared SVG helpers for grid-based modes."""

from __future__ import annotations

import hashlib
from html import escape
from pathlib import Path
from typing import Any

from readme_arcade.github import counts_from_calendar
from readme_arcade.themes import THEMES


GridFrames = list[list[list[str]]]


def layout(options: dict[str, Any]) -> dict[str, int]:
    width = int(options.get("width", 53))
    height = int(options.get("height", 7))
    cell = int(options.get("cellSize", 13))
    gap = int(options.get("gap", 4))
    grid_width = width * cell + (width - 1) * gap
    grid_height = height * cell + (height - 1) * gap
    svg_width = max(int(options.get("canvasWidth", 960)), grid_width + 48)
    svg_height = max(int(options.get("canvasHeight", 190)), grid_height + 72)

    return {
        "width": width,
        "height": height,
        "cell": cell,
        "gap": gap,
        "radius": int(options.get("radius", 2)),
        "grid_width": grid_width,
        "grid_height": grid_height,
        "svg_width": svg_width,
        "svg_height": svg_height,
        "x0": (svg_width - grid_width) // 2,
        "y0": int(options.get("gridTop", 56)),
    }


def contribution_fill(theme: dict[str, str], count: int, x: int, y: int, user: str) -> str:
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


def serpentine_path(width: int, height: int) -> list[tuple[int, int]]:
    path: list[tuple[int, int]] = []
    for y in range(height):
        xs = range(width) if y % 2 == 0 else range(width - 1, -1, -1)
        for x in xs:
            path.append((x, y))
    return path


def write_theme_svgs(
    config: dict[str, Any],
    mode_name: str,
    options: dict[str, Any],
    user: str,
    calendar: dict | None,
    out_dir: Path,
    frames_by_theme: dict[str, GridFrames],
) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    base_name = str(config.get("output", {}).get("baseName", "readme-arcade"))
    written: list[Path] = []

    for theme_name in ("dark", "light"):
        suffix = "-dark" if theme_name == "dark" else ""
        path = out_dir / f"{base_name}{suffix}.svg"
        path.write_text(
            make_svg(frames_by_theme[theme_name], user, mode_name, options, theme_name),
            encoding="utf-8",
            newline="\n",
        )
        written.append(path)

    return written


def make_svg(frames: GridFrames, user: str, mode_name: str, options: dict[str, Any], theme_name: str) -> str:
    theme = THEMES[theme_name]
    box = layout(options)
    width = box["width"]
    height = box["height"]
    svg_width = box["svg_width"]
    svg_height = box["svg_height"]
    duration = str(options.get("duration", "42s"))
    title_left = str(options.get("titleLeft", mode_name.upper()))
    title_right = str(options.get("titleRight", "README ARCADE"))
    title = f"{user} README Arcade {mode_name}"

    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" '
        'role="img" aria-labelledby="title desc">',
        f'<title id="title">{escape(title)}</title>',
        f'<desc id="desc">An animated {escape(mode_name)} grid for GitHub profile READMEs.</desc>',
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

    for y in range(height):
        for x in range(width):
            px = box["x0"] + x * (box["cell"] + box["gap"])
            py = box["y0"] + y * (box["cell"] + box["gap"])
            values = ";".join(frame[y][x] for frame in frames)
            lines.append(
                f'<rect x="{px}" y="{py}" width="{box["cell"]}" height="{box["cell"]}" rx="{box["radius"]}" '
                f'fill="{frames[0][y][x]}">'
                f'<animate attributeName="fill" dur="{duration}" repeatCount="indefinite" values="{values}"/>'
                "</rect>"
            )

    lines.append("</svg>")
    return "\n".join(lines)


def base_grid(theme: dict[str, str], width: int, height: int) -> list[list[str]]:
    return [[theme["level0"] for _ in range(width)] for _ in range(height)]


def calendar_levels(calendar: dict | None, width: int, height: int, user: str, theme: dict[str, str]) -> list[list[str]]:
    counts, _total = counts_from_calendar(calendar, width, height)
    return [[contribution_fill(theme, counts[y][x], x, y, user) for x in range(width)] for y in range(height)]

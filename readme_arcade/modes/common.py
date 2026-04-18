"""Shared helpers for grid modes."""

from __future__ import annotations

import hashlib

from readme_arcade.grid_svg import base_grid
from readme_arcade.modes.lifegrid import FONT_5X7


def stable_byte(user: str, salt: str) -> int:
    return hashlib.sha256(f"{user}:{salt}".encode("utf-8")).digest()[0]


def login_grid(user: str, width: int, height: int, theme: dict[str, str], salt: str) -> list[list[str]]:
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
                    level = 1 + ((stable_byte(user, f"{salt}:{index}:{dx}:{y}") + x + gy) % 4)
                    grid[gy][x] = theme[f"level{level}"]

    return grid

"""Configuration loading for README Arcade."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_CONFIG: dict[str, Any] = {
    "user": "ECD5A",
    "mode": "lifegrid",
    "output": {
        "baseName": "readme-arcade",
    },
    "lifegrid": {
        "width": 53,
        "height": 7,
        "frames": 96,
        "duration": "42s",
        "holdFrames": 4,
        "density": "balanced",
        "activityStream": True,
        "streamEvery": 2,
        "titleLeft": "CONWAY LIFEGRID",
        "titleRight": "B3/S23",
        "cellSize": 13,
        "gap": 4,
        "radius": 2,
        "canvasWidth": 960,
        "canvasHeight": 190,
        "gridTop": 56,
    },
    "snake": {
        "width": 53,
        "height": 7,
        "frames": 120,
        "duration": "40s",
        "holdFrames": 12,
        "length": 6,
        "maxLength": 7,
        "growPerFood": 0,
        "worm": True,
        "wormLength": 5,
        "wormMaxLength": 5,
        "wormSpeed": 2,
        "wormGrowPerFood": 0,
        "titleLeft": "SNAKE TRACE",
        "titleRight": "PINK HEAD // DARKEST FIRST",
        "cellSize": 13,
        "gap": 4,
        "radius": 2,
        "canvasWidth": 960,
        "canvasHeight": 190,
        "gridTop": 56,
    },
    "pacman": {
        "width": 53,
        "height": 7,
        "frames": 96,
        "duration": "34s",
        "titleLeft": "PACMAN TRACE",
        "titleRight": "DOT EATER",
        "cellSize": 13,
        "gap": 4,
        "radius": 2,
        "canvasWidth": 960,
        "canvasHeight": 190,
        "gridTop": 56,
    },
}


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return dict(DEFAULT_CONFIG)

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")

    return deep_merge(DEFAULT_CONFIG, data)

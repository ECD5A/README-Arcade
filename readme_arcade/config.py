"""Configuration loading for README Arcade."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any


DEFAULT_CONFIG: dict[str, Any] = {
    "user": "ECD5A",
    "mode": "lifegrid",
    "speed": "normal",
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
        "duration": "32s",
        "holdFrames": 12,
        "transitionFrames": 8,
        "birthFrames": 8,
        "fieldRevealFrames": 7,
        "edgeRunDelay": 8,
        "edgeRunFrames": 28,
        "length": 6,
        "maxLength": 7,
        "growPerFood": 0,
        "worm": True,
        "wormLength": 5,
        "wormMaxLength": 5,
        "wormSpeed": 2,
        "wormGrowPerFood": 0,
        "titleLeft": "SNAKE",
        "titleRight": "",
        "cellSize": 13,
        "gap": 4,
        "radius": 2,
        "canvasWidth": 960,
        "canvasHeight": 190,
        "gridTop": 56,
    },
    "matrix": {
        "width": 53,
        "height": 7,
        "frames": 120,
        "duration": "36s",
        "holdFrames": 12,
        "transitionFrames": 10,
        "titleLeft": "MATRIX",
        "titleRight": "",
        "cellSize": 13,
        "gap": 4,
        "radius": 2,
        "canvasWidth": 960,
        "canvasHeight": 190,
        "gridTop": 56,
    },
    "defrag": {
        "width": 53,
        "height": 7,
        "frames": 120,
        "duration": "42s",
        "holdFrames": 12,
        "titleLeft": "DEFRAG",
        "titleRight": "",
        "cellSize": 13,
        "gap": 4,
        "radius": 2,
        "canvasWidth": 960,
        "canvasHeight": 190,
        "gridTop": 56,
    },
}


SPEED_PRESETS: dict[str, dict[str, str]] = {
    "slow": {
        "lifegrid": "54s",
        "snake": "40s",
        "matrix": "46s",
        "defrag": "54s",
    },
    "normal": {
        "lifegrid": "42s",
        "snake": "32s",
        "matrix": "36s",
        "defrag": "42s",
    },
    "fast": {
        "lifegrid": "34s",
        "snake": "26s",
        "matrix": "28s",
        "defrag": "34s",
    },
    "turbo": {
        "lifegrid": "26s",
        "snake": "20s",
        "matrix": "22s",
        "defrag": "26s",
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


def apply_speed_preset(config: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    speed = str(config.get("speed", "normal")).lower()
    if speed not in SPEED_PRESETS:
        available = ", ".join(SPEED_PRESETS)
        raise ValueError(f"unknown speed {speed!r}; available speeds: {available}")

    for mode, duration in SPEED_PRESETS[speed].items():
        mode_override = override.get(mode, {})
        if isinstance(mode_override, dict) and "duration" in mode_override:
            continue
        config.setdefault(mode, {})["duration"] = duration

    return config


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return apply_speed_preset(deepcopy(DEFAULT_CONFIG), {})

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")

    return apply_speed_preset(deep_merge(deepcopy(DEFAULT_CONFIG), data), data)

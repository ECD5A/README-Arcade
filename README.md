<h1 align="center">README Arcade</h1>

<p align="center">
  Animated GitHub README blocks for profile pages.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-2da44e?style=flat-square" alt="MIT license">
  <img src="https://img.shields.io/badge/python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/dependencies-zero-6f7787?style=flat-square" alt="Zero dependencies">
  <img src="https://img.shields.io/badge/mode-lifegrid-39d353?style=flat-square" alt="Lifegrid mode">
  <img src="https://img.shields.io/badge/theme-auto-58a6ff?style=flat-square" alt="Auto theme">
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/readme-arcade-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/readme-arcade.svg">
    <img src="./dist/readme-arcade.svg" width="920" alt="Animated README Arcade lifegrid">
  </picture>
</p>

## What It Does

README Arcade generates animated SVG blocks for GitHub profile READMEs.

The first mode is `lifegrid`: a GitHub contribution-style Conway Game of Life board. It starts from your login, pauses for a few frames, then evolves with real Conway `B3/S23` rules. If a GitHub token is available, contribution counts tint the cells. Without a token, the SVG is still deterministic and never blank.

Dark and light theme assets are generated separately, so your README can switch automatically with `prefers-color-scheme`.

## Quick Start

Clone or fork this repository, then edit `readme-arcade.config.json`:

```json
{
  "user": "YOUR_LOGIN",
  "mode": "lifegrid"
}
```

Render the SVG files:

```bash
python scripts/render.py --config readme-arcade.config.json --out-dir dist
```

Put this in your profile README:

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/readme-arcade-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/readme-arcade.svg">
    <img src="./dist/readme-arcade.svg" width="920" alt="Animated README Arcade lifegrid">
  </picture>
</p>
```

## Config

`duration` controls how long one full animation loop takes. The SVG repeats forever.

`frames` controls how many Conway states are precomputed into that loop. More frames make the loop feel longer and less repetitive.

`holdFrames` controls how long the initial login mark stays visible before the game starts.

```json
{
  "user": "ECD5A",
  "mode": "lifegrid",
  "output": {
    "baseName": "readme-arcade"
  },
  "lifegrid": {
    "frames": 96,
    "duration": "42s",
    "holdFrames": 4,
    "density": "balanced",
    "activityStream": true,
    "titleLeft": "CONWAY LIFEGRID",
    "titleRight": "B3/S23"
  }
}
```

Useful timing presets:

```json
{ "frames": 72, "duration": "30s", "holdFrames": 3 }
```

```json
{ "frames": 120, "duration": "60s", "holdFrames": 5 }
```

## GitHub Actions

The included workflow renders the SVG:

- on push
- once per day
- manually from the Actions tab

Daily rendering lets the block pick up fresh GitHub contribution data when `GITHUB_TOKEN` is available.

## Modes

Available now:

- `lifegrid`: Conway Game of Life on a contribution-style grid.

Planned:

- `snake`
- `pacman`
- `matrix`
- `hashwave`

## License

MIT

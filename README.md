<h1 align="center">README Arcade</h1>

<p align="center">
  Animated arcade blocks for GitHub profile READMEs.
</p>

<p align="center">
  <a href="./README.ru.md">Russian mirror</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-2da44e?style=flat-square" alt="MIT license">
  <img src="https://img.shields.io/badge/python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/dependencies-zero-6f7787?style=flat-square" alt="Zero dependencies">
  <img src="https://img.shields.io/badge/modes-5-39d353?style=flat-square" alt="Five modes">
  <img src="https://img.shields.io/badge/theme-auto-58a6ff?style=flat-square" alt="Auto theme">
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/readme-arcade-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/readme-arcade.svg">
    <img src="./dist/readme-arcade.svg" width="920" alt="Animated README Arcade block">
  </picture>
</p>

## What It Does

README Arcade generates animated SVG blocks for GitHub profile READMEs.

It is built around GitHub contribution-style grids: small cells, dark/light theme assets, deterministic motion, and optional contribution data from the GitHub API. The SVG repeats forever, so it keeps moving inside a README without JavaScript.

Available modes:

- `lifegrid`: Conway Game of Life, started from your GitHub login.
- `snake`: a short pink-headed snake and a faster worm start after the login intro, eat the darkest cells first, and keep moving without taking over the grid.
- `matrix`: vertical code rain with login intro and GitHub-style intensity trails.
- `hashwave`: a dense crypto-native wave of hashed contribution cells and scan pulses.
- `boot`: an old-machine boot sweep with memory-map fill, cursor ticks, and login intro.

## Gallery

### Lifegrid

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/gallery/lifegrid-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/gallery/lifegrid.svg">
    <img src="./dist/gallery/lifegrid.svg" width="920" alt="README Arcade lifegrid mode">
  </picture>
</p>

### Snake

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/gallery/snake-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/gallery/snake.svg">
    <img src="./dist/gallery/snake.svg" width="920" alt="README Arcade snake mode">
  </picture>
</p>

### Matrix

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/gallery/matrix-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/gallery/matrix.svg">
    <img src="./dist/gallery/matrix.svg" width="920" alt="README Arcade matrix mode">
  </picture>
</p>

### Hashwave

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/gallery/hashwave-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/gallery/hashwave.svg">
    <img src="./dist/gallery/hashwave.svg" width="920" alt="README Arcade hashwave mode">
  </picture>
</p>

### Boot

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/gallery/boot-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/gallery/boot.svg">
    <img src="./dist/gallery/boot.svg" width="920" alt="README Arcade boot mode">
  </picture>
</p>

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
    <img src="./dist/readme-arcade.svg" width="920" alt="Animated README Arcade block">
  </picture>
</p>
```

## Config

`mode` selects the animation.

`duration` controls how long one full animation loop takes. The SVG repeats forever.

`frames` controls how many precomputed states are embedded into that loop. More frames make the loop feel longer and less repetitive.

`holdFrames` controls how long the initial login mark stays visible before the selected mode starts moving.

For `snake`, `length` sets the main body length, `maxLength` caps growth, and `growPerFood` controls how much the snake grows after eating a cell. Keep `growPerFood` at `0` for a clean runner that eats cells without getting long. The optional fast worm uses `worm`, `wormLength`, `wormSpeed`, and `wormGrowPerFood`.

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

Render another mode:

```bash
python scripts/render.py --mode snake --base-name readme-arcade --out-dir dist
```

```bash
python scripts/render.py --mode matrix --base-name readme-arcade --out-dir dist
```

```bash
python scripts/render.py --mode hashwave --base-name readme-arcade --out-dir dist
```

```bash
python scripts/render.py --mode boot --base-name readme-arcade --out-dir dist
```

## GitHub Actions

The included workflow renders the SVG:

- on push
- once per day
- manually from the Actions tab

Daily rendering lets the block pick up fresh GitHub contribution data when `GITHUB_TOKEN` is available.

## Donate

If README Arcade is useful for your profile or project, you can support the author:

```text
TON: pointoncurve.ton
BTC: 1ECDSA1b4d5TcZHtqNpcxmY8pBH1GgHntN
USDT (TRC20): TSWcFVfqCp4WCXrUkkzdCkcLnhtFLNN3Ba
```

Donations are optional. Always verify the address and network before sending crypto.

## Disclaimer

README Arcade is provided as-is under the MIT License. Generated SVGs are decorative README assets; use them at your own risk. The project does not provide financial, security, or investment advice.

## License

MIT

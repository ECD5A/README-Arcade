<h1 align="center">README Arcade</h1>

<p align="center">
  Turn your GitHub login into an animated contribution-grid arcade block.
</p>

<p align="center">
  <a href="./README.ru.md">Русская версия</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-2da44e?style=flat-square" alt="MIT license">
  <img src="https://img.shields.io/badge/python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/dependencies-zero-6f7787?style=flat-square" alt="Zero dependencies">
  <img src="https://img.shields.io/badge/modes-4-39d353?style=flat-square" alt="Four modes">
  <img src="https://img.shields.io/badge/theme-auto-58a6ff?style=flat-square" alt="Auto theme">
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/readme-arcade-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/readme-arcade.svg">
    <img src="./dist/readme-arcade.svg" width="920" alt="Animated README Arcade block">
  </picture>
</p>

## Quick Start

1. Fork this repository.

2. Open `readme-arcade.config.json` and change three fields:

```json
{
  "user": "YOUR_LOGIN",
  "mode": "snake",
  "speed": "normal"
}
```

`user` is your GitHub login. `mode` is `lifegrid`, `snake`, `matrix`, or `defrag`. `speed` is `slow`, `normal`, `fast`, or `turbo`.

3. Commit the file. GitHub Actions will render SVG files into `dist/`.

If Actions are disabled in your fork, open the Actions tab, enable workflows, then run `render README Arcade` once.

4. Paste this into your profile README.

Your profile README is the `README.md` file inside the special repository named `YOUR_LOGIN/YOUR_LOGIN`.

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YOUR_LOGIN/readme-arcade/main/dist/readme-arcade-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/YOUR_LOGIN/readme-arcade/main/dist/readme-arcade.svg">
    <img src="https://raw.githubusercontent.com/YOUR_LOGIN/readme-arcade/main/dist/readme-arcade.svg" width="920" alt="README Arcade">
  </picture>
</p>
```

Replace `YOUR_LOGIN` in the snippet. If your fork has another repository name, replace `readme-arcade` too.

## Modes

| Mode | What it does |
| --- | --- |
| `lifegrid` | Conway's Game of Life starts from your login. |
| `snake` | A snake and a fast worm appear from your login and eat GitHub-colored cells. |
| `matrix` | Code rain drops over your login. |
| `defrag` | A Windows 98-style disk map compacts fragmented cells. |

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

### Defrag

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/gallery/defrag-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/gallery/defrag.svg">
    <img src="./dist/gallery/defrag.svg" width="920" alt="README Arcade defrag mode">
  </picture>
</p>

## Local Preview

You do not need local setup if you use GitHub Actions. Local render is optional:

```bash
python scripts/render.py
python scripts/render_gallery.py
```

Open `preview/index.html` to view all modes.

## Advanced Config

The small config is enough for most users. You can still override a mode:

```json
{
  "user": "YOUR_LOGIN",
  "mode": "snake",
  "speed": "fast",
  "snake": {
    "duration": "24s",
    "titleLeft": "SNAKE"
  }
}
```

Mode-specific `duration` wins over `speed`.

## Support

If README Arcade helped your profile, tips are welcome:

```text
TON: pointoncurve.ton
BTC: 1ECDSA1b4d5TcZHtqNpcxmY8pBH1GgHntN
USDT (TRC20): TSWcFVfqCp4WCXrUkkzdCkcLnhtFLNN3Ba
```

## License

MIT

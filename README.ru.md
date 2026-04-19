<h1 align="center">README Arcade</h1>

<p align="center">
  Преврати свой GitHub-ник в анимированный arcade-арт в стиле contribution grid.
</p>

<p align="center">
  <a href="./README.md">English README</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-2da44e?style=flat-square" alt="MIT license">
  <img src="https://img.shields.io/badge/python-3.10%2B-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/dependencies-zero-6f7787?style=flat-square" alt="Zero dependencies">
  <img src="https://img.shields.io/badge/modes-4-39d353?style=flat-square" alt="Four modes">
  <img src="https://img.shields.io/badge/dark%2Flight-auto-58a6ff?style=flat-square" alt="Auto dark and light theme">
</p>

## Галерея

### Lifegrid

Conway's Game of Life стартует из твоего GitHub-ника.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/gallery/lifegrid-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/gallery/lifegrid.svg">
    <img src="./dist/gallery/lifegrid.svg" width="920" alt="README Arcade lifegrid mode">
  </picture>
</p>

### Snake

Змейка и быстрый червяк появляются из ника и едят GitHub-цветные клетки.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/gallery/snake-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/gallery/snake.svg">
    <img src="./dist/gallery/snake.svg" width="920" alt="README Arcade snake mode">
  </picture>
</p>

### Matrix

Code rain падает поверх твоего ника.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/gallery/matrix-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/gallery/matrix.svg">
    <img src="./dist/gallery/matrix.svg" width="920" alt="README Arcade matrix mode">
  </picture>
</p>

### Defrag

Карта диска в духе Windows 98 уплотняет фрагментированные клетки.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/gallery/defrag-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/gallery/defrag.svg">
    <img src="./dist/gallery/defrag.svg" width="920" alt="README Arcade defrag mode">
  </picture>
</p>

## Быстрый Старт

1. Сделай fork этого репозитория.

2. Открой `readme-arcade.config.json` и поменяй три поля:

```json
{
  "user": "YOUR_LOGIN",
  "mode": "snake",
  "speed": "normal"
}
```

`user` это твой GitHub-логин. `mode`: `lifegrid`, `snake`, `matrix` или `defrag`. `speed`: `slow`, `normal`, `fast` или `turbo`.

3. Закоммить файл. GitHub Actions сгенерирует SVG-файлы в `dist/`.

Если Actions отключены в форке, открой вкладку Actions, включи workflows и один раз запусти `render README Arcade`.

4. Вставь это в свой profile README.

Profile README лежит в специальном репозитории с именем `YOUR_LOGIN/YOUR_LOGIN`.

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YOUR_LOGIN/README-Arcade/main/dist/readme-arcade-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/YOUR_LOGIN/README-Arcade/main/dist/readme-arcade.svg">
    <img src="https://raw.githubusercontent.com/YOUR_LOGIN/README-Arcade/main/dist/readme-arcade.svg" width="920" alt="README Arcade">
  </picture>
</p>
```

Замени `YOUR_LOGIN` в сниппете. Если форк называется не `README-Arcade`, замени и имя репозитория.
Блок `<picture>` сам подставляет темный или светлый SVG под тему GitHub.

## Локальный Просмотр

Локальная установка не нужна, если используешь GitHub Actions. Локальная генерация опциональна:

```bash
python scripts/render.py
python scripts/render_gallery.py
```

Открой `preview/index.html`, чтобы посмотреть все режимы.

## Расширенный Конфиг

Короткого конфига хватает большинству пользователей. Но любой режим можно настроить вручную:

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

Если у режима указан свой `duration`, он важнее общего `speed`.

## Поддержать Автора

Если README Arcade пригодился для профиля, можно поддержать автора:

```text
TON: pointoncurve.ton
BTC: 1ECDSA1b4d5TcZHtqNpcxmY8pBH1GgHntN
USDT (TRC20): TSWcFVfqCp4WCXrUkkzdCkcLnhtFLNN3Ba
```

## Лицензия

MIT

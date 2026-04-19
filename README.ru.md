<h1 align="center">README Arcade</h1>

<p align="center">
  Анимированные arcade-блоки в стиле GitHub contribution grid для profile README.
</p>

<p align="center">
  <a href="./README.md">English README</a>
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

## Что Это?

README Arcade генерирует анимированные SVG-блоки, которые выглядят как GitHub contribution grid, но ведут себя как маленькие ретро-экраны.

Проект сделан для profile README:

- без JavaScript
- без установки пакетов
- отдельные SVG для светлой и темной темы
- детерминированная анимация от GitHub-ника
- ежедневная пересборка через GitHub Actions
- contribution-данные GitHub, если доступен `GITHUB_TOKEN`

Проект оставлен на Python, потому что так удобнее для форков: Python уже есть в GitHub Actions, работает на Windows/macOS/Linux и не требует компилятора или Node-зависимостей. На C/C++ было бы лампово, но порог входа для обычного пользователя стал бы выше.

## Режимы

- `lifegrid`: Conway's Game of Life, стартует из твоего GitHub-ника.
- `snake`: короткая змейка и быстрый червяк появляются из клеток ника и едят GitHub-цветные квадраты.
- `matrix`: code rain накрывает интро с ником и остается в стиле contribution grid.
- `defrag`: карта диска в духе Windows 98, где фрагменты постепенно уплотняются.

## Галерея

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

## Быстрый Старт

Сделай fork репозитория и измени `readme-arcade.config.json`:

```json
{
  "user": "YOUR_LOGIN",
  "mode": "snake",
  "speed": "normal"
}
```

Закоммить изменение. Встроенный GitHub Action сгенерирует SVG-файлы в `dist/`.
Если Actions отключены в форке, открой вкладку Actions и один раз включи workflows.

Вставь это в свой GitHub profile README. Замени `YOUR_LOGIN` и `readme-arcade`, если у форка другой владелец или другое имя репозитория:

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/YOUR_LOGIN/readme-arcade/main/dist/readme-arcade-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/YOUR_LOGIN/readme-arcade/main/dist/readme-arcade.svg">
    <img src="https://raw.githubusercontent.com/YOUR_LOGIN/readme-arcade/main/dist/readme-arcade.svg" width="920" alt="README Arcade">
  </picture>
</p>
```

Для базового подключения этого достаточно.
Этот же сниппет лежит в `examples/profile-readme.md`.

## Конфиг

Большинству пользователей нужны только три поля:

```json
{
  "user": "YOUR_LOGIN",
  "mode": "lifegrid",
  "speed": "normal"
}
```

`mode`: `lifegrid`, `snake`, `matrix` или `defrag`.

`speed`: `slow`, `normal`, `fast` или `turbo`.

Если хочется тонкой настройки, любой блок режима можно переопределить:

```json
{
  "user": "YOUR_LOGIN",
  "mode": "snake",
  "speed": "fast",
  "snake": {
    "duration": "24s",
    "frames": 120,
    "titleLeft": "SNAKE"
  }
}
```

Если у режима указан свой `duration`, он важнее общего `speed`.

## Локальная Генерация

Сгенерировать выбранный режим:

```bash
python scripts/render.py --config readme-arcade.config.json --out-dir dist
```

Сгенерировать другой режим без изменения конфига:

```bash
python scripts/render.py --mode matrix --base-name readme-arcade --out-dir dist
```

Сгенерировать галерею:

```bash
python scripts/render_gallery.py
```

Открой `preview/index.html`, чтобы посмотреть все режимы локально.

## GitHub Actions

Workflow в `.github/workflows/render.yml` генерирует SVG:

- при push
- раз в день
- вручную через вкладку Actions

Ежедневная пересборка нужна, чтобы contribution-клетки могли меняться со временем.

## Support

Если README Arcade пригодился для профиля, можно поддержать автора:

```text
TON: pointoncurve.ton
BTC: 1ECDSA1b4d5TcZHtqNpcxmY8pBH1GgHntN
USDT (TRC20): TSWcFVfqCp4WCXrUkkzdCkcLnhtFLNN3Ba
```

## Лицензия

MIT

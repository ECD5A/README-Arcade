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
Маршрут меняется вместе с ежедневным seed рендера, а правило дистанции не даёт
им проводить большую часть анимации бок о бок.

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

### Подключение как GitHub Action

Добавь файл `.github/workflows/readme-arcade.yml` в профильный репозиторий
или в другой репозиторий, где будут храниться сгенерированные SVG:

```yaml
name: README Arcade

on:
  workflow_dispatch:
  schedule:
    - cron: "17 3 * * *"

permissions:
  contents: write

jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v7

      - name: Generate arcade SVG
        uses: ECD5A/README-Arcade@v1
        with:
          user: YOUR_LOGIN
          mode: snake
          speed: normal

      - name: Commit generated SVG
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add dist
          git diff --cached --quiet || git commit -m "Update README Arcade"
          git push
```

Замени `YOUR_LOGIN`, закоммить workflow и один раз запусти его во вкладке
Actions. Action создаст `dist/readme-arcade.svg` и
`dist/readme-arcade-dark.svg` в твоём репозитории. Запуск по расписанию
обновляет contribution grid каждый день. Маршруты Snake по умолчанию используют
текущую UTC-дату как seed и тоже меняются ежедневно.

Используй `ECD5A/README-Arcade@v1` для совместимых обновлений первой версии или
`ECD5A/README-Arcade@v1.0.0` для полностью зафиксированной установки.

#### Параметры Action

| Параметр | По умолчанию | Назначение |
| --- | --- | --- |
| `user` | владелец репозитория | GitHub-логин для генерации |
| `mode` | config или `lifegrid` | `lifegrid`, `snake`, `matrix` или `defrag` |
| `speed` | config или `normal` | `slow`, `normal`, `fast` или `turbo` |
| `config` | `readme-arcade.config.json` | Необязательный JSON-config в твоём репозитории |
| `output-dir` | `dist` | Каталог для SVG |
| `base-name` | config или `readme-arcade` | Основа имени файлов |
| `seed` | текущая UTC-дата | Воспроизводимый seed анимации |
| `github-token` | workflow token | Токен для чтения contributions |
| `python-version` | `3.13` | Версия Python для renderer |

Action возвращает outputs `light-svg` и `dark-svg` с путями к созданным файлам.
Он генерирует SVG, а правила коммита и push остаются под контролем твоего workflow.

### Fork для полной кастомизации

Fork остаётся лучшим вариантом, если хочется менять renderer, создавать
собственные режимы или поддерживать глубоко изменённую сборку.

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

Встроенный workflow также запускается раз в сутки. При ручном запуске можно
указать собственный `seed`.

По умолчанию минимальная дистанция между змейкой и червяком равна трём клеткам.
Её можно изменить в конфигурации:

```json
{
  "snake": {
    "minActorDistance": 3
  }
}
```

4. Вставь это в свой profile README.

Profile README лежит в специальном репозитории с именем
`YOUR_LOGIN/YOUR_LOGIN`. Если workflow и README находятся в этом же
репозитории, используй относительные пути:

```html
<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./dist/readme-arcade-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./dist/readme-arcade.svg">
    <img src="./dist/readme-arcade.svg" width="920" alt="README Arcade">
  </picture>
</p>
```

Если SVG находятся в отдельном репозитории или форке, замени каждый
относительный путь на raw URL, например
`https://raw.githubusercontent.com/YOUR_LOGIN/README-Arcade/main/dist/readme-arcade-dark.svg`.

Блок `<picture>` автоматически подставляет тёмный или светлый SVG под тему
каждого посетителя. Обычный SVG остаётся fallback для клиентов без определения
темы.

Все режимы можно посмотреть в
[живой GitHub Pages-галерее](https://ecd5a.github.io/README-Arcade/).

## Локальный Просмотр

Локальная установка не нужна, если используешь GitHub Actions. Локальная генерация опциональна:

```bash
python scripts/render.py
python scripts/render_gallery.py
```

Команда `python scripts/render.py --mode snake --seed demo` позволяет локально
посмотреть конкретный вариант маршрута.

Открой `preview/index.html`, чтобы посмотреть все режимы.

## Участие и Безопасность

Предложения по улучшению проекта приветствуются. Перед pull request прочитай
[CONTRIBUTING.md](CONTRIBUTING.md). Для воспроизводимых ошибок и конкретных
предложений используй подготовленные формы issues.

Не публикуй уязвимости в открытых issues. Инструкция по приватной отправке
отчёта находится в [SECURITY.md](SECURITY.md).

## Поддержать Автора

Если README Arcade пригодился для профиля, можно поддержать автора:

```text
TON: pointoncurve.ton
BTC: 1ECDSA1b4d5TcZHtqNpcxmY8pBH1GgHntN
USDT (TRC20): TUF4vPdB6QkjCvZq18rBL4Qj4dK5ihCN75
```

## Лицензия

MIT

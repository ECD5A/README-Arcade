# Contributing to README Arcade

Thanks for helping improve README Arcade. Focused bug fixes, accessibility
improvements, new tests, documentation fixes, and well-scoped visual
enhancements are welcome.

## Before You Start

- Search existing issues before opening a new one.
- Use an issue for behavior changes or a new mode so the approach can be
  discussed before a large implementation.
- Keep pull requests focused on one problem.
- Never include tokens, private contribution data, or generated files
  containing sensitive information.

Security vulnerabilities must be reported privately. Follow
[SECURITY.md](SECURITY.md) instead of opening a public issue.

## Local Setup

README Arcade has no runtime dependencies. Python 3.10 or newer is sufficient.

```bash
git clone https://github.com/YOUR_LOGIN/README-Arcade.git
cd README-Arcade
python -m unittest discover -s tests -v
```

Render the configured mode:

```bash
python scripts/render.py
```

Render the complete gallery:

```bash
python scripts/render_gallery.py
```

Open `preview/index.html` to inspect all modes in both light and dark themes.

## Making Changes

1. Create a branch from the latest `main`.
2. Add or update tests for behavior changes.
3. Run the unit suite.
4. Render every affected mode and inspect both generated themes.
5. Update English and Russian documentation together when user-facing
   behavior changes.
6. Open a pull request using the repository template.

Do not commit `dist/` changes unless the visual output intentionally changed.
The render workflow updates generated assets on `main`.

## Project Layout

- `readme_arcade/modes/` contains the four renderers.
- `readme_arcade/config.py` owns defaults and configuration validation.
- `readme_arcade/github.py` reads the contribution calendar.
- `readme_arcade/grid_svg.py` contains shared SVG helpers.
- `scripts/` contains render entry points.
- `tests/` contains the standard-library test suite.
- `examples/` contains mode-specific configurations.

## Pull Request Checklist

- Tests pass locally.
- Changed render modes were visually checked.
- User-controlled text remains escaped in generated SVG.
- Output paths stay inside the requested output directory.
- Documentation matches the implementation.
- The pull request does not mix unrelated cleanup with the intended change.

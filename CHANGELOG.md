# Changelog

All notable changes to README Arcade are documented in this file.

## [1.0.0] - 2026-07-26

### Added

- A reusable composite GitHub Action with inputs for login, mode, speed,
  configuration, output paths, filenames, route seed, token, and Python version.
- Action outputs for the generated light and dark SVG paths.
- A GitHub Pages gallery with live previews and a copyable installation workflow.
- Automated smoke coverage for the public Action interface.

### Changed

- The repository's own daily renderer now uses the same composite Action exposed
  to users.
- README Arcade now uses the current UTC date as the default deterministic route
  seed when invoked as an Action.
- Package version advanced to `1.0.0`.

[1.0.0]: https://github.com/ECD5A/README-Arcade/releases/tag/v1.0.0

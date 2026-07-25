# Changelog

All notable changes to README Arcade are documented in this file.

## [Unreleased]

## [1.0.1] - 2026-07-26

### Added

- A persistent `Dark / Light / Auto` switcher for the live gallery, with dark
  mode as the first-visit default.

### Fixed

- Profile README instructions now use relative SVG paths for the recommended
  same-repository Action setup, so GitHub can resolve both theme assets.
- Donation details are consistent across the English and Russian documentation.
- Package version advanced to `1.0.1`.

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

[Unreleased]: https://github.com/ECD5A/README-Arcade/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/ECD5A/README-Arcade/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/ECD5A/README-Arcade/releases/tag/v1.0.0

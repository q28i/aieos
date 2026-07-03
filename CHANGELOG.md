# Changelog

All notable changes to AIEOS will be documented in this file.

## [1.0.2] - 2026-07-03

### Changed
- **Documentation Enhancements**: Overhauled the core `README.md` to implement a high-impact, professional-grade open-source documentation layout, adding badge panels, architecture matrices, domain tables, system requirement specifications, and FAQ blocks.

## [1.0.1] - 2026-07-03

### Changed
- **Python Missing Error Guidelines**: Updated the startup warning message in the Node binary wrapper `bin/cli.js` when Python `>= 3.11` is missing, guiding the user to standard downloads and next execution steps.

## [1.0.0] - 2026-07-03

### Added
- **Audited CLI Commands**: Fully audited all CLI execution entries, removing placeholder login/logout steps and implementing functional git update pulls and local package publishing.
- **Python 3.11+ Version Gate**: Added runtime and binary checks enforcing python version bounds.
- **CLI Flags**: Standardized flags for `--help`, `--version`, and `--debug` to prevent Python trace logs on standard console exceptions.
- **CI Workflows**: Added multi-OS GitHub Actions CI pipeline testing setups on Windows, Linux, and macOS.

# Changelog

All notable changes to AIEOS will be documented in this file.

## [1.0.0-beta.1] - 2026-07-03

### Changed
- **Package Size Optimization**: Removed the compiled dynamic specification folder (`AIEOS/`) from the NPM distribution whitelist.
- Excluded Python cache bytecodes and workspace temporary folders, reducing the NPM file count by 96% (from 454 files to 15 files) and reducing target unpacking size.

## [1.0.0-beta] - 2026-07-02

### Added
- **AIEOS CLI**: Pure-Python command-line execution engine supporting workspace initialization, packages validation, profiles activation, local telemetry diagnostic checks, and publisher adapters.
- **Git Cloning Installer**: Added direct support for running subprocess `git clone` when installing remote GitHub package URLs (e.g. `aieos install github:owner/repo`).
- **Cognitive Services, Protocols, and Policies**: Standardized specification layouts governing structured collaborative reasoning interfaces.
- **Embedded Database Registry**: Integrated local SQLite schema initialization mapping node assets and decision structures.
- **Programmatic SDK Package Creators**: Programmatic capability template builder.
- **IDE Adapters**: Hook wrappers supporting external AI framework interactions.

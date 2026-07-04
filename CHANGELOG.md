# Changelog

All notable changes to AIEOS will be documented in this file.

## [1.3.0] - 2026-07-03

### Added
- **Clean Non-Polluting Layout**: Scaffolds all workspace resources inside the `.aieos/` folder (`system/`, `project/`, `config/`, `skills/`, `state/`) to keep the root directory completely clean.
- **Global vs Local Runtime Split**: Separated AIEOS runtime capabilities and global specifications (`~/.aieos/`) from local project-specific decision memory, contracts, and SQLite DBs.
- **Clean Uninstall**: Added `uninstall` route and menu option to remove AI agent integrations while leaving project memory, decisions, and contracts intact.
- **Project Template Selects**: Introduced SaaS, Computation Engine, Backend, Library, and AI Agent templates in the interactive installation wizard.

## [1.2.0] - 2026-07-03

### Added
- **Interactive CLI Wizard**: Implemented a Socratic interactive installer when no arguments are provided. Includes Step 1 (Target location selection), Step 2 (Scan detection for active AI customization folders), Step 3 (Behavior profiles with interactive before/after previews), Step 4 (Component selects), and Step 5 (Animating console progress bars).
- **Behavior Profiles**: Added Architect, Mentor, Reviewer, and Decision OS (AIEOS) profiles containing tailored AI agent instruction templates.

## [1.1.0] - 2026-07-03

### Added
- **Direct Platform Installer**: OVERHAULED the primary CLI execution. Running `npx @q28i/aieos` acts as an automated plug-and-play installer, accepting direct targets like `--claude`, `--cursor`, `--gemini`, `--codex`, `--antigravity`, `--opencode`, `--kiro`, or `--all`.
- **Project Directory Targets**: Scaffold workspace environments on-demand by passing folders (e.g. `npx @q28i/aieos .` or `npx @q28i/aieos ../ScraperLog`).
- **Whitelisted Templates**: Re-whitelisted `AIEOS` specifications inside the NPM distribution whitelist to ensure the installer copies full policies, protocols, and profiles directly from NPM caches.

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

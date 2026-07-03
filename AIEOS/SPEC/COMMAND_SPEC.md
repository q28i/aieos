# AIEOS Command Specification (v1.0.0)

AIEOS commands are exposed inside AI chat sessions via slash commands (e.g. `/skill install`) and map natively to CLI commands (e.g. `npx @q28i/aieos skill install`). This document defines the standard namespaces, subcommands, and behaviors.

---

## 1. `/skill` Namespace
Manages individual capability packages (skills) within the active workspace.

| Slash Command | CLI Command | Arguments | Description |
| --- | --- | --- | --- |
| `/skill install` | `aieos skill install` | `<skill_id>` | Downloads and installs a capability. Resolves dependencies. |
| `/skill search` | `aieos skill search` | `<query>` | Queries the registry for matching capabilities. |
| `/skill remove` | `aieos skill remove` | `<skill_id>` | Uninstalls a capability and clears its local cache. |
| `/skill enable` | `aieos skill enable` | `<skill_id>` | Mounts an installed capability into the active runtime. |
| `/skill disable` | `aieos skill disable` | `<skill_id>` | Unmounts a capability from execution without deleting it. |
| `/skill info` | `aieos skill info` | `<skill_id>` | Displays author, version, dependencies, and permissions. |

---

## 2. `/mode` Namespace
Configures active execution workflows and team assembly rules.

| Slash Command | CLI Command | Arguments | Description |
| --- | --- | --- | --- |
| `/mode startup` | `aieos mode startup` | None | Emphasizes generalist founder workflows. |
| `/mode trading` | `aieos mode trading` | None | Focuses on finance, quant, and risk management validation. |
| `/mode research` | `aieos mode research` | None | Mounts advanced Socratic inquiry and literature checks. |
| `/mode backend` | `aieos mode backend` | None | Triggers API engineering, database, and system specs. |

---

## 3. `/aieos` Namespace
Manages workspace-level configurations, diagnostics, and memory logs.

| Slash Command | CLI Command | Arguments | Description |
| --- | --- | --- | --- |
| `/aieos recommend` | `aieos recommend` | None | Invokes project scan and outputs matched recommendations. |
| `/aieos doctor` | `aieos doctor` | None | Runs file integrity and permission validation tests. |
| `/aieos graph` | `aieos graph` | None | Visualizes capability DAG node relations and loading priorities. |
| `/aieos memory` | `aieos memory` | `<consolidate\|prune>` | Triggers memory summarization or database optimizations. |
| `/aieos status` | `aieos status` | None | Displays active mode, mounted skills, and permission states. |

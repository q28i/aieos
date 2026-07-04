<a name="top"></a>

<div align="center">

<br />

<img src="https://img.shields.io/badge/%F0%9F%A7%A0_AIEOS-f97316?style=for-the-badge&labelColor=0a0a0f" alt="AIEOS" height="52" />

<h1>AIEOS</h1>

<h3>AIEOS exists to turn ideas into professionally executed outcomes by ensuring AI researches, plans, validates, questions assumptions, and builds with the discipline of a real multidisciplinary team instead of improvising.</h3>

<p><i>The AI Execution Operating System</i></p>

<br />

[![CI](https://github.com/q28i/aieos/actions/workflows/ci.yml/badge.svg)](https://github.com/q28i/aieos/actions)
[![Release](https://img.shields.io/github/v/release/q28i/aieos?style=flat-square&color=f97316)](https://github.com/q28i/aieos/releases)
[![npm](https://img.shields.io/npm/v/@q28i/aieos?style=flat-square&color=cb3837&logo=npm)](https://www.npmjs.com/package/@q28i/aieos)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square)](#-license)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-ec4899?style=flat-square)](#-contributing)

<br />

**[⚡ Install](#-install---choose-your-target)** &nbsp;·&nbsp; **[🧠 Levels of AI](#-levels-of-ai)** &nbsp;·&nbsp; **[⚙️ Execution OS](#-the-execution-os)** &nbsp;·&nbsp; **[▶️ Commands](#-commands)** &nbsp;·&nbsp; **[❓ FAQ](#-faq)**

</div>

<br />

```bash
npx @q28i/aieos
```

<br />

---

## ✨ What is AIEOS?

**AIEOS is an AI Execution Operating System built around installable capabilities, persistent project intelligence, structured execution workflows, and multidisciplinary reasoning.**

### The Motivation
Modern AI is excellent at generating responses but often lacks the structured execution process required for complex work. It may skip research, fail to identify domain-specific best practices, overlook existing solutions, or proceed with unwarranted confidence despite missing knowledge.

**AIEOS exists to address that gap by providing an execution operating system that acquires relevant knowledge, organizes multidisciplinary expertise, applies structured planning and validation, and maintains persistent project intelligence before and during execution.**

### The Four Pillars
1. **Vision** ("I have an idea."): Deconstructing raw intent into clear success criteria.
2. **Knowledge** ("What already exists?"): Enforcing domain research, standards lookups, regulations checks, and architectural review before coding.
3. **Judgment** ("What should we build?"): Evaluating alternatives, trade-offs, and critical assumptions under uncertainty.
4. **Execution** ("Build it correctly."): Enforcing test coverage, security boundaries, and modular decoupling.

### 🧠 Levels of AI

- **Level 0 (Default AI)**: Question-answering tool or code generator. Waits for human instructions.
- **Level 1 (Persona Prompts)**: Mimics a specific role (e.g. "Act as a Senior Engineer"). Rigid, single-threaded.
- **Level 2 (Execution OS / AIEOS)**: Acts as an operating system. Identifies project gaps, recommends capabilities, assembles specialized teams dynamically, manages risk, and executes multi-step plans.

---

## ⚡ Install — Choose your target

Install AIEOS into your agent environment using `npx @q28i/aieos`. The installer will automatically scan your system and configure the appropriate paths.

### One-Command Setup

```bash
npx @q28i/aieos
```

Alternatively, bypass the wizard and target specific environments:

| Target Platform | Command | Destination Path / File |
| --- | --- | --- |
| **Claude Code** | `npx @q28i/aieos --claude` | `~/.claude/skills/` |
| **Cursor IDE** | `npx @q28i/aieos --cursor` | Creates `.cursorrules` in project directory |
| **Gemini CLI** | `npx @q28i/aieos --gemini` | `~/.gemini/skills/` |
| **Codex CLI** | `npx @q28i/aieos --codex` | `~/.codex/skills/` |
| **Antigravity IDE** | `npx @q28i/aieos --antigravity` | `~/.gemini/config/skills/` |
| **OpenCode** | `npx @q28i/aieos --opencode` | `~/.opencode/skills/` |
| **Kiro CLI** | `npx @q28i/aieos --kiro` | `~/.kiro/skills/` |
| **All platforms** | `npx @q28i/aieos --all` | Deploys to all of the above |

---

## ⚙️ The Execution OS

AIEOS shifts the execution paradigm from raw task processing to a values-aligned decision pipeline. It dynamically manages the project lifecycle through its core domains:

<div align="center">

| Domain | Scope | Key Abstractions |
| --- | --- | --- |
| 📜 **Constitutions** | `CONSTITUTION/` | User Agency, Engineering Quality, Security Constraints |
| 🔌 **Services** | `SERVICES/` | Kernel Orchestration, SQLite Memory, EventBus, Evolution |
| 🧠 **Protocols** | `PROTOCOLS/` | RealityCheck, Curiosity, Wisdom, Judgment Loops |
| ⚙️ **Policies** | `POLICIES/` | CognitiveBias Filters, LearningProgress, KnowledgeROI |

</div>

### Dynamic Team Assembly

When AIEOS scans a workspace (e.g., a complex data ingestion application), it executes the **AIEOS Decision Protocol** and loads specialized roles:
- **Lead Architect**: Handles decoupling, technical debt, and system boundaries.
- **Domain Specialist**: Formulates assumptions, checks edge cases, and verifies domain rules.
- **Vetting Officer**: Defines constraints, validates security boundaries, and verifies dependency risks.

---

## ▶️ Commands

Once AIEOS is installed, you can invoke it manually, or **your AI can invoke these commands natively** to manage its own capabilities.

### Layer 1: User Slash Commands (IDE Support)
You can directly command your agent to manage its capabilities using slash-command syntax.

- `/aieos discover` - Runs the Socratic project discovery engine (intent extraction, gap analysis, reality checks).
- `/aieos inspect` / `/aieos audit` - Scores project health metrics, lists top blockers, and recommends the Next Best Action.
- `/aieos recommend` - Scans your current project (dependencies, directories, code) and recommends capabilities.
- `/aieos install <capability>` - Installs a specific capability into your workspace.
- `/aieos enable <capability>` - Enables a locally installed capability.
- `/aieos disable <capability>` - Disables a capability without deleting it.
- `/aieos list` - Lists all currently installed capabilities and workspace status.

### Layer 2: CLI Equivalents
Under the hood, these map to the AIEOS CLI:
```bash
npx @q28i/aieos discover
npx @q28i/aieos inspect
npx @q28i/aieos install @aieos/research
npx @q28i/aieos list
```

---

## 📁 Repository Layout

```text
aieos/
├─ 📂 AIEOS/                     # Dynamic system specifications & schemas
├─ 📂 core/                      # Core JS runtime, installer, & compiler engine
├─ 📂 adapters/                  # Adapter SDK for Claude, Cursor, Gemini, & Antigravity
├─ 📂 official-capabilities/     # Core capability packages (skills) stored as files on disk
├─ 📂 marketplace/               # Package registry & specifications builder
│   ├─ doc_manager.py            # Spec build manager
│   └─ 📂 doc_system/            # Python CLI & diagnostic engines
├─ 📂 bin/                       # Node.js binary wrapper
├─ 📂 tests/                     # Core integration unit tests
├─ 📜 LICENSE                    # MIT License
└─ 📖 README.md
```

---

## 📋 System Requirements
- **Node.js**: `18.0.0` or higher
- **Python**: `3.11` or higher (automatically verified on startup)
- **Git**: Required for remote capability package operations

---

## ❓ FAQ

<details>
<summary><b>Why does AIEOS require Python?</b></summary>
<br/>
AIEOS uses lightweight, dependency-free Python modules to execute local schema validation, SQLite transactions, and mathematical benchmark computations locally.
</details>

<details>
<summary><b>How does Cursor integration work?</b></summary>
<br/>
The installer appends AIEOS agency and honesty rules directly to your <code>.cursorrules</code> file, ensuring the LLM is primed on decision-quality abstractions during chat or composer prompts.
</details>

---

## 🤝 Contributing

PRs are welcome! Feel free to file issues or submit pull requests to extend agent target support or refine cognitive protocols.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">
<br/>
<sub>Built to empower human agency. Zero lock-in.</sub>
<br/><br/>

**[⬆ back to top](#top)**

</div>

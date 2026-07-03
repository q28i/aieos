<a name="top"></a>

<div align="center">

<br />

<img src="https://img.shields.io/badge/%F0%9F%A7%A0_AIEOS-f97316?style=for-the-badge&labelColor=0a0a0f" alt="AIEOS" height="52" />

<h1>AIEOS</h1>

<h3>The model-independent <b>Human Intelligence Amplification Runtime</b> &amp; Decision OS.</h3>

<p><i>25 capabilities · 7 cognitive protocols · one SQLite database registry · zero dependencies</i></p>

<br />

[![CI](https://github.com/q28i/aieos/actions/workflows/ci.yml/badge.svg)](https://github.com/q28i/aieos/actions)
[![Release](https://img.shields.io/github/v/release/q28i/aieos?style=flat-square&color=f97316)](https://github.com/q28i/aieos/releases)
[![npm](https://img.shields.io/npm/v/@q28i/aieos?style=flat-square&color=cb3837&logo=npm)](https://www.npmjs.com/package/@q28i/aieos)
[![License](https://img.shields.io/badge/license-MIT-22c55e?style=flat-square)](#-license)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-ec4899?style=flat-square)](#-contributing)

<br />

**[⚡ Install](#-install---choose-your-target)** &nbsp;·&nbsp; **[🗂 Domains](#-the-4-domains)** &nbsp;·&nbsp; **[📦 Bundles](#-themed-bundles)** &nbsp;·&nbsp; **[▶️ Usage](#️-using-aieos)** &nbsp;·&nbsp; **[❓ FAQ](#-faq)**

</div>

<br />

```bash
npx @q28i/aieos --claude
```

<br />

---

## ✨ What is AIEOS

> **One command, then forget it exists.** Instead of treating AI as a simple question-answering tool or code generator, AIEOS structures collaboration around Socratic inquiry, preference discovery, and opportunity cost reviews—creating reusable, auditable Decision Contracts.

AIEOS is a model-independent **Human Intelligence Amplification Runtime** (a Decision OS) designed to increase decision quality under uncertainty while improving the user's independent reasoning. It operates with stable database-backed capability registers, running locally with zero external network overhead or dependency lock-in.

<table>
<tr>
<td align="center"><b>25</b><br/><sub>capabilities</sub></td>
<td align="center"><b>7</b><br/><sub>cognitive loops</sub></td>
<td align="center"><b>5</b><br/><sub>core services</sub></td>
<td align="center"><b>0</b><br/><sub>dependencies</sub></td>
</tr>
</table>

---

## ⚡ Install — choose your target

One command installs AIEOS specifications, constitutions, and policies directly into your agent's customization directory:

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

### Local Project Workspaces

If you want to configure a standalone workspace for project-specific vibe coding, run it against directory paths:

```bash
npx @q28i/aieos                 # install in current directory
npx @q28i/aieos .               # install in current directory
npx @q28i/aieos ../MyProject    # install in a specific project folder
```

This scaffolds a local `.aieos` environment containing:
```text
.aieos/          # core constitutions, protocols, and policies
skills/          # local capability package registry
contracts/       # generated decision quality contracts
memory/          # local SQLite database tracking assumptions & lessons
profiles/        # cognitive profile configurations (e.g. SoftwareEngineer)
aieos.json       # registry settings
```

---

## 📦 Themed Bundles

Optionally filter which capabilities get installed onto your agent platform:

```bash
npx @q28i/aieos --claude --bundle research     # only research & statistics capabilities
npx @q28i/aieos --cursor --bundle security     # only security capabilities
npx @q28i/aieos --bundle full                  # install everything (default)
```

---

## 🗂 The 4 Domains

AIEOS shifts the execution paradigm from raw task processing to a values-aligned decision pipeline:

<div align="center">

| Domain | Scope | Key Abstractions |
| --- | --- | --- |
| 📜 **Constitutions** | `CONSTITUTION/` | User Agency, Engineering Quality, Security Constraints |
| 🔌 **Services** | `SERVICES/` | Kernel Orchestration, SQLite Memory, EventBus, Evolution |
| 🧠 **Protocols** | `PROTOCOLS/` | RealityCheck, Curiosity, Wisdom, Judgment Loops |
| ⚙️ **Policies** | `POLICIES/` | CognitiveBias Filters, LearningProgress, KnowledgeROI |

</div>

---

## 📁 Repository Layout

```text
aieos/
├─ 📂 AIEOS/                     # Dynamic system specifications & schemas
├─ 📂 bin/                       # Node.js binary wrappers & environment gates
├─ 📂 doc_system/                # Core Python modules & engines
│   ├─ cli.py                    # CLI installer & route manager
│   ├─ doctor.py                 # Workspace integrity diagnostics
│   ├─ generator.py              # Package scaffolding generator
│   └─ registry.py               # Capability database mappings
├─ 📂 tests/                     # Core integration unit tests
├─ 🗂️ aieos.json                 # Project registry settings
├─ 📜 LICENSE                    # MIT License
└─ 📖 README.md
```

---

## ▶️ Using AIEOS

1. **Prompt Socratic Decisions**: Once AIEOS rules are active in your agent, prompt it:
   > *"I want to choose between Serverless SQL and standard Postgres for our analytics workload. Run an AIEOS Decision Protocol."*
2. **Contract Output**: The agent will challenge your assumptions, simulate trade-offs, identify evidence gaps, and emit a structured Decision Contract in your workspace.

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

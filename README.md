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

**[⚡ Install](#-install)** &nbsp;·&nbsp; **[🗂 Domains](#-the-4-domains)** &nbsp;·&nbsp; **[🛠️ CLI Reference](#️-cli-reference)** &nbsp;·&nbsp; **[▶️ Usage](#️-using-aieos)** &nbsp;·&nbsp; **[❓ FAQ](#-faq)**

</div>

<br />

```bash
npx @q28i/aieos init my_workspace
```

<br />

---

## ✨ What is AIEOS

> **One runtime for intelligence amplification.** Instead of treating AI as a simple question-answering tool or code generator, AIEOS structures collaboration around Socratic inquiry, preference discovery, and opportunity cost reviews—creating reusable, auditable Decision Contracts.

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

## ⚡ Install

Install the package globally, or scaffold workspaces on-demand:

| Method | Command | Use Case |
| --- | --- | --- |
| **On-demand Setup** | `npx @q28i/aieos init <name>` | Initialize a workspace structure without permanent installation |
| **Global Install** | `npm install -g @q28i/aieos` | Install stable CLI runner onto your system binary path |
| **Local Development** | `git clone https://github.com/q28i/aieos.git`<br>`cd aieos`<br>`npm install && npm install -g .` | Contribute to the AIEOS core modules |

---

## 🗂 The 4 Domains

AIEOS shifts the execution paradigm from raw task processing to a values-aligned decision pipeline:

<div align="center">

| Domain | Files | Purpose |
| --- | --: | --- |
| 📜 **Constitutions** | `AIEOS/CONSTITUTION/` | Core user agency, quality, engineering, and architectural constraints |
| 🔌 **Services** | `AIEOS/SERVICES/` | Operational systems (`Kernel`, `EventBus`, `Memory`, `CapabilityRegistry`, `Evolution`) |
| 🧠 **Protocols** | `AIEOS/PROTOCOLS/` | Cognitive loops (`RealityCheck`, `Curiosity`, `KnowledgeExpansion`, `FutureSimulation`, `Wisdom`) |
| ⚙️ **Policies** | `AIEOS/POLICIES/` | Learning trackers (`UserModel`, `LearningProgress`, `KnowledgeROI`, `Mentor`, `CognitiveBias`) |

</div>

---

## 🛠️ CLI Reference

Once installed, use the `aieos` command line tool inside your terminal:

```bash
# Initialize a workspace directory
aieos init my_workspace

# Create a new capability package template
aieos create package Capability_FuzzyLogic Research

# Install a remote package from GitHub directly
aieos install github:LoftyRux/research-pack

# Validate capability manifests and contracts
aieos validate packages/Capability_Research

# Run workspace diagnostic audits
aieos doctor

# Execute longitudinal collaboration benchmarks
aieos benchmark
```

---

## 📁 Repository Layout

```
aieos/
├─ 📂 AIEOS/                    # Dynamic system specifications & schemas
├─ 📂 bin/                      # Node.js binary wrappers & environment gates
├─ 📂 doc_system/               # Core Python modules & engines
│   ├─ cli.py                   # CLI commands & route manager
│   ├─ doctor.py                # Workspace integrity diagnostics
│   ├─ generator.py             # Package scaffolding generator
│   └─ registry.py              # Capability database mappings
├─ 📂 tests/                    # Core integration unit tests
├─ 🗂️ aieos.json                 # Project registry settings
├─ 📜 LICENSE                   # MIT License
└─ 📖 README.md
```

---

## 📋 System Requirements

* **Node.js**: `18.0.0` or higher
* **Python**: `3.11` or higher
* **Git**: Required for remote capability package installation

---

## ❓ FAQ

<details>
<summary><b>How does AIEOS check Python dependencies?</b></summary>
<br/>
On startup, the Node wrapper scans for <code>python</code>, <code>python3</code>, or <code>py</code> binaries. If no matching runtime version &gt;= 3.11 is found, it terminates cleanly with explicit download guides, avoiding unhandled trace logs.
</details>

<details>
<summary><b>Is the SQLite registry network-dependent?</b></summary>
<br/>
No. The SQLite database (<code>memory/aieos_local.db</code>) initialized during workspace setups runs entirely in your local folder to track logs and installed capability indices.
</details>

---

## 🛠️ Troubleshooting

### Command wrapper complains about missing Python
If you see the error `AIEOS requires Python 3.11 or newer` during execution:
1. Ensure Python is installed from [python.org](https://www.python.org/downloads/).
2. Verify that Python is added to your environment `PATH` variables.

### Permission issues when running global install
If you run into permission blocks, execute npm using path-level user configurations or run:
```bash
npm install -g @q28i/aieos --unsafe-perm
```

---

## 🤝 Contributing

PRs are welcome! Good first contributions:
* ➕ Adding new capability adapters under `doc_system/adapter.py`
* 🛡️ Expanding the `doctor` audits for configuration mismatches
* 📚 Improving markdown specifications inside the protocols compiler

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

<div align="center">
<br/>
<sub>Built as one unified catalog. No dependencies. No lock-in.</sub>
<br/><br/>

**[⬆ back to top](#top)**

</div>

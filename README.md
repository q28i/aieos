# AIEOS: Human Intelligence Amplification Runtime

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NPM version](https://img.shields.io/npm/v/@q28i/aieos.svg)](https://www.npmjs.com/package/@q28i/aieos)
[![Build Status](https://img.shields.io/github/actions/workflow/status/aieos/aieos/ci.yml)](https://github.com/aieos/aieos/actions)

AIEOS is a model-independent **Human Intelligence Amplification Runtime** (a Decision OS) designed to increase decision quality under uncertainty while improving the user's independent reasoning. 

Rather than treating AI as a simple question-answering tool or code generator, AIEOS structures collaboration around Socratic inquiry, preference discovery, and opportunity cost reviews—creating reusable Decision Contracts that move human-AI collaboration beyond static prompting.

---

## 🌐 The Ecosystem Architecture

AIEOS scales as a unified open-source platform mapped across dedicated domain zones:

```text
loftyrux.in
│
├── aieos.loftyrux.in       # Documentation and home base
├── registry.loftyrux.in    # Public package registry index
├── api.loftyrux.in         # Registry and package verification API
├── docs.loftyrux.in        # Contributor references
└── playground.loftyrux.in  # Interactive cognitive simulations
```

---

## 🚀 Key Features

* **Dialogue Orchestration**: Decoupled dialogue manager governing conversation pacing, question strategies, and Socratic reflection overlays.
* **Decision Contracts**: Encapsulates objectives, constraints, values, evidence, assumptions, tradeoffs, and reversibility parameters into auditable records.
* **Disagreement Protocol**: Formalizes rules for when the runtime should constructively disagree with user assumptions.
* **Split Confidence Scoring**: Separates confidence metrics across Evidence, Reasoning, Prediction, and Execution.
* **Real GitHub Installer**: Directly download, clone, and validate remote capabilities from GitHub repositories.

---

## 📦 Installation

### Global Installation
```bash
npm install -g @q28i/aieos
```

### Local Dev Project Installation
```bash
# Clone the repository
git clone https://github.com/loftyrux/aieos.git
cd aieos

# Install dependencies and link local CLI globally
npm install
npm install -g .
```

### On-Demand Workspace Setup
```bash
npx @q28i/aieos init my_workspace
```

---

## 🛠️ CLI Reference

```bash
# Initialize a workspace directory
aieos init

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

## 📋 System Requirements

* **Node.js**: `18.0.0` or higher
* **Python**: `3.11` or higher
* **Git**: Required for remote capability package installation

---

## ❓ FAQ

### 1. What makes AIEOS different from normal LLM prompt frameworks?
Unlike standard wrapper platforms, AIEOS enforces formal boundaries regarding cognitive bias, reality testing, and user agency constraints. It structures recommendations into auditable, parameter-controlled decision records.

### 2. Can I use AIEOS without Python?
No, the CLI wrapper requires a local Python 3.11+ installation. It will automatically check your environment path variables and exit gracefully if missing or outdated.

---

## 🛠️ Troubleshooting

### Command wrapper complains about missing Python
If you see the error `Error: Python 3.11+ is required` during startup, ensure that `python`, `python3`, or `py` is registered in your system environment path variable (`PATH`) and points to a version `>= 3.11`.

### Permission issues when running global install
If you encounter write permission issues during `npm install -g @q28i/aieos`, run with root privileges (`sudo` on Unix) or use a Node Version Manager (nvm) to install without global administrator overrides.

---

## 📄 License

Distributed under the MIT License. See [LICENSE](file:///LICENSE) for details.

# AIEOS Skill Specification (v1.0.0)

This document defines the technical contract for an AIEOS Skill. A skill in AIEOS is not merely a text prompt—it is an executable capability package that extends the cognitive logic, workflow, and permissions of the host AI.

---

## 1. Directory Structure

A valid AIEOS skill must adhere to the following package structure.

```text
skill/
├── skill.json              # Required: Package manifest and metadata
├── persona.md              # Optional: Role and identity definition
├── workflow.md             # Required: Step-by-step execution flowchart/logic
├── questions.md            # Optional: Socratic inquiry prompts for this domain
├── memory.json             # Optional: Schema for long-term memory extraction
├── triggers.json           # Required: Auto-load conditions and triggers
├── dependencies.json       # Optional: Required AIEOS skills or external modules
├── hooks/                  # Optional: Runtime execution scripts (Node/Python)
├── examples/               # Optional: Few-shot examples
├── tests/                  # Optional: Validation test cases for CI/CD
└── README.md               # Required: Human-readable documentation
```

---

## 2. The Manifest: `skill.json`

The `skill.json` file is the central contract of the package. It defines identity, versioning, constraints, and permissions.

### 2.1 Schema Definition

```json
{
  "id": "quant-research",
  "name": "Quantitative Research",
  "version": "1.0.0",
  "author": "q28i",
  "description": "Formulates hypotheses and executes statistical tests on market datasets.",
  "category": "finance",
  "requires": [
    "statistics",
    "risk-management"
  ],
  "compatible": [
    "claude",
    "cursor",
    "antigravity"
  ],
  "loadsWhen": [
    "trading",
    "backtest"
  ],
  "permissions": {
    "filesystem": "read",
    "network": true,
    "terminal": false,
    "memory": "write"
  }
}
```

### 2.2 Permissions Standard

To ensure security, skills must explicitly declare the system privileges they require:
- `filesystem`: Options: `false` (no access), `"read"` (only read workspace files), `"write"` (can create/modify workspace files).
- `network`: Options: `false`, `true`.
- `terminal`: Options: `false`, `true` (ability to spawn subprocesses or run shell scripts).
- `memory`: Options: `false`, `"read"`, `"write"` (ability to read/write workspace state databases).

The AIEOS core runtime prompts the user for approval during installation if a capability demands elevated privileges.

---

## 3. Dependency Resolution & Conflicts

AIEOS acts as a package manager (like `npm`).
1. **Resolution**: If Skill A requires `risk-management`, AIEOS will recursively fetch `risk-management` from the registry upon installation.
2. **Conflicts**: If Skill A requires `risk-management@1.0` and Skill B requires `risk-management@2.0`, AIEOS enforces a strict **singleton** rule for active cognitive modules. The user will be prompted to resolve the conflict or upgrade the trailing package.

---

## 4. Updates & Versioning

Skills must follow **Semantic Versioning (SemVer)**:
- **Major (X.y.z)**: Breaking changes to `workflow.md` logic or raised `permissions`.
- **Minor (x.Y.z)**: New capabilities, new hooks, expanded `questions.md`.
- **Patch (x.y.Z)**: Bug fixes, typo corrections in `persona.md`.

Updates are invoked via `aieos skill update <id>`. If permissions change in a Major update, the CLI will halt and request explicit user confirmation.

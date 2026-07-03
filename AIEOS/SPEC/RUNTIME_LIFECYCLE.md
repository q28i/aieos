# AIEOS Runtime Lifecycle (v1.0.0)

This document defines the execution flow and state machine for how requests flow through the AIEOS runtime ecosystem. This ensures that every AI integration (Claude, Cursor, Antigravity) behaves consistently.

---

## 1. Re-defined Execution Flow

To prevent the AI assistant from skipping straight from context reading to raw output generation, AIEOS introduces a formal **Planning Engine** phase before execution.

```text
Host AI Request
      │
      ▼
[1. Project Scanner]
      │
      ▼
[2. Capability Resolver]
      │
      ▼
[3. Dependency Loader]
      │
      ▼
[4. Memory Loader]
      │
      ▼
[5. Planning Engine] ─── (Decides: Mode, Questions, Required human approvals)
      │
      ▼
[6. Pre-Execution Hooks]
      │
      ▼
[7. Host AI Execution]
      │
      ▼
[8. Post-Execution Review Hooks]
      │
      ▼
[9. Memory Update]
      │
      ▼
Response to User
```

---

## 2. Phase Definitions

### 1. Project Scanner
**Action:** Scans the active workspace to detect the programming language, framework signatures, and directory structure layout.

### 2. Capability Resolver
**Action:** Evaluates project signatures against trigger arrays (`loadsWhen`) in installed skill manifests. Mounts matches into the workspace execution stack.

### 3. Dependency Loader
**Action:** Resolves the dependency graph and loads any requirements specified in the active skill manifests.

### 4. Memory Loader
**Action:** Hydrates the workspace context with goals, active team contracts, and past architectural decision records (ADRs).

### 5. Planning Engine
**Action:** Analyzes the active capabilities, the loaded memory, and the requested user intent to formulate an execution plan. It specifically determines:
- Which execution mode is required (e.g. `/mode backend`).
- What clarifying questions must be asked before proceeding (Socratic Inquiry).
- Whether the task demands human approval (e.g., executing code in the terminal).
- If additional capabilities must be installed first.

### 6. Pre-Execution Hooks
**Action:** Fires any pre-flight scripts declared by active skills (e.g., secret-scanning hooks).

### 7. Host AI Execution
**Action:** The LLM processes the enriched context and generates the requested code or system changes.

### 8. Post-Execution Review Hooks
**Action:** Validates results against quality constraints (e.g., syntax checks, security assessments). On failure, it triggers corrective feedback loops back to the Host AI.

### 9. Memory Update
**Action:** Synthesizes new learnings and architectural decisions, writing them to `.aieos/project/decisions` and the local knowledge database.

---

## 3. Runtime State Machine

To enforce deterministic tracking and enable real-time event reporting, the AIEOS runtime transitions through the following formal states:

| State | Description | Next Valid States |
| --- | --- | --- |
| `Idle` | System is initialized and waiting for user input. | `Scanning` |
| `Scanning` | Actively parsing workspace dependencies and code structures. | `Planning`, `Failed` |
| `Planning` | The Planning Engine is evaluating intent, resolving required capabilities, and framing Socratic questions. | `Loading`, `Failed` |
| `Loading` | Hydrating active memory scopes and mounting capability packages into the host context. | `Executing`, `Failed` |
| `Executing` | Handed over execution to the Host AI environment for processing. | `Reviewing`, `Failed` |
| `Reviewing` | Evaluating prompt responses against active post-execution verification hooks. | `Persisting`, `Executing` (if corrective loops trigger), `Failed` |
| `Persisting` | Committing ADR decisions, knowledge artifacts, and updating the capability graph. | `Complete`, `Failed` |
| `Complete` | Execution finished successfully. Returning final output to the user. | `Idle` |
| `Failed` | An unrecoverable exception occurred (e.g. permission denied or compile error). | `Idle` |


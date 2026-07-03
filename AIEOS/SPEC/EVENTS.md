# AIEOS Event-Driven Architecture (v1.0.0)

AIEOS operates on an asynchronous pub/sub model. Every transition in the runtime lifecycle, every change in workspace state, and every user decision must emit structured events. This enables modular capabilities and third-party extensions to hook into runtime behaviors without modifying core code.

---

## 1. System Events Schema

All emitted events must conform to the following schema:

```json
{
  "event": "ProjectOpened",
  "id": "evt_8f3a9d12",
  "timestamp": 1782839201000,
  "source": "kernel",
  "payload": {}
}
```

---

## 2. Event Registry

### 2.1 Workspace Lifecycles

#### `ProjectOpened`
- **Source**: Host Adapter
- **Trigger**: The user opens the workspace in their IDE.
- **Payload**:
  ```json
  { "workspace_path": "c:/Users/Void/Documents/MyApp" }
  ```

#### `ModeChanged`
- **Source**: Planning Engine
- **Trigger**: The user or AI changes the active execution mode (e.g. `/mode trading`).
- **Payload**:
  ```json
  { "from": "default", "to": "trading" }
  ```

---

### 2.2 Capability Package Lifecycles

#### `SkillInstalled`
- **Source**: Package Manager
- **Trigger**: A capability is successfully downloaded and installed.
- **Payload**:
  ```json
  { "skill_id": "@aieos/testing", "version": "1.0.0" }
  ```

#### `SkillLoaded`
- **Source**: Dependency Loader
- **Trigger**: A mounted skill is loaded into the active execution context.
- **Payload**:
  ```json
  { "skill_id": "@aieos/testing" }
  ```

---

### 2.3 Memory Lifecycles

#### `MemoryUpdated`
- **Source**: Memory Manager
- **Trigger**: Data is written back to the project JSON state or vector store.
- **Payload**:
  ```json
  { "scope": "project", "keys_modified": ["architecture", "goals"] }
  ```

#### `DecisionCreated`
- **Source**: Dialogue/Planning Engine
- **Trigger**: An ADR (Architecture Decision Record) is validated and committed.
- **Payload**:
  ```json
  {
    "decision_id": 14,
    "objective": "Establish JS SDK runtime interface",
    "confidence_score": "0.95"
  }
  ```

---

### 2.4 Execution Lifecycles

#### `ExecutionStarted`
- **Source**: Kernel
- **Trigger**: The host AI starts parsing and executing the prompt payload.
- **Payload**:
  ```json
  { "task_id": "task_482", "mode": "trading" }
  ```

#### `ExecutionFinished`
- **Source**: Kernel
- **Trigger**: Prompt output is returned, and all post-execution review hooks pass.
- **Payload**:
  ```json
  { "task_id": "task_482", "duration_ms": 3210, "status": "success" }
  ```

# AIEOS Execution Levels Specification (v1.0.0)

AIEOS classifies host AI behavior and capability compliance into three distinct **Execution Levels**. This standard defines the requirements and constraints for each level.

---

## 1. Levels Overview

```text
  ┌────────────────────────────────────────────────────────┐
  │                   AIEOS Execution Level                │
  └────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
         Level 0           Level 1           Level 2
      (Normal AI)     (Capability-Aware)  (Execution OS)
```

| Level | Name | Description | Key Requirement |
| --- | --- | --- | --- |
| **Level 0** | Normal AI | Standard conversational LLM behavior. Operates purely as a reactive chatbot. | None. Default out-of-the-box state. |
| **Level 1** | Capability-Aware | The AI is conscious of its active capabilities and loads specific markdown prompts to align behavior. | Ability to resolve and mount `.aieos/skills/` prompts in chat context. |
| **Level 2** | Execution OS | Full operating system compliance. Intercepts commands, validates execution hooks, runs planning protocols, and commits decisions. | Complete SDK / Adapter implementation satisfying `IAieosAdapter`. |

---

## 2. Behavioral Definitions

### 2.1 Level 0: Normal AI
- **Behavior**: The AI does not look at project state or ADR databases. It writes code immediately based on its pre-trained knowledge, frequently leading to architectural drift, styling inconsistency, and regression bugs.

### 2.2 Level 1: Capability-Aware AI
- **Behavior**: The AI reads the `.aieos/installed-skills.json` configuration and loads the respective capability text modules (e.g. `CTO`, `Architect`). It uses these prompts to guide its persona and structure its answers.

### 2.3 Level 2: Execution OS (Full Compliance)
- **Behavior**: 
  - **Memory Persistence**: Automatically hydration from and writing to local databases (`decisions/`, `knowledge/`).
  - **Interactive Planning**: The AI halts execution when uncertainty or risk is high, triggers Socratic prompts, and demands explicit human approval before running high-risk modifications.
  - **Subcommand Interception**: Standardizes commands natively via the local CLI/SDK without manual user intervention.

# AIEOS Design Principles (v1.0.0)

This document establishes the eight immutable design tenets of the Artificial Intelligence Execution Operating System. All architectural proposals, feature designs, and codebase refactoring must align with these principles.

---

## 1. Composable Capabilities over Monolithic Prompts
AIEOS rejects single-file "mega-prompts" or massive persona files. Intelligence must be broken down into discrete, modular, and versioned **Capability Packages** (skills) that specialize in specific domains (e.g., quant research, security, documentation). This ensures scalability and makes testing cognitive logic predictable.

## 2. Project State over Chat Context
A chat session is transient and lossy. AIEOS anchors the host AI's understanding in **persistent project state** stored locally (`.aieos/project/`). Goals, previous decisions, capability graphs, and active team contracts survive chat session resets and model changes.

## 3. Structured Execution over Reactive Responses
AIEOS forces the Host AI to step out of the naive "question-answer" loop. The runtime mandates structured execution paths (such as Socratic questioning, risk vetting, and verification checks) before code editing or final output generation begins.

## 4. Human Approval before Irreversible Actions
AI assistants must operate with a safety-first authorization layer. The runtime requires explicit human confirmation before executing critical operations, including dropping database schema targets, executing remote web hooks, or deleting workspace assets.

## 5. Tool-Agnostic Adapter Integrations
AIEOS must never be tied to a single IDE, CLI, or model vendor. The runtime core is abstract. Runtimes interface with host environments using standard **Adapters** that map platform capabilities to the AIEOS runtime API.

## 6. Transparent Reasoning and Traceable Decisions
Every design decision, assumption challenge, and trade-off exploration must be traceable. Decisions must be committed to the ADR (Architecture Decision Record) database so that developers (and downstream AI collaborators) can review the historical rationale.

## 7. Least-Privilege Permissions for Skills
Capability packages are treated like system processes. They must explicitly declare the system resources they need (filesystem read/write, terminal execution, network connection) in their manifest. The runtime enforces strict runtime verification of these requests.

## 8. Capability-First, Persona-Second
AIEOS does not define "Who the AI is" (e.g. "You are a senior python developer"). It defines "What the AI can do" by dynamically mounting capability packages based on project files. A generic AI assistant is upgraded into an execution partner by attaching capabilities, not by modifying its conversational voice.

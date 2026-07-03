# AIEOS Memory Specification (v1.0.0)

AIEOS coordinates workspace intelligence across six specialized memory layers. This document defines the retention policies, schema requirements, and consolidation mechanisms for each memory sphere.

---

## 1. The Six Memory Spheres

```text
       ┌────────────────────────────────────────────────────────┐
       │                     AIEOS Memory                       │
       └───────────────────────────────────┬────────────────────┘
                                           │
         ┌───────────────────┬─────────────┼─────────────┬───────────────────┐
         ▼                   ▼             ▼             ▼                   ▼
     Identity             Project       Session      Decision              Skill / Knowledge
(Global Preferences) (Goals/State)   (Chat Context)    (ADRs)        (Capabilities/Facts)
```

### 1.1 Identity Memory (Global)
- **Scope**: User-specific identity profiles, persistent heuristics, and cross-project knowledge.
- **Location**: Global configuration directory (`~/.aieos/identity_memory.json`).
- **Retention**: Permanent.

### 1.2 Project Memory (Workspace)
- **Scope**: Project roadmap, active capability lists, tech stack, and workspace objectives.
- **Location**: Project workspace state (`.aieos/project/project.json`).
- **Retention**: Lifetime of the project.

### 1.3 Session Memory (Transient)
- **Scope**: Current prompt history and local terminal execution inputs/outputs.
- **Location**: Transient JSON logs or active chat context window.
- **Retention**: Discarded on session termination or reset.

### 1.4 Decision Memory (ADRs)
- **Scope**: Immutable records of architectural decisions, tradeoffs, and Socratic alignment history.
- **Location**: Project workspace ADR database (`.aieos/project/decisions/`).
- **Retention**: Permanent history (appended only, never rewritten).

### 1.5 Skill Memory (Scope-Bound)
- **Scope**: Custom rules and heuristics learned by specific capability modules.
- **Location**: The individual skill's cache (`.aieos/skills/<skill-id>/memory.json`).
- **Retention**: Resets if the skill is uninstalled.

### 1.6 Knowledge Memory (Semantic)
- **Scope**: Discovered facts, domain ontologies, and external database mapping caches.
- **Location**: SQLite relational/vector caches (`.aieos/project/knowledge/`).
- **Retention**: Consolidated and pruned periodically.

---

## 2. Pruning & Consolidation Lifecycles

To prevent token bloating in active LLM context windows, memory must be aggressively structured.

### 2.1 Consolidation Triggers
1. **Interval**: Every 50 dialogue turns, the runtime consolidates Session Memory into short bulleted summaries inside Project Memory.
2. **Success Gate**: When a plan is successfully validated (`Validation` state), the ADR is committed to Decision Memory and Session logs are cleared.

### 2.2 Pruning Heuristics
- **Relevance Score**: Vector lookup relevance must score above `0.7` to be injected into active context.
- **Volatility Filter**: Transient variables (e.g. temporary build files) are stripped during consolidation.

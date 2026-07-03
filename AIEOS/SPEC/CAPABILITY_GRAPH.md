# AIEOS Capability Graph (v1.0.0)

AIEOS departs from simple flat capability lookups. Instead, installed capabilities are modeled as a Directed Acyclic Graph (DAG). This graph-based structure drives semantic package discovery, recursive dependency loading, and context priority resolution.

---

## 1. Graph Model Definitions

In the capability graph:
- **Nodes**: Represent individual capability packages (skills) containing manifests (`skill.json`).
- **Edges**: Directed relationships representing structured interaction models between capability nodes. Valid edge types include:
  - `depends_on`: Strict runtime prerequisite.
  - `enhances`: Dynamically injects extra rules/prompts into another skill if both are loaded.
  - `conflicts_with`: Blocks loading if the conflicting skill is active.
  - `replaces`: Obsoletes/shadows another skill (e.g. `@aieos/quant-research-v2` replaces `v1`).
  - `recommends`: Suggests secondary skills to install.
  - `inherits`: Imports structural behaviors or base definitions from a parent.
  - `loads_after` / `loads_before`: Enforces execution sequencing for hooks.

```text
    ┌────────────────┐
    │  @aieos/trading│ (Finance Domain)
    └──────┬──────┬──┘
           │      │
           │      └─────────────────┐
           ▼                        ▼
  ┌─────────────────┐      ┌────────────────┐
  │ @aieos/research │      │  @aieos/risk   │
  └────────┬────────┘      └────────┬───────┘
           │                        │
           └──────────┐  ┌──────────┘
                      ▼  ▼
            ┌─────────────────────┐
            │@aieos/basecognitive │
            └─────────────────────┘
```

### 1.1 Node Attributes

```json
{
  "id": "@aieos/trading",
  "domain": "finance",
  "dependencies": ["@aieos/research", "@aieos/risk"],
  "relationships": [
    { "type": "depends_on", "target": "@aieos/basecognitive" },
    { "type": "recommends", "target": "@aieos/backtesting" },
    { "type": "enhances", "target": "@aieos/logging" },
    { "type": "conflicts_with", "target": "@aieos/paper-trading" }
  ],
  "triggers": {
    "file_patterns": ["*.py", "*.csv"],
    "dependencies_detected": ["pandas", "numpy"],
    "keywords": ["backtest", "trade", "portfolio"]
  },
  "execution_priority": 100
}
```

---

## 2. Graph Traversal Lifecycles

### 2.1 Dependency Resolution (Topological Sort)
When installing or loading a capability, the runtime parses the capability nodes and runs a **topological sort** to resolve loading orders.
- In the graph above, `basecognitive` is loaded first, followed by `research` and `risk`, and finally `trading`.
- If a circular dependency is detected (e.g., Node A requires B, and B requires A), the runtime rejects compilation and raises an installation fault.

### 2.2 Recommending via Graph Traversal
The `/aieos recommend` engine does not just look for matching filenames. It traverses the capability graph:
1. **Detect Signatures**: Scans the project (e.g., detects `FastAPI` and python files).
2. **Mount Entry Nodes**: Finds skills where `triggers` match the detected signatures (e.g., mounts `@aieos/backend`).
3. **Traverse Upwards**: Follows category edges and recommendation weights to identify related capabilities (e.g., recommends `@aieos/security` as a high-affinity neighbor of `@aieos/backend`).
4. **Rank**: Orders recommendations based on graph-distance and priority weights.

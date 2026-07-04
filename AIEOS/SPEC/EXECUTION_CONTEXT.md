# AIEOS Execution Context Specification (v1.0.0)

To keep the AIEOS runtime completely decoupled from specific AI platforms (Claude, Cursor, ChatGPT, etc.), all adapters must compile their local environment state into a single, unified `ExecutionContext` object before dispatching execution to the AIEOS core.

---

## 1. Schema Definition

```typescript
export interface ExecutionContext {
    // Project Information
    project: {
        name: string;
        path: string;
        techStack: string[];    // e.g. ["fastapi", "react", "sqlite"]
    };

    // Capability Packages (Skills)
    installedSkills: string[];  // List of all installed skill IDs
    activeSkills: string[];     // List of skill IDs loaded for this specific request

    // Active Modes
    currentMode: string;        // e.g. "default", "analysis", "backend"

    // Context & Memory State
    memory: {
        identity: any;          // Global user preferences
        projectState: any;      // .aieos/project/project.json metadata
        sessionHistory: any[];  // Current conversation context
        adrHistory: any[];      // ADR decisions list
    };

    // Active Team Configuration
    team: {
        activeMode: string;
        members: Array<{ role: string; active: boolean }>;
    };

    // Host & Environment Gates
    adapters: string[];         // Active platform adapters (e.g. ["claude", "vscode"])
    permissions: {              // Currently granted permissions
        filesystem: "read" | "write" | false;
        network: boolean;
        terminal: boolean;
    };

    // User Intent & Prompts
    userIntent: string;         // The raw query/instruction from the user
    executionLevel: 0 | 1 | 2;  // The active intelligence compliance level

    // Planning Engine Output
    planning?: {
        recommendedSkills: string[];
        requiredApprovals: string[];
        socraticInquiryPrompt?: string;
    };

    // System Environment
    environment: {
        nodeVersion: string;
        pythonVersion: string;
        os: "windows" | "macos" | "linux";
    };
}
```

---

## 2. Execution Pipeline Integration

When the Host AI receives a user instruction:
1. **Host Adapter compiles context**: Compiles all project metrics, settings, memory databases, and permissions into this JSON schema.
2. **Core Runtime invocation**: The Core JS Runtime parses this `ExecutionContext` and decides which hooks and capability protocols to run.
3. **Model execution**: The Host AI executes, with the AIEOS engine appending rules and ADRs based strictly on the values present in this context.

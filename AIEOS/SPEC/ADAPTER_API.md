# AIEOS Adapter API Specification (v1.0.0)

This document defines the TypeScript interface that host AI environments (Claude Code, Cursor, Antigravity) must implement to support AIEOS natively. This interface enables deep, interactive IDE integrations rather than simple command wrappers.

---

## 1. The Adapter Interface (`IAieosAdapter`)

```typescript
export interface IAieosAdapter {
    
    // Lifecycle Management
    initialize(config: AieosConfig): Promise<void>;
    shutdown(): Promise<void>;

    // Project Analysis & Command Routing
    scanProject(): Promise<ProjectSignature>;
    executeCommand(command: string, args: string[]): Promise<CommandResult>;
    
    // Event System (Pub/Sub)
    emitEvent(event: AieosEvent): Promise<void>;

    // Security & User Interaction
    requestPermission(permission: PermissionRequest): Promise<boolean>;
    showPrompt(question: string, options: string[]): Promise<string>;
    showRecommendations(skills: SkillManifest[]): Promise<void>;

    // Memory State Management
    loadMemory(scope: MemoryScope): Promise<MemoryContext>;
    saveMemory(scope: MemoryScope, update: MemoryUpdate): Promise<void>;

    // Skill Package Management
    searchSkills(query: string): Promise<SkillManifest[]>;
    installSkill(skillId: string): Promise<InstallResult>;
    removeSkill(skillId: string): Promise<void>;
    enableSkill(skillId: string): Promise<void>;
    disableSkill(skillId: string): Promise<void>;
    setMode(mode: string): Promise<void>;

    // Execution Environment context
    getExecutionContext(): Promise<ExecutionContext>;
}
```

---

## 2. API Schema Details

### 2.1 Event Handling (`emitEvent`)
Enables the host environment and AIEOS runtime to maintain real-time state synchronization (e.g. updating progress bars, refreshing UI states).
```typescript
export interface AieosEvent {
    type: string;        // e.g. "ProjectOpened", "SkillInstalled", "MemoryUpdated"
    timestamp: number;
    payload: any;
}
```

### 2.2 Permissions Vetting (`requestPermission`)
Enforces the least-privilege security model. The host must ask the user for confirmation when a capability attempts a protected action (e.g. writing files, accessing external URLs).
```typescript
export interface PermissionRequest {
    skillId: string;
    action: "filesystem:read" | "filesystem:write" | "network" | "terminal";
    target?: string;    // e.g. "c:/projects/my-app/db.sqlite" or "https://api.github.com"
}
```

### 2.3 Interactive Prompting (`showPrompt`)
Allows AIEOS cognitive modules (such as the Planning Engine) to prompt the user directly inside the IDE interface (e.g. presenting multiple-choice questions or soliciting approval for architectural trade-offs).
```typescript
export interface CommandResult {
    success: boolean;
    stdout: string;
    stderr: string;
    data?: any;         // Return structured JSON data directly
}
```

# AIEOS Adapter Generator Specification (v1.0.0)

This document defines the interface and behaviors of the **AIEOS Adapter Generator**, which compiles the core runtime's capabilities, active profiles, and Socratic constraints into optimized, lightweight bootstrap prompts (thin wrappers) for target host environments (Claude Code, Cursor, Antigravity, Gemini).

---

## 1. The Thin Wrapper Philosophy

Instead of bloating the LLM prompt context with entire spec sheets or API definitions, AIEOS utilizes a **Thin Wrapper**. A thin wrapper has exactly three responsibilities:
1. **Declare System Awareness**: Inform the AI that it is operating inside an AIEOS-enhanced workspace.
2. **Expose Core Commands**: Register the standard execution triggers (`/skill`, `/mode`, `/aieos`).
3. **Bridge Execution**: Instruct the AI to delegate command parsing and execution to the terminal/CLI runtime via `npx @q28i/aieos` or its local SDK equivalent.

### Target Token Budget
- **Target Prompt Size**: < 300 tokens (approx. 1,000 to 1,500 characters).

---

## 2. Platform Output Targets

The Adapter Generator dynamically compiles and writes custom files to specific locations on the developer's system depending on the target host.

### 2.1 Cursor IDE (`.cursorrules`)
- **Output Path**: `[WorkspaceRoot]/.cursorrules`
- **Output Format**: Plain markdown.
- **Behavior**: Appended or written to the root directory to define Cursor's system-level behavior.

### 2.2 Claude Code (`aieos_bridge.md`)
- **Output Path**: `~/.claude/skills/aieos_bridge.md`
- **Output Format**: Markdown file conforming to Claude's skill spec.
- **Behavior**: Enables native terminal commands execution without requiring manual user authorization inside Claude.

### 2.3 Antigravity IDE
- **Output Path**: `~/.gemini/config/skills/aieos/SKILL.md`
- **Output Format**: Markdown with YAML frontmatter.

---

## 3. Dynamic Compilation Protocol

The generator reads the active workspace environment to build the wrapper:

```text
               +----------------------+
               |    Active Profile    |
               +----------+-----------+
                          |
+----------------------+  |  +----------------------+
| Installed Capability |--+--|  Execution Levels    |
| Graph (Namespaces)   |     |  & Permissions       |
+----------------------+     +----------------------+
                          |
                          v
               +----------------------+
               |  Adapter Generator   |
               +----------+-----------+
                          |
                          v
        Platform-Specific Thin Wrappers
```

### Compiler Input Variables
- **Profile**: e.g., `architect`, `mentor`, `reviewer`, `decision-os`.
- **Capability Schema Namespaces**: List of currently registered capabilities (e.g., `[research, trading, memory]`).
- **Permissions Context**: Current filesystem, network, and terminal execution privileges.

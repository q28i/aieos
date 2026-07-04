const fs = require('fs');
const path = require('path');

class AIEOSCompiler {
    constructor(workspaceRoot = process.cwd()) {
        this.workspaceRoot = workspaceRoot;
    }

    /**
     * Compiles raw runtime settings and active capability state into multiple target artifacts.
     * @param {Object} options - Compiler parameters:
     *   - profile: string ('architect', 'mentor', 'reviewer', 'decision-os')
     *   - activeSkills: Array<string>
     *   - executionLevel: number
     * @returns {Object} Target artifacts containing content and metadata
     */
    compile(options = {}) {
        const profile = options.profile || 'decision-os';
        const activeSkills = options.activeSkills || [];
        const executionLevel = options.executionLevel !== undefined ? options.executionLevel : 2;
        const generatedAt = new Date().toISOString();

        let profileSection = '';
        if (profile === 'decision-os') {
            profileSection = `* **Socratic Agency**: Challenge assumptions constructively. Calibrate recommendation with a Decision Contract (Objective, Constraints, Assumptions, Tradeoffs, Reversibility, Validation).`;
        } else if (profile === 'architect') {
            profileSection = `* **System Design Rigor**: Challenge structural alignment. Prioritize loose coupling, clean interfaces, and single responsibility principles.`;
        } else if (profile === 'mentor') {
            profileSection = `* **Socratic Mentorship**: Guide the user via targeted discovery instead of offering code dumps. Focus on conceptual understanding.`;
        } else if (profile === 'reviewer') {
            profileSection = `* **Line-by-Line Review**: Audit changes for edge cases, memory leaks, security, and test coverage requirements.`;
        } else {
            profileSection = `* **Objective Collaboration**: Optimize response relevance and styling correctness.`;
        }

        const skillsStr = activeSkills.length > 0 ? activeSkills.join(', ') : 'None';

        const wrapperTemplate = `# AIEOS Human Intelligence Amplification Rules
# Version: 1.4.0
# Active Profile: ${profile.toUpperCase()}

You are operating within an AIEOS-amplified workspace (Execution Level: ${executionLevel}).

## 1. Cognitive Directive
${profileSection}
* **Knowledge Validation (Immutable Law)**: An AI must never substitute confidence for knowledge. When domain expertise is missing, you MUST first acquire or request it before making consequential design decisions.
* **Momentum**: Prioritize action over paralysis. Ask: "Will another hour of thinking improve this more than an hour of building?"

## 2. Dynamic Capabilities
* **Active Skills**: ${skillsStr}
* **Command Bridge**: When the user requests \`/skill\`, \`/mode\`, or \`/aieos\` subcommands, you MUST natively invoke them via terminal execution.
  - \\\`/skill <args>\\\` -> \\\`npx @q28i/aieos skill <args>\\\` (e.g., \\\`npx @q28i/aieos skill search trading\\\`)
  - \\\`/mode <args>\\\` -> \\\`npx @q28i/aieos mode <args>\\\`
  - \\\`/aieos <args>\\\` -> \\\`npx @q28i/aieos <args>\\\`

* **Execution Bridge Rule**: Read terminal output and seamlessly take the next logical action. Never fabricate runtime state or verify commands manually.`;

        const readmeSnippet = `## AIEOS Integration
This project is configured with AIEOS (Artificial Intelligence Execution Operating System).
- Active Profile: **${profile.toUpperCase()}**
- Active Capabilities: ${activeSkills.map(s => `\`${s}\``).join(', ')}

To run command operations, use:
\`\`\`bash
npx @q28i/aieos <command>
\`\`\``;

        const manifest = {
            runtimeVersion: "1.4.0",
            wrapperVersion: "1.0",
            generatedAt,
            activeProfile: profile,
            capabilities: activeSkills,
            executionLevel
        };

        return {
            cursorrules: wrapperTemplate,
            claude_bridge: wrapperTemplate,
            antigravity_skill: `---\nname: aieos\ndescription: AIEOS Dynamic Cognition Bridge\n---\n${wrapperTemplate}`,
            manifest,
            readme: readmeSnippet
        };
    }

    /**
     * Compiles and writes the compiled artifacts to the specified platform paths.
     * @param {string} targetPlatform - 'cursor', 'claude', 'antigravity'
     * @param {Object} options - Wrapper compiler options
     * @param {string} customPath - Optional directory path override
     * @returns {Object} Array of paths written
     */
    writeArtifacts(targetPlatform, options = {}, customPath = null) {
        const artifacts = this.compile(options);
        const home = process.env.HOME || process.env.USERPROFILE || '';
        const pathsWritten = [];

        if (targetPlatform === 'cursor') {
            const destDir = customPath || this.workspaceRoot;
            fs.mkdirSync(destDir, { recursive: true });

            const cursorrulesPath = path.join(destDir, '.cursorrules');
            fs.writeFileSync(cursorrulesPath, artifacts.cursorrules, 'utf-8');
            pathsWritten.push(cursorrulesPath);

            const manifestPath = path.join(destDir, 'aieos_manifest.json');
            fs.writeFileSync(manifestPath, JSON.stringify(artifacts.manifest, null, 2), 'utf-8');
            pathsWritten.push(manifestPath);

        } else if (targetPlatform === 'claude') {
            const destDir = customPath || path.join(home, '.claude', 'skills');
            fs.mkdirSync(destDir, { recursive: true });

            const bridgePath = path.join(destDir, 'aieos_bridge.md');
            fs.writeFileSync(bridgePath, artifacts.claude_bridge, 'utf-8');
            pathsWritten.push(bridgePath);

            const manifestPath = path.join(destDir, 'aieos_manifest.json');
            fs.writeFileSync(manifestPath, JSON.stringify(artifacts.manifest, null, 2), 'utf-8');
            pathsWritten.push(manifestPath);

        } else if (targetPlatform === 'antigravity') {
            const destDir = customPath || path.join(home, '.gemini', 'config', 'skills', 'aieos');
            fs.mkdirSync(destDir, { recursive: true });

            const skillPath = path.join(destDir, 'SKILL.md');
            fs.writeFileSync(skillPath, artifacts.antigravity_skill, 'utf-8');
            pathsWritten.push(skillPath);

            const manifestPath = path.join(destDir, 'aieos_manifest.json');
            fs.writeFileSync(manifestPath, JSON.stringify(artifacts.manifest, null, 2), 'utf-8');
            pathsWritten.push(manifestPath);

        } else {
            throw new Error(`Unsupported platform compilation target: ${targetPlatform}`);
        }

        return pathsWritten;
    }
}

module.exports = AIEOSCompiler;

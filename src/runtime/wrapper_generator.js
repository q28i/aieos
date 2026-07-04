const fs = require('fs');
const path = require('path');

class WrapperGenerator {
    constructor(workspaceRoot = process.cwd()) {
        this.workspaceRoot = workspaceRoot;
    }

    /**
     * Compiles the dynamic thin wrapper instructions based on profile and active capabilities.
     * @param {Object} options - Compiler parameters:
     *   - profile: string ('architect', 'mentor', 'reviewer', 'decision-os')
     *   - activeSkills: Array<string>
     *   - executionLevel: number
     * @returns {string} Compiled prompt wrapper
     */
    compile(options = {}) {
        const profile = options.profile || 'decision-os';
        const activeSkills = options.activeSkills || [];
        const executionLevel = options.executionLevel !== undefined ? options.executionLevel : 2;

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

        return `# AIEOS Human Intelligence Amplification Rules
# Version: 1.4.0
# Active Profile: ${profile.toUpperCase()}

You are operating within an AIEOS-amplified workspace (Execution Level: ${executionLevel}).

## 1. Cognitive Directive
${profileSection}
* **Momentum**: Prioritize action over paralysis. Ask: "Will another hour of thinking improve this more than an hour of building?"

## 2. Dynamic Capabilities
* **Active Skills**: ${skillsStr}
* **Command Bridge**: When the user requests \`/skill\`, \`/mode\`, or \`/aieos\` subcommands, you MUST natively invoke them via terminal execution.
  - \\\`/skill <args>\\\` -> \\\`npx @q28i/aieos skill <args>\\\` (e.g., \\\`npx @q28i/aieos skill search trading\\\`)
  - \\\`/mode <args>\\\` -> \\\`npx @q28i/aieos mode <args>\\\`
  - \\\`/aieos <args>\\\` -> \\\`npx @q28i/aieos <args>\\\`

* **Execution Bridge Rule**: Read terminal output and seamlessly take the next logical action. Never fabricate runtime state or verify commands manually.`;
    }

    /**
     * Generates and writes thin wrappers to the filesystem for target platforms.
     * @param {string} targetPlatform - 'cursor', 'claude', 'antigravity'
     * @param {Object} options - Wrapper options
     * @param {string} customPath - Optional target directory overrides
     */
    generate(targetPlatform, options = {}, customPath = null) {
        const wrapper = this.compile(options);
        const home = process.env.HOME || process.env.USERPROFILE || '';
        
        if (targetPlatform === 'cursor') {
            const destDir = customPath || this.workspaceRoot;
            const cursorrulesPath = path.join(destDir, '.cursorrules');
            fs.writeFileSync(cursorrulesPath, wrapper, 'utf-8');
            return cursorrulesPath;
        } else if (targetPlatform === 'claude') {
            const destDir = customPath || path.join(home, '.claude', 'skills');
            fs.mkdirSync(destDir, { recursive: true });
            const bridgePath = path.join(destDir, 'aieos_bridge.md');
            fs.writeFileSync(bridgePath, wrapper, 'utf-8');
            return bridgePath;
        } else if (targetPlatform === 'antigravity') {
            const destDir = customPath || path.join(home, '.gemini', 'config', 'skills', 'aieos');
            fs.mkdirSync(destDir, { recursive: true });
            const skillPath = path.join(destDir, 'SKILL.md');
            
            // Add frontmatter for Antigravity skills
            const frontmatter = `---
name: aieos
description: AIEOS Dynamic Cognition Bridge
---
${wrapper}`;
            fs.writeFileSync(skillPath, frontmatter, 'utf-8');
            return skillPath;
        } else {
            throw new Error(`Unsupported target platform adapter: ${targetPlatform}`);
        }
    }
}

module.exports = WrapperGenerator;

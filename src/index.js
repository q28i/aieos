const AIEOSRuntime = require('./runtime');
const eventBus = require('./event_bus');
const ClaudeAieosAdapter = require('./adapters/claude');
const CursorAieosAdapter = require('./adapters/cursor');

// Instantiate a default singleton runtime for backwards compatibility
const runtime = new AIEOSRuntime();

/**
 * Backwards-compatible exports mapping to the singleton runtime.
 */
async function searchSkills(query) {
    await runtime.initialize();
    return await runtime.searchSkills(query);
}

async function installSkill(packageName) {
    await runtime.initialize();
    return await runtime.installSkill(packageName);
}

async function removeSkill(packageName) {
    await runtime.initialize();
    return await runtime.removeSkill(packageName);
}

async function recommendSkills(projectContext) {
    await runtime.initialize();
    return await runtime.recommendSkills(projectContext);
}

async function setExecutionMode(mode) {
    await runtime.initialize();
    return await runtime.setMode(mode);
}

module.exports = {
    // Core Engine Exports
    AIEOSRuntime,
    runtime,
    eventBus,

    // Adapters
    ClaudeAieosAdapter,
    CursorAieosAdapter,

    // Backwards-compatible SDK functions
    searchSkills,
    installSkill,
    removeSkill,
    recommendSkills,
    setExecutionMode
};

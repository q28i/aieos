const eventBus = require('../event_bus');

/**
 * Base abstract class defining the Adapter SDK contract.
 * Every platform (Claude Code, Cursor, Antigravity) subclass must implement this.
 */
class BaseAieosAdapter {
    constructor(platformName) {
        this.platformName = platformName;
    }

    async initialize(config) {
        throw new Error(`initialize() not implemented on ${this.platformName}`);
    }

    async shutdown() {
        throw new Error(`shutdown() not implemented on ${this.platformName}`);
    }

    async scanProject() {
        throw new Error(`scanProject() not implemented on ${this.platformName}`);
    }

    async getExecutionContext() {
        throw new Error(`getExecutionContext() not implemented on ${this.platformName}`);
    }

    async showPrompt(question, options) {
        throw new Error(`showPrompt() not implemented on ${this.platformName}`);
    }

    async requestPermission(permissionRequest) {
        throw new Error(`requestPermission() not implemented on ${this.platformName}`);
    }

    async executeTerminal(command) {
        throw new Error(`executeTerminal() not implemented on ${this.platformName}`);
    }

    async readFile(filePath) {
        throw new Error(`readFile() not implemented on ${this.platformName}`);
    }

    async writeFile(filePath, content) {
        throw new Error(`writeFile() not implemented on ${this.platformName}`);
    }

    async emitEvent(type, payload) {
        eventBus.emit(type, { ...payload, platform: this.platformName });
    }

    async notify(message) {
        console.log(`[AIEOS ${this.platformName}] Notification: ${message}`);
    }
}

module.exports = BaseAieosAdapter;

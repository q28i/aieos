const BaseAieosAdapter = require('./base');

class AntigravityAieosAdapter extends BaseAieosAdapter {
    constructor() {
        super('Antigravity');
    }

    async initialize(config) {
        this.config = config;
        this.emitEvent('ProjectOpened', { platform: 'Antigravity' });
    }

    async shutdown() {
        this.emitEvent('ProjectClosed', { platform: 'Antigravity' });
    }

    async scanProject() {
        return { platform: 'Antigravity', status: 'scanned' };
    }

    async getExecutionContext() {
        return {
            platform: 'Antigravity',
            active: true
        };
    }

    emitEvent(name, payload) {
        // Simple event emitter delegation
    }
}

module.exports = AntigravityAieosAdapter;

const BaseAieosAdapter = require('./base');

class GeminiAieosAdapter extends BaseAieosAdapter {
    constructor() {
        super('Gemini');
    }

    async initialize(config) {
        this.config = config;
        this.emitEvent('ProjectOpened', { platform: 'Gemini' });
    }

    async shutdown() {
        this.emitEvent('ProjectClosed', { platform: 'Gemini' });
    }

    async scanProject() {
        return { platform: 'Gemini', status: 'scanned' };
    }

    async getExecutionContext() {
        return {
            platform: 'Gemini',
            active: true
        };
    }

    emitEvent(name, payload) {
        // Simple event emitter delegation
    }
}

module.exports = GeminiAieosAdapter;

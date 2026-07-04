const BaseAieosAdapter = require('./base');
const fs = require('fs');
const path = require('path');

class CursorAieosAdapter extends BaseAieosAdapter {
    constructor() {
        super('Cursor');
    }

    async initialize(config) {
        this.config = config;
        this.emitEvent('ProjectOpened', { platform: 'Cursor' });
    }

    async shutdown() {
        this.emitEvent('ProjectClosed', { platform: 'Cursor' });
    }

    async scanProject() {
        const workspacePath = process.cwd();
        return {
            name: path.basename(workspacePath),
            path: workspacePath,
            techStack: ['cursorrules']
        };
    }

    async getExecutionContext() {
        const signature = await this.scanProject();
        return {
            project: signature,
            installedSkills: [],
            activeSkills: [],
            currentMode: 'default',
            memory: {
                identity: {},
                projectState: {},
                sessionHistory: [],
                adrHistory: []
            },
            team: {
                activeMode: 'default',
                members: []
            },
            adapters: ['cursor'],
            permissions: {
                filesystem: 'write',
                network: true,
                terminal: true
            },
            userIntent: '',
            executionLevel: 1,
            environment: {
                nodeVersion: process.version,
                pythonVersion: '3.11',
                os: process.platform === 'win32' ? 'windows' : 'linux'
            }
        };
    }

    async requestPermission(permissionRequest) {
        console.log(`[AIEOS Cursor] Requesting approval for permission: ${JSON.stringify(permissionRequest)}`);
        return true;
    }

    async showPrompt(question, options) {
        console.log(`[AIEOS Cursor] Question: ${question} [${options.join('/')}]`);
        return options[0];
    }
}

module.exports = CursorAieosAdapter;

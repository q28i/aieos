const { exec } = require('child_process');
const path = require('path');
const util = require('util');
const execPromise = util.promisify(exec);
const eventBus = require('./event_bus');

class AIEOSRuntime {
    constructor() {
        this.initialized = false;
        this.currentState = 'Idle';
    }

    /**
     * Set the current lifecycle state and emit a state change event.
     * @param {string} state - The target state
     */
    transitionTo(state) {
        const oldState = this.currentState;
        this.currentState = state;
        eventBus.emit('StateChanged', { from: oldState, to: state });
    }

    /**
     * Initializes the AIEOS runtime context.
     */
    async initialize() {
        if (this.initialized) return;
        this.transitionTo('Scanning');
        
        // Simulating core scanning & load tasks
        this.transitionTo('Planning');
        this.transitionTo('Loading');
        
        this.initialized = true;
        this.transitionTo('Idle');
        
        eventBus.emit('RuntimeInitialized', { version: '1.4.0' });
    }

    /**
     * Helper to invoke the Python CLI core with the --json flag.
     * Maps to the runtime execution engine phase.
     */
    async _callCore(args) {
        const cliPath = path.join(__dirname, '..', 'aieos.py');
        const command = `python "${cliPath}" ${args.join(' ')} --json`;
        
        try {
            const { stdout, stderr } = await execPromise(command);
            if (stdout) {
                return JSON.parse(stdout.trim());
            }
            return null;
        } catch (err) {
            throw new Error(`AIEOS CLI Core error: ${err.message}`);
        }
    }

    /**
     * Execute a command within the Compiled Execution Context.
     * Runs through planning, pre-flight checks, LLM trigger and reviews.
     * @param {Object} input - Contains command and context parameters
     */
    async execute({ command, context }) {
        this.transitionTo('Planning');
        eventBus.emit('ExecutionStarted', { command, context });

        // Phase 5: Planning Engine simulation
        const isProtectedAction = command.includes('install') || command.includes('remove');
        if (isProtectedAction) {
            const hasPermission = context.permissions.terminal || context.permissions.filesystem === 'write';
            if (!hasPermission) {
                this.transitionTo('Failed');
                throw new Error('AIEOS Permission Denied: execution context requires elevated permissions for capability installation.');
            }
        }

        this.transitionTo('Loading');
        // Parse namespaces
        const parts = command.trim().split(/\s+/);
        const namespace = parts[0]; // e.g. "/skill" or "/mode"
        const subcommand = parts[1]; // e.g. "install", "search"
        const target = parts.slice(2).join(' ');

        let result = null;
        this.transitionTo('Executing');

        try {
            if (namespace === '/skill' || namespace === 'skill') {
                if (subcommand === 'search') {
                    result = await this.searchSkills(target);
                } else if (subcommand === 'install') {
                    result = await this.installSkill(target);
                } else if (subcommand === 'remove') {
                    result = await this.removeSkill(target);
                }
            } else if (namespace === '/mode' || namespace === 'mode') {
                result = await this.setMode(subcommand);
            } else {
                // Fallback legacy execution routing
                result = await this._callCore(parts);
            }

            this.transitionTo('Reviewing');
            this.transitionTo('Persisting');
            eventBus.emit('MemoryUpdated', { scope: 'project', changes: { lastCommand: command } });
            
            this.transitionTo('Complete');
            eventBus.emit('ExecutionFinished', { command, status: 'success', data: result });
            
            return {
                success: true,
                data: result
            };

        } catch (error) {
            this.transitionTo('Failed');
            eventBus.emit('ExecutionFinished', { command, status: 'failed', error: error.message });
            throw error;
        } finally {
            this.transitionTo('Idle');
        }
    }

    async searchSkills(query) {
        return await this._callCore(['skill', 'search', `"${query}"`]);
    }

    async installSkill(packageName) {
        const result = await this._callCore(['skill', 'install', `"${packageName}"`]);
        eventBus.emit('SkillInstalled', { packageName });
        return result;
    }

    async removeSkill(packageName) {
        const result = await this._callCore(['skill', 'remove', `"${packageName}"`]);
        eventBus.emit('SkillRemoved', { packageName });
        return result;
    }

    async recommendSkills(projectContext) {
        return await this._callCore(['skill', 'recommend', `"${projectContext}"`]);
    }

    async setMode(mode) {
        const result = await this._callCore(['mode', `"${mode}"`]);
        eventBus.emit('ModeChanged', { mode });
        return result;
    }
}

module.exports = AIEOSRuntime;

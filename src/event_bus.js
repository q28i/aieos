/**
 * A lightweight pub/sub Event Bus for real-time synchronization
 * across the AIEOS runtime, SDK, and adapters.
 */
class AIEOSEventBus {
    constructor() {
        this.listeners = new Map();
    }

    /**
     * Subscribe to an event topic.
     * @param {string} event - Event name (e.g. 'ProjectOpened', 'SkillInstalled')
     * @param {Function} callback - Execution handler
     */
    on(event, callback) {
        if (!this.listeners.has(event)) {
            this.listeners.set(event, []);
        }
        this.listeners.get(event).push(callback);
    }

    /**
     * Unsubscribe a callback from an event topic.
     * @param {string} event 
     * @param {Function} callback 
     */
    off(event, callback) {
        if (!this.listeners.has(event)) return;
        const filtered = this.listeners.get(event).filter(cb => cb !== callback);
        this.listeners.set(event, filtered);
    }

    /**
     * Emit an event payload to all registered subscribers.
     * @param {string} event - Event name
     * @param {Object} payload - Associated event parameters
     */
    emit(event, payload = {}) {
        if (!this.listeners.has(event)) return;
        
        const timestamp = Date.now();
        const eventObject = {
            event,
            timestamp,
            payload
        };

        this.listeners.get(event).forEach(callback => {
            try {
                callback(eventObject);
            } catch (err) {
                console.error(`[AIEOS EventBus] Error in subscriber callback for '${event}':`, err);
            }
        });
    }
}

module.exports = new AIEOSEventBus();

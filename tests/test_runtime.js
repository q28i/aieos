const { AIEOSRuntime, eventBus, ClaudeAieosAdapter } = require('../src/index');
const fs = require('fs');
const path = require('path');
const os = require('os');

async function runTests() {
    console.log("Starting Phase 4 Integration Tests...\n");

    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'aieos-test-'));
    const oldCwd = process.cwd();
    process.chdir(tempDir);
    console.log(`Working in temporary directory: ${tempDir}`);

    const eventsFired = [];
    eventBus.on('RuntimeInitialized', (e) => {
        eventsFired.push(e.event);
        console.log(`[Event Received] ${e.event} with payload:`, JSON.stringify(e.payload));
    });
    eventBus.on('StateChanged', (e) => {
        eventsFired.push(`${e.event}:${e.payload.to}`);
        console.log(`[State Transition] ${e.payload.from} -> ${e.payload.to}`);
    });
    eventBus.on('SkillInstalled', (e) => {
        eventsFired.push(e.event);
        console.log(`[Event Received] ${e.event} for:`, e.payload.packageName);
    });
    eventBus.on('MemoryUpdated', (e) => {
        eventsFired.push(e.event);
        console.log(`[Event Received] ${e.event} changes logged:`, JSON.stringify(e.payload.changes));
    });

    try {
        const runtime = new AIEOSRuntime();
        const adapter = new ClaudeAieosAdapter();

        console.log("--- 1. Testing runtime.initialize() ---");
        await runtime.initialize();
        await adapter.initialize({});

        console.log("\n--- 2. Testing workspace initialization ---");
        // We must initialize the workspace so AIEOS commands can execute
        await runtime._callCore(['init']);
        console.log("Workspace initialized successfully.");

        console.log("\n--- 3. Testing Compiled Execution Context ---");
        const executionContext = await adapter.getExecutionContext();
        console.log("Compiled Context Keys:", Object.keys(executionContext));

        console.log("\n--- 4. Testing runtime.execute() for '/skill install' ---");
        // Grant permissions for the test
        executionContext.permissions.filesystem = 'write';
        executionContext.userIntent = "Install computation tools please";
        const result = await runtime.execute({
            command: "/skill install @aieos/performance",
            context: executionContext
        });

        console.log("\nCommand Output result:", result);

        // Verification checks
        const expectedEvents = [
            'StateChanged:Scanning',
            'StateChanged:Planning',
            'StateChanged:Loading',
            'StateChanged:Idle',
            'RuntimeInitialized',
            'StateChanged:Planning',
            'StateChanged:Loading',
            'StateChanged:Executing',
            'StateChanged:Reviewing',
            'StateChanged:Persisting',
            'MemoryUpdated',
            'StateChanged:Complete',
            'SkillInstalled',
            'StateChanged:Idle'
        ];

        console.log("\n--- 5. Verification Check ---");
        let allPassed = true;
        for (const exp of expectedEvents) {
            if (eventsFired.includes(exp)) {
                console.log(`\x1b[32m✓\x1b[0m Verified Event: ${exp}`);
            } else {
                console.log(`\x1b[31m✗\x1b[0m Missing Event: ${exp}`);
                allPassed = false;
            }
        }

        if (allPassed) {
            console.log("\n\x1b[32mALL TESTS COMPLETED SUCCESSFULLY!\x1b[0m");
        } else {
            console.log("\n\x1b[31mTEST SUITE FAILED - MISSING EVENTS\x1b[0m");
            process.exit(1);
        }

    } catch (err) {
        console.error("Test Suite crashed with error:", err);
        process.exit(1);
    } finally {
        process.chdir(oldCwd);
        try {
            fs.rmSync(tempDir, { recursive: true, force: true });
        } catch (rmErr) {
            // Ignore clean up errors
        }
    }
}

runTests();

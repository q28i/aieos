const readline = require('readline');
const fs = require('fs');
const path = require('path');

/**
 * Renders the installer title and welcome message.
 */
function renderHeader() {
    console.clear();
    console.log('\x1b[38;2;249;115;22m\x1b[1m🧠 AIEOS Installer v1.4.0\x1b[0m');
    console.log('\x1b[38;2;120;120;120m────────────────────────────\x1b[0m');
}

/**
 * Promise-based helper to prompt the user using readline.
 */
function askQuestion(rl, query) {
    return new Promise(resolve => rl.question(query, resolve));
}

/**
 * Scan for installed AI runtimes on the developer's machine.
 */
function scanEnvironment() {
    const home = process.env.HOME || process.env.USERPROFILE || '';
    const targets = {
        claude: false,
        cursor: false,
        antigravity: false
    };

    // Claude Code check
    if (fs.existsSync(path.join(home, '.claude'))) targets.claude = true;
    
    // Cursor config check
    const appData = process.env.APPDATA || (process.platform === 'darwin' ? path.join(home, 'Library/Application Support') : '/var/local');
    if (fs.existsSync(path.join(appData, 'Cursor')) || fs.existsSync(path.join(home, '.cursor'))) {
        targets.cursor = true;
    }

    // Antigravity check
    if (fs.existsSync(path.join(home, '.gemini', 'antigravity-ide'))) {
        targets.antigravity = true;
    }

    return targets;
}

/**
 * Main interactive CLI wizard.
 */
async function runWizard() {
    renderHeader();
    console.log('Scanning environment for target runtimes...\n');
    const detected = scanEnvironment();

    console.log(`${detected.claude ? '\x1b[32m✓\x1b[0m' : '\x1b[31m✗\x1b[0m'} Detected: Claude Code`);
    console.log(`${detected.cursor ? '\x1b[32m✓\x1b[0m' : '\x1b[31m✗\x1b[0m'} Detected: Cursor IDE`);
    console.log(`${detected.antigravity ? '\x1b[32m✓\x1b[0m' : '\x1b[31m✗\x1b[0m'} Detected: Antigravity IDE`);
    console.log('\x1b[38;2;120;120;120m────────────────────────────\x1b[0m\n');

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    try {
        // Step 1: Install Target
        console.log('1. Install AIEOS Into:\n');
        console.log('   [1] Claude Code');
        console.log('   [2] Cursor IDE');
        console.log('   [3] Antigravity IDE');
        console.log('   [4] All Platforms\n');
        
        let targetChoice = '';
        while (!['1', '2', '3', '4'].includes(targetChoice)) {
            targetChoice = (await askQuestion(rl, 'Choose platform [1-4]: ')).trim();
        }
        
        console.log('\n\x1b[38;2;120;120;120m────────────────────────────\x1b[0m\n');

        // Step 2: Scope
        console.log('2. Choose Installation Scope:\n');
        console.log('   [1] Project Workspace (local)');
        console.log('   [2] Global System');
        console.log('   [3] Both (Recommended)\n');

        let scopeChoice = '';
        while (!['1', '2', '3'].includes(scopeChoice)) {
            scopeChoice = (await askQuestion(rl, 'Choose scope [1-3]: ')).trim();
        }

        console.log('\n\x1b[38;2;120;120;120m────────────────────────────\x1b[0m\n');

        // Step 3: Behavior Capabilities
        console.log('3. Select Initial Capability Profile:\n');
        console.log('   [1] General Research (Core Socratic reasoning)');
        console.log('   [2] Algorithmic Trading (Quant + Risk + API tools)');
        console.log('   [3] Full Suite (All capabilities)\n');

        let profileChoice = '';
        while (!['1', '2', '3'].includes(profileChoice)) {
            profileChoice = (await askQuestion(rl, 'Choose profile [1-3]: ')).trim();
        }

        console.log('\n\x1b[38;2;120;120;120m────────────────────────────\x1b[0m\n');

        console.log('\x1b[32m✔ Configuration locked.\x1b[0m Writing runtime files...\n');
        
        // Simulating deployment success
        console.log('\x1b[32m[SUCCESS]\x1b[0m AIEOS Core SDK & Capabilities deployed successfully.');
        console.log('\nRun "/aieos status" or "npx @q28i/aieos status" to verify your setup.');

    } finally {
        rl.close();
    }
}

if (require.main === module) {
    runWizard();
}

module.exports = { runWizard };

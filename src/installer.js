const readline = require('readline');
const fs = require('fs');
const path = require('path');
const AIEOSCompiler = require('./runtime/compiler');

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
        console.log('   [2] Data Science & Optimization (Computation + Validation + Performance)');
        console.log('   [3] Full Suite (All capabilities)\n');

        let profileChoice = '';
        while (!['1', '2', '3'].includes(profileChoice)) {
            profileChoice = (await askQuestion(rl, 'Choose profile [1-3]: ')).trim();
        }

        console.log('\n\x1b[38;2;120;120;120m────────────────────────────\x1b[0m\n');

        console.log('\x1b[32m✔ Configuration locked.\x1b[0m Writing thin wrapper rules & manifests...\n');
        
        // Define active capabilities based on choices
        let profileName = 'decision-os';
        let skills = ['research'];
        if (profileChoice === '2') {
            skills = ['research', 'computation', 'validation'];
        } else if (profileChoice === '3') {
            skills = ['research', 'computation', 'validation', 'testing', 'security', 'datapipeline', 'performance', 'docs', 'memory'];
        }

        const compiler = new AIEOSCompiler();
        const options = {
            profile: profileName,
            activeSkills: skills,
            executionLevel: 2
        };

        const platformsToInstall = [];
        if (targetChoice === '1') platformsToInstall.push('claude');
        if (targetChoice === '2') platformsToInstall.push('cursor');
        if (targetChoice === '3') platformsToInstall.push('antigravity');
        if (targetChoice === '4') platformsToInstall.push('claude', 'cursor', 'antigravity');

        for (const platform of platformsToInstall) {
            try {
                const pathsWritten = compiler.writeArtifacts(platform, options);
                console.log(`  * Generated thin wrapper & manifest for \x1b[33m${platform.toUpperCase()}\x1b[0m:`);
                for (const p of pathsWritten) {
                    console.log(`    - ${p}`);
                }
            } catch (err) {
                console.error(`  * \x1b[31mError writing to ${platform}:\x1b[0m ${err.message}`);
            }
        }
        
        console.log('\n\x1b[32m[SUCCESS]\x1b[0m AIEOS Core thin wrappers generated and deployed successfully.');
        console.log('\nRun "/aieos status" or "npx @q28i/aieos status" to verify your setup.');

    } finally {
        rl.close();
    }
}

/**
 * Non-interactive command line runner.
 * @param {Array<string>} args - CLI arguments
 */
async function runCli(args) {
    const targets = [];
    let profile = 'decision-os';
    let skills = ['research'];
    let workspacePath = process.cwd();
    let uninstallMode = false;

    let i = 0;
    while (i < args.length) {
        const arg = args[i].toLowerCase();
        if (arg === 'uninstall') {
            uninstallMode = true;
        } else if (arg === '--cursor') {
            targets.push('cursor');
        } else if (arg === '--claude') {
            targets.push('claude');
        } else if (arg === '--antigravity') {
            targets.push('antigravity');
        } else if (arg === '--all') {
            targets.push('cursor', 'claude', 'antigravity');
        } else if (arg === '--profile') {
            if (i + 1 < args.length) {
                profile = args[i + 1].toLowerCase();
                i++;
            }
        } else if (arg === '--skills') {
            if (i + 1 < args.length) {
                skills = args[i + 1].split(',').map(s => s.trim().toLowerCase());
                i++;
            }
        } else if (arg === '--project') {
            if (i + 1 < args.length) {
                workspacePath = path.resolve(args[i + 1]);
                i++;
            }
        }
        i++;
    }

    if (uninstallMode) {
        console.log('Uninstalling AIEOS integrations...');
        const home = process.env.HOME || process.env.USERPROFILE || '';
        const cursorrulesPath = path.join(workspacePath, '.cursorrules');
        const manifestCursor = path.join(workspacePath, 'aieos_manifest.json');
        const claudeBridge = path.join(home, '.claude', 'skills', 'aieos_bridge.md');
        const manifestClaude = path.join(home, '.claude', 'skills', 'aieos_manifest.json');
        const antigravitySkill = path.join(home, '.gemini', 'config', 'skills', 'aieos', 'SKILL.md');
        const manifestAntigravity = path.join(home, '.gemini', 'config', 'skills', 'aieos', 'aieos_manifest.json');

        const filesToDelete = [cursorrulesPath, manifestCursor, claudeBridge, manifestClaude, antigravitySkill, manifestAntigravity];
        for (const file of filesToDelete) {
            if (fs.existsSync(file)) {
                fs.unlinkSync(file);
                console.log(`  * Removed: ${file}`);
            }
        }
        console.log('\n\x1b[32m[SUCCESS]\x1b[0m AIEOS integrations uninstalled.');
        return true;
    }

    if (targets.length === 0) {
        return runWizard();
    }

    console.log(`\nCompiling and installing AIEOS wrappers (Profile: ${profile.toUpperCase()})...`);
    const compiler = new AIEOSCompiler(workspacePath);
    const options = {
        profile,
        activeSkills: skills,
        executionLevel: 2
    };

    for (const platform of [...new Set(targets)]) {
        try {
            const pathsWritten = compiler.writeArtifacts(platform, options);
            console.log(`  * Generated \x1b[33m${platform.toUpperCase()}\x1b[0m wrappers:`);
            for (const p of pathsWritten) {
                console.log(`    - ${p}`);
            }
        } catch (err) {
            console.error(`  * \x1b[31mError writing to ${platform}:\x1b[0m ${err.message}`);
        }
    }
    console.log('\n\x1b[32m[SUCCESS]\x1b[0m Installation complete.');
    return true;
}

if (require.main === module) {
    const args = process.argv.slice(2);
    if (args.length > 0) {
        runCli(args);
    } else {
        runWizard();
    }
}

module.exports = { runWizard, runCli };

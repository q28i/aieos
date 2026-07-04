#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const path = require('path');

const cliPath = path.join(__dirname, '../aieos.py');
const { runCli, runWizard } = require('../src/installer');
const args = process.argv.slice(2);

const isInstallCmd = args.length > 0 && (
    args[0] === 'install' || 
    args[0] === 'uninstall' || 
    args.some(a => ['--cursor', '--claude', '--antigravity', '--all'].includes(a))
);

if (args.length === 0) {
    runWizard();
    return;
}

if (isInstallCmd) {
    const installArgs = args[0] === 'install' ? args.slice(1) : args;
    runCli(installArgs);
    return;
}

const candidates = ['python', 'python3', 'py'];
let chosenPython = null;

for (const candidate of candidates) {
    try {
        const output = execSync(`${candidate} -c "import sys; print(sys.version_info[:2])"`, { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim();
        const match = output.match(/\((\d+),\s*(\d+)\)/);
        if (match) {
            const major = parseInt(match[1], 10);
            const minor = parseInt(match[2], 10);
            if (major > 3 || (major === 3 && minor >= 11)) {
                chosenPython = candidate;
                break;
            }
        }
    } catch (e) {
        // Continue checking candidates
    }
}

if (!chosenPython) {
    console.error('\x1b[31mAIEOS requires Python 3.11 or newer.\x1b[0m\n');
    console.error('Install Python:');
    console.error('https://www.python.org/downloads/\n');
    console.error('After installation, run the command again.');
    process.exit(1);
}

const py = spawn(chosenPython, [cliPath, ...args], { stdio: 'inherit' });
py.on('close', (code) => {
    process.exit(code || 0);
});

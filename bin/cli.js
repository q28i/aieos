#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const path = require('path');

const cliPath = path.join(__dirname, '../aieos.py');
const args = process.argv.slice(2);

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
    console.error('\x1b[31mError: Python 3.11+ is required.\x1b[0m');
    console.error('Install from https://python.org');
    process.exit(1);
}

const py = spawn(chosenPython, [cliPath, ...args], { stdio: 'inherit' });
py.on('close', (code) => {
    process.exit(code || 0);
});

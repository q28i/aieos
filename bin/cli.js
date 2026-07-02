#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const cliPath = path.join(__dirname, '../aieos.py');
const args = process.argv.slice(2);

const py = spawn('python', [cliPath, ...args], { stdio: 'inherit' });
py.on('close', (code) => {
    process.exit(code);
});

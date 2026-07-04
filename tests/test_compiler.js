const AIEOSCompiler = require('../src/runtime/compiler');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

function runTest() {
    console.log('Running test for AIEOSCompiler...');
    const compiler = new AIEOSCompiler(__dirname);

    // Test 1: Compile targets
    const artifacts = compiler.compile({
        profile: 'architect',
        activeSkills: ['research', 'memory'],
        executionLevel: 1
    });

    // Check all artifact keys exist
    assert.ok(artifacts.cursorrules);
    assert.ok(artifacts.claude_bridge);
    assert.ok(artifacts.antigravity_skill);
    assert.ok(artifacts.manifest);
    assert.ok(artifacts.readme);

    // Verify manifest keys
    const manifest = artifacts.manifest;
    assert.strictEqual(manifest.runtimeVersion, "1.4.0");
    assert.strictEqual(manifest.activeProfile, "architect");
    assert.deepStrictEqual(manifest.capabilities, ['research', 'memory']);
    assert.strictEqual(manifest.executionLevel, 1);
    assert.ok(manifest.generatedAt);
    
    // Verify thin rules content
    assert.ok(artifacts.cursorrules.includes('Active Profile: ARCHITECT'));
    assert.ok(artifacts.cursorrules.includes('System Design Rigor'));
    console.log('✓ Compile targets check passed.');

    // Test 2: Write artifacts to temporary directories
    const testDir = path.join(__dirname, 'test_compiler_out');
    if (!fs.existsSync(testDir)) {
        fs.mkdirSync(testDir);
    }

    try {
        const pathsCursor = compiler.writeArtifacts('cursor', { profile: 'mentor' }, testDir);
        assert.strictEqual(pathsCursor.length, 2);
        assert.ok(fs.existsSync(path.join(testDir, '.cursorrules')));
        assert.ok(fs.existsSync(path.join(testDir, 'aieos_manifest.json')));

        const manifestWritten = JSON.parse(fs.readFileSync(path.join(testDir, 'aieos_manifest.json'), 'utf-8'));
        assert.strictEqual(manifestWritten.activeProfile, 'mentor');
        console.log('✓ Write Cursor rules and manifest check passed.');

        // Verify file sizes/token budgets
        const rulesSize = fs.statSync(path.join(testDir, '.cursorrules')).size;
        console.log(`  * Cursor rules file size: ${rulesSize} bytes`);
        assert.ok(rulesSize < 2000, "Thin wrapper size should be reasonably small (< 2KB)");

    } finally {
        // Clean up test files
        if (fs.existsSync(path.join(testDir, '.cursorrules'))) fs.unlinkSync(path.join(testDir, '.cursorrules'));
        if (fs.existsSync(path.join(testDir, 'aieos_manifest.json'))) fs.unlinkSync(path.join(testDir, 'aieos_manifest.json'));
        fs.rmdirSync(testDir);
    }

    console.log('ALL COMPILER TESTS PASSED!\n');
}

runTest();

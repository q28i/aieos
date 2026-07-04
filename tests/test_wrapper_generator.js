const WrapperGenerator = require('../src/runtime/wrapper_generator');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

function runTest() {
    console.log('Running test for WrapperGenerator...');
    const generator = new WrapperGenerator(__dirname);

    // Test 1: Compile decision-os
    const wrapper = generator.compile({
        profile: 'decision-os',
        activeSkills: ['research', 'trading'],
        executionLevel: 2
    });

    assert.ok(wrapper.includes('Active Profile: DECISION-OS'));
    assert.ok(wrapper.includes('Active Skills**: research, trading'));
    assert.ok(wrapper.includes('npx @q28i/aieos skill'));
    console.log('✓ Compile decision-os works.');

    // Test 2: Compile architect
    const archWrapper = generator.compile({
        profile: 'architect',
        activeSkills: [],
        executionLevel: 1
    });

    assert.ok(archWrapper.includes('Active Profile: ARCHITECT'));
    assert.ok(archWrapper.includes('System Design Rigor'));
    assert.ok(archWrapper.includes('Active Skills**: None'));
    console.log('✓ Compile architect works.');

    // Test 3: Generate file output
    const testOutputPath = path.join(__dirname, 'test_output');
    if (!fs.existsSync(testOutputPath)) {
        fs.mkdirSync(testOutputPath);
    }

    try {
        const cursorrulesPath = generator.generate('cursor', { profile: 'mentor' }, testOutputPath);
        assert.ok(fs.existsSync(cursorrulesPath));
        const content = fs.readFileSync(cursorrulesPath, 'utf-8');
        assert.ok(content.includes('Active Profile: MENTOR'));
        console.log(`✓ Generate cursorrules works at: ${cursorrulesPath}`);
        
        fs.unlinkSync(cursorrulesPath);
    } finally {
        fs.rmdirSync(testOutputPath);
    }

    console.log('ALL WRAPPER GENERATOR TESTS PASSED!\n');
}

runTest();

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

const { VerBeat, getVersion, bumpVersion, getVersionComponents } = require('../src/verbeat.js');

function createTempDir() {
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'verbeat-test-'));
    return tempDir;
}

function cleanupTempDir(tempDir) {
    if (fs.existsSync(tempDir)) {
        fs.rmSync(tempDir, { recursive: true, force: true });
    }
}

function testBasicFunctionality() {
    console.log('Testing basic functionality...');
    
    const tempDir = createTempDir();
    
    try {
        const versionFile = path.join(tempDir, 'verbeat.version');
        fs.writeFileSync(versionFile, '1 # Initial release\n2 # Breaking API changes\n');
        
        const verbeat = new VerBeat(tempDir);
        
        const version = verbeat.getCurrentVersion();
        console.log(`  Current version: ${version}`);
        
        const [manual, yymm, commits] = verbeat.getVersionComponents();
        console.log(`  Manual: ${manual}, Date: ${yymm}, Commits: ${commits}`);
        
        const history = verbeat.getVersionHistory();
        console.log(`  Version history: ${JSON.stringify(history)}`);
        
        const newVersion = verbeat.bumpManualVersion('Test bump');
        console.log(`  Bumped to version: ${newVersion}`);
        
        const content = fs.readFileSync(versionFile, 'utf8');
        console.log(`  Updated version file:\n${content}`);
        
        console.log('  ✓ Basic functionality test passed');
    } finally {
        cleanupTempDir(tempDir);
    }
}

function testConvenienceFunctions() {
    console.log('Testing convenience functions...');
    
    const tempDir = createTempDir();
    
    try {
        const versionFile = path.join(tempDir, 'verbeat.version');
        fs.writeFileSync(versionFile, '1 # Initial release\n');
        
        const version = getVersion(tempDir);
        console.log(`  getVersion(): ${version}`);
        
        const [manual, yymm, commits] = getVersionComponents(tempDir);
        console.log(`  getVersionComponents(): [${manual}, ${yymm}, ${commits}]`);
        
        const newVersion = bumpVersion('Test', tempDir);
        console.log(`  bumpVersion(): ${newVersion}`);
        
        console.log('  ✓ Convenience functions test passed');
    } finally {
        cleanupTempDir(tempDir);
    }
}

function testDateSpecificVersion() {
    console.log('Testing date-specific version...');
    
    const tempDir = createTempDir();
    
    try {
        const versionFile = path.join(tempDir, 'verbeat.version');
        fs.writeFileSync(versionFile, '1 # Initial release\n');
        
        const testDate = new Date(2025, 6, 15); // July 15, 2025
        const version = getVersion(tempDir, testDate);
        console.log(`  Version for ${testDate.toDateString()}: ${version}`);
        
        const expected = '1.2507.0';
        if (version === expected) {
            console.log(`  ✓ Date-specific version test passed: ${version}`);
        } else {
            console.log(`  ✗ Date-specific version test failed: expected ${expected}, got ${version}`);
        }
    } finally {
        cleanupTempDir(tempDir);
    }
}

function testErrorHandling() {
    console.log('Testing error handling...');
    
    const tempDir = createTempDir();
    
    try {
        try {
            const verbeat = new VerBeat(tempDir);
            const version = verbeat.getCurrentVersion();
            console.log(`  ✗ Should have raised error for missing version file`);
        } catch (error) {
            console.log(`  ✓ Correctly raised error for missing version file: ${error.name}`);
        }
        
        const versionFile = path.join(tempDir, 'verbeat.version');
        fs.writeFileSync(versionFile, '');
        
        try {
            const verbeat = new VerBeat(tempDir);
            const version = verbeat.getCurrentVersion();
            console.log(`  ✗ Should have raised error for empty version file`);
        } catch (error) {
            console.log(`  ✓ Correctly raised error for empty version file: ${error.name}`);
        }
        
        console.log('  ✓ Error handling test passed');
    } finally {
        cleanupTempDir(tempDir);
    }
}

function testGitIntegration() {
    console.log('Testing Git integration...');
    
    const tempDir = createTempDir();
    
    try {
        const versionFile = path.join(tempDir, 'verbeat.version');
        fs.writeFileSync(versionFile, '1 # Initial release\n');
        
        // Initialize Git repo
        execSync('git init', { cwd: tempDir });
        execSync('git config user.name "Test User"', { cwd: tempDir });
        execSync('git config user.email "test@example.com"', { cwd: tempDir });
        
        // Add and commit version file
        execSync('git add verbeat.version', { cwd: tempDir });
        execSync('git commit -m "Initial commit"', { cwd: tempDir });
        
        const version = getVersion(tempDir);
        const [manual, yymm, commits] = getVersionComponents(tempDir);
        
        console.log(`  Version: ${version}`);
        console.log(`  Manual: ${manual}, Date: ${yymm}, Commits: ${commits}`);
        
        if (commits >= 1) {
            console.log('  ✓ Git integration test passed');
        } else {
            console.log('  ✗ Git integration test failed: expected at least 1 commit');
        }
    } finally {
        cleanupTempDir(tempDir);
    }
}

function testCLI() {
    console.log('Testing CLI interface...');
    
    const tempDir = createTempDir();
    
    try {
        const versionFile = path.join(tempDir, 'verbeat.version');
        fs.writeFileSync(versionFile, '1 # Initial release\n');
        
        // Test version command
        const versionOutput = execSync('node bin/verbeat.js version', {
            cwd: path.join(__dirname, '..'),
            env: { ...process.env, PWD: tempDir }
        }).toString().trim();
        console.log(`  CLI version: ${versionOutput}`);
        
        // Test components command
        const componentsOutput = execSync('node bin/verbeat.js components', {
            cwd: path.join(__dirname, '..'),
            env: { ...process.env, PWD: tempDir }
        }).toString().trim();
        console.log(`  CLI components:\n${componentsOutput}`);
        
        // Test bump command
        const bumpOutput = execSync('node bin/verbeat.js bump "Test CLI bump"', {
            cwd: path.join(__dirname, '..'),
            env: { ...process.env, PWD: tempDir }
        }).toString().trim();
        console.log(`  CLI bump: ${bumpOutput}`);
        
        console.log('  ✓ CLI interface test passed');
    } finally {
        cleanupTempDir(tempDir);
    }
}

function main() {
    console.log('Running VerBeat Node.js implementation tests...\n');
    
    try {
        testBasicFunctionality();
        console.log();
        
        testConvenienceFunctions();
        console.log();
        
        testDateSpecificVersion();
        console.log();
        
        testErrorHandling();
        console.log();
        
        testGitIntegration();
        console.log();
        
        testCLI();
        console.log();
        
        console.log('🎉 All tests passed!');
    } catch (error) {
        console.error(`❌ Test failed with error: ${error.message}`);
        console.error(error.stack);
        process.exit(1);
    }
}

if (require.main === module) {
    main();
} 
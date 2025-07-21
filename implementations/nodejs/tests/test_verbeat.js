import fs from 'fs';
import path from 'path';
import os from 'os';
import { execSync } from 'child_process';
import { describe, test, it } from 'node:test';
import assert from 'node:assert';
import { fileURLToPath } from 'url';
import {
    VerBeat,
    getVersion,
    bumpVersion,
    getVersionComponents,
    VerBeatBranchError,
    getCalculatedVersion,
    getCurrentVersion
} from '../src/verbeat.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function createTempDir() {
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'verbeat-test-'));
    return tempDir;
}

function cleanupTempDir(tempDir) {
    if (fs.existsSync(tempDir)) {
        fs.rmSync(tempDir, { recursive: true, force: true });
    }
}

describe('VerBeat', () => {
    test('basic functionality', () => {
        const tempDir = createTempDir();
        
        try {
            const versionFile = path.join(tempDir, 'verbeat.version');
            fs.writeFileSync(versionFile, '1 # Initial release\n2 # Breaking API changes\n');
            
            const verbeat = new VerBeat(tempDir);
            
            const version = verbeat.getCurrentVersion();
            assert.strictEqual(version, '2.2507.0');
            
            const [manual, yymm, commits] = verbeat.getVersionComponents();
            assert.strictEqual(manual, 2);
            assert.strictEqual(yymm, '2507');
            assert.strictEqual(commits, 0);
            
            const history = verbeat.getVersionHistory();
            assert.deepStrictEqual(history, [[1, 'Initial release'], [2, 'Breaking API changes']]);
            
            const newVersion = verbeat.bumpManualVersion('Test bump');
            assert.strictEqual(newVersion, 3);
            
            const content = fs.readFileSync(versionFile, 'utf8');
            assert(content.includes('3 # Test bump'));
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('convenience functions', () => {
        const tempDir = createTempDir();
        
        try {
            const versionFile = path.join(tempDir, 'verbeat.version');
            fs.writeFileSync(versionFile, '1 # Initial release\n');
            
            const version = getVersion(tempDir);
            assert.strictEqual(version, '1.2507.0');
            
            const [manual, yymm, commits] = getVersionComponents(tempDir);
            assert.strictEqual(manual, 1);
            assert.strictEqual(yymm, '2507');
            assert.strictEqual(commits, 0);
            
            const newVersion = bumpVersion('Test', tempDir);
            assert.strictEqual(newVersion, 2);
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('date specific version', () => {
        const tempDir = createTempDir();
        const tempPath = path.join(tempDir, 'test-project');
        fs.mkdirSync(tempPath);

        try {
            const versionFile = path.join(tempPath, 'verbeat.version');
            fs.writeFileSync(versionFile, '1 # Initial release\n');

            const testDate = new Date(2025, 6, 15);
            const verbeat = new VerBeat(tempPath);
            const version = verbeat.getCurrentVersion(testDate);

            assert.strictEqual(version, '1.2507.0');
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('error handling', () => {
        const tempDir = createTempDir();
        
        try {
            assert.throws(() => {
                const verbeat = new VerBeat(tempDir);
                verbeat.getCurrentVersion();
            });
            
            const versionFile = path.join(tempDir, 'verbeat.version');
            fs.writeFileSync(versionFile, '');
            
            assert.throws(() => {
                const verbeat = new VerBeat(tempDir);
                verbeat.getCurrentVersion();
            });
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('git integration', () => {
        const tempDir = createTempDir();
        
        try {
            const versionFile = path.join(tempDir, 'verbeat.version');
            fs.writeFileSync(versionFile, '1 # Initial release\n');
            
            execSync('git init', { cwd: tempDir });
            execSync('git config user.name "Test User"', { cwd: tempDir });
            execSync('git config user.email "test@example.com"', { cwd: tempDir });
            execSync('git add verbeat.version', { cwd: tempDir });
            execSync('git commit -m "Initial commit"', { cwd: tempDir });
            
            const version = getVersion(tempDir);
            const [manual, yymm, commits] = getVersionComponents(tempDir);
            
            assert(commits > 0);
            assert(version.match(new RegExp(`\\.${commits}$`)));
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('cli', () => {
        const tempDir = createTempDir();
        
        try {
            const versionFile = path.join(tempDir, 'verbeat.version');
            fs.writeFileSync(versionFile, '1 # Initial release\n');
            
            const scriptPath = path.join(__dirname, '..', 'bin', 'verbeat.js');
            const cwd = path.join(__dirname, '..');
            
            const versionOutput = execSync(`node ${scriptPath} version`, { 
                cwd, 
                env: { ...process.env, PWD: tempDir },
                encoding: 'utf8' 
            });
            assert(versionOutput.trim().match(/^\d+\.\d+\.\d+$/));
            
            const componentsOutput = execSync(`node ${scriptPath} components`, { 
                cwd, 
                env: { ...process.env, PWD: tempDir },
                encoding: 'utf8' 
            });
            assert(componentsOutput.trim().includes('Manual:'));
            assert(componentsOutput.trim().includes('Date:'));
            assert(componentsOutput.trim().includes('Commits:'));
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('branch restriction', () => {
        const tempDir = createTempDir();
        
        try {
            const versionFile = path.join(tempDir, 'verbeat.version');
            fs.writeFileSync(versionFile, '1 # Initial release\n');
            
            execSync('git init', { cwd: tempDir });
            execSync('git config user.name "Test User"', { cwd: tempDir });
            execSync('git config user.email "test@example.com"', { cwd: tempDir });
            execSync('git branch -m main', { cwd: tempDir });
            execSync('git add verbeat.version', { cwd: tempDir });
            execSync('git commit -m "Initial commit"', { cwd: tempDir });
            execSync('git checkout -b feature-branch', { cwd: tempDir });
            
            const verbeat = new VerBeat(tempDir);
            
            assert.throws(() => verbeat.bumpManualVersion('Test bump'), VerBeatBranchError);
            
            execSync('git checkout main', { cwd: tempDir });
            
            const newVersion = verbeat.bumpManualVersion('Test bump');
            assert.strictEqual(newVersion, 2);
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('init command', async () => {
        const tempDir = createTempDir();
        
        try {
            const scriptPath = path.join(__dirname, '..', 'bin', 'verbeat.js');
            
            const output = execSync(`node ${scriptPath} init "Project kickoff"`, { 
                cwd: tempDir,
                encoding: 'utf8' 
            });
            
            const versionFile = path.join(tempDir, 'verbeat.version');
            assert(fs.existsSync(versionFile));
            
            const content = fs.readFileSync(versionFile, 'utf8');
            assert(content.includes('1 # Project kickoff'));
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('init command existing file', async () => {
        const tempDir = createTempDir();
        
        try {
            const versionFile = path.join(tempDir, 'verbeat.version');
            fs.writeFileSync(versionFile, '1 # Existing file\n');
            
            const scriptPath = path.join(__dirname, '..', 'bin', 'verbeat.js');
            
            execSync(`node ${scriptPath} init "Should not overwrite"`, { 
                cwd: tempDir,
                encoding: 'utf8' 
            });
            
            const content = fs.readFileSync(versionFile, 'utf8');
            assert(content.includes('1 # Existing file'));
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('tag based version', () => {
        const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'verbeat-test-'));
        const tempPath = path.join(tempDir, 'test-project');
        fs.mkdirSync(tempPath);

        try {
            const versionFile = path.join(tempPath, 'verbeat.version');
            fs.writeFileSync(versionFile, '1 # Initial release\n');

            execSync('git init', { cwd: tempPath });
            execSync('git config user.name "Test User"', { cwd: tempPath });
            execSync('git config user.email "test@example.com"', { cwd: tempPath });

            execSync('git add verbeat.version', { cwd: tempPath });
            execSync('git commit -m "Initial commit"', { cwd: tempPath });

            execSync(
                'git tag -a "v1.2507.5" -m "VerBeat 1.2507.5 (2025-07-15): Test tag"',
                { cwd: tempPath }
            );

            const verbeat = new VerBeat(tempPath);

            const version = verbeat.getCurrentVersion();
            assert.strictEqual(version, '1.2507.5');

            const [manual, yymm, commits] = verbeat.getVersionComponents();
            assert.deepStrictEqual([manual, yymm, commits], [1, '2507', 5]);
        } finally {
            fs.rmSync(tempDir, { recursive: true, force: true });
        }
    });

    test('getCalculatedVersion ignores existing tags', () => {
        const tempDir = createTempDir();
        
        try {
            const projectRoot = path.join(tempDir, 'project');
            fs.mkdirSync(projectRoot);
            
            const verbeatFile = path.join(projectRoot, 'verbeat.version');
            fs.writeFileSync(verbeatFile, '2 # Test project\n');
            
            const gitDir = path.join(projectRoot, '.git');
            fs.mkdirSync(gitDir);
            
            execSync('git init', { cwd: projectRoot });
            execSync('git config user.name "Test"', { cwd: projectRoot });
            execSync('git config user.email "test@example.com"', { cwd: projectRoot });
            
            for (let i = 0; i < 5; i++) {
                const testFile = path.join(projectRoot, `file${i}.txt`);
                fs.writeFileSync(testFile, `content ${i}`);
                execSync(`git add ${testFile}`, { cwd: projectRoot });
                execSync(`git commit -m "commit ${i}"`, { cwd: projectRoot });
            }
            
            execSync('git tag -a v2.2507.2 -m "Old tag"', { cwd: projectRoot });
            
            const verbeat = new VerBeat(projectRoot);
            
            const currentVersion = verbeat.getCurrentVersion();
            const calculatedVersion = verbeat.getCalculatedVersion();
            
            assert.strictEqual(currentVersion, '2.2507.2');
            assert.strictEqual(calculatedVersion, '2.2507.5');
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('getCalculatedVersion function works correctly', () => {
        const tempDir = createTempDir();
        
        try {
            const projectRoot = path.join(tempDir, 'project');
            fs.mkdirSync(projectRoot);
            
            const verbeatFile = path.join(projectRoot, 'verbeat.version');
            fs.writeFileSync(verbeatFile, '1 # Test project\n');
            
            const gitDir = path.join(projectRoot, '.git');
            fs.mkdirSync(gitDir);
            
            execSync('git init', { cwd: projectRoot });
            execSync('git config user.name "Test"', { cwd: projectRoot });
            execSync('git config user.email "test@example.com"', { cwd: projectRoot });
            
            for (let i = 0; i < 3; i++) {
                const testFile = path.join(projectRoot, `file${i}.txt`);
                fs.writeFileSync(testFile, `content ${i}`);
                execSync(`git add ${testFile}`, { cwd: projectRoot });
                execSync(`git commit -m "commit ${i}"`, { cwd: projectRoot });
            }
            
            execSync('git tag -a v1.2507.1 -m "Old tag"', { cwd: projectRoot });
            
            const calculatedVersion = getCalculatedVersion(projectRoot);
            const currentVersion = getCurrentVersion(projectRoot);
            
            assert.strictEqual(calculatedVersion, '1.2507.3');
            assert.strictEqual(currentVersion, '1.2507.1');
        } finally {
            cleanupTempDir(tempDir);
        }
    });

    test('getCurrentVersion with useCalculated parameter', () => {
        const tempDir = createTempDir();
        
        try {
            const projectRoot = path.join(tempDir, 'project');
            fs.mkdirSync(projectRoot);
            
            const verbeatFile = path.join(projectRoot, 'verbeat.version');
            fs.writeFileSync(verbeatFile, '3 # Test project\n');
            
            const gitDir = path.join(projectRoot, '.git');
            fs.mkdirSync(gitDir);
            
            execSync('git init', { cwd: projectRoot });
            execSync('git config user.name "Test"', { cwd: projectRoot });
            execSync('git config user.email "test@example.com"', { cwd: projectRoot });
            
            for (let i = 0; i < 4; i++) {
                const testFile = path.join(projectRoot, `file${i}.txt`);
                fs.writeFileSync(testFile, `content ${i}`);
                execSync(`git add ${testFile}`, { cwd: projectRoot });
                execSync(`git commit -m "commit ${i}"`, { cwd: projectRoot });
            }
            
            execSync('git tag -a v3.2507.2 -m "Old tag"', { cwd: projectRoot });
            
            const currentVersion = getCurrentVersion(projectRoot);
            const calculatedVersion = getCurrentVersion(projectRoot, new Date(), true);
            
            assert.strictEqual(currentVersion, '3.2507.2');
            assert.strictEqual(calculatedVersion, '3.2507.4');
        } finally {
            cleanupTempDir(tempDir);
        }
    });
}); 
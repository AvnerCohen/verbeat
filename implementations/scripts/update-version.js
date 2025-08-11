#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';

// Get __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function getCurrentVerBeatVersion() {
    try {
        const projectRoot = path.join(__dirname, '..', '..');
        
        // First priority: try to get version from git tags
        try {
            const gitTags = execSync('git tag --sort=-version:refname', { 
                cwd: projectRoot, 
                encoding: 'utf8' 
            }).trim().split('\n');
            
            if (gitTags.length > 0 && gitTags[0]) {
                const latestTag = gitTags[0];
                if (latestTag.startsWith('v')) {
                    return latestTag.substring(1);
                }
            }
        } catch (error) {
            console.log('Could not get git tags, trying version file...');
        }
        
        // Second priority: get version from the main project
        const versionFile = path.join(projectRoot, 'verbeat.version');
        
        if (fs.existsSync(versionFile)) {
            // Read the version file and get the latest version
            const content = fs.readFileSync(versionFile, 'utf8');
            const lines = content.trim().split('\n');
            
            // Get the latest version number (last line with a number)
            for (let i = lines.length - 1; i >= 0; i--) {
                const line = lines[i].trim();
                if (line && !line.startsWith('#')) {
                    const version = line.split('#')[0].trim();
                    if (version && !isNaN(version)) {
                        return version;
                    }
                }
            }
        }
        
        // Final fallback
        return '1.0.0';
        
    } catch (error) {
        console.error('Error getting VerBeat version:', error.message);
        return '1.0.0';
    }
}

function updatePackageJson(implementationPath) {
    try {
        const packageJsonPath = path.join(implementationPath, 'package.json');
        if (!fs.existsSync(packageJsonPath)) {
            console.log(`No package.json found in ${implementationPath}`);
            return;
        }
        
        const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
        
        const currentVersion = getCurrentVerBeatVersion();
        console.log(`Current VerBeat version: ${currentVersion}`);
        
        // Replace the placeholder
        if (packageJson.version === 'CURRENT_VERSION_PLACEHOLDER') {
            packageJson.version = currentVersion;
            
            // Write back to package.json
            fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2) + '\n');
            console.log(`Updated ${packageJsonPath} version to: ${currentVersion}`);
        } else {
            console.log(`${packageJsonPath} version is not a placeholder: ${packageJson.version}`);
        }
        
    } catch (error) {
        console.error(`Error updating ${implementationPath}/package.json:`, error.message);
    }
}

function updateSetupPy(implementationPath) {
    try {
        const setupPyPath = path.join(implementationPath, 'setup.py');
        if (!fs.existsSync(setupPyPath)) {
            console.log(`No setup.py found in ${implementationPath}`);
            return;
        }
        
        let content = fs.readFileSync(setupPyPath, 'utf8');
        const currentVersion = getCurrentVerBeatVersion();
        
        // Replace the placeholder
        if (content.includes('CURRENT_VERSION_PLACEHOLDER')) {
            content = content.replace(/CURRENT_VERSION_PLACEHOLDER/g, currentVersion);
            fs.writeFileSync(setupPyPath, content);
            console.log(`Updated ${setupPyPath} version to: ${currentVersion}`);
        } else {
            console.log(`${setupPyPath} version is not a placeholder`);
        }
        
    } catch (error) {
        console.error(`Error updating ${implementationPath}/setup.py:`, error.message);
    }
}

function updatePyProjectToml(implementationPath) {
    try {
        const pyProjectPath = path.join(implementationPath, 'pyproject.toml');
        if (!fs.existsSync(pyProjectPath)) {
            console.log(`No pyproject.toml found in ${implementationPath}`);
            return;
        }
        
        let content = fs.readFileSync(pyProjectPath, 'utf8');
        const currentVersion = getCurrentVerBeatVersion();
        
        // Replace the placeholder
        if (content.includes('CURRENT_VERSION_PLACEHOLDER')) {
            content = content.replace(/CURRENT_VERSION_PLACEHOLDER/g, currentVersion);
            fs.writeFileSync(pyProjectPath, content);
            console.log(`Updated ${pyProjectPath} version to: ${currentVersion}`);
        } else {
            console.log(`${pyProjectPath} version is not a placeholder`);
        }
        
    } catch (error) {
        console.error(`Error updating ${implementationPath}/pyproject.toml:`, error.message);
    }
}

function updateImplementation(implementationName) {
    console.log(`\n=== Updating ${implementationName} ===`);
    const implementationPath = path.join(__dirname, '..', implementationName);
    
    if (!fs.existsSync(implementationPath)) {
        console.error(`Implementation path not found: ${implementationPath}`);
        return;
    }
    
    // Update Node.js implementation
    if (implementationName === 'nodejs') {
        updatePackageJson(implementationPath);
    }
    
    // Update Python implementation
    if (implementationName === 'python') {
        updateSetupPy(implementationPath);
        updatePyProjectToml(implementationPath);
    }
}

// Main execution
const implementation = process.argv[2];
if (!implementation) {
    console.error('Usage: node update-version.js <implementation>');
    console.error('Example: node update-version.js nodejs');
    process.exit(1);
}

updateImplementation(implementation);

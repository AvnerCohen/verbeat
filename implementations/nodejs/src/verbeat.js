#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

function getVerBeatVersion() {
    try {
        // Try multiple possible locations for verbeat.version
        const possiblePaths = [
            // Current directory (if running from project root)
            path.join(process.cwd(), 'verbeat.version'),
            // Parent directory (if running from implementations/nodejs)
            path.join(process.cwd(), '../verbeat.version'),
            // Two levels up (if running from implementations/nodejs)
            path.join(process.cwd(), '../../verbeat.version'),
            // Three levels up (if running from implementations/nodejs)
            path.join(process.cwd(), '../../../verbeat.version'),
        ];
        
        for (const versionFile of possiblePaths) {
            if (fs.existsSync(versionFile)) {
                const content = fs.readFileSync(versionFile, 'utf8');
                const lines = content.split('\n');
                
                for (const line of lines) {
                    const trimmedLine = line.trim();
                    if (trimmedLine && !trimmedLine.startsWith('#')) {
                        const versionStr = trimmedLine.split('#')[0].trim();
                        try {
                            const manualVersion = parseInt(versionStr, 10);
                            
                            // Get current date
                            const now = new Date();
                            const year = now.getFullYear().toString().slice(-2);
                            const month = (now.getMonth() + 1).toString().padStart(2, '0');
                            const yymm = `${year}${month}`;
                            
                            // Get commit count (simplified - just return 0 for now)
                            const commitCount = 0;
                            
                            return `${manualVersion}.${yymm}.${commitCount}`;
                        } catch (error) {
                            // Continue to next line
                        }
                    }
                }
            }
        }
        
        // Fallback: try to use the VerBeat class
        const verbeat = new VerBeat();
        return verbeat.getCurrentVersion();
    } catch (error) {
        return '1.0.0';
    }
}

const VERSION = getVerBeatVersion();

class VerBeatError extends Error {
    constructor(message) {
        super(message);
        this.name = 'VerBeatError';
    }
}

class VerBeatVersionFileError extends VerBeatError {
    constructor(message) {
        super(message);
        this.name = 'VerBeatVersionFileError';
    }
}

class VerBeatGitError extends VerBeatError {
    constructor(message) {
        super(message);
        this.name = 'VerBeatGitError';
    }
}

class VerBeat {
    constructor(projectRoot = null) {
        this.projectRoot = projectRoot || process.cwd();
        this.versionFile = path.join(this.projectRoot, 'verbeat.version');
    }

    getCurrentVersion(date = null) {
        const manualVersion = this._getManualVersion();
        const dateObj = date || new Date();
        const commitCount = this._getCommitCountForMonth(dateObj);
        
        const year = dateObj.getFullYear().toString().slice(-2);
        const month = (dateObj.getMonth() + 1).toString().padStart(2, '0');
        
        return `${manualVersion}.${year}${month}.${commitCount}`;
    }

    getVersionComponents(date = null) {
        const manualVersion = this._getManualVersion();
        const dateObj = date || new Date();
        const commitCount = this._getCommitCountForMonth(dateObj);
        
        const year = dateObj.getFullYear().toString().slice(-2);
        const month = (dateObj.getMonth() + 1).toString().padStart(2, '0');
        const yymm = `${year}${month}`;
        
        return [manualVersion, yymm, commitCount];
    }

    bumpManualVersion(comment = '') {
        const currentVersion = this._getManualVersion();
        const newVersion = currentVersion + 1;
        
        let lines = [];
        if (fs.existsSync(this.versionFile)) {
            lines = fs.readFileSync(this.versionFile, 'utf8').split('\n');
        }
        
        const commentLine = comment ? ` # ${comment}` : '';
        lines.push(`${newVersion}${commentLine}`);
        
        try {
            fs.writeFileSync(this.versionFile, lines.join('\n') + '\n');
        } catch (error) {
            throw new VerBeatVersionFileError(`Cannot write to version file: ${error.message}`);
        }
        
        return newVersion;
    }

    getVersionHistory() {
        if (!fs.existsSync(this.versionFile)) {
            return [];
        }
        
        try {
            const content = fs.readFileSync(this.versionFile, 'utf8');
            const lines = content.split('\n');
            
            const history = [];
            for (const line of lines) {
                const trimmedLine = line.trim();
                if (!trimmedLine || trimmedLine.startsWith('#')) {
                    continue;
                }
                
                const parts = trimmedLine.split('#', 2);
                const versionStr = parts[0].trim();
                const comment = parts[1] ? parts[1].trim() : '';
                
                try {
                    const versionNum = parseInt(versionStr, 10);
                    history.push([versionNum, comment]);
                } catch (error) {
                    throw new VerBeatVersionFileError(`Invalid version number: ${versionStr}`);
                }
            }
            
            return history.sort((a, b) => a[0] - b[0]);
        } catch (error) {
            if (error instanceof VerBeatVersionFileError) {
                throw error;
            }
            throw new VerBeatVersionFileError(`Cannot read version file: ${error.message}`);
        }
    }

    _getManualVersion() {
        if (!fs.existsSync(this.versionFile)) {
            throw new VerBeatVersionFileError(
                `Version file not found: ${this.versionFile}. ` +
                'Create a verbeat.version file with at least one version number.'
            );
        }
        
        const history = this.getVersionHistory();
        if (history.length === 0) {
            throw new VerBeatVersionFileError(
                `No valid versions found in ${this.versionFile}. ` +
                'Add at least one version number (e.g., "1 # Initial release").'
            );
        }
        
        return Math.max(...history.map(([version]) => version));
    }

    _getCommitCountForMonth(date) {
        try {
            const gitDir = path.join(this.projectRoot, '.git');
            if (!fs.existsSync(gitDir)) {
                return 0;
            }
            
            try {
                execSync('git --version', { stdio: 'ignore' });
            } catch (error) {
                return 0;
            }
            
            try {
                const result = execSync('git rev-list --count HEAD', {
                    cwd: this.projectRoot,
                    encoding: 'utf8'
                });
                const totalCommits = parseInt(result.trim(), 10);
                if (totalCommits === 0) {
                    return 0;
                }
            } catch (error) {
                return 0;
            }
            
            const startDate = new Date(date.getFullYear(), date.getMonth(), 1);
            const endDate = new Date(date.getFullYear(), date.getMonth() + 1, 1);
            
            const startStr = startDate.toISOString().split('T')[0];
            const endStr = endDate.toISOString().split('T')[0];
            
            const result = execSync(
                `git rev-list --count --since=${startStr} --until=${endStr} HEAD`,
                {
                    cwd: this.projectRoot,
                    encoding: 'utf8'
                }
            );
            
            return parseInt(result.trim(), 10);
        } catch (error) {
            return 0;
        }
    }
}

function getVersion(projectRoot = null, date = null) {
    const verbeat = new VerBeat(projectRoot);
    return verbeat.getCurrentVersion(date);
}

function bumpVersion(comment = '', projectRoot = null) {
    const verbeat = new VerBeat(projectRoot);
    return verbeat.bumpManualVersion(comment);
}

function getVersionComponents(projectRoot = null, date = null) {
    const verbeat = new VerBeat(projectRoot);
    return verbeat.getVersionComponents(date);
}

export {
    VerBeat,
    VerBeatError,
    VerBeatVersionFileError,
    VerBeatGitError,
    getVersion,
    bumpVersion,
    getVersionComponents,
    VERSION
}; 
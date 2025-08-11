#!/usr/bin/env node

import fs from 'fs';
import path from 'path';
import { execSync } from 'child_process';

function _findProjectRoot() {
    const current = process.cwd();
    const paths = [
        current,
        path.join(current, '..'),
        path.join(current, '..', '..'),
        path.join(current, '..', '..', '..')
    ];

    for (const projectPath of paths) {
        const versionFile = path.join(projectPath, 'verbeat.version');
        if (fs.existsSync(versionFile)) {
            return projectPath;
        }
    }

    return null;
}

function getVersion(projectRoot = null, date = null) {
    const dateObj = date || new Date();
    if (projectRoot) {
        const verbeat = new VerBeat(projectRoot);
        return verbeat.getCurrentVersion(dateObj);
    }

    const projectRootPath = _findProjectRoot();
    if (!projectRootPath) {
        return '1.2508.0';
    }

    const verbeat = new VerBeat(projectRootPath);
    return verbeat.getCurrentVersion(dateObj);
}

function getVersionComponents(projectRoot = null, date = null) {
    const dateObj = date || new Date();
    if (projectRoot) {
        const verbeat = new VerBeat(projectRoot);
        return verbeat.getVersionComponents(dateObj);
    }

    const projectRootPath = _findProjectRoot();
    if (!projectRootPath) {
        return [1, '2508', 0];
    }

    const verbeat = new VerBeat(projectRootPath);
    return verbeat.getVersionComponents(dateObj);
}

function bumpVersion(comment = '', projectRoot = null) {
    if (projectRoot) {
        const verbeat = new VerBeat(projectRoot);
        return verbeat.bumpManualVersion(comment);
    }

    const projectRootPath = _findProjectRoot();
    if (!projectRootPath) {
        throw new VerBeatVersionFileError('No verbeat.version file found');
    }

    const verbeat = new VerBeat(projectRootPath);
    return verbeat.bumpManualVersion(comment);
}

function initProject(comment = 'Initial release', projectRoot = null) {
    const projectPath = projectRoot || process.cwd();
    const versionFile = path.join(projectPath, 'verbeat.version');
    
    if (fs.existsSync(versionFile)) {
        console.log('Already initialized. Use \'verbeat version\' to see current version.');
        return;
    }
    
    try {
        fs.writeFileSync(versionFile, `1 # ${comment}\n`);
        console.log(`Created ${versionFile}`);
        console.log(`VerBeat initialized with version: ${getVersion(projectPath)}`);
        
    } catch (error) {
        throw new VerBeatError(`Failed to initialize project: ${error.message}`);
    }
}

function getCalculatedVersion(projectRoot = null, date = new Date()) {
    const verbeat = new VerBeat(projectRoot);
    return verbeat.getCalculatedVersion(date);
}

function getCurrentVersion(projectRoot = null, date = new Date(), useCalculated = false) {
    const verbeat = new VerBeat(projectRoot);
    return verbeat.getCurrentVersion(date, useCalculated);
}

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

class VerBeatBranchError extends VerBeatError {
    constructor(message) {
        super(message);
        this.name = 'VerBeatBranchError';
    }
}

class VerBeat {
    constructor(projectRoot = null) {
        this.projectRoot = projectRoot || process.cwd();
        this.versionFile = path.join(this.projectRoot, 'verbeat.version');
    }

    _getLatestTagVersion() {
        try {
            const gitDir = path.join(this.projectRoot, '.git');
            if (!fs.existsSync(gitDir)) {
                return null;
            }

            try {
                execSync('git --version', { stdio: 'ignore' });
            } catch (error) {
                return null;
            }

            const result = execSync(
                'git tag --list "v*" --sort=-version:refname',
                { cwd: this.projectRoot, encoding: 'utf8' }
            );

            const tags = result.trim().split('\n');
            if (!tags || tags[0] === '') {
                return null;
            }

            return tags[0];

        } catch (error) {
            return null;
        }
    }

    _createVersionTag(version, comment = '') {
        try {
            const gitDir = path.join(this.projectRoot, '.git');
            if (!fs.existsSync(gitDir)) {
                return false;
            }

            try {
                execSync('git --version', { stdio: 'ignore' });
            } catch (error) {
                return false;
            }

            const date = new Date();
            const dateStr = date.toISOString().split('T')[0];
            let tagMessage = `VerBeat ${version} (${dateStr})`;
            if (comment) {
                tagMessage += `: ${comment}`;
            }

            execSync(
                `git tag -a "v${version}" -m "${tagMessage}"`,
                { cwd: this.projectRoot }
            );

            return true;

        } catch (error) {
            return false;
        }
    }

    getCalculatedVersion(date = new Date()) {
        const manualVersion = this._getManualVersion();
        const commitCount = this._getCommitCountForMonth(date);
        const year = date.getFullYear().toString().slice(-2);
        const month = date.getMonth() + 1;
        const monthStr = month.toString().padStart(2, '0');
        
        return `${manualVersion}.${year}${monthStr}.${commitCount}`;
    }

    getCurrentVersion(date = new Date(), useCalculated = false) {
        if (useCalculated) {
            return this.getCalculatedVersion(date);
        }
        
        const latestTag = this._getLatestTagVersion();
        if (latestTag) {
            return latestTag.substring(1);
        }
        
        return this.getCalculatedVersion(date);
    }

    getVersionComponents(date = null) {
        const latestTag = this._getLatestTagVersion();
        if (latestTag) {
            const versionStr = latestTag.substring(1);
            const parts = versionStr.split('.');
            if (parts.length === 3) {
                try {
                    const manualVersion = parseInt(parts[0]);
                    const yymm = parts[1];
                    const commitCount = parseInt(parts[2]);
                    return [manualVersion, yymm, commitCount];
                } catch (error) {
                }
            }
        }

        const manualVersion = this._getManualVersion();
        const dateObj = date || new Date();
        const commitCount = this._getCommitCountForMonth(dateObj);

        const year = dateObj.getFullYear().toString().slice(-2);
        const month = (dateObj.getMonth() + 1).toString().padStart(2, '0');
        const yymm = `${year}${month}`;

        return [manualVersion, yymm, commitCount];
    }

    _getCurrentBranch() {
        try {
            const gitDir = path.join(this.projectRoot, '.git');
            if (!fs.existsSync(gitDir)) {
                return '';
            }
            
            try {
                execSync('git --version', { stdio: 'ignore' });
            } catch (error) {
                return '';
            }
            
            const result = execSync('git rev-parse --abbrev-ref HEAD', {
                cwd: this.projectRoot,
                encoding: 'utf8'
            });
            return result.trim();
            
        } catch (error) {
            return '';
        }
    }

    _getMainBranchName() {
        const mainBranch = process.env.VERBEAT_MAIN_BRANCH;
        if (mainBranch) {
            return mainBranch;
        }

        try {
            execSync('git --version', { stdio: 'ignore' });
        } catch (error) {
            return 'main';
        }

        const gitDir = path.join(this.projectRoot, '.git');
        if (!fs.existsSync(gitDir)) {
            return 'main';
        }

        try {
            const result = execSync('git show-ref --verify --quiet refs/heads/main', {
                cwd: this.projectRoot,
                stdio: 'ignore'
            });
            return 'main';
        } catch (error) {
            try {
                execSync('git show-ref --verify --quiet refs/heads/master', {
                    cwd: this.projectRoot,
                    stdio: 'ignore'
                });
                return 'master';
            } catch (error) {
                return 'main';
            }
        }
    }

    bumpManualVersion(comment = '') {
        const currentBranch = this._getCurrentBranch();
        const mainBranch = this._getMainBranchName();
        
        if (currentBranch && currentBranch !== mainBranch) {
            throw new VerBeatBranchError(
                `Version bump is only allowed on the main branch (${mainBranch}). ` +
                `Current branch: ${currentBranch}. ` +
                'Set VERBEAT_MAIN_BRANCH environment variable to override the ' +
                'main branch name.'
            );
        }

        const currentVersion = this._getManualVersion();
        const newVersion = currentVersion + 1;

        let lines = [];
        if (fs.existsSync(this.versionFile)) {
            const content = fs.readFileSync(this.versionFile, 'utf8');
            lines = content.split('\n').filter(line => line.trim() !== '');
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

// Get current VerBeat version for package.json
const VERSION = getVersion();

export {
    VerBeat,
    VerBeatError,
    VerBeatVersionFileError,
    VerBeatGitError,
    VerBeatBranchError,
    getVersion,
    bumpVersion,
    getVersionComponents,
    initProject,
    VERSION,
    getCalculatedVersion,
    getCurrentVersion
}; 
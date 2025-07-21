#!/usr/bin/env node

import { getVersion, bumpVersion, getVersionComponents, initProject } from '../src/verbeat.js';

function main() {
    const args = process.argv.slice(2);
    
    if (args.length === 0) {
        console.log('Usage: verbeat <command> [options]');
        console.log('');
        console.log('Commands:');
        console.log('  version                    - Get current version');
        console.log('  bump [comment]             - Bump manual version');
        console.log('  components                 - Get version components');
        console.log('  init [comment]             - Initialize new VerBeat project');
        console.log('');
        console.log('Examples:');
        console.log('  verbeat version');
        console.log('  verbeat bump "New feature"');
        console.log('  verbeat components');
        console.log('  verbeat init "Project kickoff"');
        process.exit(1);
    }
    
    const command = args[0];
    
    try {
        switch (command) {
            case 'version':
                const version = getVersion();
                console.log(version);
                break;
                
            case 'bump':
                const comment = args.slice(1).join(' ');
                const newVersion = bumpVersion(comment);
                console.log(newVersion);
                break;
                
            case 'components':
                const [manual, yymm, commits] = getVersionComponents();
                console.log(`Manual: ${manual}`);
                console.log(`Date: ${yymm}`);
                console.log(`Commits: ${commits}`);
                break;
                
            case 'init':
                const initComment = args.slice(1).join(' ');
                initProject(initComment);
                break;
                
            default:
                console.error(`Unknown command: ${command}`);
                process.exit(1);
        }
    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}

if (import.meta.url === `file://${process.argv[1]}`) {
    main();
} 
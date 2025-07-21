# VerBeat Node.js Implementation

A Node.js implementation of VerBeat - A 3D Versioning System for Real-World Dev Flow.

## Installation

```bash
npm install
```

## Usage

### As a Library

```javascript
const { getVersion, bumpVersion, getVersionComponents } = require('./src/verbeat.js');

// Get current version
const version = getVersion();
console.log(version); // e.g., "1.2507.14"

// Get version components
const [manual, yymm, commits] = getVersionComponents();
console.log(`Manual: ${manual}, Date: ${yymm}, Commits: ${commits}`);

// Bump manual version (only works on main/master branch)
const newVersion = bumpVersion("New feature");
console.log(newVersion); // e.g., 2
```

### As a CLI Tool

```bash
# Get current version
node bin/verbeat.js version

# Bump manual version
node bin/verbeat.js bump "New feature"

# Get version components
node bin/verbeat.js components
```

## Testing

```bash
# Run all tests
make test

# Install dependencies
make install

# Clean up
make clean
```

## API Reference

### `getVersion(projectRoot = null, date = null)`
Returns the current VerBeat version string.

**Parameters:**
- `projectRoot` (string, optional): Path to project root (defaults to current directory)
- `date` (Date, optional): Date to use for version calculation (defaults to current date)

**Returns:** Version string in format `M.YYMM.C`

### `getVersionComponents(projectRoot = null, date = null)`
Returns the individual components of the version.

**Returns:** Array `[manual_version, yymm, commit_count]`

### `bumpVersion(comment = '', projectRoot = null)`
Bumps the manual version and adds a comment to the version file. **Only works on the main branch.**

**Parameters:**
- `comment` (string, optional): Comment describing the version bump
- `projectRoot` (string, optional): Path to project root (defaults to current directory)

**Returns:** The new manual version number

**Throws:** `VerBeatBranchError` if not on the main branch

## Branch Protection

VerBeat enforces that version bumps can only occur on the main branch:

- **Automatic detection**: VerBeat automatically detects whether your repository uses `main` or `master` as the primary branch
- **Environment override**: Set `VERBEAT_MAIN_BRANCH` environment variable to override the detected main branch name
- **Clear error messages**: Attempting to bump versions on feature branches provides clear guidance

```javascript
const { bumpVersion, VerBeatBranchError } = require('./src/verbeat.js');

try {
    const newVersion = bumpVersion("New feature");
    console.log(`Bumped to version ${newVersion}`);
} catch (error) {
    if (error instanceof VerBeatBranchError) {
        console.log(`Branch error: ${error.message}`);
        // Output: Branch error: Version bump is only allowed on the main branch (main). Current branch: feature-branch
    }
}
```

## Error Handling

The implementation gracefully handles edge cases:

- **Outside Git repository** → Returns 0 for commit count
- **Empty Git repository** → Returns 0 for commit count
- **Git not installed** → Returns 0 for commit count
- **Git command failures** → Returns 0 for commit count
- **Missing version file** → Clear error message with instructions
- **Invalid version file** → Detailed error reporting

## Version File Format

Create a `verbeat.version` file in your project root:

```
1 # Initial release
2 # Breaking API changes
3 # New feature
```

Each line contains a version number followed by an optional comment starting with `#`. 
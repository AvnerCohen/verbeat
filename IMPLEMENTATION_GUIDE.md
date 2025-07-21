# VerBeat Implementation Guide

This guide provides the specifications for implementing VerBeat in any programming language. Each implementation should provide a consistent API and integrate seamlessly with the VerBeat ecosystem.

## Core Requirements

### 1. Version File Management

**File**: `verbeat.version` (in project root)

**Format**: Simple text file with one version per line:
```
1 # Initial release
2 # Breaking API changes
3 # New feature
```

**Rules**:
- Each line contains a version number followed by an optional comment
- Comments start with `#` and are separated by at least one space
- Version numbers must be positive integers
- The highest version number is the current manual version
- Empty lines and lines starting with `#` are ignored

### 2. Core API Functions

Every implementation must provide these core functions:

#### `get_current_version(project_root: str = None, date: datetime = None) -> str`
Returns the complete VerBeat version string in format `M.YYMM.C` (SemVer compliant)

**Parameters**:
- `project_root`: Path to project root (defaults to current directory)
- `date`: Date to use for version calculation (defaults to current date)

**Returns**: Version string like `"2.2507.14"`

**Example**:
```python
version = get_current_version()  # "2.2507.14"
version = get_current_version("/path/to/project", datetime(2025, 7, 15))  # "2.2507.0"
```

#### `get_version_components(project_root: str = None, date: datetime = None) -> tuple`
Returns the individual components of the version.

**Returns**: Tuple of `(manual_version, yymm, commit_count)`

**Example**:
```python
manual, yymm, commits = get_version_components()  # (2, "2507", 14)
```

#### `bump_manual_version(comment: str = "", project_root: str = None) -> int`
Bumps the manual version and adds a comment to the version file. **Only works on the main branch.**

**Parameters**:
- `comment`: Optional comment describing the version bump
- `project_root`: Path to project root (defaults to current directory)

**Returns**: The new manual version number

**Raises**: `VerBeatBranchError` if not on the main branch

**Example**:
```python
new_version = bump_manual_version("Breaking API changes")  # 3
```

### 3. Git Integration

**Commit Counting**:
- Count commits for the current month (from 1st day to last day)
- Use Git's `rev-list --count --since=YYYY-MM-DD --until=YYYY-MM-DD HEAD`
- Handle edge cases gracefully:
  - No Git repository → return 0
  - Git not installed → return 0
  - No commits in repository → return 0
  - No commits in current month → return 0

**Branch Detection**:
- Detect current branch using `git rev-parse --abbrev-ref HEAD`
- Detect main branch by checking for `main` first, then `master`
- Support environment variable override: `VERBEAT_MAIN_BRANCH`
- Only allow version bumps on the main branch

**Error Handling**:
- Never crash on Git-related errors
- Return 0 for commit count when Git operations fail
- Provide informative error messages for debugging
- Raise `VerBeatBranchError` for non-main branch version bumps

### 4. Git Tag Integration

**Tag-Based Versioning**:
- Versions are stored as Git tags in the format `v{M}.{YYMM}.{C}`
- **Example**: `v2.2507.14`
- **Tag Message**: `VerBeat 2.2507.14 (2025-07-15): feat: add branch restriction`

**Version Resolution Priority**:
1. **Primary**: Read version from latest Git tag (if available)
2. **Fallback**: Calculate from `verbeat.version` file + current state

**Required Methods**:

#### `_get_latest_tag_version() -> Optional[str]`
Returns the latest VerBeat tag version.

- **Returns**: Latest tag (e.g., "v2.2507.14") or `null`/`None` if no tags found
- **Behavior**:
  - Lists tags matching pattern `v*`
  - Sorts by version (newest first)
  - Returns the first (latest) tag
  - Handles Git errors gracefully

#### `_create_version_tag(version: str, comment: str = "") -> bool`
Creates a Git tag for the given version.

- **Parameters**:
  - `version`: Version string (e.g., "2.2507.14")
  - `comment`: Optional comment for the tag message
- **Returns**: `true` if tag created successfully, `false` otherwise
- **Behavior**:
  - Creates annotated tag with format `v{version}`
  - Tag message: `VerBeat {version} ({date}): {comment}`
  - Handles Git errors gracefully
- **Note**: Tag creation is typically handled by CI/CD, not local development

### 5. Error Handling

Implement these exception types:

#### `VerBeatError` (base exception)
Base exception for all VerBeat operations.

#### `VerBeatVersionFileError`
Raised when there are issues with the `verbeat.version` file:
- File not found
- Invalid format
- No valid versions

#### `VerBeatGitError`
Raised when Git operations fail (though commit counting should return 0 instead of raising).

#### `VerBeatBranchError`
Raised when version bump is attempted on a non-main branch.

### 6. CLI Interface

Provide a command-line interface with these commands:

#### `verbeat init [comment]`
Initialize a new VerBeat project by creating the `verbeat.version` file.

**Parameters**:
- `comment`: Optional comment for the initial version (defaults to "Initial release")

**Example**:
```bash
$ verbeat init "Project kickoff"
Created verbeat.version
VerBeat initialized with version: 1.2507.0
```

#### `verbeat version`
Display the current version.

#### `verbeat bump [comment]`
Bump the manual version with an optional comment. **Only works on the main branch.**

#### `verbeat components`
Display the individual version components.

**Example**:
```bash
$ verbeat version
2.2507.14

$ verbeat bump "New feature"
3

$ verbeat components
Manual: 3
Date: 2507
Commits: 14
```

### 7. Package Manager Integration

Implementations should support package manager execution patterns:

#### Python
- **uvx**: `uvx verbeat [command]`
- **pipx**: `pipx run verbeat [command]`
- **pip**: `python -m verbeat [command]`

#### Node.js
- **npx**: `npx verbeat [command]`
- **npm**: `npm exec verbeat [command]`
- **yarn**: `yarn verbeat [command]`

#### Other Languages
- Follow language-specific package manager conventions
- Ensure zero-install execution is possible
- Provide both global and local installation options

### 8. Testing Requirements

Every implementation must include comprehensive tests using **standard testing frameworks**:

#### Unit Tests
- Version file parsing
- Manual version bumping
- Date-specific version calculation
- Error handling for missing/invalid files
- Git integration edge cases

#### Integration Tests
- End-to-end workflow testing
- CLI command testing
- Real Git repository testing

#### Testing Framework Requirements

**Python Implementations**:
- Use **pytest** as the testing framework
- Test files should be in `tests/` directory
- Use `assert` statements for assertions
- Use `pytest.raises()` for exception testing
- Example Makefile target:
```makefile
test:
	@echo "Running VerBeat Python implementation tests..."
	@uv run pytest tests/ -v
```

**Node.js Implementations**:
- Use **Node.js built-in test runner** (`node --test`)
- Test files should be in `tests/` directory
- Use `assert` module for assertions (`assert.strictEqual()`, `assert.deepStrictEqual()`, `assert.throws()`)
- Support ES modules out of the box
- Example Makefile target:
```makefile
test:
	@echo "Running VerBeat Node.js implementation tests..."
	@yarn test
```

**Other Languages**:
- Use the **most popular, standard testing framework** for the language
- Follow language-specific testing conventions
- Ensure tests are discoverable and runnable via `make test`

#### Test Command
Implement a `make test` target that runs all tests using the standard framework:

```makefile
test:
	@echo "Running VerBeat tests..."
	@[standard framework command]
```

### 9. Documentation

Each implementation must include:

#### README.md
- Installation instructions
- Basic usage examples
- API documentation
- CLI reference
- Contributing guidelines

#### API Documentation
- Complete function signatures
- Parameter descriptions
- Return value descriptions
- Example usage
- Error handling

### 10. UI Integration Points

For web-based implementations or those with UI components:

#### Version Display
- Large, prominent version display
- Real-time updates
- Responsive design

#### Interactive Controls
- Manual version input
- Date picker
- Commit counter with increment button
- Real-time version calculation

#### Demo Interface
- Interactive version calculator
- Visual representation of version components
- Educational examples

### 11. File Structure

Recommended structure for each implementation:

```
implementations/[language]/
├── README.md
├── Makefile (or equivalent)
├── [language-specific config files]
├── src/
│   └── verbeat.[ext]
├── tests/
│   └── test_verbeat.[ext]
├── examples/
│   └── basic_usage.[ext]
└── docs/
    └── api.md
```

### 12. Quality Standards

#### Code Quality
- Follow language-specific best practices
- Include comprehensive error handling
- Provide clear, readable code
- Include appropriate comments

#### Performance
- Efficient file I/O operations
- Minimal Git command execution
- Fast version calculation

#### Security
- Safe file operations
- Input validation
- Path traversal protection

#### Compatibility
- Support multiple platforms
- Handle different Git configurations
- Graceful degradation for missing dependencies

### 13. CI/CD Integration

Each implementation should include:

#### GitHub Actions Workflow
- Automated testing on multiple platforms
- Code quality checks
- Documentation generation
- Release automation

#### Example Workflow Structure
```yaml
name: Test VerBeat [Language]

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
    
    steps:
    - uses: actions/checkout@v3
    - name: Setup [Language]
      # Language-specific setup
    - name: Run tests
      run: make test
```

### 14. Version Compatibility

All implementations should:
- Support the same version file format
- Produce identical version strings for the same inputs
- Handle edge cases consistently
- Maintain backward compatibility

### 15. Contributing Guidelines

Each implementation should include:
- Code of conduct
- Contributing guidelines
- Issue templates
- Pull request templates
- Development setup instructions

## Implementation Checklist

- [ ] Core API functions implemented
- [ ] Version file parsing and writing
- [ ] Git integration with error handling
- [ ] Git tag integration (version resolution)
- [ ] CLI interface (including `init` command)
- [ ] Package manager integration (uvx/npx patterns)
- [ ] Comprehensive test suite (using standard framework)
- [ ] Documentation (README, API docs)
- [ ] Makefile with test target
- [ ] CI/CD pipeline
- [ ] Error handling and edge cases
- [ ] Code quality and linting
- [ ] Examples and demos
- [ ] Cross-platform compatibility

## Getting Started

1. Choose your target language
2. Create the implementation directory structure
3. Implement the core API functions
4. Add Git integration
5. Create CLI interface
6. Write comprehensive tests (using standard framework)
7. Add documentation
8. Set up CI/CD
9. Create examples and demos
10. Submit for review

## Support

For questions about implementing VerBeat in a new language:
- Check existing implementations for reference
- Review the test suite for expected behavior
- Open an issue for clarification
- Submit a pull request for review 
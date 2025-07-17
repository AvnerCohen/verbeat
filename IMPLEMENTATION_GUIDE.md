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
Returns the complete VerBeat version string in format `M.YYMM.C`

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
Bumps the manual version and adds a comment to the version file.

**Parameters**:
- `comment`: Optional comment describing the version bump
- `project_root`: Path to project root (defaults to current directory)

**Returns**: The new manual version number

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

**Error Handling**:
- Never crash on Git-related errors
- Return 0 for commit count when Git operations fail
- Provide informative error messages for debugging

### 4. Error Handling

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

### 5. CLI Interface

Provide a command-line interface with these commands:

#### `verbeat version`
Display the current version.

#### `verbeat bump [comment]`
Bump the manual version with an optional comment.

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

### 6. Testing Requirements

Every implementation must include:

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

#### Test Command
Implement a `make test` target that runs all tests:

```makefile
test:
	@echo "Running VerBeat tests..."
	@[language-specific test command]
```

### 7. Documentation

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

### 8. UI Integration Points

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

### 9. File Structure

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

### 10. Quality Standards

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

### 11. CI/CD Integration

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

### 12. Version Compatibility

All implementations should:
- Support the same version file format
- Produce identical version strings for the same inputs
- Handle edge cases consistently
- Maintain backward compatibility

### 13. Contributing Guidelines

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
- [ ] CLI interface
- [ ] Comprehensive test suite
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
6. Write comprehensive tests
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
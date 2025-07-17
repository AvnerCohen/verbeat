# VerBeat Python Implementation

A simple and efficient Python library for managing VerBeat versions.

## Installation

Copy `verbeat.py` to your project or install it as a module.

## Quick Start

### 1. Create a version file

Create a `verbeat.version` file in your project root:

```
1 # Initial release
2 # Breaking API changes
```

### 2. Use the library

```python
from verbeat import VerBeat, get_version, bump_version

# Get current version
version = get_version()
print(version)  # e.g., "2.2507.14"

# Bump manual version
new_version = bump_version("New feature release")
print(new_version)  # 3

# Get version components
from verbeat import get_version_components
manual, yymm, commits = get_version_components()
print(f"Manual: {manual}, Date: {yymm}, Commits: {commits}")
```

## API Reference

### VerBeat Class

The main class for version management.

#### `__init__(project_root=None)`

Initialize VerBeat for a project.

- **project_root**: Path to project root (defaults to current directory)

#### `get_current_version(date=None)`

Get the current VerBeat version string.

- **date**: Date to use for version calculation (defaults to current date)
- **Returns**: VerBeat version string in format `M.YYMM.C`

#### `get_version_components(date=None)`

Get the individual components of the current version.

- **date**: Date to use for version calculation (defaults to current date)
- **Returns**: Tuple of `(manual_version, yymm, commit_count)`

#### `bump_manual_version(comment="")`

Bump the manual version and add a comment.

- **comment**: Comment describing the version bump
- **Returns**: The new manual version number

#### `get_version_history()`

Get the history of manual versions and their comments.

- **Returns**: List of tuples `(version_number, comment)`

### Convenience Functions

#### `get_version(project_root=None, date=None)`

Get current VerBeat version.

#### `bump_version(comment="", project_root=None)`

Bump manual version.

#### `get_version_components(project_root=None, date=None)`

Get version components.

## Command Line Usage

The module can also be used as a command-line tool:

```bash
# Get current version
python verbeat.py version

# Bump manual version
python verbeat.py bump "New feature release"

# Get version components
python verbeat.py components

# Show version history
python verbeat.py history
```

## Error Handling

The library provides specific exceptions for different error conditions:

- `VerBeatError`: Base exception for all VerBeat operations
- `VerBeatVersionFileError`: Issues with the verbeat.version file
- `VerBeatGitError`: Issues with Git operations

```python
from verbeat import VerBeat, VerBeatError

try:
    version = get_version()
    print(version)
except VerBeatError as e:
    print(f"Error: {e}")
```

## Requirements

- Python 3.6+
- Git (optional, for commit counting)

## Examples

### Basic Usage

```python
from verbeat import VerBeat

verbeat = VerBeat()

# Get current version
version = verbeat.get_current_version()
print(f"Current version: {version}")

# Get components
manual, yymm, commits = verbeat.get_version_components()
print(f"Manual version: {manual}")
print(f"Date: {yymm}")
print(f"Commits this month: {commits}")
```

### Version Bumping

```python
from verbeat import bump_version

# Bump version with comment
new_version = bump_version("Major API changes")
print(f"Bumped to version {new_version}")

# Bump without comment
new_version = bump_version()
print(f"Bumped to version {new_version}")
```

### Working with Dates

```python
from datetime import datetime
from verbeat import get_version

# Get version for a specific date
date = datetime(2025, 7, 15)
version = get_version(date=date)
print(f"Version for {date.date()}: {version}")
```

### Version History

```python
from verbeat import VerBeat

verbeat = VerBeat()
history = verbeat.get_version_history()

print("Version History:")
for version, comment in history:
    print(f"  {version}: {comment}")
```

## Integration Examples

### With CI/CD

```python
# In your CI script
from verbeat import get_version

version = get_version()
print(f"Building version {version}")

# Use version in build process
build_command = f"docker build -t myapp:{version} ."
```

### With Setup Tools

```python
# In setup.py
from verbeat import get_version

setup(
    name="myapp",
    version=get_version(),
    # ... other setup parameters
)
```

### With Flask/FastAPI

```python
from flask import Flask
from verbeat import get_version

app = Flask(__name__)

@app.route('/version')
def version():
    return {'version': get_version()}
```

## File Format

The `verbeat.version` file uses a simple format:

```
1 # Initial release
2 # Breaking API changes
3 # New feature set
```

- One version per line
- Version number followed by optional comment (separated by `#`)
- Comments are stripped of leading/trailing whitespace
- Empty lines and lines starting with `#` are ignored
- The highest version number is used as the current manual version

## Git Integration

The library automatically detects Git repositories and counts commits for the current month. If Git is not available or the project is not a Git repository, the commit count defaults to 0.

The commit counting uses `git rev-list --count` with date filtering to get accurate monthly commit counts. 
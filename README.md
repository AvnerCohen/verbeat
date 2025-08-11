<img src="verbeat_logo.png" alt="VerBeat Logo" width="64" height="64" />

# VerBeat

**Manual Intent. Calendar Context. Commit Tempo.**

VerBeat is a 3D versioning system that combines manual semantic milestones with automated time-based and activity-driven versioning. It bridges the gap between traditional semantic versioning and calendar-based approaches, providing a practical solution for modern development workflows.

👉 **Explore the [VerBeat website and live demo](https://avnercohen.github.io/verbeat/)**

![npm version](https://img.shields.io/npm/v/verbeat?label=VerBeat&color=blue)

---

VerBeat uses a unique version format: **M.YYMM.C**
- **M**: Manual milestone (semantic bump)
- **YYMM**: Year and month (calendar context)
- **C**: Commit count for the current month (activity)

> Example: `2.2507.14` = Manual version 2, July 2025, 14 commits this month

---

## Why VerBeat?

Existing versioning systems have fundamental limitations that waste time and provide inadequate information:

**📅 [Calendar Versioning (CalVer)](https://calver.org/)**
- **Pros:** Automatic, no version decisions needed, clear time context
- **Problem:** All versions are equal - a version only tells you "when" it was released, not "what" changed or "how significant" it is. You lose semantic meaning entirely.

**🎯 [Semantic Versioning (SemVer)](https://semver.org/)**
- **Pros:** Clear indication of change significance and compatibility
- **Problem:** Requires constant decision-making about what constitutes "breaking" vs "minor" changes. Teams waste time debating version bumps for 90% of releases where the distinction is meaningless. The complexity often leads to version inflation or inconsistent practices.

**VerBeat solves both problems:** You get automatic time-based versioning (like CalVer) while preserving meaningful semantic milestones (like SemVer) - but only when you actually need them. No more version debates for routine releases.

## Quick Start

### Using VerBeat (Recommended)

```bash
# Python with uvx
git init
uvx verbeat init "Project kickoff"
uvx verbeat version
uvx verbeat bump "New feature"
uvx verbeat components

# Node.js with npx
git init
npx verbeat init "Project kickoff"
npx verbeat version
npx verbeat bump "New feature"
npx verbeat components
```

### Development Setup

```bash
# Python Implementation
cd implementations/python

# Initialize a new VerBeat project
git init
python verbeat.py init "Project kickoff"
# Creates verbeat.version with "1 # Project kickoff"

# Get current version
python verbeat.py version
# Output: 1.2507.14

# Bump manual version (only works on main/master branch)
python verbeat.py bump "New feature"
# Output: 2

# Get version components
python verbeat.py components
# Output:
# Manual: 2
# Date: 2507
# Commits: 14
```

### Running Tests

```bash
# Run all tests (basic + Git edge cases)
make test

# Run linting (requires flake8)
make lint

# Format code (requires black)
make format
```

## Version Format

**M.YYMM.C** (SemVer Compliant)

- **M** - Manual version number from `verbeat.version` file (Major version)
- **YYMM** - Two-digit year and month (e.g., 2507 for July 2025) (Minor version)
- **C** - Number of Git commits in the current month (Patch version)

### SemVer Compliance

VerBeat follows Semantic Versioning 2.0.0 specification:
- **Major (M)**: Manual semantic milestones (breaking changes, major features)
- **Minor (YYMM)**: Calendar-based versioning (time context)
- **Patch (C)**: Activity-based versioning (commit count)

### Git Tags

Versions are stored as Git tags in the format `v{M}.{YYMM}.{C}`:
- **Example**: `v2.2507.14`
- **Tag Message**: `VerBeat 2.2507.14 (2025-07-15): feat: add branch restriction`

### Example

With `verbeat.version`:
```
1 # Initial release
2 # Breaking API changes
```

On July 15, 2025, with 14 commits this month:
**2.2507.14** (stored as Git tag `v2.2507.14`)

This tells us: Manual version 2, July 2025, 14 commits this month.

## Problems VerBeat Solves

- **🔄 Manual Versioning Pain** - Eliminates tedious manual version bumps while retaining human judgment for meaningful changes
- **⏰ Time Context** - Provides clear temporal context that semantic versioning lacks
- **📊 Activity Insight** - Commit count reveals development velocity and iteration intensity
- **🤖 CI/CD Friendly** - Automated parts reduce merge conflicts and integrate seamlessly
- **👥 Human Readable** - Clear, intuitive format that's easy to understand and communicate
- **🎯 Semantic Meaning** - Preserves intentional versioning while adding automated context

## When to Use VerBeat

VerBeat is ideal for:
- Internal tools and platforms
- SaaS services with regular releases
- Fast-paced development projects
- API-based services
- Projects where release clarity is more valuable than strict compatibility guarantees

## Usage

### Basic Version Retrieval

```python
from verbeat import get_version, get_calculated_version

# Get current version (prioritizes Git tags)
current = get_version()  # e.g., "2.2507.2"

# Get calculated version (ignores tags, always calculates)
calculated = get_calculated_version()  # e.g., "2.2507.8"
```

```javascript
import { getCurrentVersion, getCalculatedVersion } from 'verbeat';

// Get current version (prioritizes Git tags)
const current = getCurrentVersion();  // e.g., "2.2507.2"

// Get calculated version (ignores tags, always calculates)
const calculated = getCalculatedVersion();  // e.g., "2.2507.8"
```

### When to Use Each Method

- **`get_version()` / `getCurrentVersion()`**: Use for displaying the "official" current version (CLI, website, package metadata)
- **`get_calculated_version()` / `getCalculatedVersion()`**: Use for CI/CD release decisions and development planning

### Package Manager (Recommended)
```bash
# Python
git init
uvx verbeat init "Project kickoff"
uvx verbeat version
uvx verbeat bump "New feature"

# Node.js
git init
npx verbeat init "Project kickoff"
npx verbeat version
npx verbeat bump "New feature"
```

### Quick Reference
| Command | Python | Node.js |
|---------|--------|---------|
| Initialize | `uvx verbeat init "comment"` | `npx verbeat init "comment"` |
| Get version | `uvx verbeat version` | `npx verbeat version` |
| Bump version | `uvx verbeat bump "comment"` | `npx verbeat bump "comment"` |
| Get components | `uvx verbeat components` | `npx verbeat components` |

## Implementations

### Python
- **Location:** `implementations/python/`
- **Features:** Complete library with CLI tools, comprehensive testing, Git integration
- **Testing:** `make test` runs full test suite including Git edge cases
- **CLI:** `python verbeat.py version|bump|components|init`
- **Package:** `uvx verbeat` or `pipx run verbeat`

### Node.js
- **Location:** `implementations/nodejs/`
- **Features:** Complete library with CLI tools, comprehensive testing, Git integration
- **Testing:** `make test` runs full test suite
- **CLI:** `node bin/verbeat.js version|bump|components|init`
- **Package:** `npx verbeat`
- **Install:** `npm install`

### Creating New Implementations

See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for detailed specifications on creating VerBeat implementations in any programming language.

## CI/CD Integration

This project includes comprehensive GitHub Actions workflows that:

- **Test Python implementation** across multiple platforms (Ubuntu, Windows, macOS) and Python versions (3.8-3.12)
- **Validate website functionality** including HTML validation and link checking
- **Run code quality checks** including linting and formatting
- **Deploy website** to GitHub Pages on main branch
- **Manage version updates** - Only CI creates Git tags and updates `current_version.json` for the website

### Local Development

```bash
# Run tests locally
cd implementations/python
make test

# Test CLI interface (for development)
python verbeat.py version
python verbeat.py bump "Test"
python verbeat.py components
python verbeat.py init "Test project"

# Get current project version
python scripts/get_version.py
```

**Note:** Version updates (`current_version.json` and Git tags) are managed automatically by CI. Local development should focus on testing and development, not version management.

## Branch Protection

VerBeat enforces that version bumps can only occur on the main branch:

- **Automatic detection**: VerBeat automatically detects whether your repository uses `main` or `master` as the primary branch
- **Environment override**: Set `VERBEAT_MAIN_BRANCH` environment variable to override the detected main branch name
- **Clear error messages**: Attempting to bump versions on feature branches provides clear guidance

```bash
# This will work on main/master branch
verbeat bump "New feature"

# This will fail on feature branches with a clear error message
# Error: Version bump is only allowed on the main branch (main). Current branch: feature-branch

# Override main branch name
VERBEAT_MAIN_BRANCH=develop verbeat bump "New feature"
```

## Error Handling

The Python implementation gracefully handles edge cases:

- **Outside Git repository** → Returns 0 for commit count
- **Empty Git repository** → Returns 0 for commit count  
- **Git not installed** → Returns 0 for commit count
- **Git command failures** → Returns 0 for commit count
- **Missing version file** → Clear error message with instructions
- **Invalid version file** → Detailed error reporting
- **Non-main branch version bump** → Clear error with branch information

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the full test suite: `make test`
6. Submit a pull request

### For New Language Implementations

1. Follow the [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
2. Create implementation in `implementations/[language]/`
3. Include comprehensive tests
4. Add CI/CD workflow for the new language
5. Update this README with implementation details

## License

MIT License - see LICENSE file for details.

## Logo

VerBeat Bot - A Robot DJ with 3 knobs representing the 3D versioning concept. See [logo_prompt.md](logo_prompt.md) for detailed specifications. # Test change for GitHub Actions

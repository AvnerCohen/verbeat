# VerBeat - A 3D Versioning System for Real-World Dev Flow

VerBeat combines manual semantic milestones with automated time-based and activity-driven versioning in the format **M.YYMM.C**:

- **M** - Manual version bump (semantic milestone)
- **YYMM** - Year and month (calendar context)
- **C** - Commit count for the current month (activity tempo)

## Why VerBeat?

Existing versioning systems have fundamental limitations that waste time and provide inadequate information:

**📅 Calendar Versioning (CalVer)**
- **Pros:** Automatic, no version decisions needed, clear time context
- **Problem:** All versions are equal - a version only tells you "when" it was released, not "what" changed or "how significant" it is. You lose semantic meaning entirely.

**🎯 Semantic Versioning (SemVer)**
- **Pros:** Clear indication of change significance and compatibility
- **Problem:** Requires constant decision-making about what constitutes "breaking" vs "minor" changes. Teams waste time debating version bumps for 90% of releases where the distinction is meaningless. The complexity often leads to version inflation or inconsistent practices.

**VerBeat solves both problems:** You get automatic time-based versioning (like CalVer) while preserving meaningful semantic milestones (like SemVer) - but only when you actually need them. No more version debates for routine releases.

## Quick Start

### Python Implementation

```bash
# Install (no dependencies required)
cd implementations/python

# Create a version file
echo "1 # Initial release" > verbeat.version

# Get current version
python verbeat.py version
# Output: 1.2507.14

# Bump manual version
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
# Run all tests
make test

# Run Git edge case tests only
make test-git

# Run linting (requires flake8)
make lint

# Format code (requires black)
make format
```

## Version Format

**M.YYMM.C**

- **M** - Manual version number from `verbeat.version` file
- **YYMM** - Two-digit year and month (e.g., 2507 for July 2025)
- **C** - Number of Git commits in the current month

### Example

With `verbeat.version`:
```
1 # Initial release
2 # Breaking API changes
```

On July 15, 2025, with 14 commits this month:
**2.2507.14**

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

## Implementations

### Python
- **Location:** `implementations/python/`
- **Features:** Complete library with CLI tools, comprehensive testing, Git integration
- **Testing:** `make test` runs full test suite including Git edge cases
- **CLI:** `python verbeat.py version|bump|components`

### Creating New Implementations

See [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) for detailed specifications on creating VerBeat implementations in any programming language.

## CI/CD Integration

This project includes comprehensive GitHub Actions workflows that:

- **Test Python implementation** across multiple platforms (Ubuntu, Windows, macOS) and Python versions (3.8-3.12)
- **Validate website functionality** including HTML validation and link checking
- **Run code quality checks** including linting and formatting
- **Perform security scans** using CodeQL analysis
- **Build and package** the project for distribution
- **Deploy website** to GitHub Pages on main branch

### Local Development

```bash
# Run tests locally
cd implementations/python
make test

# Test CLI interface
python verbeat.py version
python verbeat.py bump "Test"
python verbeat.py components

# Test Git integration
make test-git
```

## Error Handling

The Python implementation gracefully handles edge cases:

- **Outside Git repository** → Returns 0 for commit count
- **Empty Git repository** → Returns 0 for commit count  
- **Git not installed** → Returns 0 for commit count
- **Git command failures** → Returns 0 for commit count
- **Missing version file** → Clear error message with instructions
- **Invalid version file** → Detailed error reporting

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

VerBeat Bot - A Robot DJ with 3 knobs representing the 3D versioning concept. See [logo_prompt.md](logo_prompt.md) for detailed specifications. 
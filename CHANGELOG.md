# Changelog

All notable changes to the VerBeat project will be documented in this file.

## [Unreleased] - 2025-01-XX

### Added
- **Git Tag-Based Versioning** - Versions now stored as Git tags with automatic resolution
- **CLI Init Command** - `verbeat init` command for project setup
- **Branch Protection** - Version bumps restricted to main/master branches only
- **CI-Only Version Management** - Version updates handled automatically in CI/CD
- **Package Manager Support** - `uvx` and `npx` integration for easy usage
- **Comprehensive CI/CD Pipeline** - GitHub Actions workflows for testing across multiple platforms and Python versions
- **Implementation Guide** - Detailed specifications for creating VerBeat implementations in any programming language
- **Enhanced Testing** - Git edge case tests and comprehensive test suite
- **CLI Interface** - Full command-line interface for Python implementation
- **Makefile Support** - Standardized build and test commands
- **Error Handling** - Robust handling of Git edge cases and error conditions
- **Website Demo Testing** - Automated testing of website functionality and demo

### Fixed
- **Title Visibility** - Improved contrast and readability of the VerBeat title
- **Demo Functionality** - Fixed demo initialization and version display
- **Git Integration** - Graceful handling of edge cases:
  - Outside Git repository
  - Empty Git repository
  - Git not installed
  - Git command failures
- **Error Messages** - Clear, informative error messages for all failure scenarios

### Changed
- **Version Management** - Moved from local git hooks to CI-only version updates
- **Website UI** - Improved color contrast and fixed footer positioning
- **Playbook Structure** - Streamlined to focus on actual workflow steps
- **Documentation** - Updated to prioritize `uvx`/`npx` usage and CI-based approach
- **Python Implementation** - Enhanced with better error handling and CLI interface
- **Testing Strategy** - Comprehensive test coverage including edge cases
- **Project Structure** - Better organization with implementation guide and CI/CD

### Technical Improvements
- **Git Tag Integration**: Version resolution now prioritizes Git tags over local calculation
- **Branch Protection**: Automatic main branch detection with environment variable override
- **CLI Enhancements**: Added `init` command and improved error messages
- **Git Edge Cases**: All Git-related operations now return 0 for commit count instead of crashing
- **Test Coverage**: Comprehensive tests for all functionality including error conditions
- **CI/CD**: Multi-platform testing, linting, security scanning, and automated deployment
- **Documentation**: Implementation guide for creating new language implementations

## [Initial Release] - 2025-01-XX

### Added
- **Core VerBeat System** - 3D versioning system combining manual, calendar, and commit-based versioning
- **Python Implementation** - Complete library with basic functionality
- **Website** - Landing page with interactive demo
- **Basic Documentation** - README and implementation details
- **Version File Format** - Simple text-based version tracking
- **Git Integration** - Basic commit counting functionality

### Features
- Version format: M.YYMM.C (Manual.Calendar.Commit)
- Manual version bumping with comments
- Automatic calendar-based versioning
- Git commit counting per month
- Interactive web demo
- Basic error handling 
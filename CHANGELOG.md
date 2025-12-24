# Changelog

All notable changes to OG USB will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-24

### Added
- Initial release of OG USB tool
- Automatic USB device detection using lsblk
- Intelligent filesystem recommendation based on USB size:
  - ≤32GB: FAT32 (vfat) - maximum compatibility
  - >32GB: exFAT - large file support
- Support for multiple filesystem types:
  - FAT32 (vfat) - universal compatibility
  - exFAT - modern cross-platform with large file support
  - NTFS - Windows optimized
  - ext4 - Linux optimized
- Complete data wiping using dd (zero-fill)
- GPT partition table creation
- Interactive CLI menu system
- Safety features:
  - Explicit confirmation required (type "YES")
  - Device verification before formatting
  - Automatic unmounting of partitions
  - Root privilege checking
- Custom volume label support
- Four-step process with progress feedback:
  1. Wipe device
  2. Create partition
  3. Format partition
  4. Verify operation
- Cross-platform Linux support:
  - Ubuntu/Debian
  - Fedora/RHEL
  - Arch Linux
  - openSUSE
- Comprehensive documentation:
  - README with installation and usage instructions
  - Quick reference guide
  - Filesystem comparison table
  - Troubleshooting section
- Automated installation script (install.sh)
- Python 3 compatibility (uses only standard library)
- Proper error handling and user feedback
- .gitignore for Python artifacts

### Security
- Passed CodeQL security scan with zero alerts
- Explicit user confirmation before destructive operations
- Proper exception handling
- No hardcoded credentials or sensitive data

### Code Quality
- Addressed all code review feedback:
  - Removed unused imports
  - Used Python's time.sleep() instead of subprocess
  - Improved exception handling (no bare except clauses)
  - Fixed exfat package conflicts in documentation

## [Unreleased]

### Potential Future Enhancements
- GUI version using tkinter or PyQt
- Multiple partition support
- Disk speed testing
- Bad block scanning
- macOS support
- Windows support
- Progress bars for long operations
- Configuration file for default preferences
- Logging to file
- Batch mode for multiple USB drives
- Verification with checksums
- Bootable USB creation
- ISO to USB writing
- Encrypted partition support

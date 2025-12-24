# OG USB - USB Formatting & Partitioning Tool

A powerful, user-friendly command-line tool for completely erasing, formatting, and partitioning USB drives with automatic filesystem detection.

## Features

- 🔍 **Automatic USB Detection** - Automatically detects all connected USB storage devices
- 🧠 **Intelligent Filesystem Selection** - Recommends optimal filesystem based on USB size:
  - ≤4GB: FAT32 (maximum compatibility)
  - 4-32GB: FAT32 (good compatibility)
  - >32GB: exFAT (large file support)
- 🗑️ **Secure Data Wiping** - Completely erases existing data before formatting
- 🎯 **Multiple Filesystem Support** - FAT32, exFAT, NTFS, ext4
- ✅ **Safety Confirmations** - Requires explicit confirmation before erasing data
- 📊 **Progress Feedback** - Real-time progress updates during operations
- 🔒 **Verification** - Automatically verifies successful formatting

## Requirements

### System Requirements
- Linux operating system (Ubuntu, Debian, Fedora, etc.)
- Root/sudo access
- Python 3.6 or higher

### System Dependencies

Install the required system tools:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install parted dosfstools exfat-fuse exfatprogs ntfs-3g e2fsprogs
```

**Fedora/RHEL:**
```bash
sudo dnf install parted dosfstools exfatprogs ntfs-3g e2fsprogs
```

**Arch Linux:**
```bash
sudo pacman -S parted dosfstools exfatprogs ntfs-3g e2fsprogs
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/wobbob89/OG-USB.git
cd OG-USB
```

2. Make the script executable:
```bash
chmod +x og_usb.py
```

## Usage

### Basic Usage

Run the tool with sudo privileges:

```bash
sudo python3 og_usb.py
```

### Step-by-Step Process

1. **Launch the tool** - The tool will automatically detect all connected USB devices
2. **Select device** - Choose the USB device you want to format from the list
3. **Choose filesystem** - Select the filesystem type or use auto-detection
4. **Enter label** - Provide a volume label (optional, default: OG_USB)
5. **Confirm** - Type 'YES' to confirm and start the formatting process
6. **Wait** - The tool will:
   - Wipe the device (remove all data)
   - Create a new partition table
   - Format the partition
   - Verify the operation

### Example Session

```
=============================================================
   OG USB - USB Formatting & Partitioning Tool
=============================================================

=== Detected USB Devices ===
1. /dev/sdb - 14.92GB - SanDisk Cruzer

Select device number (or 'q' to quit): 1

=== Select Filesystem Type ===
1. FAT32 (vfat) - Maximum compatibility, <4GB files
2. exFAT - Large file support, modern systems
3. NTFS - Windows optimized
4. ext4 - Linux optimized
5. Auto-detect (Recommended: FAT32)

Select filesystem (1-5) or 'b' to go back: 5

Enter volume label (default: OG_USB): MY_USB

============================================================
⚠️  WARNING: ALL DATA ON THIS DEVICE WILL BE PERMANENTLY ERASED!
============================================================
Device: /dev/sdb - 14.92GB - SanDisk Cruzer
Filesystem: FAT32
Label: MY_USB
============================================================

Type 'YES' to continue or anything else to cancel: YES

[1/4] Wiping device /dev/sdb...
✓ Device wiped successfully

[2/4] Creating partition on /dev/sdb...
✓ Partition created successfully

[3/4] Formatting partition as FAT32...
✓ Formatted successfully as FAT32

[4/4] Verifying /dev/sdb...
✓ Device verification successful

============================================================
✓ USB FORMATTING COMPLETE!
============================================================
Your USB drive is ready to use.
```

## Filesystem Comparison

| Filesystem | Max File Size | Max Volume Size | Compatibility | Best Use Case |
|------------|---------------|-----------------|---------------|---------------|
| **FAT32** | 4GB | 2TB | Excellent (All systems) | Small files, universal compatibility |
| **exFAT** | 16EB | 128PB | Good (Modern systems) | Large files, cross-platform |
| **NTFS** | 16EB | 256TB | Good (Windows/Linux) | Windows-centric usage |
| **ext4** | 16TB | 1EB | Linux only | Linux-only environments |

## Safety Features

- **Root privilege check** - Ensures the tool is run with necessary permissions
- **Explicit confirmation** - Requires typing 'YES' to proceed with formatting
- **Device verification** - Confirms successful formatting before completion
- **Unmounting** - Automatically unmounts partitions before operations

## Troubleshooting

### "No USB devices detected"
- Ensure your USB drive is properly connected
- Try unplugging and re-plugging the USB drive
- Check if the system recognizes the device: `lsblk`

### "Permission denied" errors
- Make sure you're running with sudo: `sudo python3 og_usb.py`

### "Command not found" errors
- Install the missing system dependencies (see Requirements section)

### Formatting fails
- Try unplugging and re-plugging the USB drive
- Check if the device is write-protected
- Try a different USB port

## How It Works

1. **Detection** - Uses `lsblk` to detect USB devices connected via USB transport
2. **Wiping** - Uses `dd` to write zeros to the beginning of the device
3. **Partitioning** - Uses `parted` to create a GPT partition table and partition
4. **Formatting** - Uses appropriate `mkfs.*` tools based on chosen filesystem
5. **Verification** - Uses `lsblk` to confirm the partition and filesystem

## Security Considerations

⚠️ **WARNING**: This tool will permanently erase all data on the selected device. Make sure you:
- Select the correct device
- Have backups of any important data
- Confirm the device path before proceeding

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available for personal and commercial use.

## Author

Created for hassle-free USB drive management.

## Changelog

### Version 1.0.0
- Initial release
- USB device detection
- Multiple filesystem support (FAT32, exFAT, NTFS, ext4)
- Automatic filesystem recommendation
- Secure data wiping
- Interactive CLI menu
- Safety confirmations and verification
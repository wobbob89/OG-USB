# OG USB Quick Reference

## Quick Start
```bash
# 1. Install dependencies
sudo ./install.sh

# 2. Run the tool
sudo python3 og_usb.py
```

## Command Cheat Sheet

### Check Connected USB Devices
```bash
lsblk
```

### Manual Formatting (Advanced Users)
```bash
# Wipe device
sudo dd if=/dev/zero of=/dev/sdX bs=1M count=100

# Create partition table
sudo parted -s /dev/sdX mklabel gpt
sudo parted -s /dev/sdX mkpart primary 0% 100%

# Format as FAT32
sudo mkfs.vfat -F 32 -n LABEL /dev/sdX1

# Format as exFAT
sudo mkfs.exfat -n LABEL /dev/sdX1

# Format as NTFS
sudo mkfs.ntfs -f -L LABEL /dev/sdX1

# Format as ext4
sudo mkfs.ext4 -F -L LABEL /dev/sdX1
```

## Filesystem Selection Guide

### Choose FAT32 if:
- USB size ≤ 32GB
- Need maximum compatibility
- Files are all < 4GB
- Using with older devices (cameras, game consoles, etc.)

### Choose exFAT if:
- USB size > 32GB
- Need to store files > 4GB
- Using with modern systems (Windows 7+, macOS 10.6.5+, Linux)
- Cross-platform use

### Choose NTFS if:
- Primarily using with Windows
- Need advanced features (permissions, encryption)
- Files > 4GB

### Choose ext4 if:
- Only using with Linux
- Need best performance on Linux
- Using with Linux-based embedded systems

## Troubleshooting Quick Fixes

### Device not detected
```bash
# Refresh USB
sudo udevadm trigger

# Check dmesg
dmesg | tail -20
```

### Permission errors
```bash
# Always use sudo
sudo python3 og_usb.py
```

### Device busy
```bash
# Unmount all partitions
sudo umount /dev/sdX*

# Force unmount if needed
sudo umount -f /dev/sdX*
```

### Verify formatting
```bash
# Check filesystem
sudo lsblk -f /dev/sdX

# Get detailed info
sudo parted /dev/sdX print
```

## Safety Reminders

⚠️ **Always:**
- Double-check device path before confirming
- Backup important data first
- Type 'YES' exactly as shown
- Eject safely after formatting

⚠️ **Never:**
- Format system drives (/, /home, etc.)
- Rush through confirmations
- Format without backups
- Remove USB during operation

## Common Device Paths

- `/dev/sdb` - Usually first USB drive
- `/dev/sdc` - Usually second USB drive
- `/dev/sda` - **Often your main hard drive - BE CAREFUL!**

Always verify with `lsblk` before formatting!

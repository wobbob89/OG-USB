#!/bin/bash
# OG USB Installation Script
# This script installs system dependencies for OG USB tool

echo "============================================"
echo "   OG USB - Installation Script"
echo "============================================"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo: sudo ./install.sh"
    exit 1
fi

# Detect package manager and distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect OS. Please install dependencies manually."
    exit 1
fi

echo "Detected OS: $OS"
echo ""

# Install dependencies based on OS
case $OS in
    ubuntu|debian|linuxmint|pop)
        echo "Installing dependencies for Debian/Ubuntu-based system..."
        apt-get update
        
        # Try modern exfatprogs first, fallback to legacy exfat-utils
        if apt-cache show exfatprogs &> /dev/null; then
            apt-get install -y parted dosfstools exfatprogs ntfs-3g e2fsprogs util-linux
        else
            echo "exfatprogs not available, using exfat-utils instead"
            apt-get install -y parted dosfstools exfat-fuse exfat-utils ntfs-3g e2fsprogs util-linux
        fi
        ;;
    
    fedora|rhel|centos)
        echo "Installing dependencies for Fedora/RHEL-based system..."
        dnf install -y parted dosfstools exfatprogs ntfs-3g e2fsprogs util-linux
        ;;
    
    arch|manjaro)
        echo "Installing dependencies for Arch-based system..."
        pacman -Sy --noconfirm parted dosfstools exfatprogs ntfs-3g e2fsprogs util-linux
        ;;
    
    opensuse*)
        echo "Installing dependencies for openSUSE..."
        zypper install -y parted dosfstools exfatprogs ntfs-3g e2fsprogs util-linux
        ;;
    
    *)
        echo "Unsupported OS: $OS"
        echo "Please install the following packages manually:"
        echo "  - parted"
        echo "  - dosfstools"
        echo "  - exfatprogs (or exfat-utils)"
        echo "  - ntfs-3g"
        echo "  - e2fsprogs"
        echo "  - util-linux"
        exit 1
        ;;
esac

# Check installation
echo ""
echo "Verifying installation..."
MISSING=0

for cmd in lsblk parted mkfs.vfat mkfs.exfat mkfs.ntfs mkfs.ext4; do
    if ! command -v $cmd &> /dev/null; then
        echo "✗ $cmd not found"
        MISSING=1
    else
        echo "✓ $cmd found"
    fi
done

echo ""
if [ $MISSING -eq 0 ]; then
    echo "============================================"
    echo "✓ Installation complete!"
    echo "============================================"
    echo ""
    echo "You can now run OG USB with:"
    echo "  sudo python3 og_usb.py"
    echo ""
    
    # Make the main script executable
    chmod +x og_usb.py
    echo "Made og_usb.py executable"
else
    echo "============================================"
    echo "⚠ Installation incomplete"
    echo "============================================"
    echo "Some dependencies are missing. Please install them manually."
    exit 1
fi

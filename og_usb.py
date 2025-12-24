#!/usr/bin/env python3
"""
OG USB - USB Formatting and Partitioning Tool
Automatically detects and formats USB drives with intelligent filesystem selection
"""

import os
import sys
import subprocess
import time
from typing import List, Dict, Optional, Tuple


class USBDevice:
    """Represents a USB storage device"""
    
    def __init__(self, device: str, size: int, model: str = ""):
        self.device = device
        self.size = size  # Size in bytes
        self.model = model
    
    def get_size_gb(self) -> float:
        """Convert size to GB"""
        return self.size / (1024 ** 3)
    
    def __str__(self) -> str:
        return f"{self.device} - {self.get_size_gb():.2f}GB - {self.model}"


class OG_USB:
    """Main OG USB tool class"""
    
    def __init__(self):
        self.devices: List[USBDevice] = []
        self.is_root = os.geteuid() == 0 if hasattr(os, 'geteuid') else True
    
    def check_root(self) -> bool:
        """Check if running with root/admin privileges"""
        if not self.is_root:
            print("ERROR: This tool requires root/administrator privileges")
            print("Please run with sudo: sudo python3 og_usb.py")
            return False
        return True
    
    def detect_usb_devices(self) -> List[USBDevice]:
        """Detect all USB storage devices"""
        devices = []
        
        try:
            # Use lsblk to list block devices
            result = subprocess.run(
                ['lsblk', '-b', '-d', '-o', 'NAME,SIZE,TRAN,MODEL', '-n'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                
                parts = line.split()
                if len(parts) >= 3:
                    name = parts[0]
                    size = int(parts[1])
                    transport = parts[2] if len(parts) > 2 else ""
                    model = " ".join(parts[3:]) if len(parts) > 3 else "Unknown"
                    
                    # Filter for USB devices
                    if transport == "usb":
                        device_path = f"/dev/{name}"
                        devices.append(USBDevice(device_path, size, model))
        
        except subprocess.CalledProcessError as e:
            print(f"Error detecting USB devices: {e}")
        except FileNotFoundError:
            print("Error: lsblk command not found. Please install util-linux package.")
        
        self.devices = devices
        return devices
    
    def list_devices(self) -> None:
        """Display all detected USB devices"""
        if not self.devices:
            print("\nNo USB devices detected!")
            print("Please insert a USB drive and try again.")
            return
        
        print("\n=== Detected USB Devices ===")
        for idx, device in enumerate(self.devices, 1):
            print(f"{idx}. {device}")
        print()
    
    def recommend_filesystem(self, size_gb: float) -> str:
        """Recommend filesystem type based on USB size and use case"""
        if size_gb <= 4:
            # Small drives (≤4GB) - FAT32 for maximum compatibility
            return "vfat"
        elif size_gb <= 32:
            # Medium drives (4-32GB) - FAT32 or exFAT
            return "vfat"
        else:
            # Large drives (>32GB) - exFAT for large file support
            return "exfat"
    
    def get_filesystem_label(self, fs_type: str) -> str:
        """Get human-readable filesystem label"""
        labels = {
            "vfat": "FAT32",
            "exfat": "exFAT",
            "ntfs": "NTFS",
            "ext4": "ext4"
        }
        return labels.get(fs_type, fs_type.upper())
    
    def wipe_device(self, device: str) -> bool:
        """Securely wipe the device by writing zeros"""
        print(f"\n[1/4] Wiping device {device}...")
        print("This may take several minutes depending on the USB size...")
        
        try:
            # First, unmount any mounted partitions
            self.unmount_device(device)
            
            # Use dd to zero out the first 100MB (this is faster and sufficient)
            # For full wipe, change count to the full device size
            subprocess.run(
                ['dd', 'if=/dev/zero', f'of={device}', 'bs=1M', 'count=100', 'status=progress'],
                check=True
            )
            
            # Sync to ensure all writes are flushed
            subprocess.run(['sync'], check=True)
            
            print("✓ Device wiped successfully")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"✗ Error wiping device: {e}")
            return False
    
    def unmount_device(self, device: str) -> None:
        """Unmount all partitions of a device"""
        try:
            # Find all mounted partitions for this device
            result = subprocess.run(
                ['lsblk', '-ln', '-o', 'NAME', device],
                capture_output=True,
                text=True
            )
            
            for line in result.stdout.strip().split('\n'):
                partition = f"/dev/{line.strip()}"
                if partition != device:
                    try:
                        subprocess.run(['umount', partition], 
                                     stderr=subprocess.DEVNULL,
                                     check=False)
                    except Exception:
                        pass
        except Exception:
            pass
    
    def create_partition(self, device: str) -> bool:
        """Create a new partition table and partition"""
        print(f"\n[2/4] Creating partition on {device}...")
        
        try:
            # Create a new GPT partition table
            subprocess.run(
                ['parted', '-s', device, 'mklabel', 'gpt'],
                check=True
            )
            
            # Create a single primary partition using the entire disk
            subprocess.run(
                ['parted', '-s', device, 'mkpart', 'primary', '0%', '100%'],
                check=True
            )
            
            # Sync
            subprocess.run(['sync'], check=True)
            
            # Wait a moment for the partition to be recognized
            time.sleep(2)
            
            print("✓ Partition created successfully")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"✗ Error creating partition: {e}")
            return False
    
    def format_partition(self, device: str, fs_type: str, label: str = "OG_USB") -> bool:
        """Format the partition with the specified filesystem"""
        print(f"\n[3/4] Formatting partition as {self.get_filesystem_label(fs_type)}...")
        
        # Determine the partition name (e.g., /dev/sdb1)
        if device[-1].isdigit():
            partition = f"{device}p1"
        else:
            partition = f"{device}1"
        
        try:
            if fs_type == "vfat":
                # Format as FAT32
                subprocess.run(
                    ['mkfs.vfat', '-F', '32', '-n', label, partition],
                    check=True
                )
            elif fs_type == "exfat":
                # Format as exFAT
                subprocess.run(
                    ['mkfs.exfat', '-n', label, partition],
                    check=True
                )
            elif fs_type == "ntfs":
                # Format as NTFS
                subprocess.run(
                    ['mkfs.ntfs', '-f', '-L', label, partition],
                    check=True
                )
            elif fs_type == "ext4":
                # Format as ext4
                subprocess.run(
                    ['mkfs.ext4', '-F', '-L', label, partition],
                    check=True
                )
            else:
                print(f"✗ Unsupported filesystem type: {fs_type}")
                return False
            
            # Sync
            subprocess.run(['sync'], check=True)
            
            print(f"✓ Formatted successfully as {self.get_filesystem_label(fs_type)}")
            return True
        
        except subprocess.CalledProcessError as e:
            print(f"✗ Error formatting partition: {e}")
            return False
        except FileNotFoundError as e:
            print(f"✗ Required tool not found. Please install: {e}")
            return False
    
    def verify_device(self, device: str) -> bool:
        """Verify the device was formatted correctly"""
        print(f"\n[4/4] Verifying {device}...")
        
        try:
            # Determine the partition name
            if device[-1].isdigit():
                partition = f"{device}p1"
            else:
                partition = f"{device}1"
            
            # Check if partition exists and has a filesystem
            result = subprocess.run(
                ['lsblk', '-f', partition],
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout:
                print("✓ Device verification successful")
                print("\nDevice information:")
                print(result.stdout)
                return True
            else:
                print("✗ Verification failed")
                return False
        
        except subprocess.CalledProcessError as e:
            print(f"✗ Error verifying device: {e}")
            return False
    
    def format_usb(self, device: USBDevice, fs_type: Optional[str] = None, 
                   label: str = "OG_USB") -> bool:
        """Complete USB formatting process"""
        
        # Recommend filesystem if not specified
        if not fs_type:
            fs_type = self.recommend_filesystem(device.get_size_gb())
            print(f"\nRecommended filesystem: {self.get_filesystem_label(fs_type)}")
        
        # Display warning
        print("\n" + "="*60)
        print("⚠️  WARNING: ALL DATA ON THIS DEVICE WILL BE PERMANENTLY ERASED!")
        print("="*60)
        print(f"Device: {device}")
        print(f"Filesystem: {self.get_filesystem_label(fs_type)}")
        print(f"Label: {label}")
        print("="*60)
        
        # Get confirmation
        response = input("\nType 'YES' to continue or anything else to cancel: ")
        if response != "YES":
            print("\nOperation cancelled by user.")
            return False
        
        # Execute formatting steps
        if not self.wipe_device(device.device):
            return False
        
        if not self.create_partition(device.device):
            return False
        
        if not self.format_partition(device.device, fs_type, label):
            return False
        
        if not self.verify_device(device.device):
            return False
        
        print("\n" + "="*60)
        print("✓ USB FORMATTING COMPLETE!")
        print("="*60)
        print("Your USB drive is ready to use.")
        
        return True
    
    def show_menu(self) -> None:
        """Display interactive menu"""
        print("\n" + "="*60)
        print("   OG USB - USB Formatting & Partitioning Tool")
        print("="*60)
        
        while True:
            # Detect devices
            self.detect_usb_devices()
            self.list_devices()
            
            if not self.devices:
                response = input("Press Enter to retry detection or 'q' to quit: ")
                if response.lower() == 'q':
                    break
                continue
            
            # Device selection
            try:
                choice = input("Select device number (or 'q' to quit): ")
                if choice.lower() == 'q':
                    break
                
                device_idx = int(choice) - 1
                if device_idx < 0 or device_idx >= len(self.devices):
                    print("Invalid selection. Please try again.")
                    continue
                
                selected_device = self.devices[device_idx]
                
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            
            # Filesystem selection
            print("\n=== Select Filesystem Type ===")
            print("1. FAT32 (vfat) - Maximum compatibility, <4GB files")
            print("2. exFAT - Large file support, modern systems")
            print("3. NTFS - Windows optimized")
            print("4. ext4 - Linux optimized")
            print(f"5. Auto-detect (Recommended: {self.get_filesystem_label(self.recommend_filesystem(selected_device.get_size_gb()))})")
            
            fs_choice = input("\nSelect filesystem (1-5) or 'b' to go back: ")
            if fs_choice.lower() == 'b':
                continue
            
            fs_map = {
                '1': 'vfat',
                '2': 'exfat',
                '3': 'ntfs',
                '4': 'ext4',
                '5': None  # Auto-detect
            }
            
            fs_type = fs_map.get(fs_choice)
            if fs_type is None and fs_choice != '5':
                print("Invalid filesystem selection.")
                continue
            
            # Volume label
            label = input("\nEnter volume label (default: OG_USB): ").strip()
            if not label:
                label = "OG_USB"
            
            # Format the device
            self.format_usb(selected_device, fs_type, label)
            
            # Ask if user wants to format another device
            again = input("\nFormat another device? (y/n): ")
            if again.lower() != 'y':
                break
        
        print("\nThank you for using OG USB!")
    
    def run(self) -> None:
        """Main entry point"""
        if not self.check_root():
            sys.exit(1)
        
        self.show_menu()


def main():
    """Main function"""
    tool = OG_USB()
    tool.run()


if __name__ == "__main__":
    main()

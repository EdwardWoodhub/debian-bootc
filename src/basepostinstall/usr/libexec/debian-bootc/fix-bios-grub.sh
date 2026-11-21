#!/usr/bin/env bash
set -euo pipefail

# Skip automatically on UEFI systems
if [ -d /sys/firmware/efi ]; then
  exit 0
fi

# Resolve the underlying block device hosting /boot (or / if /boot is on rootfs)
BOOT_DEV=$(findmnt -no SOURCE /boot 2>/dev/null || findmnt -no SOURCE /)
BOOT_DEV="${BOOT_DEV%%\[*}"
DISK_NAME=$(lsblk -no PKNAME "$BOOT_DEV" 2>/dev/null | head -n 1)

if [ -z "$DISK_NAME" ]; then
  echo "fix-bios-grub: unable to resolve parent disk for $BOOT_DEV" >&2
  exit 0
fi

TARGET_DISK="/dev/${DISK_NAME}"
if [ -b "$TARGET_DISK" ] && command -v grub-install >/dev/null 2>&1; then
  echo "fix-bios-grub: syncing i386-pc GRUB core.img and modules to $TARGET_DISK"
  grub-install --target=i386-pc --boot-directory=/boot --recheck "$TARGET_DISK"
fi

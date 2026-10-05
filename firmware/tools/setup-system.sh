#!/usr/bin/env bash
# System-level setup for nRF54LM20 DK development on Arch Linux.
# Run as root:  sudo bash tools/setup-system.sh
#
# What it does:
#   1. Installs Nordic udev rules (USB access to J-Link OB and Nordic devices without root)
#   2. Adds the invoking user to the uucp group (serial port /dev/ttyACM* access)
#   3. Reloads udev
#
# After running: log out and back in (or reboot) so the new group takes effect.
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
  echo "Run with sudo: sudo bash $0" >&2
  exit 1
fi

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_USER="${SUDO_USER:-}"
if [[ -z "$TARGET_USER" ]]; then
  echo "SUDO_USER is empty; run via sudo from your normal user account." >&2
  exit 1
fi

echo "[1/3] Installing Nordic udev rules"
install -m 0644 "$HERE/71-nrf.rules" /etc/udev/rules.d/71-nrf.rules
install -m 0644 "$HERE/72-segger-jlink-ob.rules" /etc/udev/rules.d/72-segger-jlink-ob.rules
install -m 0644 "$HERE/99-mm-nrf-blacklist.rules" /etc/udev/rules.d/99-mm-nrf-blacklist.rules

echo "[2/3] Adding $TARGET_USER to group uucp"
usermod -aG uucp "$TARGET_USER"

echo "[3/3] Reloading udev"
udevadm control --reload-rules
udevadm trigger

echo
echo "Done. Log out and back in so the uucp group membership applies."
echo "Then plug in the DK and check:  nrfutil device list"

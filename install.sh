#!/usr/bin/env bash
# install.sh — Install hackrack-wordlist as a system-wide command
# Run with: sudo bash install.sh

set -e

TOOL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INSTALL_PATH="/usr/local/bin/hackrack-wordlist"

echo "[*] Installing HackRack Wordlist Generator..."

# Option A: pip install (preferred — manages uninstall cleanly)
if command -v pip3 &>/dev/null; then
    pip3 install --quiet -e "$TOOL_DIR"
    echo "[+] Installed via pip3."
    echo "[+] Run:  hackrack-wordlist"
    exit 0
fi

# Option B: direct symlink fallback
echo "[~] pip3 not found — falling back to symlink install."
chmod +x "$TOOL_DIR/main.py"
ln -sf "$TOOL_DIR/main.py" "$INSTALL_PATH"
echo "[+] Symlink created: $INSTALL_PATH → $TOOL_DIR/main.py"
echo "[+] Run:  hackrack-wordlist"

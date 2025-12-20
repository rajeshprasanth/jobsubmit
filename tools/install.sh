#!/usr/bin/env bash

# ==============================================================================
#  Jobsubmit Interactive Installer
#  Version: 1.0.8
#  License: GNU GPL v3
# ==============================================================================

set -e

# -----------------------
# Configuration
# -----------------------
PACKAGE_NAME="jobsubmit"
VERSION="1.0.5"

DEFAULT_DIR="$HOME/jobsubmit"
PROFILE_FILE="$HOME/.bashrc"

# -----------------------
# Banner
# -----------------------
echo "===================================="
echo "        Jobsubmit Installer          "
echo "        Version $VERSION             "
echo "===================================="

# -----------------------
# Installation directory
# -----------------------
read -rp "Enter installation directory [$DEFAULT_DIR]: " INSTALL_DIR
INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_DIR}"

echo "Installing Jobsubmit to:"
echo "  $INSTALL_DIR"
echo

# -----------------------
# Create target directory
# -----------------------
mkdir -p "$INSTALL_DIR"

# -----------------------
# Copy entire distribution
# -----------------------
echo "Copying Jobsubmit distribution..."

cp -r ../* "$INSTALL_DIR/"  2>/dev/null || true

# -----------------------
# Make executables runnable
# -----------------------


if [[ -f "$INSTALL_DIR/bin/jobsubmit" ]]; then
    chmod +x "$INSTALL_DIR/bin/jobsubmit"
fi


# -----------------------
# Add to PATH (user scope)
# -----------------------
if ! grep -qs "$INSTALL_DIR/bin" "$PROFILE_FILE"; then
    echo >> "$PROFILE_FILE"
    echo "# Jobsubmit $VERSION" >> "$PROFILE_FILE"
    echo "export PATH=\$PATH:$INSTALL_DIR/bin" >> "$PROFILE_FILE"
    echo "Added $INSTALL_DIR/bin to PATH in $PROFILE_FILE"
else
    echo "PATH already contains Jobsubmit."
fi

# -----------------------
# Completion message
# -----------------------
echo
echo "===================================="
echo " Jobsubmit installation completed!"
echo "===================================="
echo
echo "To start using Jobsubmit:"
echo "  source $PROFILE_FILE"
echo
echo "Example:"
echo "  jobsubmit cmd.lst all"
echo
echo "Installation directory:"
echo "  $INSTALL_DIR"
echo "===================================="

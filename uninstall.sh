#!/bin/bash
# uninstall.sh - Remove DZAJTCPER environment and dependencies (Python only)
set -e

if [ -d "venv" ]; then
    echo "Removing Python virtual environment..."
    rm -rf venv
else
    echo "No Python virtual environment found."
fi

echo "Uninstallation complete!"

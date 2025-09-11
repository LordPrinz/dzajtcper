#!/bin/bash
# uninstall.sh - Remove TCP CWND Monitor environment and dependencies (Python only)
set -e

# Remove Python virtual environment
if [ -d "venv" ]; then
    echo "Removing Python virtual environment..."
    rm -rf venv
else
    echo "No Python virtual environment found."
fi

echo "Uninstallation complete!"

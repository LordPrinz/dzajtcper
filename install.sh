#!/bin/bash

echo "=== Installing system dependencies for BCC ==="

# Check distribution
if command -v apt-get &> /dev/null; then
    # Ubuntu/Debian
    echo "Detected Ubuntu/Debian..."
    sudo apt-get update
    sudo apt-get install -y \
        bpfcc-tools \
        linux-headers-$(uname -r) \
        python3-bpfcc \
        python3-pip \
        python3-venv
elif command -v yum &> /dev/null; then
    # CentOS/RHEL/Fedora
    echo "Detected CentOS/RHEL/Fedora..."
    sudo yum install -y \
        bcc-tools \
        kernel-devel \
        python3-bcc \
        python3-pip
elif command -v dnf &> /dev/null; then
    # Fedora (newer versions)
    echo "Detected Fedora (dnf)..."
    sudo dnf install -y \
        bcc-tools \
        kernel-devel \
        python3-bcc \
        python3-pip
else
    echo "Unknown distribution. Check BCC documentation for your system:"
    echo "https://github.com/iovisor/bcc/blob/master/INSTALL.md"
    exit 1
fi

echo "=== Creating Python virtual environment ==="
python3 -m venv venv
source venv/bin/activate

echo "=== Installing Python packages ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Installation completed ==="
echo "To use the system:"
echo ""
echo "🚀 QUICK START:"
echo "   ./run.sh quick --duration 30"
echo ""
echo "📋 MAIN COMMANDS:"
echo "   ./run.sh monitor    # Start monitoring"
echo "   ./run.sh analyze    # Data analysis"
echo "   ./run.sh list       # List sessions"
echo "   ./run.sh --help     # Help"
echo ""
echo "📖 DOCUMENTATION:"
echo "   cat docs/README.md"
echo "   cat docs/CHEAT_SHEET.md"
echo ""
echo "⚠️  WARNING: System requires sudo privileges!"

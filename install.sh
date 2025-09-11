#!/bin/bash

echo "=== Instalacja zależności systemowych dla BCC ==="

# Sprawdź dystrybucję
if command -v apt-get &> /dev/null; then
    # Ubuntu/Debian
    echo "Wykryto Ubuntu/Debian..."
    sudo apt-get update
    sudo apt-get install -y \
        bpfcc-tools \
        linux-headers-$(uname -r) \
        python3-bpfcc \
        python3-pip \
        python3-venv
elif command -v yum &> /dev/null; then
    # CentOS/RHEL/Fedora
    echo "Wykryto CentOS/RHEL/Fedora..."
    sudo yum install -y \
        bcc-tools \
        kernel-devel \
        python3-bcc \
        python3-pip
elif command -v dnf &> /dev/null; then
    # Fedora (nowsze wersje)
    echo "Wykryto Fedora (dnf)..."
    sudo dnf install -y \
        bcc-tools \
        kernel-devel \
        python3-bcc \
        python3-pip
else
    echo "Nieznana dystrybucja. Sprawdź dokumentację BCC dla swojego systemu:"
    echo "https://github.com/iovisor/bcc/blob/master/INSTALL.md"
    exit 1
fi

echo "=== Tworzenie środowiska wirtualnego Python ==="
python3 -m venv venv
source venv/bin/activate

echo "=== Instalacja pakietów Python ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Instalacja zakończona ==="
echo "Aby użyć systemu:"
echo ""
echo "🚀 SZYBKI START:"
echo "   ./run.sh quick --duration 30"
echo ""
echo "📋 GŁÓWNE KOMENDY:"
echo "   ./run.sh monitor    # Start monitoringu"
echo "   ./run.sh analyze    # Analiza danych"
echo "   ./run.sh list       # Lista sesji"
echo "   ./run.sh --help     # Pomoc"
echo ""
echo "📖 DOKUMENTACJA:"
echo "   cat docs/README.md"
echo "   cat docs/CHEAT_SHEET.md"
echo ""
echo "⚠️  UWAGA: System wymaga uprawnień sudo!"

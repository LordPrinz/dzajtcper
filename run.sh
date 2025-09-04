#!/bin/bash

# Skrypt uruchamiający TCP CWND Monitor

# Sprawdź czy środowisko wirtualne istnieje
if [ -d "venv" ]; then
    echo "Aktywuję środowisko wirtualne..."
    source venv/bin/activate
fi

# Sprawdź czy skrypt jest uruchamiany jako root
if [ "$EUID" -ne 0 ]; then
    echo "Ten skrypt wymaga uprawnień root."
    echo "Uruchamiam ponownie z sudo..."
    exec sudo -E "$0" "$@"
fi

echo "Uruchamiam TCP CWND Monitor..."
python3 tcp_cwnd_monitor.py

# TCP CWND Monitor

Program do monitorowania okna przeciążenia (cwnd) TCP Cubic bezpośrednio z kernela Linuxa przy użyciu eBPF.

## Opis

Ten skrypt używa BCC (BPF Compiler Collection) do śledzenia punktów śledzenia TCP w kernelu i wyodrębniania informacji o oknie przeciążenia (cwnd) dla połączeń TCP. Dane są wyświetlane w czasie rzeczywistym na konsoli i zapisywane do pliku CSV.

## Wymagania

- Linux z obsługą eBPF (kernel 4.1+, zalecane 4.9+)
- Uprawnienia root
- BCC (BPF Compiler Collection)
- Python 3

## Instalacja

### Automatyczna instalacja

```bash
./install.sh
```

### Instalacja ręczna

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install bpfcc-tools linux-headers-$(uname -r) python3-bpfcc python3-pip python3-venv
```

#### CentOS/RHEL/Fedora:
```bash
# CentOS/RHEL
sudo yum install bcc-tools kernel-devel python3-bcc python3-pip

# Fedora (nowsze wersje)
sudo dnf install bcc-tools kernel-devel python3-bcc python3-pip
```

#### Środowisko wirtualne Python:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Użycie

```bash
# Aktywuj środowisko wirtualne (jeśli używasz)
source venv/bin/activate

# Uruchom monitor (wymaga uprawnień root)
sudo python3 tcp_cwnd_monitor.py
```

## Format wyjścia

### Konsola
```
2024-01-15T10:30:45.123456  PID  1234  192.168.1.100:  443 -> 10.0.0.1: 8080   cwnd=10
```

### Plik CSV (/tmp/cwnd_log.csv)
```csv
timestamp,pid,saddr,sport,daddr,dport,cwnd
2024-01-15T10:30:45.123456,1234,192.168.1.100,443,10.0.0.1,8080,10
```

## Kolumny danych

- `timestamp`: Znacznik czasu zdarzenia
- `pid`: ID procesu
- `saddr`: Adres IP źródłowy
- `sport`: Port źródłowy
- `daddr`: Adres IP docelowy  
- `dport`: Port docelowy
- `cwnd`: Rozmiar okna przeciążenia

## Rozwiązywanie problemów

### Błąd "operation not permitted"
- Upewnij się, że uruchamiasz skrypt z uprawnieniami root (`sudo`)

### Błąd "No such file or directory" dla nagłówków kernela
```bash
# Ubuntu/Debian
sudo apt-get install linux-headers-$(uname -r)

# CentOS/RHEL/Fedora
sudo yum install kernel-devel
```

### Błąd importu bcc
- Sprawdź czy BCC jest zainstalowane: `python3 -c "import bcc"`
- Jeśli używasz środowiska wirtualnego, upewnij się że jest aktywowane

### Brak danych wyjściowych
- Sprawdź czy jest aktywny ruch TCP w systemie
- Niektóre kernele mogą wymagać włączenia punktów śledzenia TCP

## Uwagi

- Skrypt śledzi wszystkie połączenia TCP w systemie
- Może generować dużo danych przy intensywnym ruchu sieciowym
- Plik CSV może szybko rosnąć - rozważ rotację logów dla długoterminowego użycia
- eBPF wymaga odpowiednich uprawnień i może być ograniczony przez polityki bezpieczeństwa

## Licencja

MIT License

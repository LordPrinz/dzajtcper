# TCP CWND Monitor - Przewodnik użytkownika

## Opis
TCP CWND Monitor to zaawansowane narzędzie do monitorowania okna przesyłania (congestion window) z algorytmu Cubic bezpośrednio z jądra Linux za pomocą eBPF. Program oferuje unified command interface przez single `./run.sh` script z automatycznym zarządzaniem uprawnieniami.

## Wymagania systemowe
- **System**: Linux z jądrem obsługującym eBPF (>= 4.7)
- **Pakiety systemowe**: `python3-bpfcc` (dla eBPF)
- **Uprawnienia**: Automatycznie obsługiwane przez `./run.sh`
- **Python**: Wersja 3.7+

## Instalacja i konfiguracja

### 1. Szybka instalacja
```bash
# Wykonaj skrypt instalacyjny
./install.sh
```

### 2. Ręczna instalacja
```bash
# Instalacja pakietów systemowych
sudo apt update
sudo apt install python3-bpfcc python3-venv python3-pip
sudo apt install python3-pandas python3-matplotlib python3-seaborn python3-plotly python3-numpy

# Setup projektu
chmod +x *.py *.sh
```

## Sposoby uruchamiania

### 🚀 METODA 1: Szybki start (Rekomendowana)
Wszystko w jednej komendzie - monitoring + analiza + wykresy:

```bash
# Podstawowe użycie (60 sekund monitoring)
./run.sh quick

# Monitoring przez określony czas
./run.sh quick --duration 30

# Przykłady różnych czasów
./run.sh quick --duration 15   # 15 sekund
./run.sh quick --duration 120  # 2 minuty
```

**Wynik**: Program automatycznie:
- Zbiera dane przez określony czas (z automatycznym sudo)
- Analizuje zebraną zawartość (z automatycznym zarządzaniem uprawnieniami)
- Generuje wykresy w session directory
- Zapisuje dane w out/session_TIMESTAMP/

### 📊 METODA 2: Etapowe podejście

#### Krok 1: Monitoring
```bash
# Podstawowy monitoring (60 sekund)
./run.sh monitor

# Monitoring z określonym czasem
./run.sh monitor --duration 30
```

#### Krok 2: Analiza zebranych danych
```bash
# Analiza najnowszej sesji
./run.sh analyze

# Analiza konkretnej sesji
./run.sh analyze session_20250911_143025

# Analiza z filtrowaniem
./run.sh analyze --pid 1234
./run.sh analyze --saddr 192.168.1.100
./run.sh analyze --cwnd-min 50 --cwnd-max 200
```

### � METODA 3: Comprehensive reporting
Generowanie komprehensywnych raportów:

```bash
# Raport z najnowszej sesji
./run.sh report

# Raport z konkretnej sesji
./run.sh report session_20250911_143025

# Raport z custom nazwą
./run.sh report session_20250911_143025 custom_analysis.html
```

### � METODA 4: Live monitoring
Monitoring na żywo z określonym czasem:

```bash
# Live monitoring przez 60 sekund
./run.sh live --duration 60

### 🔧 METODA 5: Zarządzanie sesjami

#### Lista sesji
```bash
# Pokaż wszystkie dostępne sesje
./run.sh list
```

#### Czyszczenie
```bash
# Usuń puste sesje
./run.sh clean
```

## Zarządzanie sesjami

### Struktura unified session directory
```
out/
├── session_20250911_143025/
│   ├── cwnd_log.csv                         # 📊 Raw TCP data
│   ├── analysis_20250911_143225_timeline.png       # 📈 First analysis  
│   ├── analysis_20250911_143225_connections.png    # 🔗 Connection analysis
│   ├── analysis_20250911_143225_heatmap.png        # 🌡️ Heatmap
│   ├── analysis_20250911_143225_timeline_interactive.html  # 🎯 Interactive
│   └── analysis_20250911_145030_*                  # 📈 Second analysis (filtered)
├── session_20250911_145123/
└── session_20250911_150245/
```

### Session commands
```bash
# Lista wszystkich sesji
./run.sh list

# Czyszczenie pustych sesji  
./run.sh clean

# Analiza konkretnej sesji
./run.sh analyze session_20250911_143025

# Raport z konkretnej sesji
./run.sh report session_20250911_143025
```

## Rodzaje generowanych wykresów

1. **Timeline** (`*_timeline.png`) - Zmiana CWND w czasie dla każdego połączenia
2. **Connections** (`*_connections.png`) - Analiza per połączenie
3. **Heatmap** (`*_heatmap.png`) - Mapa ciepła aktywności  
4. **Overview** (`*_overview.png`) - Statystyki podsumowujące
5. **Interactive** (`*_timeline_interactive.html`) - Interaktywny wykres w przeglądarce

## Przykłady użycia

### Scenariusz 1: Szybka diagnoza
```bash
# 30 sekund monitoringu z automatyczną analizą
./run.sh quick --duration 30
# Sprawdź wyniki w out/session_*/
```

### Scenariusz 2: Długi monitoring konkretnego procesu
```bash
# Zbieranie danych przez 10 minut
./run.sh monitor --duration 600

# Analiza z filtrowaniem dla konkretnego PID
./run.sh analyze --pid 1234 --charts timeline connections
```

### Scenariusz 3: Comprehensive analysis z raportem
```bash
# Monitor i generate comprehensive report
./run.sh monitor --duration 300
./run.sh report  # Generate HTML report
```

### Scenariusz 4: Analiza połączeń sieciowych
```bash
# Monitor specific network traffic
./run.sh monitor --duration 120

# Analyze specific ports
./run.sh analyze --dport 443 --charts timeline heatmap
```

## Opcje filtrowania

### Filtry dostępne w analizie:
- `--pid PID` - Konkretny proces
- `--saddr IP` - Źródłowy adres IP  
- `--daddr IP` - Docelowy adres IP
- `--sport PORT` - Port źródłowy
- `--dport PORT` - Port docelowy
- `--cwnd-min VALUE` - Minimalna wartość CWND
- `--cwnd-max VALUE` - Maksymalna wartość CWND

### Przykłady filtrowania:
```bash
# Tylko SSH connections (port 22)
./run.sh analyze --dport 22

# CWND powyżej 50
./run.sh analyze --cwnd-min 50

# Konkretny host
# Kombinowane filtry
./run.sh analyze --dport 443 --cwnd-min 20 --charts timeline connections
```

## Rozwiązywanie problemów

### Problem: Permission conflicts
```bash
# run.sh automatycznie obsługuje uprawnienia
./run.sh monitor --duration 30  # Auto-sudo + permission fixing
./run.sh analyze                # Auto permission handling
```

### Problem: "ModuleNotFoundError: No module named 'pandas'"
```bash
# Reinstaluj systemowe pakiety Python
sudo apt install python3-pandas python3-matplotlib python3-seaborn python3-plotly

# Lub użyj installation script
./install.sh
```

### Problem: "No data collected"
```bash
# Sprawdź czy masz aktywne połączenia TCP
ss -tuln

# Spróbuj dłuższego czasu monitorowania
./run.sh monitor --duration 120
```

### Problem: Puste sesje
```bash
# Wyczyść puste sesje
./run.sh clean

# Sprawdź dostępne sesje
./run.sh list
```

## Interpretacja wyników

### Wartości CWND
- **Małe wartości (1-10)**: Początek połączenia lub po stracie pakietów
- **Średnie wartości (10-100)**: Normalna praca algorytmu Cubic  
- **Duże wartości (>100)**: Optymalne wykorzystanie przepustowości

### Wzorce w wykresach
- **Wzrost piłokształtny**: Charakterystyczny dla Cubic TCP
- **Nagłe spadki**: Wykryte straty pakietów
- **Plateau**: Ograniczenie przez odbiorcę (rwnd) lub sieć

## Wskazówki optymalizacji

### Dla długotrwałego monitoringu:
```bash
# Użyj większych interwałów przy długim czasie
./run.sh monitor --duration 3600  # 1 godzina
```

### Dla analizy wydajności:
```bash
# Skup się na połączeniach o wysokim CWND
./run.sh analyze --cwnd-min 50 --charts timeline

# Generate comprehensive report
./run.sh report
```

### Dla debugowania sieci:
```bash
# Live monitoring określonego czasu
./run.sh live --duration 300
```

## Struktura danych wyjściowych

### Format CSV:
```
timestamp,pid,saddr,sport,daddr,dport,cwnd,connection
2025-01-01T12:00:00.123456,1234,192.168.1.1,12345,192.168.1.2,80,42,192.168.1.1:12345->192.168.1.2:80
```

### Kolumny:
- `timestamp`: Czas zdarzenia (ISO format)
- `pid`: ID procesu (0 dla jądra)
- `saddr`: Źródłowy adres IP
- `sport`: Port źródłowy  
- `daddr`: Docelowy adres IP
- `dport`: Port docelowy
- `cwnd`: Wartość congestion window
- `connection`: String identyfikujący połączenie

## Dostępne komendy - podsumowanie

| Komenda | Opis | Przykład |
|---------|------|----------|
| `./run.sh monitor` | eBPF monitoring | `./run.sh monitor --duration 60` |
| `./run.sh analyze` | Analiza danych | `./run.sh analyze --dport 443` |
| `./run.sh live` | Live monitoring | `./run.sh live --duration 60` |
| `./run.sh quick` | Monitor + analiza | `./run.sh quick --duration 30` |
| `./run.sh report` | Comprehensive report | `./run.sh report` |
| `./run.sh list` | Lista sesji | `./run.sh list` |
| `./run.sh clean` | Usuń puste sesje | `./run.sh clean` |

---

## Przykład kompletnego workflow

```bash
# 1. Szybka analiza (najprostsze)
./run.sh quick --duration 60

# 2. Sprawdzenie wyników w session directory
./run.sh list

# 3. Generate comprehensive report
./run.sh report

# 4. Otworzenie interaktywnego wykresu
firefox out/session_*/*_interactive.html

# 5. Dla głębszej analizy konkretnego procesu
./run.sh monitor --duration 300
./run.sh analyze --pid $(pgrep nginx) --charts timeline connections

# 6. Live monitoring podczas testów
./run.sh live --duration 180
# Uruchom swoje testy sieciowe w innym terminalu
```
```

## Rozwiązywanie problemów

### Problem: "Permission denied" lub "Operation not permitted"
```bash
# Upewnij się, że używasz sudo
sudo ./run.sh quick --duration 30
```

### Problem: "ModuleNotFoundError: No module named 'pandas'"
```bash
# Reinstaluj systemowe pakiety Python
sudo apt install python3-pandas python3-matplotlib python3-seaborn python3-plotly
```

### Problem: "No data collected"
```bash
# Sprawdź czy masz aktywne połączenia TCP
ss -tuln

# Spróbuj dłuższego czasu monitorowania
sudo ./run.sh quick --duration 60
```

### Problem: Brak wykresów
```bash
# Sprawdź czy istnieją sesje z wynikami
ls -la out/session_*/

# Sprawdź czy w sesji są wygenerowane wykresy
ls -la out/session_*/*.html out/session_*/*.png
```

## Interpretacja wyników

### Wartości CWND
- **Małe wartości (1-10)**: Początek połączenia lub po stracie pakietów
- **Średnie wartości (10-100)**: Normalna praca algorytmu Cubic  
- **Duże wartości (>100)**: Optymalne wykorzystanie przepustowości

### Wzorce w wykresach
- **Wzrost piłokształtny**: Charakterystyczny dla Cubic TCP
- **Nagłe spadki**: Wykryte straty pakietów
- **Plateau**: Ograniczenie przez odbiorcę (rwnd) lub sieć

## Wskazówki optymalizacji

### Dla długotrwałego monitoringu:
```bash
# Użyj większych interwałów przy długim czasie
sudo ./run.sh monitor --duration 3600  # 1 godzina
```

### Dla analizy wydajności:
```bash
# Skup się na połączeniach o wysokim CWND
sudo ./run.sh analyze --min-cwnd 50 --charts
```

### Dla debugowania sieci:
```bash
# Monitoruj konkretne połączenia
sudo ./run.sh live --saddr YOUR_SERVER_IP
```

## Struktura danych wyjściowych

### Format CSV:
```
timestamp,pid,saddr,sport,daddr,dport,cwnd,connection
2025-01-01T12:00:00.123456,1234,192.168.1.1,12345,192.168.1.2,80,42,192.168.1.1:12345->192.168.1.2:80
```

### Kolumny:
- `timestamp`: Czas zdarzenia (ISO format)
- `pid`: ID procesu (0 dla jądra)
- `saddr`: Źródłowy adres IP
- `sport`: Port źródłowy  
- `daddr`: Docelowy adres IP
- `dport`: Port docelowy
- `cwnd`: Wartość congestion window
- `connection`: String identyfikujący połączenie

## Skróty klawiszowe w trybie live

- `Ctrl+C`: Zatrzymanie monitoringu
- Program automatycznie przewija wyniki w terminalu

---

## Przykład kompletnego workflow

```bash
# 1. Szybka analiza (najprostsze)
sudo ./run.sh quick --duration 60

# 2. Sprawdzenie wyników  
ls out/session_*/

# 3. Otworzenie interaktywnego wykresu
firefox out/session_*/*_interactive.html

# 4. Dla głębszej analizy konkretnego procesu
sudo ./run.sh monitor --duration 300
sudo ./run.sh analyze --pid $(pgrep nginx) --charts

# 5. Monitoring na żywo podczas testów
sudo ./run.sh live &
# Uruchom swoje testy sieciowe
# Ctrl+C aby zatrzymać
```

To narzędzie daje pełną kontrolę nad monitoringiem TCP CWND z elastycznymi opcjami analizy i wizualizacji!

# TCP CWND Monitor - Cheat Sheet

## 🚀 NAJWAŻNIEJSZE KOMENDY

### Szybki start (Rekomendowany)
```bash
./run.sh monitor --duration 30      # Monitor 30s (auto-sudo)
./run.sh analyze                    # Analiza najnowszej sesji
```

### Quick mode (monitoring + analiza + HTML report w jednej komendzie)
```bash
./run.sh quick --duration 30       # Monitor + analiza + wykresy + HTML report
```

### Analiza wcześniejszych sesji
```bash
./run.sh list                       # Lista wszystkich sesji
./run.sh analyze session_20250911_143025  # Konkretna sesja
```

## 📋 GŁÓWNE KOMENDY

| Komenda | Opis | Przykład |
|---------|------|----------|
| `monitor` | 🎯 eBPF monitoring | `./run.sh monitor --duration 60` |
| `analyze` | 📊 Analiza danych | `./run.sh analyze --dport 443` |
| `live` | 📺 Live monitoring | `./run.sh live --duration 60` |
| `quick` | ⚡ Monitor + analiza + HTML report | `./run.sh quick --duration 30` |
| `report` | 📄 Comprehensive report | `./run.sh report` |
| `list` | 📋 Lista sesji | `./run.sh list` |
| `clean` | 🧹 Usuń puste sesje | `./run.sh clean` |

## 🔧 OPCJE FILTROWANIA

### Podstawowe filtry
```bash
# Por proces (PID)
./run.sh analyze --pid 1234

# Por port docelowy (np. HTTPS)
./run.sh analyze --dport 443

# Por port źródłowy (np. SSH)
./run.sh analyze --sport 22

# Por adres IP
./run.sh analyze --saddr 192.168.1.100
./run.sh analyze --daddr 10.0.0.1

# Por zakres CWND
./run.sh analyze --cwnd-min 10 --cwnd-max 100
```

### Złożone filtry
```bash
# HTTPS z wysokim CWND
./run.sh analyze --dport 443 --cwnd-min 50

# SSH od konkretnego IP
./run.sh analyze --sport 22 --saddr 192.168.1.*

# Konkretny proces z wybranymi wykresami
./run.sh analyze --pid 1234 --charts timeline connections
```

## 📊 TYPY WYKRESÓW

| Typ | Opis | Użycie |
|-----|------|--------|
| `timeline` | 📈 Ewolucja CWND w czasie | Główny wykres wydajności |
| `connections` | 🔗 Analiza połączeń | Porównanie połączeń |
| `heatmap` | 🌡️ Mapa aktywności | Identyfikacja wzorców |
| `overview` | 📋 Statystyki | Szybki przegląd |

### Przykłady wykresów
```bash
# Pojedynczy wykres
./run.sh analyze --charts timeline

# Wybrane wykresy  
./run.sh analyze --charts timeline connections

# Wszystkie wykresy (domyślnie)
./run.sh analyze
```

## 📄 RAPORTY

### Comprehensive reports
```bash
# Główny raport HTML (z wykresami)
./run.sh report

# Raport z konkretnej sesji
./run.sh report session_20250911_143025

# Raport z custom nazwą
./run.sh report session_20250911_143025 my_analysis.html
```

## 🎯 TYPOWE SCENARIUSZE

### 1. Szybka diagnoza problemu z HTML reportem
```bash
./run.sh quick --duration 30
# Sprawdź out/session_*/charts/ dla wykresów i HTML reportu
```

### 2. Analiza serwera web
```bash
# Monitor podczas testów obciążenia
./run.sh monitor --duration 300
./run.sh analyze --dport 80 --charts timeline connections
./run.sh report
```

### 3. Debugging konkretnej aplikacji
```bash
# Znajdź PID aplikacji
pgrep nginx

# Monitoruj tylko tę aplikację
./run.sh quick --duration 60
./run.sh analyze --pid 1234 --charts timeline connections
```

### 4. Analiza połączeń SSH
```bash
./run.sh monitor --duration 120
./run.sh analyze --sport 22 --charts heatmap connections
```

### 5. Analiza bazy danych
```bash
./run.sh monitor --duration 180
./run.sh analyze --dport 3306  # MySQL
./run.sh analyze --dport 5432  # PostgreSQL
./run.sh report                # Comprehensive analysis
```

### 6. Live monitoring podczas testów
```bash
# Terminal 1: Live monitoring
./run.sh live

# Terminal 2: Uruchom testy aplikacji
curl -o /dev/null http://your-server.com/large-file
```

## 🔍 INTERPRETACJA WYNIKÓW

### Wartości CWND
- **1-10**: 🟡 Start połączenia / po utracie pakietów
- **10-50**: 🟢 Normalna praca 
- **50-200**: 🔵 Optymalne wykorzystanie
- **>200**: 🚀 Bardzo szybkie połączenia

### Wzorce wykresów
- **Piłokształtne wzrosty**: ✅ Cubic TCP w akcji  
- **Nagłe spadki**: ⚠️ Straty pakietów
- **Płaskie linie**: 📊 Ograniczenia przepustowości
- **Szybkie oscylacje**: ⚡ Aktywne sterowanie przepływem

### Pliki wykresów i raportów
- `*_timeline.png`: 📈 Główny wykres zmian w czasie
- `*_connections.png`: 🔗 Analiza per połączenie  
- `*_heatmap.png`: 🌡️ Mapa aktywności
- `*_timeline_interactive.html`: 🎯 Interaktywny wykres (otwórz w przeglądarce)
- `tcp_analysis_*.html`: 📋 Comprehensive HTML report z wszystkimi danymi

## ⚠️ CZĘSTE PROBLEMY I ROZWIĄZANIA

### Problem: "Permission denied"
```bash
# ❌ Błąd: Conflicting permissions
# ✅ Rozwiązanie: run.sh automatically handles permissions
./run.sh monitor --duration 30   # Handles sudo automatically
./run.sh analyze                 # Handles file permissions automatically
```

### Problem: "No module named 'pandas'"
```bash
# ✅ Instalacja pakietów systemowych
sudo apt install python3-pandas python3-matplotlib python3-seaborn python3-plotly

# ✅ Użyj installation script
./install.sh
```

### Problem: "No data collected"
```bash
# ✅ Sprawdź aktywne połączenia TCP
ss -tuln
netstat -tlnp

# ✅ Użyj dłuższego czasu monitoringu
./run.sh monitor --duration 120

# ✅ Generuj ruch sieciowy
curl http://example.com &
```

### Problem: Puste foldery sesji
```bash
# ✅ Wyczyść puste sesje
./run.sh clean

# ✅ Sprawdź czy monitoring zbierał dane
./run.sh list
```

### Problem: Brak wykresów
```bash
# ✅ Sprawdź że analiza działa
./run.sh analyze --charts timeline

# ✅ Sprawdź sesje
./run.sh list
```

### Problem: Filtry zwracają 0 wyników
```bash
# ✅ Sprawdź dostępne dane
./run.sh list

# ✅ Sprawdź bez filtrów najpierw
./run.sh analyze  # Bez filtrów
```

## 🛠️ KOMENDY DEBUG

### Sprawdzanie danych
```bash
# Lista sesji
./run.sh list

# Analiza bez filtrów
./run.sh analyze

# Comprehensive debug report
./run.sh report
```

## 💡 WSKAZÓWKI WYDAJNOŚCI

### Czas monitoringu
- **Szybka diagnoza**: 15-30 sekund
- **Analiza wydajności**: 2-5 minut  
- **Długoterminowa analiza**: 10+ minut
- **Testy obciążenia**: Cały czas trwania testu

### Zarządzanie danymi
- **Duże zbiory danych**: Używaj filtrów do fokusowania analizy
- **Wiele sesji**: Regularnie czyść puste sesje (`--clean`)
- **Live monitoring**: Monitoruj podczas aktywnego ruchu sieciowego
- **Raporty**: Używaj HTML dla szczegółowej analizy, TXT dla szybkiego przeglądu

### Optymalizacja
```bash
# Szybka analiza tylko z timelinami
./run.sh analyze --charts timeline

# Fokus na konkretny ruch
./run.sh analyze --dport 443 --charts connections

# Analiza najnowszej sesji
./run.sh analyze  # Automatycznie najnowsze

# Comprehensive report
./run.sh report
```

## 📁 STRUKTURA SESJI

```
out/session_20250911_143025/
├── cwnd_log.csv                         # 📊 Surowe dane TCP
├── charts/                              # 📁 Quick analysis results
│   ├── chart_20250911_143225_timeline.png      # 📈 Timeline chart
│   ├── chart_20250911_143225_connections.png   # 🔗 Connection analysis
│   ├── chart_20250911_143225_heatmap.png       # 🌡️ Heatmap
│   ├── chart_20250911_143225_timeline_interactive.html  # 🎯 Interactive
│   └── tcp_analysis_20250911_143225.html       # 📋 Comprehensive HTML report
├── analysis_20250911_145030/           # 📁 Additional analysis
│   ├── chart_20250911_145030_timeline.png      # 📈 Filtered analysis
│   └── chart_20250911_145030_connections.png   # 🔗 Filtered analysis
```

**Każda analiza ma swój timestamp, więc można śledzić historię różnych analiz tej samej sesji!**

---

**TL;DR**: 
- Monitor: `./run.sh monitor --duration 30`
- Analizuj: `./run.sh analyze --dport 443`  
- All-in-one + HTML: `./run.sh quick --duration 30`
- Report: `./run.sh report`

**💡 Pro tip**: Używaj `./run.sh list` żeby zobaczyć wszystkie dostępne sesje! HTML raporty znajdziesz w folderze `charts/` każdej sesji! 🎯

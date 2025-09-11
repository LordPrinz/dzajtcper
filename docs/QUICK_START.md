# 🚀 DZAJTCPER - Quick Start Guide

## Najszybszy sposób na rozpoczęcie

### 1. Monitoring + Analiza + HTML Report w jednej komendzie
```bash
sudo ./run.sh quick --duration 30
```

**Co się dzieje:**
1. 🎯 Monitoruje TCP przez 30 sekund
2. 📊 Automatycznie analizuje zebrane dane  
3. 📈 Generuje wykresy (timeline, connections, heatmap)
4. 📋 Tworzy comprehensive HTML report z wszystkimi danymi
5. 📊 Pokazuje szybkie statystyki

### 2. Gdzie znajdę wyniki?

Po wykonaniu komendy sprawdź folder:
```
out/session_YYYYMMDD_HHMMSS/charts/
├── chart_*_timeline.png              # 📈 Wykres zmian CWND w czasie
├── chart_*_connections.png           # 🔗 Analiza połączeń  
├── chart_*_heatmap.png               # 🌡️ Mapa aktywności
├── chart_*_timeline_interactive.html # 🎯 Interaktywny wykres
└── tcp_analysis_*.html               # 📋 COMPREHENSIVE HTML REPORT
```

### 3. Jak otworzyć HTML report?

**W przeglądarce:**
```bash
# Znajdź najnowszy raport
ls -t out/session_*/charts/tcp_analysis_*.html | head -1

# Otwórz w przeglądarce
firefox "$(ls -t out/session_*/charts/tcp_analysis_*.html | head -1)"
# lub
google-chrome "$(ls -t out/session_*/charts/tcp_analysis_*.html | head -1)"
```

**Na serwerze przez SSH:**
```bash
# Skopiuj raport lokalnie
scp user@server:/path/to/tcp-sniffer/out/session_*/charts/tcp_analysis_*.html .

# Potem otwórz lokalnie
```

## 📋 Co zawiera HTML Report?

### Główne sekcje raportu:

1. **📊 General Statistics**
   - Liczba rekordów
   - Liczba połączeń  
   - Liczba procesów (PIDs)
   - Czas trwania sesji

2. **📈 CWND Statistics**
   - Średnia wartość CWND
   - Min/Max CWND
   - Odchylenie standardowe
   - Mediana

3. **🔗 Connection Analysis**
   - Tabela wszystkich połączeń
   - Statystyki per połączenie
   - Source/Destination breakdown

4. **📡 PID Analysis** 
   - Lista procesów
   - Aktywność per proces
   - Wydajność aplikacji

### Przykład wyglądu raportu:

```html
<!DOCTYPE html>
<html>
<head>
    <title>TCP CWND Analysis Report</title>
    <style>/* Professional CSS styling */</style>
</head>
<body>
    <div class="header">
        <h1>TCP CWND Analysis Report</h1>
        <p>Generated: 2025-09-11 15:39:34</p>
    </div>
    
    <div class="section">
        <h2>General Statistics</h2>
        <div class="metric">Total Records: <span class="value">661</span></div>
        <div class="metric">Unique Connections: <span class="value">4</span></div>
        <!-- ... więcej statystyk ... -->
    </div>
    <!-- ... więcej sekcji ... -->
</body>
</html>
```

## 🎯 Przykłady użycia

### Szybka diagnoza aplikacji web
```bash
# Monitoruj serwer HTTP podczas testów
sudo ./run.sh quick --duration 60

# Sprawdź raport HTML - zawiera pełną analizę:
# - Ile połączeń HTTP
# - Jak zmienia się CWND dla każdego połączenia  
# - Które procesy generują ruch
# - Mapy cieplne aktywności
```

### Debugging konkretnej aplikacji
```bash
# 1. Uruchom quick analysis
sudo ./run.sh quick --duration 30

# 2. Następnie wyfiltruj do konkretnej aplikacji
./run.sh analyze --pid $(pgrep nginx) --charts timeline connections

# 3. Generuj dedykowany raport dla nginx
./run.sh report
```

### Monitorowanie podczas testów obciążenia
```bash
# Terminal 1: Start quick monitoring
sudo ./run.sh quick --duration 300  # 5 minut

# Terminal 2: Uruchom testy obciążenia
ab -n 1000 -c 10 http://localhost/
# lub 
siege -c 20 -t 5m http://localhost/

# Wynik: Comprehensive HTML report z analizą wydajności pod obciążeniem
```

## 💡 Tips & Tricks

### 1. Automatyczne otwieranie raportu
```bash
# Dodaj do ~/.bashrc lub ~/.zshrc
alias tcpquick='sudo ./run.sh quick --duration 30 && firefox "$(ls -t out/session_*/charts/tcp_analysis_*.html | head -1)"'

# Potem używaj:
tcpquick
```

### 2. Monitoring w tle z automatycznym raportem
```bash
# Start monitoringu w tle
sudo ./run.sh quick --duration 120 &

# Rób swoją pracę...
curl http://example.com
wget https://files.com/bigfile.zip

# Po 2 minutach automatycznie będzie gotowy raport HTML
```

### 3. Porównywanie różnych scenariuszy  
```bash
# Scenario 1: Bez obciążenia
sudo ./run.sh quick --duration 30
mv out/session_$(date +%Y%m%d)_*/charts/tcp_analysis_*.html baseline_report.html

# Scenario 2: Pod obciążeniem  
sudo ./run.sh quick --duration 30  # Uruchom testy równolegle
mv out/session_$(date +%Y%m%d)_*/charts/tcp_analysis_*.html load_test_report.html

# Porównaj raporty obok siebie w przeglądarce
```

## 🚀 Next Steps

Po przejrzeniu HTML raportu:

1. **Jeśli widzisz problemy** → Użyj filtrów do analizy konkretnych połączeń:
   ```bash
   ./run.sh analyze --dport 443 --charts timeline connections
   ```

2. **Jeśli chcesz longer analysis** → Extend monitoring time:
   ```bash
   sudo ./run.sh quick --duration 300  # 5 minut
   ```

3. **Jeśli potrzebujesz live monitoring** → Use live mode:
   ```bash
   sudo ./run.sh live --duration 120
   ```

4. **Jeśli chcesz automated reports** → Set up scheduled monitoring:
   ```bash
   # Dodaj do cron co godzinę
   0 * * * * cd /path/to/tcp-sniffer && sudo ./run.sh quick --duration 60
   ```

---

**🎯 Remember:** HTML raporty zawierają wszystkie dane potrzebne do comprehensive analizy TCP performance! Wystarczy jeden `quick` command żeby mieć pełny obraz stanu sieci. 

**📋 Pro tip:** HTML raporty są self-contained - możesz je wysłać kolegom, wrzucić na serwer, nebo załączyć do dokumentacji. Wszystkie dane i stylowanie są wewnątrz jednego pliku!

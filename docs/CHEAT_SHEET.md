# DZAJTCPER - Cheat Sheet

## 🚀 MOST IMPORTANT COMMANDS

### Quick Start (Recommended)
```bash
./run.sh monitor --duration 30      # Monitor 30s (auto-sudo)
./run.sh analyze                    # Analyze latest session
```

### Quick mode (monitoring + analysis in one command)
```bash
./run.sh quick --duration 30       # Monitor + analysis + charts
```

### Analysis of previous sessions
```bash
./run.sh list                       # List all sessions
./run.sh analyze session_20250911_143025  # Specific session
```

## 📋 MAIN COMMANDS

| Command | Description | Example |
|---------|-------------|---------|
| `monitor` | 🎯 eBPF monitoring | `./run.sh monitor --duration 60` |
| `analyze` | 📊 Data analysis | `./run.sh analyze --dport 443` |
| `live` | 📺 Live monitoring | `./run.sh live --duration 60` |
| `quick` | ⚡ Monitor + analysis + HTML report | `./run.sh quick --duration 30` |
| `report` | 📄 Comprehensive report | `./run.sh report` |
| `list` | 📋 List sessions | `./run.sh list` |
| `clean` | 🧹 Remove empty sessions | `./run.sh clean` |

## 🔧 FILTERING OPTIONS

### Basic filters
```bash
# By process (PID)
./run.sh analyze --pid 1234

# By destination port (e.g. HTTPS)
./run.sh analyze --dport 443

# By source port (e.g. SSH)
./run.sh analyze --sport 22

# By IP address
./run.sh analyze --saddr 192.168.1.100
./run.sh analyze --daddr 10.0.0.1

# By CWND range
./run.sh analyze --cwnd-min 10 --cwnd-max 100
```

### Complex filters
```bash
# HTTPS with high CWND
./run.sh analyze --dport 443 --cwnd-min 50

# SSH from specific IP
./run.sh analyze --sport 22 --saddr 192.168.1.*

# Specific process with selected charts
./run.sh analyze --pid 1234 --charts timeline connections
```

## 📊 CHART TYPES

| Type | Description | Usage |
|------|-------------|-------|
| `timeline` | 📈 CWND evolution over time | Main performance chart |
| `connections` | 🔗 Connection analysis | Compare connections |
| `heatmap` | 🌡️ Activity heatmap | Pattern identification |
| `overview` | 📋 Statistics | Quick overview |

### Chart Examples
```bash
# Single chart
./run.sh analyze --charts timeline

# Selected charts  
./run.sh analyze --charts timeline connections

# All charts (default)
./run.sh analyze
```

## 📄 REPORTS

### Comprehensive reports
```bash
# Main HTML report (with charts)
./run.sh report

# Report from specific session
./run.sh report session_20250911_143025

# Report with custom name
./run.sh report session_20250911_143025 my_analysis.html
```

## 🎯 TYPICAL SCENARIOS

### 1. Quick problem diagnosis
```bash
./run.sh quick --duration 30
# Check out/session_*/ for results
```

### 2. Web server analysis
```bash
# Monitor during load testing
./run.sh monitor --duration 300
./run.sh analyze --dport 80 --charts timeline connections
./run.sh report
```

### 3. Debugging specific application
```bash
# Find application PID
pgrep nginx

# Monitor only this application
./run.sh quick --duration 60
./run.sh analyze --pid 1234 --charts timeline connections
```

### 4. SSH connection analysis
```bash
./run.sh monitor --duration 120
./run.sh analyze --sport 22 --charts heatmap connections
```

### 5. Database analysis
```bash
./run.sh monitor --duration 180
./run.sh analyze --dport 3306  # MySQL
./run.sh analyze --dport 5432  # PostgreSQL
./run.sh report                # Comprehensive analysis
```

### 6. Live monitoring during tests
```bash
# Terminal 1: Live monitoring
./run.sh live

# Terminal 2: Uruchom testy aplikacji
curl -o /dev/null http://your-server.com/large-file
```

## 🔍 RESULTS INTERPRETATION

### CWND Values
- **1-10**: 🟡 Connection start / after packet loss
- **10-50**: 🟢 Normalna praca 
- **50-200**: 🔵 Optymalne wykorzystanie
- **>200**: 🚀 Very fast connections

### Chart patterns
- **Sawtooth growth**: ✅ Cubic TCP in action  
- **Sudden drops**: ⚠️ Packet losses
- **Flat lines**: 📊 Bandwidth limitations
- **Fast oscillations**: ⚡ Active flow control

### Chart files
- `*_timeline.png`: 📈 Main time-based chart
- `*_connections.png`: 🔗 Per-connection analysis  
- `*_heatmap.png`: 🌡️ Activity heatmap
- `*_timeline_interactive.html`: 🎯 Interactive chart (open in browser)

### Report files  
- `*.html`: 📄 Comprehensive HTML reports with statistics and embedded charts
- `*.json`: 🔧 Machine-readable reports for automation
- `*.txt`: 📝 Plain text reports for command-line viewing

## ⚠️ COMMON PROBLEMS AND SOLUTIONS

### Problem: "Permission denied"
```bash
# ❌ Error: Conflicting permissions
# ✅ Solution: run.sh automatically handles permissions
./run.sh monitor --duration 30   # Handles sudo automatically
./run.sh analyze                 # Handles file permissions automatically
```

### Problem: "No module named 'pandas'"
```bash
# ✅ Install system packages
sudo apt install python3-pandas python3-matplotlib python3-seaborn python3-plotly

# ✅ Use installation script
./install.sh
```

### Problem: "No data collected"
```bash
# ✅ Check active TCP connections
ss -tuln
netstat -tlnp

# ✅ Use longer monitoring time
./run.sh monitor --duration 120

# ✅ Generuj ruch sieciowy
curl http://example.com &
```

### Problem: Puste foldery sesji
```bash
# ✅ Clean empty sessions
./run.sh clean

# ✅ Check if monitoring collected data
./run.sh list
```

### Problem: No charts
```bash
# ✅ Check that analysis works
./run.sh analyze --charts timeline

# ✅ Check sessions
./run.sh list
```

### Problem: Filters return 0 results
```bash
# ✅ Check available data
./run.sh list

# ✅ Check without filters first
./run.sh analyze  # Without filters
```

## 🛠️ DEBUG COMMANDS

### Data checking
```bash
# List sessions
./run.sh list

# Analysis without filters
./run.sh analyze

# Comprehensive debug report
./run.sh report
```

## 💡 PERFORMANCE TIPS

### Monitoring time
- **Quick diagnosis**: 15-30 seconds
- **Performance analysis**: 2-5 minutes  
- **Long-term analysis**: 10+ minutes
- **Load testing**: Entire test duration

### Data management
- **Large datasets**: Use filters to focus analysis
- **Multiple sessions**: Regularly clean empty sessions (`--clean`)
- **Live monitoring**: Monitor during active network traffic
- **Reports**: Use HTML for detailed analysis, TXT for quick overview

### Optimization
```bash
# Quick analysis with timelines only
./run.sh analyze --charts timeline

# Focus on specific traffic
./run.sh analyze --dport 443 --charts connections

# Analysis of latest session
./run.sh analyze  # Automatically latest

# Comprehensive report
./run.sh report
```

## 📁 SESSION STRUCTURE

```
out/session_20250911_143025/
├── cwnd_log.csv                         # 📊 Raw TCP data
├── analysis_20250911_143225_timeline.png       # 📈 First analysis
├── analysis_20250911_143225_connections.png    # 🔗 Connection analysis
├── analysis_20250911_143225_heatmap.png        # 🌡️ Heat map
├── analysis_20250911_143225_timeline_interactive.html  # 🎯 Interactive
├── analysis_20250911_145030_timeline.png       # 📈 Second analysis (filtered)
└── analysis_20250911_145030_connections.png    # 🔗 Filtered analysis
```

**Each analysis has its own timestamp, so you can track the history of different analyses of the same session!**

---

**TL;DR**: 
- Monitor: `./run.sh monitor --duration 30`
- Analyze: `./run.sh analyze --dport 443`  
- All-in-one: `./run.sh quick --duration 30`
- Report: `./run.sh report`

**💡 Pro tip**: Use `./run.sh list` to see all available sessions! 🎯

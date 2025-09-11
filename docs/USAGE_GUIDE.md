# DZAJTCPER - User Guide

## Description
# 🚀 What is DZAJTCPER?

DZAJTCPER is an advanced tool for monitoring the congestion window from the Cubic algorithm directly from the Linux kernel using eBPF. The program offers a unified command interface through a single `./run.sh` script with automatic permission management.

## System Requirements
- **System**: Linux with eBPF-supporting kernel (>= 4.7)
- **System packages**: `python3-bpfcc` (for eBPF)
- **Permissions**: Automatically handled by `./run.sh`
- **Python**: Version 3.7+

## Installation and Configuration

### 1. Quick Installation
```bash
# Run installation script
./install.sh
```

### 2. Manual Installation
```bash
# System package installation
sudo apt update
sudo apt install python3-bpfcc python3-venv python3-pip
sudo apt install python3-pandas python3-matplotlib python3-seaborn python3-plotly python3-numpy

# Project setup
chmod +x *.py *.sh
```

## Usage Methods

### 🚀 METHOD 1: Quick Start (Recommended)
Everything in one command - monitoring + analysis + charts:

```bash
# Basic usage (60 seconds monitoring)
./run.sh quick

# Monitoring for specified time
./run.sh quick --duration 30

# Examples of different times
./run.sh quick --duration 15   # 15 seconds
./run.sh quick --duration 120  # 2 minutes
```

**Result**: Program automatically:
- Collects data for specified time (with automatic sudo)
- Analyzes collected content (with automatic permission management)
- Generates charts in session directory
- Saves data in out/session_TIMESTAMP/

### 📊 METHOD 2: Step-by-step Approach

#### Step 1: Monitoring
```bash
# Basic monitoring (60 seconds)
./run.sh monitor

# Monitoring with specified time
./run.sh monitor --duration 30
```

#### Step 2: Analysis of collected data
```bash
# Analyze latest session
./run.sh analyze

# Analyze specific session
./run.sh analyze session_20250911_143025

# Analysis with filtering
./run.sh analyze --pid 1234
./run.sh analyze --saddr 192.168.1.100
./run.sh analyze --cwnd-min 50 --cwnd-max 200
```

### 📋 METHOD 3: Comprehensive reporting
Generating comprehensive reports:

```bash
# Report from latest session
./run.sh report

# Report from specific session
./run.sh report session_20250911_143025

# Report with custom name
./run.sh report session_20250911_143025 custom_analysis.html
```

### ⚡ METHOD 4: Live monitoring
Live monitoring with specified time:

```bash
# Live monitoring for 60 seconds
./run.sh live --duration 60

### 🔧 METHOD 5: Session Management

#### Session List
```bash
# Show all available sessions
./run.sh list
```

#### Cleanup
```bash
# Remove empty sessions
./run.sh clean
```

## Session Management

### Unified session directory structure
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
# List all sessions
./run.sh list

# Clean empty sessions  
./run.sh clean

# Analysis of specific session
./run.sh analyze session_20250911_143025

# Report from specific session
./run.sh report session_20250911_143025
```

## Types of Generated Charts

1. **Timeline** (`*_timeline.png`) - CWND change over time for each connection
2. **Connections** (`*_connections.png`) - Per-connection analysis
3. **Heatmap** (`*_heatmap.png`) - Activity heatmap  
4. **Overview** (`*_overview.png`) - Summary statistics
5. **Interactive** (`*_timeline_interactive.html`) - Interactive chart in browser

## Usage Examples

### Scenario 1: Quick Diagnosis
```bash
# 30 seconds monitoring with automatic analysis
./run.sh quick --duration 30
# Check results in out/session_*/
```

### Scenario 2: Long monitoring of specific process
```bash
# Collect data for 10 minutes
./run.sh monitor --duration 600

# Analysis with filtering for specific PID
./run.sh analyze --pid 1234 --charts timeline connections
```

### Scenario 3: Comprehensive analysis with report
```bash
# Monitor and generate comprehensive report
./run.sh monitor --duration 300
./run.sh report  # Generate HTML report
```

### Scenario 4: Network connections analysis
```bash
# Monitor specific network traffic
./run.sh monitor --duration 120

# Analyze specific ports
./run.sh analyze --dport 443 --charts timeline heatmap
```

## Filtering Options

### Filters available in analysis:
- `--pid PID` - Specific process
- `--saddr IP` - Source IP address  
- `--daddr IP` - Destination IP address
- `--sport PORT` - Source port
- `--dport PORT` - Destination port
- `--cwnd-min VALUE` - Minimum CWND value
- `--cwnd-max VALUE` - Maximum CWND value

### Filtering Examples:
```bash
# Only SSH connections (port 22)
./run.sh analyze --dport 22

# CWND above 50
./run.sh analyze --cwnd-min 50

# Specific host
# Combined filters
./run.sh analyze --dport 443 --cwnd-min 20 --charts timeline connections
```

## Troubleshooting

### Problem: Permission conflicts
```bash
# run.sh automatically handles permissions
./run.sh monitor --duration 30  # Auto-sudo + permission fixing
./run.sh analyze                # Auto permission handling
```

### Problem: "ModuleNotFoundError: No module named 'pandas'"
```bash
# Reinstall system Python packages
sudo apt install python3-pandas python3-matplotlib python3-seaborn python3-plotly

# Or use installation script
./install.sh
```

### Problem: "No data collected"
```bash
# Check if you have active TCP connections
ss -tuln

# Try longer monitoring time
./run.sh monitor --duration 120
```

### Problem: Empty sessions
```bash
# Clean empty sessions
./run.sh clean

# Check available sessions
./run.sh list
```

## Results Interpretation

### CWND Values
- **Small values (1-10)**: Connection start or after packet loss
- **Medium values (10-100)**: Normal Cubic algorithm operation  
- **Large values (>100)**: Optimal bandwidth utilization

### Chart Patterns
- **Sawtooth growth**: Characteristic of Cubic TCP
- **Sudden drops**: Detected packet losses
- **Plateau**: Receiver (rwnd) or network limitation

## Optimization Tips

### For long-term monitoring:
```bash
# Use larger intervals for long time periods
./run.sh monitor --duration 3600  # 1 hour
```

### For performance analysis:
```bash
# Focus on high CWND connections
./run.sh analyze --cwnd-min 50 --charts timeline

# Generate comprehensive report
./run.sh report
```

### For network debugging:
```bash
# Live monitoring for specified time
./run.sh live --duration 300
```

## Output Data Structure

### CSV Format:
```
timestamp,pid,saddr,sport,daddr,dport,cwnd,connection
2025-01-01T12:00:00.123456,1234,192.168.1.1,12345,192.168.1.2,80,42,192.168.1.1:12345->192.168.1.2:80
```

### Columns:
- `timestamp`: Event time (ISO format)
- `pid`: Process ID (0 for kernel)
- `saddr`: Source IP address
- `sport`: Source port  
- `daddr`: Destination IP address
- `dport`: Destination port
- `cwnd`: Congestion window value
- `connection`: String identifying connection

## Available Commands - Summary

| Command | Description | Example |
|---------|-------------|---------|
| `./run.sh monitor` | eBPF monitoring | `./run.sh monitor --duration 60` |
| `./run.sh analyze` | Data analysis | `./run.sh analyze --dport 443` |
| `./run.sh live` | Live monitoring | `./run.sh live --duration 60` |
| `./run.sh quick` | Monitor + analysis | `./run.sh quick --duration 30` |
| `./run.sh report` | Comprehensive report | `./run.sh report` |
| `./run.sh list` | List sessions | `./run.sh list` |
| `./run.sh clean` | Remove empty sessions | `./run.sh clean` |

---

## Complete Workflow Example

```bash
# 1. Quick analysis (simplest)
./run.sh quick --duration 60

# 2. Check results in session directory
./run.sh list

# 3. Generate comprehensive report
./run.sh report

# 4. Open interactive chart
firefox out/session_*/*_interactive.html

# 5. For deeper analysis of specific process
./run.sh monitor --duration 300
./run.sh analyze --pid $(pgrep nginx) --charts timeline connections

# 6. Live monitoring during tests
./run.sh live --duration 180
# Run your network tests in another terminal
```

## Troubleshooting

### Problem: "Permission denied" or "Operation not permitted"
```bash
# Make sure you use sudo
sudo ./run.sh quick --duration 30
```

### Problem: "ModuleNotFoundError: No module named 'pandas'"
```bash
# Reinstall system Python packages
sudo apt install python3-pandas python3-matplotlib python3-seaborn python3-plotly
```

### Problem: "No data collected"
```bash
# Check if you have active TCP connections
ss -tuln

# Try longer monitoring time
sudo ./run.sh quick --duration 60
```

### Problem: No charts
```bash
# Check if sessions with results exist
ls -la out/session_*/

# Check if charts are generated in session
ls -la out/session_*/*.html out/session_*/*.png
```

## Results Interpretation

### CWND Values
- **Small values (1-10)**: Connection start or after packet loss
- **Medium values (10-100)**: Normal Cubic algorithm operation  
- **Large values (>100)**: Optimal bandwidth utilization

### Chart Patterns
- **Sawtooth growth**: Characteristic of Cubic TCP
- **Sudden drops**: Detected packet losses
- **Plateau**: Receiver (rwnd) or network limitation

## Optimization Tips

### For long-term monitoring:
```bash
# Use larger intervals for long time periods
sudo ./run.sh monitor --duration 3600  # 1 hour
```

### For performance analysis:
```bash
# Focus on high CWND connections
sudo ./run.sh analyze --min-cwnd 50 --charts
```

### For network debugging:
```bash
# Monitor specific connections
sudo ./run.sh live --saddr YOUR_SERVER_IP
```

## Keyboard Shortcuts in Live Mode

- `Ctrl+C`: Stop monitoring
- Program automatically scrolls results in terminal

---

## Complete Workflow Example

```bash
# 1. Quick analysis (simplest)
sudo ./run.sh quick --duration 60

# 2. Check results  
ls out/session_*/

# 3. Open interactive chart
firefox out/session_*/*_interactive.html

# 4. For deeper analysis of specific process
sudo ./run.sh monitor --duration 300
sudo ./run.sh analyze --pid $(pgrep nginx) --charts

# 5. Live monitoring during tests
sudo ./run.sh live &
# Run your network tests
# Ctrl+C to stop
```

This tool provides full control over TCP CWND monitoring with flexible analysis and visualization options!

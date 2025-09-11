# DZAJTCPER - TCP CWND Monitor & Analyzer

Comprehensive TCP congestion window monitoring and analysis toolkit using eBPF for kernel-level monitoring with advanced filtering, visualization, and reporting capabilities.

## 🚀 Features

- **Real-time eBPF monitoring** of TCP CWND directly from kernel  
- **Unified command interface** through single `./run.sh` script
- **Session-based organization** with automatic timestamped folders
- **Advanced filtering** by PID, addresses, ports, CWND ranges
- **Multiple chart types** (timeline, connections, heatmap, overview)
- **Interactive HTML reports** with Plotly visualization
- **Live monitoring** with real-time updates
- **Comprehensive reporting** in text, JSON, and HTML formats
- **Automatic session management** with cleanup functionality
- **Historical analysis** of previously collected data
- **Automatic permission handling** for seamless operation

## 📦 Installation

### Prerequisites

```bash
# Install BCC and Python dependencies
sudo apt update
sudo apt install python3-bpfcc python3-pip

# Install Python packages
pip3 install pandas matplotlib seaborn plotly numpy
```

### Quick Setup

```bash
git clone <repository>
cd dzajtcper
chmod +x install.sh
./install.sh
```

### Manual Setup

```bash
git clone <repository>
cd dzajtcper
chmod +x *.py *.sh
```

## 📁 Session Management

### Output Directory Structure

All TCP CWND data is automatically organized in session directories with unified structure:

```
out/
├── session_20250911_143025/
│   ├── cwnd_log.csv                         # 📊 Raw TCP monitoring data
│   ├── analysis_20250911_143225_timeline.png       # 📈 Timeline chart
│   ├── analysis_20250911_143225_connections.png    # 🔗 Connection analysis
│   ├── analysis_20250911_143225_heatmap.png        # 🌡️ Traffic heatmap
│   ├── analysis_20250911_143225_timeline_interactive.html  # 🎯 Interactive charts
│   ├── analysis_20250911_145030_timeline.png       # 📈 Second analysis (filtered)
│   └── analysis_20250911_145030_connections.png    # 🔗 Filtered analysis
├── session_20250911_145123/
│   └── cwnd_log.csv                         # 📊 Session with data only
└── session_20250911_150245/
    ├── cwnd_log.csv                         # 📊 Raw data
    └── analysis_*_...                       # 📈 Multiple analysis files
```

### Session Commands

```bash
# List all sessions with data summary
./run.sh list

# Clean up empty session directories  
./run.sh clean
```

## 🎯 Quick Start

### 1. Monitor TCP for 30 seconds and analyze
```bash
./run.sh monitor --duration 30    # Automatically handles permissions
./run.sh analyze                  # Analyze latest session
```

### 2. Monitor and analyze in one command
```bash
./run.sh quick --duration 60      # Monitor + analyze automatically
```

### 3. Generate comprehensive report
```bash
./run.sh report                   # Generate HTML report from latest session
```

## 💡 Usage Examples

### Basic Monitoring

```bash
# Monitor indefinitely (Ctrl+C to stop)
./run.sh monitor

# Monitor for specific duration
./run.sh monitor --duration 300
```

### Analyzing Previous Sessions

```bash
# Analyze latest session automatically
./run.sh analyze

# Analyze specific session
./run.sh analyze session_20250911_143025

# List available sessions
./run.sh list

# Clean empty sessions
./run.sh clean
```

### Advanced Filtering

```bash
# Filter by destination port (HTTPS traffic)
./run.sh analyze --dport 443 --charts timeline connections

# Filter by source port (SSH traffic)  
./run.sh analyze --sport 22 --charts heatmap

# Filter by PID (specific process)
./run.sh analyze --pid 1234 --charts timeline

# Filter by IP addresses
./run.sh analyze --saddr 192.168.1.100 --daddr 10.0.0.1

# Filter by CWND range
./run.sh analyze --cwnd-min 10 --cwnd-max 100

# Combine multiple filters
./run.sh analyze --dport 443 --cwnd-min 20 --charts timeline connections
```

### Chart Generation

```bash
# Generate specific chart types
./run.sh analyze --charts timeline          # Only timeline
./run.sh analyze --charts connections       # Only connections  
./run.sh analyze --charts heatmap          # Only heatmap
./run.sh analyze --charts overview         # Only overview
./run.sh analyze --charts timeline connections heatmap  # Multiple

# All charts (default behavior when no --charts specified)
./run.sh analyze
```

### Report Generation

```bash
# Comprehensive HTML report
./run.sh report

# Report from specific session  
./run.sh report session_20250911_143025

# Report with custom output name
./run.sh report session_20250911_143025 custom_analysis.html

# Quick monitoring with immediate report
./run.sh quick --duration 30 && ./run.sh report
```

### Live Monitoring

```bash
# Live monitoring of latest session
./run.sh live

# Live monitoring for specific duration
./run.sh live --duration 60
```

## 🔧 Command Reference

### Main Commands

| Command | Description | Example |
|---------|-------------|---------|
| `monitor` | Start eBPF monitoring | `./run.sh monitor --duration 60` |
| `analyze` | Analyze existing data | `./run.sh analyze --dport 443` |
| `live` | Live monitoring dashboard | `./run.sh live --duration 60` |
| `quick` | Monitor + analyze | `./run.sh quick --duration 30` |
| `report` | Generate comprehensive report | `./run.sh report` |
| `list` | List all sessions | `./run.sh list` |
| `clean` | Clean empty sessions | `./run.sh clean` |

### Global Options

| Option | Type | Description | Example |
|--------|------|-------------|---------|
| `--duration` | int | Monitoring duration in seconds | `--duration 300` |
| `--help` | flag | Show command help | `./run.sh --help` |

### Filter Options

| Option | Type | Description | Example |
|--------|------|-------------|---------|
| `--pid` | int | Filter by process ID | `--pid 1234` |
| `--saddr` | string | Source address pattern | `--saddr 192.168.1.*` |
| `--daddr` | string | Destination address pattern | `--daddr 10.0.0.1` |
| `--sport` | int | Source port | `--sport 22` |
| `--dport` | int | Destination port | `--dport 443` |
| `--cwnd-min` | int | Minimum CWND value | `--cwnd-min 10` |
| `--cwnd-max` | int | Maximum CWND value | `--cwnd-max 100` |

### Chart Options

| Chart Type | Description | Use Case |
|------------|-------------|----------|
| `timeline` | CWND evolution over time | Overall performance analysis |
| `connections` | Per-connection statistics | Connection comparison |
| `heatmap` | Activity intensity map | Pattern identification |
| `overview` | Summary statistics | Quick overview |

### Report Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| HTML | Rich formatted report with embedded charts | Detailed analysis and presentation |
| Text | Plain text summary | Quick review |
| JSON | Machine readable data | Automation/scripting |

## 🛠️ Troubleshooting

### Common Issues

#### 1. Permission Errors
```bash
# Problem: Permission conflicts between root monitoring and user analysis
# Solution: run.sh automatically handles permissions

./run.sh monitor --duration 60   # Handles sudo automatically
./run.sh analyze                 # Handles file permissions automatically
```

#### 2. No Data Collected
```bash
# Check if there's active TCP traffic
ss -tuln

# Use longer monitoring duration
./run.sh monitor --duration 120

# Check specific process
sudo netstat -tlnp | grep :80
```

#### 3. Module Import Errors
```bash
# Install missing dependencies
sudo apt install python3-pandas python3-matplotlib python3-seaborn python3-plotly

# Use installation script
./install.sh
```

#### 4. Empty Session Folders
```bash
# Clean up empty sessions
./run.sh clean

# Check if monitoring collected data
./run.sh list
```

#### 5. Charts Not Generated
```bash
# Ensure analysis runs properly
./run.sh analyze --charts timeline

# Check session data
./run.sh list
```

#### 6. Filter Returns No Results
```bash
# Check available sessions first
./run.sh list

# Verify data exists
./run.sh analyze   # Without filters first
```

### Debug Commands

```bash
# Check available sessions
./run.sh list

# Analyze without filters first
./run.sh analyze

# Generate comprehensive report for debugging
./run.sh report
```

### Performance Tips

- **Short analysis**: 15-30 seconds monitoring
- **Performance testing**: 2-5 minutes monitoring
- **Long-term analysis**: 10+ minutes monitoring
- **Live monitoring**: Use with active network traffic
- **Large datasets**: Use filters to focus analysis

## 📊 Data Analysis Examples

### Scenario 1: Web Server Performance
```bash
# Monitor during load test
./run.sh monitor --duration 300

# Analyze HTTP traffic
./run.sh analyze --dport 80 --charts timeline connections

# Generate comprehensive report
./run.sh report
```

### Scenario 2: SSH Connection Analysis
```bash
# Monitor SSH activity  
./run.sh monitor --duration 120

# Analyze SSH connections
./run.sh analyze --sport 22 --charts connections heatmap
```

### Scenario 3: Database Connection Monitoring
```bash
# Monitor database traffic
./run.sh monitor --duration 180

# Analyze MySQL connections
./run.sh analyze --dport 3306

# Generate MySQL analysis report
./run.sh report
```

### Scenario 4: Application-Specific Analysis
```bash
# Find application PID
pgrep nginx

# Monitor and analyze application traffic
./run.sh quick --duration 60
./run.sh analyze --pid 1234 --charts timeline connections
```

## 🏗️ Architecture

### Modular Structure

```
dzajtcper/
├── run.sh                  # 🎯 Unified command interface
├── tcp_monitor.py          # 🔧 Core monitoring engine  
├── src/                    # 📦 Core modules
│   ├── __init__.py         # Package initialization
│   ├── data_loader.py      # 📊 Data loading and validation
│   ├── data_filter.py      # 🔍 Advanced filtering capabilities
│   ├── visualizer.py       # 📈 Chart generation
│   ├── monitor.py          # 📡 Live monitoring functionality
│   ├── reporter.py         # 📄 Report generation
│   └── log_manager.py      # 📁 Session management
├── out/                    # 💾 Session data storage
├── install.sh              # ⚙️ Installation script
├── uninstall.sh           # 🗑️ Uninstallation script
├── README.md               # 📚 This documentation
└── CHEAT_SHEET.md         # ⚡ Quick reference
```

### Core Components

1. **Session Manager** (`src/log_manager.py`)
   - Automatic session creation with timestamps
   - Empty session cleanup
   - Session listing and selection

2. **DataLoader** (`src/data_loader.py`)
   - CSV data loading and validation
   - Connection string creation
   - Data integrity checks

3. **DataFilter** (`src/data_filter.py`)
   - Method chaining for complex filters
   - PID, address, port, CWND range filtering
   - Time-based and connection-based filtering

4. **ChartGenerator** (`src/visualizer.py`)
   - Timeline plots with high-contrast colors
   - Connection analysis charts
   - Activity heatmaps
   - Interactive HTML charts

5. **ReportGenerator** (`src/reporter.py`)
   - Comprehensive analysis reports
   - Multiple output formats (text, JSON, HTML)
   - Performance metrics calculation

## 📋 Requirements

- Linux kernel with eBPF support (>= 4.4)
- Root privileges for eBPF monitoring
- Python 3.7+
- BCC (Berkeley Packet Filter Compiler Collection)
- Python packages: pandas, matplotlib, seaborn, plotly, numpy

## 📝 License

MIT License - see LICENSE file for details.

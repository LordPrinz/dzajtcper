#!/bin/bash

# DZAJTCPER - Main Control Script
# Unified interface for all monitoring and analysis operations

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

show_help() {
    echo -e "${CYAN}DZAJTCPER - Unified Control Script${NC}"
    echo ""
    echo -e "${YELLOW}USAGE:${NC}"
    echo "  ./run.sh <command> [options]"
    echo ""
    echo -e "${YELLOW}COMMANDS:${NC}"
    echo -e "  ${GREEN}monitor${NC} [--duration SECONDS]    Start eBPF monitoring"
    echo -e "  ${GREEN}analyze${NC} [FILE] [OPTIONS]        Analyze data with filters"
    echo -e "  ${GREEN}list${NC}                            List available sessions"
    echo -e "  ${GREEN}clean${NC}                           Clean empty sessions"
    echo -e "  ${GREEN}live${NC} [FILE]                     Live monitoring dashboard"
    echo -e "  ${GREEN}quick${NC} [--duration SECONDS]      Monitor + analyze (recommended)"
    echo -e "  ${GREEN}report${NC} [FILE] [FORMAT]          Generate comprehensive report"
    echo ""
    echo -e "${YELLOW}ANALYSIS OPTIONS:${NC}"
    echo "  --pid PID                        Filter by process ID"
    echo "  --saddr ADDRESS                  Filter by source address"
    echo "  --daddr ADDRESS                  Filter by destination address"
    echo "  --sport PORT                     Filter by source port"
    echo "  --dport PORT                     Filter by destination port"
    echo "  --cwnd-min VALUE                 Minimum CWND value"
    echo "  --cwnd-max VALUE                 Maximum CWND value"
    echo "  --charts TYPE1,TYPE2             Chart types: timeline,connections,heatmap,overview"
    echo "  --report FILENAME                Generate report (txt/html/json)"
    echo ""
    echo -e "${YELLOW}EXAMPLES:${NC}"
    echo -e "  ${BLUE}# Quick start (recommended)${NC}"
    echo "  ./run.sh quick --duration 30"
    echo ""
    echo -e "  ${BLUE}# Monitor for 2 minutes${NC}"
    echo "  ./run.sh monitor --duration 120"
    echo ""
    echo -e "  ${BLUE}# Analyze HTTPS traffic${NC}"
    echo "  ./run.sh analyze --dport 443 --charts timeline,connections"
    echo ""
    echo -e "  ${BLUE}# Analyze specific process${NC}"
    echo "  ./run.sh analyze --pid 1234 --report process_analysis.html"
    echo ""
    echo -e "  ${BLUE}# List and clean sessions${NC}"
    echo "  ./run.sh list"
    echo "  ./run.sh clean"
    echo ""
    echo -e "  ${BLUE}# Generate comprehensive report${NC}"
    echo "  ./run.sh report analysis_report.html"
}

if [[ $# -eq 0 ]] || [[ "$1" == "--help" ]] || [[ "$1" == "-h" ]]; then
    show_help
    exit 0
fi

COMMAND="$1"
shift

case "$COMMAND" in
    "monitor")
        echo -e "${GREEN}🔍 Starting TCP CWND monitoring...${NC}"
        if [[ "$1" == "--duration" ]]; then
            echo -e "${YELLOW}Duration: $2 seconds${NC}"
            sudo ./tcp_monitor.py monitor --duration "$2"
            if [[ -d "out" ]]; then
                sudo chown -R "$USER:$USER" out/
            fi
        else
            echo -e "${YELLOW}Monitoring indefinitely (Ctrl+C to stop)${NC}"
            sudo ./tcp_monitor.py monitor "$@"
            if [[ -d "out" ]]; then
                sudo chown -R "$USER:$USER" out/
            fi
        fi
        ;;
        
    "analyze")
        echo -e "${GREEN}📊 Analyzing TCP CWND data...${NC}"
        if [[ -d "out" ]]; then
            sudo chown -R "$USER:$USER" out/ 2>/dev/null || true
        fi
        ./tcp_monitor.py analyze "$@"
        echo -e "${GREEN}✅ Analysis complete!${NC}"
        ;;
        
    "list")
        echo -e "${GREEN}📋 Available sessions:${NC}"
        ./tcp_monitor.py analyze --list
        ;;
        
    "clean")
        echo -e "${GREEN}🧹 Cleaning empty sessions...${NC}"
        ./tcp_monitor.py analyze --clean
        echo -e "${GREEN}✅ Cleanup complete!${NC}"
        ;;
        
    "live")
        echo -e "${GREEN}📡 Starting live monitoring...${NC}"
        ./tcp_monitor.py live "$@"
        ;;
        
    "quick")
        echo -e "${GREEN}🚀 Quick start: Monitor + Analyze${NC}"
        DURATION=60
        if [[ "$1" == "--duration" ]]; then
            DURATION="$2"
            shift 2
        fi
        
        echo -e "${YELLOW}Step 1: Monitoring for $DURATION seconds...${NC}"
        sudo ./tcp_monitor.py monitor --duration "$DURATION"
        
        if [[ -d "out" ]]; then
            sudo chown -R "$USER:$USER" out/
        fi
        
        echo -e "${YELLOW}Step 2: Analyzing data...${NC}"
        ./tcp_monitor.py analyze "$@"
        
        echo -e "${GREEN}✅ Quick analysis complete!${NC}"
        echo -e "${CYAN}Check out/ directory for results${NC}"
        ;;
        
    "report")
        echo -e "${GREEN}📄 Generating comprehensive report...${NC}"
        if [[ -n "$1" ]]; then
            REPORT_FILE="$1"
            shift
        else
            REPORT_FILE="tcp_analysis_$(date +%Y%m%d_%H%M%S).html"
        fi
        
        if [[ -d "out" ]]; then
            sudo chown -R "$USER:$USER" out/ 2>/dev/null || true
        fi
        
        ./tcp_monitor.py analyze --report "$REPORT_FILE" "$@"
        echo -e "${GREEN}✅ Report saved as: $REPORT_FILE${NC}"
        ;;
        
    "help")
        show_help
        ;;
        
    *)
        echo -e "${RED}❌ Unknown command: $COMMAND${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

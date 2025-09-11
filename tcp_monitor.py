#!/usr/bin/env python3
"""
TCP CWND Monitor - Main CLI Interface
Unified command-line interface for TCP congestion window monitoring and analysis
"""

import argparse
import sys
import os
import signal
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data_loader import DataLoader
from src.data_filter import DataFilter
from src.visualizer import ChartGenerator
from src.monitor import LiveMonitor
from src.reporter import ReportGenerator


class TCPMonitorCLI:
    """Main CLI class for TCP CWND monitoring"""
    
    def __init__(self):
        from src.log_manager import LogManager
        
        self.log_manager = LogManager()
        self.csv_file = None
        self.ebpf_script = "tcp_cwnd_monitor.py"
        
    def run_ebpf_monitor(self, duration=None):
        """Start eBPF monitoring"""
        print("Starting eBPF TCP CWND monitoring...")
        
        self.csv_file = self.log_manager.get_new_log_path()
        
        if not os.path.exists(self.ebpf_script):
            print(f"Error: eBPF script {self.ebpf_script} not found!")
            print("Make sure the cwnd_tracer.py script is in the current directory.")
            return False
        
        try:
            import subprocess
            
            if duration:
                print(f"Monitoring for {duration} seconds...")
                result = subprocess.run(
                    [sys.executable, self.ebpf_script, self.csv_file],
                    timeout=duration,
                    capture_output=False
                )
            else:
                print("Monitoring indefinitely... Press Ctrl+C to stop")
                result = subprocess.run(
                    [sys.executable, self.ebpf_script, self.csv_file],
                    capture_output=False
                )
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print(f"\nMonitoring stopped after {duration} seconds")
            return True
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")
            return True
        except Exception as e:
            print(f"Error running eBPF monitor: {e}")
            return False
    
    def analyze_data(self, args):
        """Analyze existing data"""
        try:
            log_file = self.log_manager.select_log_file(args.file)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return False
            
        print(f"Analyzing data from: {log_file}")
        
        loader = DataLoader(log_file)
        if not loader.load_data():
            print("Error: Could not load data file")
            return False
        
        data = loader.get_data()
        print(f"Loaded {len(data)} records")
        
        if any([args.pid, args.saddr, args.daddr, args.sport, args.dport, args.cwnd_min, args.cwnd_max]):
            filter_obj = DataFilter(data)
            filters = {}
            
            if args.pid:
                filters['pid'] = args.pid
            if args.saddr:
                filters['saddr'] = args.saddr
            if args.daddr:
                filters['daddr'] = args.daddr
            if args.sport:
                filters['sport'] = args.sport
            if args.dport:
                filters['dport'] = args.dport
            if args.cwnd_min is not None:
                filters['cwnd_min'] = args.cwnd_min
            if args.cwnd_max is not None:
                filters['cwnd_max'] = args.cwnd_max
            
            filter_obj.apply_multiple_filters(**filters)
            data = filter_obj.get_data()
            print(f"After filtering: {len(data)} records")
        
        session_dir = os.path.dirname(log_file)
        
        from datetime import datetime
        analysis_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        analysis_dir = os.path.join(session_dir, f"analysis_{analysis_timestamp}")
        os.makedirs(analysis_dir, exist_ok=True)
        
        from src.visualizer import ChartGenerator
        chart_gen = ChartGenerator(data)
        
        chart_gen.generate_all_charts(analysis_dir, "chart")
        print(f"Charts generated in: {analysis_dir}/")
        
        if args.report:
            reporter = ReportGenerator(log_file)
            if args.report.endswith('.html'):
                format_type = 'html'
            elif args.report.endswith('.json'):
                format_type = 'json'
            else:
                format_type = 'text'
            
            report_filename = os.path.basename(args.report)
            report_path = os.path.join(analysis_dir, report_filename)
            reporter.save_report(report_path, format_type)
            print(f"Report saved as: {report_path}")
        
        return True
    
    def live_monitor(self, args):
        """Start live monitoring"""
        try:
            log_file = self.log_manager.select_log_file(args.file if hasattr(args, 'file') else None)
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return False
            
        print(f"Starting live monitoring of: {log_file}")
        
        monitor = LiveMonitor(log_file, args.interval)
        
        try:
            monitor.start_monitoring(
                plot_type=args.plot_type,
                max_connections=args.max_connections,
                max_records=args.max_records
            )
        except KeyboardInterrupt:
            print("\nLive monitoring stopped")
            monitor.stop_monitoring()
        
        return True
    
    def quick_start(self, args):
        """Quick start: monitor, then analyze"""
        print("=== QUICK START: TCP CWND MONITORING ===")
        
        duration = args.duration if args.duration else 60
        print(f"Step 1/3: Collecting data for {duration} seconds...")
        
        if not self.run_ebpf_monitor(duration):
            print("Failed to collect data")
            return False
        
        if not os.path.exists(self.csv_file):
            print(f"No data file found: {self.csv_file}")
            return False
        
        print("\nStep 2/3: Analyzing collected data...")
        loader = DataLoader(self.csv_file)
        if not loader.load_data():
            print("Could not load collected data")
            return False
        
        data = loader.get_data()
        print(f"Analyzed {len(data)} records from {data['connection'].nunique()} connections")
        
        print("\nStep 3/3: Generating overview charts...")
        chart_gen = ChartGenerator(data)
        
        session_dir = self.log_manager.get_session_dir()
        
        success = chart_gen.generate_all_charts("charts", "quick_analysis", session_dir)
        
        if success:
            charts_path = f"{session_dir}/charts" if session_dir else "charts/"
            print(f"✓ Charts generated successfully in {charts_path}")
        else:
            print("⚠ Some charts could not be generated")
        
        print("\n=== QUICK STATISTICS ===")
        print(f"Total Records: {len(data):,}")
        print(f"Unique Connections: {data['connection'].nunique():,}")
        print(f"Unique PIDs: {data['pid'].nunique():,}")
        print(f"CWND Range: {data['cwnd'].min()} - {data['cwnd'].max()} segments")
        print(f"Average CWND: {data['cwnd'].mean():.2f} segments")
        
        return True
    
    def main(self):
        """Main CLI entry point"""
        parser = argparse.ArgumentParser(
            description="TCP CWND Monitor - Comprehensive TCP congestion window monitoring and analysis",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s monitor                           # Start eBPF monitoring (indefinite)
  %(prog)s monitor --duration 300          # Monitor for 5 minutes
  %(prog)s analyze                         # Analyze latest log file
  %(prog)s analyze --list                  # List available log files
  %(prog)s analyze --file logs/cwnd_log_20240115_143025.csv  # Analyze specific file
  %(prog)s live                            # Start live analysis of latest log
  %(prog)s quick --duration 120            # Quick start: 2min monitor + analysis
  %(prog)s analyze --charts timeline connections --report report.html
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        monitor_parser = subparsers.add_parser('monitor', help='Start eBPF monitoring')
        monitor_parser.add_argument('--duration', type=int, help='Monitoring duration in seconds')
        
        analyze_parser = subparsers.add_parser('analyze', help='Analyze existing data')
        analyze_parser.add_argument('file', nargs='?', help='CSV file to analyze (auto-selects latest if not specified)')
        analyze_parser.add_argument('--list', action='store_true', help='List available log files')
        analyze_parser.add_argument('--clean', action='store_true', help='Clean empty session directories')
        analyze_parser.add_argument('--pid', type=int, help='Filter by PID')
        analyze_parser.add_argument('--saddr', help='Filter by source address')
        analyze_parser.add_argument('--daddr', help='Filter by destination address')
        analyze_parser.add_argument('--sport', type=int, help='Filter by source port')
        analyze_parser.add_argument('--dport', type=int, help='Filter by destination port')
        analyze_parser.add_argument('--cwnd-min', type=int, help='Minimum CWND value')
        analyze_parser.add_argument('--cwnd-max', type=int, help='Maximum CWND value')
        analyze_parser.add_argument('--charts', nargs='+', 
                                  choices=['timeline', 'connections', 'heatmap', 'overview'],
                                  help='Charts to generate')
        analyze_parser.add_argument('--report', help='Generate report file (.txt/.html/.json)')
        
        live_parser = subparsers.add_parser('live', help='Start live monitoring and analysis')
        live_parser.add_argument('--file', help='CSV file to monitor (auto-selects latest if not specified)')
        live_parser.add_argument('--interval', type=int, default=2, help='Update interval in seconds')
        live_parser.add_argument('--plot-type', choices=['timeline', 'connections', 'activity'], 
                               default='timeline', help='Type of live plot')
        live_parser.add_argument('--max-connections', type=int, default=5, help='Max connections to display')
        live_parser.add_argument('--max-records', type=int, default=200, help='Max records to keep in memory')
        
        quick_parser = subparsers.add_parser('quick', help='Quick start: monitor then analyze')
        quick_parser.add_argument('--duration', type=int, default=60, help='Monitoring duration in seconds')
        
        list_parser = subparsers.add_parser('list', help='List existing monitoring sessions')
        
        args = parser.parse_args()
        
        if not args.command:
            parser.print_help()
            return 1
        
        try:
            if args.command == 'monitor':
                success = self.run_ebpf_monitor(args.duration)
            elif args.command == 'analyze':
                if hasattr(args, 'list') and args.list:
                    self.log_manager.print_log_summary()
                    return 0
                elif hasattr(args, 'clean') and args.clean:
                    removed = self.log_manager.clean_empty_sessions()
                    print(f"Cleaned {removed} empty session directories")
                    return 0
                success = self.analyze_data(args)
            elif args.command == 'live':
                success = self.live_monitor(args)
            elif args.command == 'quick':
                success = self.quick_start(args)
            elif args.command == 'list':
                self.log_manager.print_log_summary()
                return 0
            else:
                print(f"Unknown command: {args.command}")
                return 1
            
            return 0 if success else 1
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            return 1
        except Exception as e:
            print(f"Error: {e}")
            return 1


if __name__ == "__main__":
    cli = TCPMonitorCLI()
    sys.exit(cli.main())

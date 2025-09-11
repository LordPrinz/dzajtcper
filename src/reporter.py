"""
Report Generator Module
Provides comprehensive analysis and reporting capabilities for TCP CWND data
"""

import pandas as pd
from datetime import datetime
import json
from typing import Dict, Any, Optional
from data_loader import DataLoader
from data_filter import DataFilter


class ReportGenerator:
    """Generates comprehensive analysis reports for TCP CWND data"""
    
    def __init__(self, csv_file: str = None):
        """
        Initialize ReportGenerator
        
        Args:
            csv_file: Path to the CSV file with data
        """
        if csv_file is None:
            from log_manager import get_default_log_file
            csv_file = get_default_log_file()
        self.csv_file = csv_file
        self.data_loader = DataLoader(csv_file)
        self.data_filter = None
        self.chart_generator = None
        
    def generate_summary_report(self, output_format: str = 'text') -> str:
        """
        Generate a comprehensive summary report
        
        Args:
            output_format: Output format ('text', 'json', 'html')
            
        Returns:
            str: Formatted report
        """
        if not self.data_loader.load_data():
            return "Error: Could not load data for analysis"
            
        data = self.data_loader.get_data()
        if data is None or len(data) == 0:
            return "No data available for analysis"
        
        stats = self._calculate_comprehensive_stats(data)
        
        if output_format == 'json':
            return json.dumps(stats, indent=2, default=str)
        elif output_format == 'html':
            return self._format_html_report(stats)
        else:
            return self._format_text_report(stats)
    
    def _calculate_comprehensive_stats(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive statistics from the data"""
        stats = {
            'general': {
                'total_records': len(data),
                'unique_connections': data['connection'].nunique(),
                'unique_pids': data['pid'].nunique(),
                'time_range': {
                    'start': data['timestamp'].min(),
                    'end': data['timestamp'].max(),
                    'duration_minutes': (data['timestamp'].max() - data['timestamp'].min()).total_seconds() / 60
                }
            },
            'cwnd_analysis': {
                'mean': float(data['cwnd'].mean()),
                'median': float(data['cwnd'].median()),
                'std': float(data['cwnd'].std()),
                'min': int(data['cwnd'].min()),
                'max': int(data['cwnd'].max()),
                'percentiles': {
                    '25th': float(data['cwnd'].quantile(0.25)),
                    '75th': float(data['cwnd'].quantile(0.75)),
                    '90th': float(data['cwnd'].quantile(0.90)),
                    '95th': float(data['cwnd'].quantile(0.95))
                }
            },
            'connection_analysis': self._analyze_connections(data),
            'pid_analysis': self._analyze_pids(data),
            'temporal_analysis': self._analyze_temporal_patterns(data),
            'performance_metrics': self._calculate_performance_metrics(data)
        }
        
        return stats
    
    def _analyze_connections(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze connection patterns"""
        conn_stats = {}
        
        top_connections = data['connection'].value_counts().head(10)
        conn_stats['most_active'] = {
            'connections': top_connections.to_dict(),
            'top_connection_percentage': (top_connections.iloc[0] / len(data)) * 100 if len(top_connections) > 0 else 0
        }
        
        cwnd_by_conn = data.groupby('connection')['cwnd'].agg(['mean', 'max', 'min', 'std']).fillna(0)
        conn_stats['cwnd_patterns'] = {
            'highest_avg_cwnd': {
                'connection': cwnd_by_conn['mean'].idxmax(),
                'value': float(cwnd_by_conn['mean'].max())
            },
            'highest_max_cwnd': {
                'connection': cwnd_by_conn['max'].idxmax(), 
                'value': int(cwnd_by_conn['max'].max())
            },
            'most_variable': {
                'connection': cwnd_by_conn['std'].idxmax(),
                'std_value': float(cwnd_by_conn['std'].max())
            }
        }
        
        return conn_stats
    
    def _analyze_pids(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze PID patterns"""
        pid_stats = {}
        
        pid_activity = data['pid'].value_counts().head(10)
        pid_stats['most_active_pids'] = pid_activity.to_dict()
        
        cwnd_by_pid = data.groupby('pid')['cwnd'].agg(['mean', 'max', 'count']).fillna(0)
        pid_stats['cwnd_by_pid'] = {
            'highest_avg': {
                'pid': int(cwnd_by_pid['mean'].idxmax()),
                'avg_cwnd': float(cwnd_by_pid['mean'].max())
            },
            'most_records': {
                'pid': int(cwnd_by_pid['count'].idxmax()),
                'record_count': int(cwnd_by_pid['count'].max())
            }
        }
        
        return pid_stats
    
    def _analyze_temporal_patterns(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Analyze temporal patterns in the data"""
        temporal_stats = {}
        
        data_copy = data.copy()
        data_copy['hour'] = data_copy['timestamp'].dt.hour
        data_copy['minute'] = data_copy['timestamp'].dt.minute
        
        hourly_activity = data_copy['hour'].value_counts().sort_index()
        temporal_stats['hourly_pattern'] = {
            'most_active_hour': int(hourly_activity.idxmax()),
            'activity_by_hour': hourly_activity.to_dict()
        }
        
        time_grouped = data_copy.groupby(data_copy['timestamp'].dt.floor('1min'))['cwnd'].agg(['mean', 'count'])
        temporal_stats['time_patterns'] = {
            'avg_records_per_minute': float(time_grouped['count'].mean()),
            'peak_activity_time': str(time_grouped['count'].idxmax()),
            'peak_activity_records': int(time_grouped['count'].max())
        }
        
        return temporal_stats
    
    def _calculate_performance_metrics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate performance-related metrics"""
        metrics = {}
        
        cwnd_changes = data.groupby('connection')['cwnd'].apply(lambda x: x.diff().dropna())
        
        if len(cwnd_changes) > 0:
            metrics['cwnd_dynamics'] = {
                'avg_change': float(cwnd_changes.mean()),
                'total_increases': int((cwnd_changes > 0).sum()),
                'total_decreases': int((cwnd_changes < 0).sum()),
                'largest_increase': int(cwnd_changes.max()) if not cwnd_changes.empty else 0,
                'largest_decrease': int(cwnd_changes.min()) if not cwnd_changes.empty else 0
            }
        else:
            metrics['cwnd_dynamics'] = {
                'avg_change': 0,
                'total_increases': 0,
                'total_decreases': 0,
                'largest_increase': 0,
                'largest_decrease': 0
            }
        
        conn_efficiency = data.groupby('connection').agg({
            'cwnd': ['mean', 'max', 'count'],
            'timestamp': lambda x: (x.max() - x.min()).total_seconds()
        }).fillna(0)
        
        conn_efficiency.columns = ['avg_cwnd', 'max_cwnd', 'record_count', 'duration_seconds']
        
        metrics['connection_efficiency'] = {
            'avg_duration_seconds': float(conn_efficiency['duration_seconds'].mean()),
            'avg_records_per_connection': float(conn_efficiency['record_count'].mean()),
            'most_efficient_connection': {
                'connection': conn_efficiency['avg_cwnd'].idxmax(),
                'avg_cwnd': float(conn_efficiency['avg_cwnd'].max())
            }
        }
        
        return metrics
    
    def _format_text_report(self, stats: Dict[str, Any]) -> str:
        """Format statistics as readable text report"""
        report = []
        report.append("="*60)
        report.append("TCP CWND ANALYSIS REPORT")
        report.append("="*60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        general = stats['general']
        report.append("GENERAL STATISTICS:")
        report.append("-" * 20)
        report.append(f"Total Records: {general['total_records']:,}")
        report.append(f"Unique Connections: {general['unique_connections']:,}")
        report.append(f"Unique PIDs: {general['unique_pids']:,}")
        report.append(f"Time Range: {general['time_range']['start']} to {general['time_range']['end']}")
        report.append(f"Duration: {general['time_range']['duration_minutes']:.1f} minutes")
        report.append("")
        
        cwnd = stats['cwnd_analysis']
        report.append("CWND ANALYSIS:")
        report.append("-" * 15)
        report.append(f"Mean CWND: {cwnd['mean']:.2f} segments")
        report.append(f"Median CWND: {cwnd['median']:.2f} segments")
        report.append(f"Standard Deviation: {cwnd['std']:.2f}")
        report.append(f"Range: {cwnd['min']} - {cwnd['max']} segments")
        report.append(f"95th Percentile: {cwnd['percentiles']['95th']:.2f} segments")
        report.append("")
        
        conn = stats['connection_analysis']
        report.append("CONNECTION ANALYSIS:")
        report.append("-" * 20)
        most_active = list(conn['most_active']['connections'].items())[0] if conn['most_active']['connections'] else ('N/A', 0)
        report.append(f"Most Active Connection: {most_active[0][:50]}... ({most_active[1]} records)")
        report.append(f"Top Connection Activity: {conn['most_active']['top_connection_percentage']:.1f}% of total")
        
        cwnd_patterns = conn['cwnd_patterns']
        report.append(f"Highest Avg CWND: {cwnd_patterns['highest_avg_cwnd']['value']:.2f} segments")
        report.append(f"Highest Max CWND: {cwnd_patterns['highest_max_cwnd']['value']} segments")
        report.append("")
        
        perf = stats['performance_metrics']
        report.append("PERFORMANCE METRICS:")
        report.append("-" * 20)
        cwnd_dyn = perf['cwnd_dynamics']
        report.append(f"CWND Increases: {cwnd_dyn['total_increases']:,}")
        report.append(f"CWND Decreases: {cwnd_dyn['total_decreases']:,}")
        report.append(f"Largest CWND Increase: {cwnd_dyn['largest_increase']} segments")
        report.append(f"Largest CWND Decrease: {cwnd_dyn['largest_decrease']} segments")
        
        conn_eff = perf['connection_efficiency']
        report.append(f"Avg Connection Duration: {conn_eff['avg_duration_seconds']:.1f} seconds")
        report.append(f"Avg Records per Connection: {conn_eff['avg_records_per_connection']:.1f}")
        report.append("")
        
        report.append("="*60)
        
        return "\n".join(report)
    
    def _format_html_report(self, stats: Dict[str, Any]) -> str:
        """Format statistics as HTML report"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>TCP CWND Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f8ff; padding: 20px; border-radius: 8px; }}
                .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 8px; }}
                .metric {{ margin: 10px 0; }}
                .value {{ font-weight: bold; color: #2c5aa0; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>TCP CWND Analysis Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="section">
                <h2>General Statistics</h2>
                <div class="metric">Total Records: <span class="value">{stats['general']['total_records']:,}</span></div>
                <div class="metric">Unique Connections: <span class="value">{stats['general']['unique_connections']:,}</span></div>
                <div class="metric">Unique PIDs: <span class="value">{stats['general']['unique_pids']:,}</span></div>
                <div class="metric">Duration: <span class="value">{stats['general']['time_range']['duration_minutes']:.1f} minutes</span></div>
            </div>
            
            <div class="section">
                <h2>CWND Analysis</h2>
                <div class="metric">Mean CWND: <span class="value">{stats['cwnd_analysis']['mean']:.2f} segments</span></div>
                <div class="metric">Median CWND: <span class="value">{stats['cwnd_analysis']['median']:.2f} segments</span></div>
                <div class="metric">Range: <span class="value">{stats['cwnd_analysis']['min']} - {stats['cwnd_analysis']['max']} segments</span></div>
                <div class="metric">95th Percentile: <span class="value">{stats['cwnd_analysis']['percentiles']['95th']:.2f} segments</span></div>
            </div>
            
            <div class="section">
                <h2>Performance Metrics</h2>
                <div class="metric">CWND Increases: <span class="value">{stats['performance_metrics']['cwnd_dynamics']['total_increases']:,}</span></div>
                <div class="metric">CWND Decreases: <span class="value">{stats['performance_metrics']['cwnd_dynamics']['total_decreases']:,}</span></div>
                <div class="metric">Avg Connection Duration: <span class="value">{stats['performance_metrics']['connection_efficiency']['avg_duration_seconds']:.1f} seconds</span></div>
            </div>
        </body>
        </html>
        """
        return html
    
    def save_report(self, filename: str, format: str = 'text') -> bool:
        """
        Save report to file
        
        Args:
            filename: Output filename
            format: Report format ('text', 'json', 'html')
            
        Returns:
            bool: True if saved successfully
        """
        try:
            report = self.generate_summary_report(format)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report)
            
            print(f"Report saved to: {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving report: {e}")
            return False
    
    def generate_filtered_report(self, filters: Dict[str, Any], 
                                output_file: Optional[str] = None) -> str:
        """
        Generate report for filtered data
        
        Args:
            filters: Dictionary of filters to apply
            output_file: Optional output file path
            
        Returns:
            str: Report content
        """
        data = self.data_loader.get_data()
        if data is None:
            return "No data available"
        
        filter_obj = DataFilter(data)
        filter_obj.apply_multiple_filters(**filters)
        filtered_data = filter_obj.get_data()
        
        if len(filtered_data) == 0:
            return "No data matches the specified filters"
        
        original_data = self.data_loader.data
        self.data_loader.data = filtered_data
        
        report = self.generate_summary_report('text')
        report = f"FILTERED REPORT\nFilters Applied: {filters}\n\n{report}"
        
        self.data_loader.data = original_data
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report)
            print(f"Filtered report saved to: {output_file}")
        
        return report

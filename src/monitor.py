"""
Live Monitor Module
Provides real-time monitoring capabilities with live data updates and visualization
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import pandas as pd
from datetime import datetime
from typing import Optional, Callable
from data_loader import DataLoader
from visualizer import ChartGenerator


class LiveMonitor:
    """Handles real-time monitoring and visualization of TCP CWND data"""
    
    def __init__(self, csv_file: str = None, update_interval: int = 2):
        """
        Initialize LiveMonitor
        
        Args:
            csv_file: Path to the CSV file being monitored
            update_interval: Update interval in seconds
        """
        if csv_file is None:
            from log_manager import get_default_log_file
            csv_file = get_default_log_file()
        self.csv_file = csv_file
        self.update_interval = update_interval
        self.data_loader = DataLoader(csv_file)
        self.is_running = False
        self.animation = None
        self.fig = None
        self.ax = None
        
    def start_monitoring(self, plot_type: str = 'timeline', 
                        max_connections: int = 5,
                        max_records: int = 200) -> None:
        """
        Start live monitoring with real-time plotting
        
        Args:
            plot_type: Type of plot ('timeline', 'distribution', 'activity')
            max_connections: Maximum number of connections to display
            max_records: Maximum number of records to keep in memory
        """
        print(f"Starting live monitoring... (updating every {self.update_interval}s)")
        print("Press Ctrl+C to stop")
        
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        self.is_running = True
        
        try:
            while self.is_running:
                if self.data_loader.load_live_data():
                    data = self.data_loader.get_data()
                    
                    if data is not None and len(data) > 0:
                        self._update_plot(data, plot_type, max_connections, max_records)
                
                time.sleep(self.update_interval)
                
        except KeyboardInterrupt:
            print("\nLive monitoring stopped")
            self.stop_monitoring()
    
    def _update_plot(self, data: pd.DataFrame, plot_type: str, 
                    max_connections: int, max_records: int) -> None:
        """Update the live plot with new data"""
        self.ax.clear()
        
        recent_data = data.tail(max_records)
        
        if plot_type == 'timeline':
            self._plot_timeline_live(recent_data, max_connections)
        elif plot_type == 'connections':
            self._plot_connections_live(recent_data)
        elif plot_type == 'activity':
            self._plot_activity_live(recent_data)
        
        plt.tight_layout()
        plt.draw()
        plt.pause(0.1)
    
    def _plot_timeline_live(self, data: pd.DataFrame, max_connections: int) -> None:
        """Plot timeline for live monitoring"""
        connections = data['connection'].value_counts().head(max_connections).index
        
        for i, conn in enumerate(connections):
            conn_data = data[data['connection'] == conn]
            label = conn[:30] + '...' if len(conn) > 30 else conn
            self.ax.plot(conn_data['timestamp'], conn_data['cwnd'], 
                        label=label, alpha=0.8, linewidth=2)
        
        self.ax.set_title(f'Live TCP CWND Monitor - {datetime.now().strftime("%H:%M:%S")}')
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('CWND (segments)')
        self.ax.legend(fontsize=8)
        self.ax.grid(True, alpha=0.3)
    
    def _plot_connections_live(self, data: pd.DataFrame) -> None:
        """Plot connections analysis for live monitoring"""
        top_connections = data['connection'].value_counts().head(5)
        
        self.ax.bar(range(len(top_connections)), top_connections.values)
        self.ax.set_title(f'Live Connection Activity - {datetime.now().strftime("%H:%M:%S")}')
        self.ax.set_xlabel('Connection Rank')
        self.ax.set_ylabel('Number of Records')
        
        labels = [conn[:20] + '...' if len(conn) > 20 else conn for conn in top_connections.index]
        self.ax.set_xticks(range(len(top_connections)))
        self.ax.set_xticklabels(labels, rotation=45, ha='right')
        
        self.ax.grid(True, alpha=0.3)
    
    def _plot_activity_live(self, data: pd.DataFrame) -> None:
        """Plot connection activity for live monitoring"""
        connection_counts = data['connection'].value_counts().head(10)
        
        if len(connection_counts) > 0:
            y_pos = range(len(connection_counts))
            labels = [conn[:25] + '...' if len(conn) > 25 else conn for conn in connection_counts.index]
            
            self.ax.barh(y_pos, connection_counts.values)
            self.ax.set_yticks(y_pos)
            self.ax.set_yticklabels(labels)
            self.ax.set_title(f'Live Connection Activity - {datetime.now().strftime("%H:%M:%S")}')
            self.ax.set_xlabel('Number of Records')
    
    def stop_monitoring(self) -> None:
        """Stop live monitoring"""
        self.is_running = False
        plt.ioff()
        if self.fig:
            plt.close(self.fig)
    
    def monitor_with_callback(self, callback: Callable[[pd.DataFrame], None],
                             check_interval: int = 1) -> None:
        """
        Monitor data and call callback function when new data arrives
        
        Args:
            callback: Function to call with new data
            check_interval: Interval to check for new data (seconds)
        """
        print(f"Starting monitoring with callback... (checking every {check_interval}s)")
        print("Press Ctrl+C to stop")
        
        self.is_running = True
        
        try:
            while self.is_running:
                if self.data_loader.load_live_data():
                    data = self.data_loader.get_data()
                    if data is not None and len(data) > 0:
                        callback(data)
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\nCallback monitoring stopped")
            self.is_running = False
    
    def get_live_stats(self) -> dict:
        """
        Get current statistics from live data
        
        Returns:
            dict: Current statistics
        """
        if self.data_loader.load_live_data():
            data = self.data_loader.get_data()
            if data is not None and len(data) > 0:
                return {
                    'timestamp': datetime.now(),
                    'total_records': len(data),
                    'unique_connections': data['connection'].nunique(),
                    'unique_pids': data['pid'].nunique(),
                    'avg_cwnd': data['cwnd'].mean(),
                    'max_cwnd': data['cwnd'].max(),
                    'min_cwnd': data['cwnd'].min(),
                    'latest_records': data.tail(5).to_dict('records')
                }
        
        return {'error': 'No data available'}
    
    def create_live_dashboard(self, output_file: str = "live_dashboard.html",
                            refresh_interval: int = 5) -> bool:
        """
        Create a simple HTML dashboard for live monitoring
        
        Args:
            output_file: Output HTML file path
            refresh_interval: Auto-refresh interval in seconds
            
        Returns:
            bool: True if dashboard created successfully
        """
        try:
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>TCP CWND Live Dashboard</title>
                <meta http-equiv="refresh" content="{refresh_interval}">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; }}
                    .stats {{ background-color:
                    .record {{ background-color:
                </style>
            </head>
            <body>
                <h1>TCP CWND Live Dashboard</h1>
                <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <div class="stats">
                    <h2>Current Statistics</h2>
                    <div id="stats-content">
                        Loading...
                    </div>
                </div>
                
                <script>
                    // Auto-refresh functionality
                    setTimeout(function() {{
                        location.reload();
                    }}, {refresh_interval * 1000});
                </script>
            </body>
            </html>
            """
            
            with open(output_file, 'w') as f:
                f.write(html_content)
            
            print(f"Live dashboard created: {output_file}")
            return True
            
        except Exception as e:
            print(f"Error creating live dashboard: {e}")
            return False

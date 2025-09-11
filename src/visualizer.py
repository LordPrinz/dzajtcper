"""
Visualizer Module
Generates various types of charts and visualizations for TCP CWND data
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import pandas as pd
import numpy as np
import os
from datetime import datetime
from typing import Optional, List, Tuple

try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.offline as pyo
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class ChartGenerator:
    """Generates various types of charts for TCP CWND data visualization"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize ChartGenerator
        
        Args:
            data: DataFrame containing TCP CWND data
        """
        self.data = data
        self.setup_style()
    
    def setup_style(self):
        """Set up matplotlib and seaborn styling"""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def plot_timeline(self, save_path: Optional[str] = None, 
                     interactive: bool = False, 
                     max_connections: int = 10) -> bool:
        """
        Plot CWND evolution over time
        
        Args:
            save_path: Path to save the chart (without extension)
            interactive: Whether to create interactive Plotly chart
            max_connections: Maximum number of connections to display
            
        Returns:
            bool: True if chart was generated successfully
        """
        if self.data is None or len(self.data) == 0:
            print("No data to plot")
            return False
        
        try:
            if interactive and PLOTLY_AVAILABLE:
                return self._plot_timeline_interactive(save_path, max_connections)
            else:
                return self._plot_timeline_static(save_path, max_connections)
        except Exception as e:
            print(f"Error generating timeline chart: {e}")
            return False
    
    def _plot_timeline_interactive(self, save_path: Optional[str], 
                                 max_connections: int) -> bool:
        """Generate interactive timeline chart using Plotly"""
        fig = px.line(self.data, x='timestamp', y='cwnd', color='connection',
                     title='TCP Congestion Window Over Time',
                     labels={'cwnd': 'Congestion Window (segments)', 'timestamp': 'Time'})
        
        fig.update_layout(
            hovermode='x unified',
            xaxis_title="Time",
            yaxis_title="CWND (segments)",
            legend_title="Connections",
            width=1200,
            height=600
        )
        
        if save_path:
            fig.write_html(save_path + "_timeline_interactive.html")
            print(f"Interactive timeline saved to {save_path}_timeline_interactive.html")
        else:
            fig.show()
        
        return True
    
    def _plot_timeline_static(self, save_path: Optional[str], 
                            max_connections: int) -> bool:
        """Generate static timeline chart using matplotlib"""
        plt.figure(figsize=(15, 8))
        
        connections = self.data['connection'].value_counts().head(max_connections).index
        
        distinct_colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        
        for i, conn in enumerate(connections):
            conn_data = self.data[self.data['connection'] == conn]
            label = conn[:50] + '...' if len(conn) > 50 else conn
            color = distinct_colors[i % len(distinct_colors)]
            plt.plot(conn_data['timestamp'], conn_data['cwnd'], 
                    label=label, color=color, alpha=0.8, linewidth=2.5)
        
        plt.title('TCP Congestion Window Evolution Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('CWND (segments)', fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path + "_timeline.png", dpi=300, bbox_inches='tight')
            print(f"Timeline chart saved to {save_path}_timeline.png")
        else:
            plt.show()
        
        plt.close()
        return True
    
    def plot_connection_analysis(self, save_path: Optional[str] = None) -> bool:
        """
        Generate connection-focused analysis charts
        
        Args:
            save_path: Path to save the chart (without extension)
            
        Returns:
            bool: True if chart was generated successfully
        """
        if self.data is None or len(self.data) == 0:
            print("No data to plot")
            return False
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            
            top_connections = self.data['connection'].value_counts().head(10)
            top_connections.plot(kind='barh', ax=axes[0,0])
            axes[0,0].set_title('Most Active Connections', fontweight='bold')
            axes[0,0].set_xlabel('Number of Records')
            
            for conn in top_connections.head(5).index:
                conn_data = self.data[self.data['connection'] == conn]
                if len(conn_data) > 1:
                    label = conn[:30] + '...' if len(conn) > 30 else conn
                    axes[0,1].plot(conn_data['timestamp'], conn_data['cwnd'], 
                                  label=label, alpha=0.8, linewidth=2)
            
            axes[0,1].set_title('CWND Evolution - Top 5 Connections', fontweight='bold')
            axes[0,1].set_xlabel('Time')
            axes[0,1].set_ylabel('CWND (segments)')
            axes[0,1].legend(fontsize=8)
            axes[0,1].grid(True, alpha=0.3)
            
            port_data = self.data.groupby('dport')['cwnd'].agg(['count', 'mean', 'max']).reset_index()
            port_data = port_data.sort_values('count', ascending=False).head(10)
            
            if len(port_data) > 0:
                axes[1,0].bar(port_data['dport'].astype(str), port_data['count'])
                axes[1,0].set_title('Activity by Destination Port', fontweight='bold')
                axes[1,0].set_xlabel('Destination Port')
                axes[1,0].set_ylabel('Number of Records')
                axes[1,0].tick_params(axis='x', rotation=45)
            
            pid_data = self.data.groupby('pid')['cwnd'].agg(['count', 'mean']).reset_index()
            pid_data = pid_data.sort_values('count', ascending=False).head(10)
            
            if len(pid_data) > 0:
                scatter = axes[1,1].scatter(pid_data['count'], pid_data['mean'], 
                                           s=100, alpha=0.7, c=range(len(pid_data)), cmap='viridis')
                axes[1,1].set_title('Process Analysis: Activity vs Avg CWND', fontweight='bold')
                axes[1,1].set_xlabel('Number of Records')
                axes[1,1].set_ylabel('Average CWND')
                
                for i, row in pid_data.iterrows():
                    axes[1,1].annotate(f'PID {row["pid"]}', 
                                      (row['count'], row['mean']), 
                                      xytext=(5, 5), textcoords='offset points', fontsize=8)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path + "_connections.png", dpi=300, bbox_inches='tight')
                print(f"Connection analysis saved to {save_path}_connections.png")
            else:
                plt.show()
            
            plt.close()
            return True
            
        except Exception as e:
            print(f"Error generating connection analysis: {e}")
            return False
    
    def plot_heatmap(self, save_path: Optional[str] = None, 
                    time_interval: str = '1min') -> bool:
        """
        Generate CWND heatmap over time for different connections
        
        Args:
            save_path: Path to save the chart (without extension)
            time_interval: Time interval for aggregation (e.g., '1min', '5min', '1h')
            
        Returns:
            bool: True if chart was generated successfully
        """
        if self.data is None or len(self.data) == 0:
            print("No data to plot")
            return False
        
        try:
            top_connections = self.data['connection'].value_counts().head(10).index
            filtered_data = self.data[self.data['connection'].isin(top_connections)]
            
            pivot_data = filtered_data.set_index('timestamp').groupby('connection').resample(time_interval)['cwnd'].mean().unstack(level=0).fillna(0)
            
            if len(pivot_data) == 0:
                print("No data available for heatmap")
                return False
            
            plt.figure(figsize=(15, 8))
            sns.heatmap(pivot_data.T, cmap='YlOrRd', cbar_kws={'label': 'Average CWND'})
            plt.title(f'CWND Heatmap Over Time ({time_interval} intervals)', fontweight='bold')
            plt.xlabel('Time')
            plt.ylabel('Connections')
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path + "_heatmap.png", dpi=300, bbox_inches='tight')
                print(f"Heatmap saved to {save_path}_heatmap.png")
            else:
                plt.show()
            
            plt.close()
            return True
            
        except Exception as e:
            print(f"Error generating heatmap: {e}")
            return False
    
    def generate_all_charts(self, output_dir: str, prefix: str = "analysis", session_dir: Optional[str] = None) -> bool:
        """
        Generate all available chart types
        
        Args:
            output_dir: Directory to save charts (session directory)
            prefix: Prefix for output filenames
            session_dir: Deprecated parameter for backward compatibility
            
        Returns:
            bool: True if all charts were generated successfully
        """
        charts_dir = output_dir
            
        if not os.path.exists(charts_dir):
            os.makedirs(charts_dir)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_path = os.path.join(charts_dir, f"{prefix}_{timestamp}")
        
        success = True
        
        print("Generating charts...")
        
        if not self.plot_timeline(base_path):
            success = False
        
        if not self.plot_connection_analysis(base_path):
            success = False
        
        if not self.plot_heatmap(base_path):
            success = False
        
        if PLOTLY_AVAILABLE:
            if not self.plot_timeline(base_path, interactive=True):
                success = False
        
        return success

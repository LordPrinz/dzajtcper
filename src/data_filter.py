"""
Data Filter Module
Provides advanced filtering capabilities for TCP CWND data
"""

import pandas as pd
from typing import Optional, List, Union
from datetime import datetime


class DataFilter:
    """Handles filtering of TCP CWND data based on various criteria"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize DataFilter
        
        Args:
            data: DataFrame containing TCP CWND data
        """
        self.original_data = data.copy()
        self.filtered_data = data.copy()
        self.active_filters = {}
    
    def filter_by_pid(self, pids: Union[int, List[int]]) -> 'DataFilter':
        """
        Filter data by process ID(s)
        
        Args:
            pids: Single PID or list of PIDs to include
            
        Returns:
            DataFilter: Self for method chaining
        """
        if isinstance(pids, int):
            pids = [pids]
        
        self.filtered_data = self.filtered_data[self.filtered_data['pid'].isin(pids)]
        self.active_filters['pid'] = pids
        return self
    
    def filter_by_address(self, saddr: Optional[str] = None, 
                         daddr: Optional[str] = None) -> 'DataFilter':
        """
        Filter data by source and/or destination addresses
        
        Args:
            saddr: Source address pattern (regex supported)
            daddr: Destination address pattern (regex supported)
            
        Returns:
            DataFilter: Self for method chaining
        """
        if saddr:
            self.filtered_data = self.filtered_data[
                self.filtered_data['saddr'].str.contains(saddr, na=False, regex=True)
            ]
            self.active_filters['saddr'] = saddr
        
        if daddr:
            self.filtered_data = self.filtered_data[
                self.filtered_data['daddr'].str.contains(daddr, na=False, regex=True)
            ]
            self.active_filters['daddr'] = daddr
        
        return self
    
    def filter_by_port(self, sport: Optional[Union[int, List[int]]] = None,
                      dport: Optional[Union[int, List[int]]] = None) -> 'DataFilter':
        """
        Filter data by source and/or destination ports
        
        Args:
            sport: Source port(s) to include
            dport: Destination port(s) to include
            
        Returns:
            DataFilter: Self for method chaining
        """
        if sport is not None:
            if isinstance(sport, int):
                sport = [sport]
            self.filtered_data = self.filtered_data[self.filtered_data['sport'].isin(sport)]
            self.active_filters['sport'] = sport
        
        if dport is not None:
            if isinstance(dport, int):
                dport = [dport]
            self.filtered_data = self.filtered_data[self.filtered_data['dport'].isin(dport)]
            self.active_filters['dport'] = dport
        
        return self
    
    def filter_by_connection(self, connection_pattern: str) -> 'DataFilter':
        """
        Filter data by connection string pattern
        
        Args:
            connection_pattern: Pattern to match in connection strings (regex supported)
            
        Returns:
            DataFilter: Self for method chaining
        """
        self.filtered_data = self.filtered_data[
            self.filtered_data['connection'].str.contains(connection_pattern, na=False, regex=True)
        ]
        self.active_filters['connection'] = connection_pattern
        return self
    
    def filter_by_cwnd_range(self, min_cwnd: Optional[int] = None,
                           max_cwnd: Optional[int] = None) -> 'DataFilter':
        """
        Filter data by CWND value range
        
        Args:
            min_cwnd: Minimum CWND value (inclusive)
            max_cwnd: Maximum CWND value (inclusive)
            
        Returns:
            DataFilter: Self for method chaining
        """
        if min_cwnd is not None:
            self.filtered_data = self.filtered_data[self.filtered_data['cwnd'] >= min_cwnd]
            self.active_filters['min_cwnd'] = min_cwnd
        
        if max_cwnd is not None:
            self.filtered_data = self.filtered_data[self.filtered_data['cwnd'] <= max_cwnd]
            self.active_filters['max_cwnd'] = max_cwnd
        
        return self
    
    def filter_by_time_range(self, start_time: Optional[datetime] = None,
                           end_time: Optional[datetime] = None) -> 'DataFilter':
        """
        Filter data by time range
        
        Args:
            start_time: Start of time range (inclusive)
            end_time: End of time range (inclusive)
            
        Returns:
            DataFilter: Self for method chaining
        """
        if start_time is not None:
            self.filtered_data = self.filtered_data[self.filtered_data['timestamp'] >= start_time]
            self.active_filters['start_time'] = start_time
        
        if end_time is not None:
            self.filtered_data = self.filtered_data[self.filtered_data['timestamp'] <= end_time]
            self.active_filters['end_time'] = end_time
        
        return self
    
    def filter_top_connections(self, top_n: int = 10) -> 'DataFilter':
        """
        Keep only the top N most active connections
        
        Args:
            top_n: Number of top connections to keep
            
        Returns:
            DataFilter: Self for method chaining
        """
        top_connections = self.filtered_data['connection'].value_counts().head(top_n).index
        self.filtered_data = self.filtered_data[self.filtered_data['connection'].isin(top_connections)]
        self.active_filters['top_connections'] = top_n
        return self
    
    def filter_top_pids(self, top_n: int = 10) -> 'DataFilter':
        """
        Keep only the top N most active PIDs
        
        Args:
            top_n: Number of top PIDs to keep
            
        Returns:
            DataFilter: Self for method chaining
        """
        top_pids = self.filtered_data['pid'].value_counts().head(top_n).index
        self.filtered_data = self.filtered_data[self.filtered_data['pid'].isin(top_pids)]
        self.active_filters['top_pids'] = top_n
        return self
    
    def filter_recent_data(self, minutes: int = 60) -> 'DataFilter':
        """
        Keep only data from the last N minutes
        
        Args:
            minutes: Number of minutes to keep from the most recent timestamp
            
        Returns:
            DataFilter: Self for method chaining
        """
        if len(self.filtered_data) > 0:
            latest_time = self.filtered_data['timestamp'].max()
            cutoff_time = latest_time - pd.Timedelta(minutes=minutes)
            self.filtered_data = self.filtered_data[self.filtered_data['timestamp'] >= cutoff_time]
            self.active_filters['recent_minutes'] = minutes
        
        return self
    
    def get_data(self) -> pd.DataFrame:
        """
        Get the filtered data
        
        Returns:
            pandas.DataFrame: The filtered data
        """
        return self.filtered_data
    
    def get_original_data(self) -> pd.DataFrame:
        """
        Get the original unfiltered data
        
        Returns:
            pandas.DataFrame: The original data
        """
        return self.original_data
    
    def reset_filters(self) -> 'DataFilter':
        """
        Reset all filters and restore original data
        
        Returns:
            DataFilter: Self for method chaining
        """
        self.filtered_data = self.original_data.copy()
        self.active_filters = {}
        return self
    
    def get_active_filters(self) -> dict:
        """
        Get currently active filters
        
        Returns:
            dict: Dictionary of active filters and their values
        """
        return self.active_filters.copy()
    
    def get_filter_summary(self) -> dict:
        """
        Get summary of filtering results
        
        Returns:
            dict: Summary statistics about the filtering
        """
        return {
            'original_records': len(self.original_data),
            'filtered_records': len(self.filtered_data),
            'reduction_percent': (1 - len(self.filtered_data) / len(self.original_data)) * 100 if len(self.original_data) > 0 else 0,
            'active_filters': self.active_filters,
            'unique_connections_filtered': self.filtered_data['connection'].nunique() if len(self.filtered_data) > 0 else 0,
            'unique_pids_filtered': self.filtered_data['pid'].nunique() if len(self.filtered_data) > 0 else 0
        }
    
    def apply_multiple_filters(self, **filters) -> 'DataFilter':
        """
        Apply multiple filters at once
        
        Args:
            **filters: Keyword arguments for various filters
                      (pid, saddr, daddr, sport, dport, connection, 
                       min_cwnd, max_cwnd, start_time, end_time)
        
        Returns:
            DataFilter: Self for method chaining
        """
        if 'pid' in filters:
            self.filter_by_pid(filters['pid'])
        
        if 'saddr' in filters or 'daddr' in filters:
            self.filter_by_address(filters.get('saddr'), filters.get('daddr'))
        
        if 'sport' in filters or 'dport' in filters:
            self.filter_by_port(filters.get('sport'), filters.get('dport'))
        
        if 'connection' in filters:
            self.filter_by_connection(filters['connection'])
        
        if 'min_cwnd' in filters or 'max_cwnd' in filters:
            self.filter_by_cwnd_range(filters.get('min_cwnd'), filters.get('max_cwnd'))
        
        if 'start_time' in filters or 'end_time' in filters:
            self.filter_by_time_range(filters.get('start_time'), filters.get('end_time'))
        
        return self

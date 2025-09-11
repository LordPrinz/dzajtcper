"""
Data Loader Module
Handles loading and preprocessing of TCP CWND data from CSV files
"""

import pandas as pd
import os
import io
from datetime import datetime
from typing import Optional, Tuple


class DataLoader:
    """Handles loading TCP CWND data from CSV files"""
    
    def __init__(self, csv_file: str = None):
        """
        Initialize DataLoader
        
        Args:
            csv_file: Path to the CSV file containing TCP CWND data
        """
        if csv_file is None:
            from log_manager import get_default_log_file
            csv_file = get_default_log_file()
        self.csv_file = csv_file
        self.data = None
        self.last_read_position = 0
        
    def load_data(self, tail_lines: Optional[int] = None) -> bool:
        """
        Load data from CSV file
        
        Args:
            tail_lines: If specified, read only the last N lines
            
        Returns:
            bool: True if data loaded successfully, False otherwise
        """
        try:
            if tail_lines:
                df = pd.read_csv(self.csv_file, nrows=tail_lines)
            else:
                df = pd.read_csv(self.csv_file)
            
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp')
            
            df['connection'] = (df['saddr'].astype(str) + ':' + df['sport'].astype(str) + 
                              ' -> ' + df['daddr'].astype(str) + ':' + df['dport'].astype(str))
            
            self.data = df
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def load_live_data(self) -> bool:
        """
        Load new data since last read for live monitoring
        
        Returns:
            bool: True if new data was loaded, False otherwise
        """
        try:
            if not os.path.exists(self.csv_file):
                return False
                
            file_size = os.path.getsize(self.csv_file)
            
            if file_size <= self.last_read_position:
                return False
                
            with open(self.csv_file, 'r') as f:
                f.seek(self.last_read_position)
                new_lines = f.readlines()
                self.last_read_position = f.tell()
            
            if not new_lines:
                return False
            
            new_data = pd.read_csv(io.StringIO(''.join(new_lines)), 
                                 header=None if self.data is not None else 0)
            
            if self.data is None:
                new_data.columns = ['timestamp', 'pid', 'saddr', 'sport', 'daddr', 'dport', 'cwnd']
                self.data = new_data
            else:
                new_data.columns = ['timestamp', 'pid', 'saddr', 'sport', 'daddr', 'dport', 'cwnd']
                self.data = pd.concat([self.data, new_data], ignore_index=True)
            
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
            self.data['connection'] = (self.data['saddr'].astype(str) + ':' + 
                                     self.data['sport'].astype(str) + ' -> ' + 
                                     self.data['daddr'].astype(str) + ':' + 
                                     self.data['dport'].astype(str))
            
            if len(self.data) > 1000:
                self.data = self.data.tail(1000).reset_index(drop=True)
            
            return True
            
        except Exception as e:
            print(f"Error loading live data: {e}")
            return False
    
    def get_data(self) -> Optional[pd.DataFrame]:
        """
        Get the loaded data
        
        Returns:
            pandas.DataFrame or None: The loaded data
        """
        return self.data
    
    def get_data_info(self) -> dict:
        """
        Get information about the loaded data
        
        Returns:
            dict: Information about the data (size, columns, etc.)
        """
        if self.data is None:
            return {"status": "No data loaded"}
        
        return {
            "total_records": len(self.data),
            "columns": list(self.data.columns),
            "time_range": {
                "start": self.data['timestamp'].min(),
                "end": self.data['timestamp'].max()
            },
            "unique_connections": self.data['connection'].nunique(),
            "unique_pids": self.data['pid'].nunique(),
            "memory_usage": f"{self.data.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB"
        }
    
    def validate_data(self) -> Tuple[bool, list]:
        """
        Validate the loaded data for completeness and correctness
        
        Returns:
            Tuple[bool, list]: (is_valid, list_of_issues)
        """
        if self.data is None:
            return False, ["No data loaded"]
        
        issues = []
        
        required_columns = ['timestamp', 'pid', 'saddr', 'sport', 'daddr', 'dport', 'cwnd']
        missing_columns = [col for col in required_columns if col not in self.data.columns]
        if missing_columns:
            issues.append(f"Missing columns: {missing_columns}")
        
        null_counts = self.data.isnull().sum()
        if null_counts.any():
            issues.append(f"Null values found: {null_counts[null_counts > 0].to_dict()}")
        
        try:
            pd.to_datetime(self.data['timestamp'])
        except:
            issues.append("Invalid timestamp format")
        
        if 'cwnd' in self.data.columns:
            invalid_cwnd = (self.data['cwnd'] < 0) | (self.data['cwnd'] > 100000)
            if invalid_cwnd.any():
                issues.append(f"Invalid CWND values: {invalid_cwnd.sum()} records")
        
        return len(issues) == 0, issues

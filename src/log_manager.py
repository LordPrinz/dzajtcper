
"""
Log Manager for TCP CWND Monitor
Manages log files in logs/ directory with timestamped names
"""

import os
import glob
from datetime import datetime
from typing import Optional, List


class LogManager:
    """Manages TCP CWND log files with timestamps and automatic selection"""
    
    def __init__(self, output_dir: str = "out"):
        self.output_dir = output_dir
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_new_log_path(self) -> str:
        """Get path for new log file with timestamp in organized directory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        session_dir = os.path.join(self.output_dir, f"session_{timestamp}")
        os.makedirs(session_dir, exist_ok=True)
        
        self.current_session_timestamp = timestamp
        self.current_session_dir = session_dir
        
        return os.path.join(session_dir, f"cwnd_log.csv")
    
    def get_session_dir(self) -> Optional[str]:
        """Get current session directory"""
        return getattr(self, 'current_session_dir', None)
    
    def get_session_timestamp(self) -> Optional[str]:
        """Get current session timestamp"""
        return getattr(self, 'current_session_timestamp', None)
    
    def get_latest_log_path(self) -> Optional[str]:
        """Get path to the most recent log file"""
        log_files = self.list_log_files()
        if not log_files:
            return None
        
        log_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return log_files[0]
    
    def list_log_files(self) -> List[str]:
        """List all log files in output directory"""
        pattern = os.path.join(self.output_dir, "session_*", "cwnd_log.csv")
        return glob.glob(pattern)
    
    def get_log_info(self) -> List[dict]:
        """Get information about all log files"""
        log_files = self.list_log_files()
        info = []
        
        for log_file in log_files:
            stat = os.stat(log_file)
            info.append({
                'path': log_file,
                'name': os.path.basename(log_file),
                'size': stat.st_size,
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'size_mb': round(stat.st_size / 1024 / 1024, 2)
            })
        
        info.sort(key=lambda x: x['modified'], reverse=True)
        return info
    
    def select_log_file(self, file_arg: Optional[str] = None) -> str:
        """
        Select appropriate log file based on argument or auto-selection
        
        Args:
            file_arg: Specific file path from command line argument
            
        Returns:
            str: Path to selected log file
        """
        if file_arg:
            if not os.path.dirname(file_arg):
                potential_path = os.path.join(self.output_dir, file_arg)
                if os.path.exists(potential_path):
                    return potential_path
            return file_arg
        
        latest = self.get_latest_log_path()
        if latest:
            return latest
        
        raise FileNotFoundError("No log files found. Please run monitoring first.")
    
    def print_log_summary(self):
        """Print summary of available session directories"""
        sessions = self.list_session_directories()
        
        if not sessions:
            print("No session directories found in out/ directory")
            return
        
        print(f"\nAvailable sessions in {self.output_dir}/:")
        print("-" * 80)
        print(f"{'Session':<30} {'CSV File':<15} {'Charts':<10} {'Modified':<20}")
        print("-" * 80)
        
        for session_dir in sessions:
            csv_path = os.path.join(session_dir, 'cwnd_log.csv')
            if os.path.exists(csv_path):
                stat = os.stat(csv_path)
                size_mb = round(stat.st_size / (1024 * 1024), 2)
                modified = datetime.fromtimestamp(stat.st_mtime)
                
                chart_count = len([f for f in os.listdir(session_dir) 
                                 if f.endswith(('.png', '.html'))])
                
                session_name = os.path.basename(session_dir)
                print(f"{session_name:<30} {size_mb:>6} MB {chart_count:>5} {modified.strftime('%Y-%m-%d %H:%M:%S')}")
        
        print(f"\nLatest session: {os.path.basename(sessions[0]) if sessions else 'None'}")
    
    def list_session_directories(self):
        """List all session directories sorted by creation time (newest first)"""
        if not os.path.exists(self.output_dir):
            return []
        
        sessions = []
        for item in os.listdir(self.output_dir):
            session_path = os.path.join(self.output_dir, item)
            if os.path.isdir(session_path) and item.startswith('session_'):
                sessions.append(session_path)
        
        sessions.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        return sessions
    
    def clean_empty_sessions(self):
        """Remove empty session directories"""
        if not os.path.exists(self.output_dir):
            return 0
        
        removed_count = 0
        for item in os.listdir(self.output_dir):
            session_path = os.path.join(self.output_dir, item)
            if os.path.isdir(session_path) and item.startswith('session_'):
                contents = os.listdir(session_path)
                if not contents:
                    try:
                        os.rmdir(session_path)
                        print(f"Removed empty session: {item}")
                        removed_count += 1
                    except Exception as e:
                        print(f"Error removing {item}: {e}")
        
        return removed_count
    
    def clean_old_logs(self, keep_count: int = 10):
        """Keep only the most recent N log files"""
        log_info = self.get_log_info()
        
        if len(log_info) <= keep_count:
            return
        
        to_remove = log_info[keep_count:]
        for info in to_remove:
            try:
                os.remove(info['path'])
                print(f"Removed old log: {info['name']}")
            except Exception as e:
                print(f"Error removing {info['name']}: {e}")


log_manager = LogManager()


def get_default_log_file(file_arg: Optional[str] = None) -> str:
    """
    Get the default log file path, auto-selecting latest if no argument provided
    
    Args:
        file_arg: Optional specific file path
        
    Returns:
        str: Path to log file to use
    """
    return log_manager.select_log_file(file_arg)

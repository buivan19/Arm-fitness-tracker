"""
Performance Monitor for Fitness Tracking Application
Tracks FPS, memory usage, and end-to-end latency.
Outputs to terminal and logs to file.
"""

import time
import psutil
import threading
from collections import deque
from datetime import datetime
import json


class PerformanceMonitor:
    """Monitor FPS, memory usage, and latency in real-time."""
    
    def __init__(self, window_size=30, log_to_file=True, terminal_interval=2.0):
        """
        Initialize the performance monitor.
        
        Args:
            window_size: Number of samples to keep for averaging (default: 30)
            log_to_file: Whether to log metrics to a file (default: True)
            terminal_interval: Seconds between terminal prints (default: 2.0)
        """
        # FPS tracking
        self.frame_times = deque(maxlen=window_size)
        self.last_frame_time = None
        
        # Latency tracking (end-to-end processing time)
        self.latencies = deque(maxlen=window_size)
        self.frame_start_time = None
        
        # Memory tracking
        self.process = psutil.Process()
        self.memory_samples = deque(maxlen=window_size)
        
        # Terminal output
        self.terminal_interval = terminal_interval
        self.last_terminal_print = time.time()
        
        # Logging
        self.log_to_file = log_to_file
        self.log_file = f"performance_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self._init_log_file()
        
        # Thread safety
        self.lock = threading.Lock()
        
    def _init_log_file(self):
        """Initialize the CSV log file with headers."""
        if self.log_to_file:
            try:
                with open(self.log_file, 'w') as f:
                    f.write("timestamp,fps,avg_latency_ms,min_latency_ms,max_latency_ms,memory_mb\n")
            except Exception as e:
                print(f"Error creating log file: {e}")
        
    def start_frame(self):
        """Call this at the start of frame processing."""
        self.frame_start_time = time.time()
        
    def end_frame(self):
        """Call this at the end of frame processing."""
        if self.frame_start_time is None:
            return
            
        current_time = time.time()
        
        with self.lock:
            # Calculate latency (end-to-end processing time)
            latency = (current_time - self.frame_start_time) * 1000  # Convert to ms
            self.latencies.append(latency)
            
            # Calculate FPS
            if self.last_frame_time is not None:
                frame_time = current_time - self.last_frame_time
                self.frame_times.append(frame_time)
            
            self.last_frame_time = current_time
            
            # Sample memory
            self.memory_samples.append(self.process.memory_info().rss / 1024 / 1024)  # MB
            
        # Print to terminal periodically
        if (current_time - self.last_terminal_print) >= self.terminal_interval:
            self._print_to_terminal()
            self.last_terminal_print = current_time
            
            # Also log to file
            if self.log_to_file:
                self._log_to_csv()
            
    def get_metrics(self):
        """
        Get current performance metrics.
        
        Returns:
            dict: Dictionary containing FPS, latency, and memory metrics
        """
        with self.lock:
            metrics = {
                'fps': 0.0,
                'avg_latency_ms': 0.0,
                'min_latency_ms': 0.0,
                'max_latency_ms': 0.0,
                'memory_mb': 0.0,
                'timestamp': datetime.now().isoformat()
            }
            
            # Calculate FPS
            if len(self.frame_times) > 0:
                avg_frame_time = sum(self.frame_times) / len(self.frame_times)
                metrics['fps'] = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
            
            # Calculate latency stats
            if len(self.latencies) > 0:
                metrics['avg_latency_ms'] = sum(self.latencies) / len(self.latencies)
                metrics['min_latency_ms'] = min(self.latencies)
                metrics['max_latency_ms'] = max(self.latencies)
            
            # Memory usage
            if len(self.memory_samples) > 0:
                metrics['memory_mb'] = sum(self.memory_samples) / len(self.memory_samples)
                
            return metrics
    
    def _print_to_terminal(self):
        """Print current metrics to terminal."""
        metrics = self.get_metrics()
        print(f"\n[Performance] {metrics['timestamp']}")
        print(f"  FPS: {metrics['fps']:.1f}")
        print(f"  Latency: avg={metrics['avg_latency_ms']:.1f}ms, "
              f"min={metrics['min_latency_ms']:.1f}ms, max={metrics['max_latency_ms']:.1f}ms")
        print(f"  Memory: {metrics['memory_mb']:.1f} MB")
    
    def _log_to_csv(self):
        """Append current metrics to CSV log file."""
        metrics = self.get_metrics()
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"{metrics['timestamp']},"
                       f"{metrics['fps']:.2f},"
                       f"{metrics['avg_latency_ms']:.2f},"
                       f"{metrics['min_latency_ms']:.2f},"
                       f"{metrics['max_latency_ms']:.2f},"
                       f"{metrics['memory_mb']:.2f}\n")
        except Exception as e:
            print(f"Error writing to log file: {e}")
    
    def reset(self):
        """Reset all metrics."""
        with self.lock:
            self.frame_times.clear()
            self.latencies.clear()
            self.memory_samples.clear()
            self.last_frame_time = None
            self.frame_start_time = None
            print("Performance monitor reset")


# Example integration with existing tracker
class TrackerWithMonitoring:
    """Wrapper to add performance monitoring to any tracker."""
    
    def __init__(self, tracker, terminal_interval=2.0):
        """
        Args:
            tracker: The exercise tracker instance (BicepsCurlTracker, etc.)
            terminal_interval: Seconds between terminal outputs (default: 2.0)
        """
        self.tracker = tracker
        self.perf_monitor = PerformanceMonitor(terminal_interval=terminal_interval)
    
    def process_frame(self, frame):
        """Process frame with performance monitoring."""
        self.perf_monitor.start_frame()
        
        # Call the original tracker's process_frame
        result = self.tracker.process_frame(frame)
        
        self.perf_monitor.end_frame()
        
        return result
    
    def reset(self):
        """Reset both tracker and performance monitor."""
        self.tracker.reset()
        self.perf_monitor.reset()
    
    def __getattr__(self, name):
        """Forward any other attribute access to the wrapped tracker."""
        return getattr(self.tracker, name)


if __name__ == "__main__":
    # Demo usage
    print("Performance Monitor Demo")
    print("=" * 60)
    
    monitor = PerformanceMonitor(terminal_interval=1.0)
    
    print("\nSimulating 50 frames at ~30 FPS...")
    print("Watch for terminal output every 1 second\n")
    
    for i in range(50):
        monitor.start_frame()
        
        # Simulate some processing
        time.sleep(0.033)  # ~30 FPS
        
        monitor.end_frame()
    
    print("\n" + "=" * 60)
    print(f"Performance log saved to: {monitor.log_file}")
    print("=" * 60)
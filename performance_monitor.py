import time
import psutil
import threading
from collections import deque
from datetime import datetime
import json

# BIẾN ĐIỀU KHIỂN CHÍNH: Chuyển thành True khi muốn bật lại
ENABLE_PERFORMANCE_MONITOR = False 

class PerformanceMonitor:
    def __init__(self, window_size=30, log_to_file=False, terminal_interval=2.0):
        self.enabled = ENABLE_PERFORMANCE_MONITOR
        
        # Nếu bị tắt, dừng khởi tạo các cấu trúc dữ liệu nặng
        if not self.enabled:
            return

        # FPS tracking
        self.frame_times = deque(maxlen=window_size)
        self.last_frame_time = None
        
        # Latency tracking
        self.latencies = deque(maxlen=window_size)
        self.frame_start_time = None
        
        # Memory tracking
        self.process = psutil.Process()
        self.memory_samples = deque(maxlen=window_size)
        
        # Output control
        self.terminal_interval = terminal_interval
        self.last_terminal_print = time.time()
        
        # Logging
        self.log_to_file = log_to_file
        self.log_file = f"performance_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self._init_log_file()
        
        self.lock = threading.Lock()
        
    def _init_log_file(self):
        if self.enabled and self.log_to_file:
            try:
                with open(self.log_file, 'w') as f:
                    f.write("timestamp,fps,avg_latency_ms,min_latency_ms,max_latency_ms,memory_mb\n")
            except Exception as e:
                print(f"Error creating log file: {e}")
        
    def start_frame(self):
        if not self.enabled: return
        self.frame_start_time = time.time()
        
    def end_frame(self):
        if not self.enabled or self.frame_start_time is None:
            return
            
        current_time = time.time()
        with self.lock:
            latency = (current_time - self.frame_start_time) * 1000
            self.latencies.append(latency)
            if self.last_frame_time is not None:
                self.frame_times.append(current_time - self.last_frame_time)
            self.last_frame_time = current_time
            self.memory_samples.append(self.process.memory_info().rss / 1024 / 1024)
            
        if (current_time - self.last_terminal_print) >= self.terminal_interval:
            self._print_to_terminal()
            self.last_terminal_print = current_time
            if self.log_to_file:
                self._log_to_csv()
            
    def get_metrics(self):
        if not self.enabled: return {}
        with self.lock:
            metrics = {'fps': 0.0, 'avg_latency_ms': 0.0, 'memory_mb': 0.0, 'timestamp': datetime.now().isoformat()}
            if len(self.frame_times) > 0:
                metrics['fps'] = 1.0 / (sum(self.frame_times) / len(self.frame_times))
            if len(self.memory_samples) > 0:
                metrics['memory_mb'] = sum(self.memory_samples) / len(self.memory_samples)
            return metrics
    
    def _print_to_terminal(self):
        if not self.enabled: return
        m = self.get_metrics()
        print(f"\n[Performance] {m['fps']:.1f} FPS | {m['memory_mb']:.1f} MB")
    
    def _log_to_csv(self):
        if not self.enabled: return

class TrackerWithMonitoring:
    def __init__(self, tracker, terminal_interval=2.0):
        self.tracker = tracker
        self.enabled = ENABLE_PERFORMANCE_MONITOR
        # Chỉ tạo đối tượng monitor nếu thực sự cần thiết
        if self.enabled:
            self.perf_monitor = PerformanceMonitor(terminal_interval=terminal_interval)
    
    def process_frame(self, frame):
        if not self.enabled:
            return self.tracker.process_frame(frame)
            
        self.perf_monitor.start_frame()
        result = self.tracker.process_frame(frame)
        self.perf_monitor.end_frame()
        return result
    
    def reset(self):
        self.tracker.reset()
        if self.enabled:
            self.perf_monitor.reset()

    def __getattr__(self, name):
        return getattr(self.tracker, name)
"""
IEC 61131-3 inspired Task Scheduler
Supports cyclic and event-driven tasks with priorities, core affinity, and watchdog monitoring.
"""

import time
import threading
from typing import Callable, Optional, List, Dict, Any
from enum import IntEnum
from dataclasses import dataclass, field #noqa: F401
import os


class TaskPriority(IntEnum):
    """Task priority levels (higher number = higher priority)"""
    IDLE = 0
    LOW = 1
    BELOW_NORMAL = 2
    NORMAL = 3
    ABOVE_NORMAL = 4
    HIGH = 5
    REALTIME = 6


class TaskState(IntEnum):
    """Task execution states"""
    CREATED = 0
    READY = 1
    RUNNING = 2
    SUSPENDED = 3
    ERROR = 4
    STOPPED = 5


class TaskType(IntEnum):
    """Task types according to IEC 61131-3"""
    CYCLIC = 0      # Periodic execution with fixed interval
    FREE = 1        # Continuous execution (as fast as possible)
    EVENT = 2        # Event-triggered execution


class WatchdogAction(IntEnum):
    """Actions to take when watchdog is triggered"""
    NONE = 0      # No action, silent
    WARNING = 1   # Log warning only
    SUSPEND = 2   # Suspend task execution
    STOP = 3      # Stop task completely


@dataclass
class TaskStatistics:
    """Statistics for task execution"""
    executions: int = 0
    total_time: float = 0.0  # Total execution time in seconds
    sum_squared_time: float = 0.0  # Sum of squared execution times for std dev
    min_time: float = float('inf')
    max_time: float = 0.0
    avg_time: float = 0.0
    std_dev: float = 0.0  # Standard deviation
    jitter: float = 0.0  # Max - Min time difference
    last_execution: float = 0.0
    overruns: int = 0  # Count of cycle time violations
    watchdog_triggers: int = 0
    watchdog_consecutive: int = 0  # Consecutive watchdog triggers


class Task:
    """
    IEC 61131-3 inspired Task class
    
    Args:
        name: Task name
        function: Callable to execute
        task_type: CYCLIC, FREEWHEELING, or EVENT
        interval_ms: Cycle time in milliseconds (for CYCLIC tasks)
        priority: Task priority (0-6)
        cpu_affinity: List of CPU cores to run on (None = any core)
        watchdog_ms: Watchdog timeout in milliseconds (0 = disabled)
        watchdog_action: Action when watchdog triggers (NONE, SUSPEND, STOP)
        watchdog_sensitivity: Number of consecutive timeouts before action (0 = disabled, 1+ = enabled)
        autostart: Start task immediately
    """
    
    def __init__(
        self,
        name: str,
        function: Callable,
        task_type: TaskType = TaskType.CYCLIC,
        interval_ms: float = 100.0,
        priority: TaskPriority = TaskPriority.NORMAL,
        cpu_affinity: Optional[List[int]] = None,
        watchdog_ms: float = 0.0,
        watchdog_action: WatchdogAction = WatchdogAction.NONE,
        watchdog_sensitivity: int = 1,
        autostart: bool = False
    ):
        self.name = name
        self.function = function
        self.task_type = task_type
        self.interval_ms = interval_ms
        self.priority = priority
        self.cpu_affinity = cpu_affinity
        self.watchdog_ms = watchdog_ms
        self.watchdog_action = watchdog_action
        self.watchdog_sensitivity = max(0, watchdog_sensitivity)  # 0 = disabled
        
        # Thread-safe state management
        self._state_lock = threading.Lock()
        self._state = TaskState.CREATED
        
        # Thread-safe statistics
        self._stats_lock = threading.Lock()
        self.statistics = TaskStatistics()
        
        # Thread-safe timing
        self._timing_lock = threading.Lock()
        self._last_cycle_time = 0.0
        
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._event_trigger = threading.Event()
        self._watchdog_exceeded = False
        self._execution_id = 0  # Unique ID for each execution
        self._current_execution_id = 0  # ID of currently running execution
        
        if autostart:
            self.start()
    
    @property
    def state(self) -> TaskState:
        """Thread-safe state getter"""
        with self._state_lock:
            return self._state
    
    @state.setter
    def state(self, value: TaskState):
        """Thread-safe state setter"""
        with self._state_lock:
            self._state = value
    
    def start(self):
        """Start task execution"""
        if self.state == TaskState.RUNNING:
            return
        
        self._stop_event.clear()
        self._event_trigger.clear()
        self.state = TaskState.READY
        
        self._thread = threading.Thread(target=self._run, name=f"Task_{self.name}", daemon=True)
        self._thread.start()
        
        # Set CPU affinity if specified (Windows/Linux)
        if self.cpu_affinity is not None:
            try:
                if os.name == 'nt':  # Windows
                    import ctypes
                    import ctypes.wintypes
                    
                    # Wait for thread to be fully initialized
                    time.sleep(0.05)
                    
                    kernel32 = ctypes.windll.kernel32
                    
                    # Properly declare OpenThread
                    kernel32.OpenThread.argtypes = [ctypes.wintypes.DWORD, ctypes.wintypes.BOOL, ctypes.wintypes.DWORD]
                    kernel32.OpenThread.restype = ctypes.wintypes.HANDLE
                    
                    # Properly declare SetThreadAffinityMask
                    kernel32.SetThreadAffinityMask.argtypes = [ctypes.wintypes.HANDLE, ctypes.c_size_t]
                    kernel32.SetThreadAffinityMask.restype = ctypes.c_size_t
                    
                    # Properly declare CloseHandle
                    kernel32.CloseHandle.argtypes = [ctypes.wintypes.HANDLE]
                    kernel32.CloseHandle.restype = ctypes.wintypes.BOOL
                    
                    THREAD_SET_INFORMATION = 0x0020
                    THREAD_QUERY_INFORMATION = 0x0040
                    
                    # Get thread handle using native_id
                    thread_handle = kernel32.OpenThread(
                        THREAD_SET_INFORMATION | THREAD_QUERY_INFORMATION,
                        False,
                        self._thread.native_id
                    )
                    
                    if thread_handle:
                        # Create affinity mask from core list
                        affinity_mask = sum(1 << core for core in self.cpu_affinity)
                        result = kernel32.SetThreadAffinityMask(thread_handle, affinity_mask)
                        kernel32.CloseHandle(thread_handle)
                        
                        if result == 0:
                            print(f"Warning: SetThreadAffinityMask failed for task '{self.name}'")
                    else:
                        print(f"Warning: Could not open thread handle for task '{self.name}' (TID: {self._thread.native_id})")
                else:  # Linux/Unix
                    import psutil
                    p = psutil.Process()
                    p.cpu_affinity(self.cpu_affinity)
            except Exception as e:
                print(f"Warning: Could not set CPU affinity for task '{self.name}': {e}")
    
    def stop(self):
        """Stop task execution"""
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2.0)
        self.state = TaskState.STOPPED
    
    def suspend(self):
        """Suspend task execution (can be resumed)"""
        self.state = TaskState.SUSPENDED
    
    def resume(self):
        """Resume suspended task"""
        if self.state == TaskState.SUSPENDED:
            self.state = TaskState.READY
    
    def trigger(self):
        """Trigger event for EVENT type tasks"""
        if self.task_type == TaskType.EVENT:
            self._event_trigger.set()
    
    def reset_statistics(self):
        """Reset task statistics - THREAD SAFE"""
        with self._stats_lock:
            self.statistics = TaskStatistics()
    
    def _run(self):
        """Main task execution loop"""
        with self._timing_lock:
            self._last_cycle_time = time.time()
        
        while not self._stop_event.is_set():
            # Check suspend state BEFORE waiting/executing
            if self.state == TaskState.SUSPENDED:
                time.sleep(0.01)
                continue
            
            # Wait for trigger based on task type
            if self.task_type == TaskType.CYCLIC:
                # Wait for next cycle
                sleep_time = self.interval_ms / 1000.0
                time.sleep(sleep_time)
                
                # Check again after sleep in case suspend was called during sleep
                if self.state == TaskState.SUSPENDED:
                    continue
                    
            elif self.task_type == TaskType.EVENT:
                # Wait for event trigger
                self._event_trigger.wait(timeout=0.1)
                if not self._event_trigger.is_set():
                    continue
                self._event_trigger.clear()
                
                # Check suspend state after event
                if self.state == TaskState.SUSPENDED:
                    continue
            # FREEWHEELING: No wait, execute as fast as possible
            
            # Final suspend check before execution
            if self.state == TaskState.SUSPENDED:
                continue
            
            # Check cycle time overrun (for CYCLIC tasks)
            if self.task_type == TaskType.CYCLIC:
                with self._timing_lock:
                    current_time = time.time()
                    actual_cycle_time = (current_time - self._last_cycle_time) * 1000.0
                    self._last_cycle_time = current_time
                
                expected_cycle_time = self.interval_ms
                
                if actual_cycle_time > expected_cycle_time * 1.1:  # 10% tolerance
                    with self._stats_lock:
                        self.statistics.overruns += 1
            
            # Execute task function with watchdog monitoring
            self.state = TaskState.RUNNING
            execution_start = time.time()
            self._watchdog_exceeded = False
            
            # Increment execution ID for this run
            self._execution_id += 1
            current_exec_id = self._execution_id
            self._current_execution_id = current_exec_id
            
            try:
                # Start watchdog thread if enabled
                watchdog_thread = None
                if self.watchdog_ms > 0:
                    watchdog_thread = threading.Thread(
                        target=self._watchdog_monitor,
                        args=(execution_start, current_exec_id),
                        daemon=True
                    )
                    watchdog_thread.start()
                
                # Execute user function
                self.function()
                
                # IMPORTANT: Set state to READY immediately after function completes
                # to prevent false watchdog triggers
                self.state = TaskState.READY
                
                # Calculate execution time
                execution_time = time.time() - execution_start
                self._update_statistics(execution_time)
                
                # Reset watchdog consecutive counter on successful execution
                if not self._watchdog_exceeded:
                    with self._stats_lock:
                        self.statistics.watchdog_consecutive = 0
                
                # Check if watchdog triggered stop action
                if self._stop_event.is_set():
                    break
                
            except Exception as e:
                self.state = TaskState.ERROR
                import traceback
                print(f"Task '{self.name}' error: {e}")
                print("Full traceback:")
                traceback.print_exc()
                execution_time = time.time() - execution_start
                self._update_statistics(execution_time)
    
    def _watchdog_monitor(self, start_time: float, execution_id: int):
        """Monitor task execution for watchdog timeout"""
        timeout_sec = self.watchdog_ms / 1000.0
        time.sleep(timeout_sec)
        
        # Check if task is still running AND this is still the current execution
        if self.state == TaskState.RUNNING and self._current_execution_id == execution_id:
            self._watchdog_exceeded = True
            
            with self._stats_lock:
                self.statistics.watchdog_triggers += 1
                self.statistics.watchdog_consecutive += 1
                consecutive = self.statistics.watchdog_consecutive
            
            # Output warning only for WARNING, SUSPEND, and STOP actions
            if self.watchdog_action in (WatchdogAction.WARNING, WatchdogAction.SUSPEND, WatchdogAction.STOP):
                print(f"WATCHDOG: Task '{self.name}' exceeded {self.watchdog_ms}ms timeout! "
                      f"(Consecutive: {consecutive})")
            
            # Check if sensitivity threshold is reached
            if self.watchdog_sensitivity > 0 and consecutive >= self.watchdog_sensitivity:
                
                if self.watchdog_action == WatchdogAction.SUSPEND:
                    print(f"WATCHDOG: Suspending task '{self.name}' after "
                          f"{self.statistics.watchdog_consecutive} consecutive timeouts")
                    self.state = TaskState.SUSPENDED
                    # Give main loop time to see the state change
                    time.sleep(0.001)
                    
                elif self.watchdog_action == WatchdogAction.STOP:
                    print(f"WATCHDOG: Stopping task '{self.name}' after "
                          f"{self.statistics.watchdog_consecutive} consecutive timeouts")
                    self._stop_event.set()
                    self.state = TaskState.STOPPED
    
    def _update_statistics(self, execution_time: float):
        """Update task statistics - THREAD SAFE"""
        with self._stats_lock:
            self.statistics.executions += 1
            self.statistics.total_time += execution_time
            self.statistics.sum_squared_time += execution_time * execution_time
            self.statistics.last_execution = execution_time
            
            if execution_time < self.statistics.min_time:
                self.statistics.min_time = execution_time
            if execution_time > self.statistics.max_time:
                self.statistics.max_time = execution_time
            
            if self.statistics.executions > 0:
                self.statistics.avg_time = self.statistics.total_time / self.statistics.executions
                
                # Calculate standard deviation: sqrt((sum(x^2) / n) - (sum(x) / n)^2)
                mean_of_squares = self.statistics.sum_squared_time / self.statistics.executions
                square_of_mean = self.statistics.avg_time * self.statistics.avg_time
                variance = mean_of_squares - square_of_mean
                self.statistics.std_dev = variance ** 0.5 if variance > 0 else 0.0
            
            # Calculate jitter (difference between max and min)
            if self.statistics.max_time != 0.0 and self.statistics.min_time != float('inf'):
                self.statistics.jitter = self.statistics.max_time - self.statistics.min_time
    
    def get_info(self) -> Dict[str, Any]:
        """Get task information and statistics - THREAD SAFE"""
        # Create snapshot of statistics under lock
        with self._stats_lock:
            # Calculate overrun ratio
            overrun_ratio = 0.0
            if self.statistics.executions > 0:
                overrun_ratio = (self.statistics.overruns / self.statistics.executions) * 100.0
            
            stats_snapshot = {
                'executions': self.statistics.executions,
                'avg_time_ms': self.statistics.avg_time * 1000.0,
                'std_dev_ms': self.statistics.std_dev * 1000.0,
                'min_time_ms': self.statistics.min_time * 1000.0 if self.statistics.min_time != float('inf') else 0.0,
                'max_time_ms': self.statistics.max_time * 1000.0,
                'jitter_ms': self.statistics.jitter * 1000.0,
                'overruns': self.statistics.overruns,
                'overrun_ratio_pct': overrun_ratio,
                'watchdog_triggers': self.statistics.watchdog_triggers,
                'watchdog_consecutive': self.statistics.watchdog_consecutive
            }
        
        return {
            'name': self.name,
            'type': self.task_type.name,
            'state': self.state.name,
            'priority': self.priority.name,
            'interval_ms': self.interval_ms,
            'cpu_affinity': self.cpu_affinity,
            'watchdog_ms': self.watchdog_ms,
            'watchdog_action': self.watchdog_action.name,
            'watchdog_sensitivity': self.watchdog_sensitivity,
            'statistics': stats_snapshot
        }


class Scheduler:
    """
    Task Scheduler for managing multiple tasks
    """
    
    def __init__(self):
        self.tasks: List[Task] = []
        self._lock = threading.Lock()
    
    def add_task(self, task: Task):
        """Add a task to the scheduler"""
        with self._lock:
            self.tasks.append(task)
            # Sort by priority (higher priority first)
            self.tasks.sort(key=lambda t: t.priority, reverse=True)
    
    def remove_task(self, task_name: str):
        """Remove a task by name"""
        with self._lock:
            for task in self.tasks:
                if task.name == task_name:
                    task.stop()
                    self.tasks.remove(task)
                    break
    
    def get_task(self, task_name: str) -> Optional[Task]:
        """Get a task by name"""
        with self._lock:
            for task in self.tasks:
                if task.name == task_name:
                    return task
        return None
    
    def start_all(self):
        """Start all tasks"""
        with self._lock:
            for task in self.tasks:
                task.start()
    
    def stop_all(self):
        """Stop all tasks"""
        with self._lock:
            for task in self.tasks:
                task.stop()
    
    def get_status(self) -> List[Dict[str, Any]]:
        """Get status of all tasks"""
        with self._lock:
            return [task.get_info() for task in self.tasks]
    
    def print_status(self):
        """Print formatted status of all tasks"""
        status = self.get_status()
        
        print("=" * 175)
        print(f"{'Task Name':<20} {'Type':<12} {'State':<10} {'Prio':<10} {'Interval':<10} {'Exec':<8} {'Avg(ms)':<10} {'StdDev':<10} {'Min(ms)':<10} {'Max(ms)':<10} {'Jitter':<10} {'Overruns':<10} {'OR %':<8} {'WD Trig':<10}")
        print("=" * 175)
        
        for info in status:
            stats = info['statistics']
            interval = f"{info['interval_ms']:.0f}ms" if info['type'] == 'CYCLIC' else "-"
            
            print(
                f"{info['name']:<20} "
                f"{info['type']:<12} "
                f"{info['state']:<10} "
                f"{info['priority']:<10} "
                f"{interval:<10} "
                f"{stats['executions']:<8} "
                f"{stats['avg_time_ms']:<10.2f} "
                f"{stats['std_dev_ms']:<10.2f} "
                f"{stats['min_time_ms']:<10.2f} "
                f"{stats['max_time_ms']:<10.2f} "
                f"{stats['jitter_ms']:<10.2f} "
                f"{stats['overruns']:<10} "
                f"{stats['overrun_ratio_pct']:<8.1f} "
                f"{stats['watchdog_triggers']:<10}"
            )
        
        print("=" * 175)


# Example usage and testing
if __name__ == "__main__":
    import random
    
    def fast_task():
        """Fast task (< 1ms)"""
        x = sum(range(100))
    
    def medium_task():
        """Medium task (~10ms)"""
        time.sleep(0.01)
    
    def slow_task():
        """Slow task (~50ms)"""
        time.sleep(0.05)
    
    def event_task():
        """Event-triggered task"""
        print(f"[{time.time():.2f}] Event task triggered!")
    
    # Create scheduler
    scheduler = Scheduler()
    
    # Add tasks with different priorities and configurations
    task1 = Task(
        name="FastCyclic",
        function=fast_task,
        task_type=TaskType.CYCLIC,
        interval_ms=10.0,
        priority=TaskPriority.HIGH,
        watchdog_ms=5.0
    )
    
    task2 = Task(
        name="MediumCyclic",
        function=medium_task,
        task_type=TaskType.CYCLIC,
        interval_ms=50.0,
        priority=TaskPriority.NORMAL,
        watchdog_ms=20.0
    )
    
    task3 = Task(
        name="SlowCyclic",
        function=slow_task,
        task_type=TaskType.CYCLIC,
        interval_ms=100.0,
        priority=TaskPriority.LOW,
        watchdog_ms=100.0,
        cpu_affinity=[0]  # Run on CPU core 0
    )
    
    task4 = Task(
        name="EventTask",
        function=event_task,
        task_type=TaskType.EVENT,
        priority=TaskPriority.ABOVE_NORMAL
    )
    
    # Add tasks to scheduler
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)
    scheduler.add_task(task4)
    
    # Start all tasks
    print("Starting scheduler...")
    scheduler.start_all()
    
    # Run for a while and trigger events
    time.sleep(2.0)
    
    # Trigger event task a few times
    for i in range(3):
        task4.trigger()
        time.sleep(0.5)
    
    time.sleep(2.0)
    
    # Print status
    scheduler.print_status()
    
    # Stop all tasks
    print("\nStopping scheduler...")
    scheduler.stop_all()
    
    print("Done!")

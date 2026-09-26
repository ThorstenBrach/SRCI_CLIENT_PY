"""
Scheduler mit Visualisierung der Task-Laufzeiten über die Zeit
"""

from RobotLibrary.IEC_Scheduler import Task, Scheduler, TaskType, TaskPriority, WatchdogAction
import time
import matplotlib.pyplot as plt
from collections import defaultdict
import threading


# Globale History für Aufzeichnung
execution_history = defaultdict(list)
time_history = defaultdict(list)
history_lock = threading.Lock()
start_time = None


def record_execution(task_name: str, execution_time: float, timestamp: float):
    """Zeichnet Ausführungszeit und Zeitstempel auf"""
    with history_lock:
        execution_history[task_name].append(execution_time * 1000.0)  # in ms
        time_history[task_name].append(timestamp)


def create_wrapper(task_name: str, original_function):
    """Erstellt einen Wrapper um die Task-Funktion für Logging"""
    def wrapper():
        exec_start = time.time()
        original_function()
        exec_time = time.time() - exec_start
        timestamp = time.time() - (start_time or 0)
        record_execution(task_name, exec_time, timestamp)
    return wrapper


def fast_task():
    """Schnelle Task - 10ms Target"""
    x = 1.0
    for _ in range(10000):
        x = x * 1.0000001


def medium_task():
    """Mittlere Task - 20ms Target"""
    x = 1.0
    for _ in range(20000):
        x = x * 1.0000001


def slow_task():
    """Langsame Task - 50ms Target"""
    x = 1.0
    for _ in range(50000):
        x = x * 1.0000001


def plot_execution_times():
    """Zeigt die Ausführungszeiten als Kurven an"""
    plt.figure(figsize=(14, 8))
    
    # Plot 1: Alle Tasks in einem Diagramm
    plt.subplot(2, 1, 1)
    colors = {'Fast': 'blue', 'Medium': 'green', 'Slow': 'red'}
    
    for task_name in execution_history:
        times = time_history[task_name]
        exec_times = execution_history[task_name]
        plt.plot(times, exec_times, label=task_name, color=colors.get(task_name, 'gray'), 
                 alpha=0.6, linewidth=0.5)
        
        # Gleitender Durchschnitt (50 Samples)
        if len(exec_times) > 50:
            window = 50
            moving_avg = [sum(exec_times[i:i+window])/window 
                         for i in range(len(exec_times)-window)]
            moving_times = times[window:]
            plt.plot(moving_times, moving_avg, label=f'{task_name} (Avg)', 
                    color=colors.get(task_name, 'gray'), linewidth=2)
    
    plt.xlabel('Zeit (s)')
    plt.ylabel('Ausführungszeit (ms)')
    plt.title('Task-Ausführungszeiten über die Zeit (mit gleitendem Durchschnitt)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 2: Histogramm der Ausführungszeiten
    plt.subplot(2, 1, 2)
    for task_name in execution_history:
        exec_times = execution_history[task_name]
        plt.hist(exec_times, bins=50, alpha=0.5, label=task_name, 
                color=colors.get(task_name, 'gray'))
    
    plt.xlabel('Ausführungszeit (ms)')
    plt.ylabel('Häufigkeit')
    plt.title('Verteilung der Ausführungszeiten')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def print_statistics():
    """Gibt Statistiken aus"""
    print("\n" + "="*80)
    print("Statistik der aufgezeichneten Ausführungszeiten:")
    print("="*80)
    print(f"{'Task':<15} {'Count':<10} {'Min(ms)':<12} {'Avg(ms)':<12} {'Max(ms)':<12} {'StdDev(ms)':<12}")
    print("-"*80)
    
    for task_name in sorted(execution_history.keys()):
        exec_times = execution_history[task_name]
        if exec_times:
            import statistics
            count = len(exec_times)
            min_time = min(exec_times)
            avg_time = sum(exec_times) / count
            max_time = max(exec_times)
            std_dev = statistics.stdev(exec_times) if count > 1 else 0.0
            
            print(f"{task_name:<15} {count:<10} {min_time:<12.3f} {avg_time:<12.3f} "
                  f"{max_time:<12.3f} {std_dev:<12.3f}")
    
    print("="*80)


if __name__ == "__main__":
    print("Task Scheduler mit Visualisierung")
    print("Laufzeit: 30 Sekunden")
    print("-" * 50)
    
    # Start-Zeit merken
    start_time = time.time()
    
    # Scheduler erstellen
    scheduler = Scheduler()
    
    # Tasks mit Wrappern hinzufügen
    scheduler.add_task(Task(
        name="Fast",
        function=create_wrapper("Fast", fast_task),
        task_type=TaskType.CYCLIC,
        interval_ms=1,
        priority=TaskPriority.HIGH,
        cpu_affinity=None, # [0,1,2,3]
        watchdog_ms=10,
        watchdog_action=WatchdogAction.NONE,
        watchdog_sensitivity=3,
        autostart=True
    ))
    
    scheduler.add_task(Task(
        name="Medium",
        function=create_wrapper("Medium", medium_task),
        task_type=TaskType.CYCLIC,
        interval_ms=5,
        priority=TaskPriority.NORMAL,
        cpu_affinity=None,
        watchdog_ms=50,
        watchdog_action=WatchdogAction.NONE,
        watchdog_sensitivity=3,
        autostart=True
    ))
    
    scheduler.add_task(Task(
        name="Slow",
        function=create_wrapper("Slow", slow_task),
        task_type=TaskType.CYCLIC,
        interval_ms=10,
        priority=TaskPriority.LOW,
        cpu_affinity=None,
        watchdog_ms=100,
        watchdog_action=WatchdogAction.NONE,
        watchdog_sensitivity=3,
        autostart=True
    ))
    
    # Laufen lassen
    print("\nTasks laufen... (30s)")
    time.sleep(30.0)
    
    # Stoppen
    scheduler.stop_all()
    
    # Status anzeigen
    print("\n>>> Scheduler Status:")
    scheduler.print_status()
    
    # Statistiken anzeigen
    print_statistics()
    
    # Visualisierung
    print("\nErstelle Visualisierung...")
    plot_execution_times()
    
    print("\nFertig!")

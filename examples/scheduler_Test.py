"""
Einfaches Scheduler-Beispiel: So verwendest du den IEC Scheduler
"""

from RobotLibrary.IEC_Scheduler import Task, Scheduler, TaskType, TaskPriority, WatchdogAction
import time


def fast_task():
    #print("  [Fast] 1ms Task")
    x = 1.0
    for _ in range(10000):
         x = x * 1.0000001

def medium_task():
    #print("  [Medium] 5ms Task")
    x = 1.0
    for _ in range(10000):
         x = x * 1.0000001

def slow_task():
    #print("  [Slow] 10ms Task")
    x = 1.0
    for _ in range(10000):
         x = x * 1.0000001

# Scheduler erstellen
scheduler = Scheduler()

# Tasks hinzufügen
scheduler.add_task(Task(name= "Fast", 
                        function = fast_task,
                        task_type = TaskType.CYCLIC, 
                        interval_ms=1, 
                        priority = TaskPriority.HIGH,
                        cpu_affinity= None, # [0,1,2,3],  # Kern 0
                        watchdog_ms= 3, 
                        watchdog_action= WatchdogAction.NONE, 
                        watchdog_sensitivity = 3, 
                        autostart = True ))

scheduler.add_task(Task(name= "Medium", 
                        function = medium_task, 
                        task_type = TaskType.CYCLIC, 
                        interval_ms=5, 
                        priority = TaskPriority.HIGH,
                        cpu_affinity= None, # [0,1,2,3],  # Kern 0
                        watchdog_ms= 15, 
                        watchdog_action= WatchdogAction.WARNING, 
                        watchdog_sensitivity = 3, 
                        autostart = True ))

scheduler.add_task(Task(name= "Slow", 
                        function = slow_task, 
                        task_type = TaskType.CYCLIC, 
                        interval_ms=10, 
                        priority = TaskPriority.HIGH,
                        cpu_affinity= None, # [0,1,2,3],  # Kern 0
                        watchdog_ms= 30, 
                        watchdog_action= WatchdogAction.WARNING, 
                        watchdog_sensitivity = 3, 
                        autostart = True ))

# Alle Tasks starten
scheduler.start_all()

# Laufen lassen
time.sleep(30.0)

# Status anzeigen
print("\n>>> Status aller Tasks:")
scheduler.print_status()

# Alle stoppen
scheduler.stop_all()
print()
"""
Test um zu verifizieren, dass der Watchdog trotz Race-Condition-Fix funktioniert
"""

from RobotLibrary.IEC_Scheduler import Task, Scheduler, TaskType, TaskPriority, WatchdogAction
import time


def fast_task():
    """Schneller Task - sollte KEINEN Watchdog auslösen"""
    x = 1.0
    for _ in range(1000):
        x = x * 1.0000001


def slow_task_timeout():
    """Langsamer Task - sollte absichtlich Watchdog auslösen"""
    time.sleep(0.025)  # 25ms - länger als 20ms Watchdog


def medium_task():
    """Mittlerer Task - sollte KEINEN Watchdog auslösen"""
    x = 1.0
    for _ in range(5000):
        x = x * 1.0000001


# Scheduler erstellen
scheduler = Scheduler()

# Task 1: Schnell, sollte KEINEN Timeout haben
scheduler.add_task(Task(
    name="Fast_OK", 
    function=fast_task,
    task_type=TaskType.CYCLIC, 
    interval_ms=10, 
    priority=TaskPriority.NORMAL,
    watchdog_ms=5,  # 5ms Watchdog
    watchdog_action=WatchdogAction.WARNING, 
    watchdog_sensitivity=3, 
    autostart=True
))

# Task 2: Absichtlich langsam - SOLLTE Timeout haben
scheduler.add_task(Task(
    name="Slow_TIMEOUT", 
    function=slow_task_timeout, 
    task_type=TaskType.CYCLIC, 
    interval_ms=50,  # Alle 50ms
    priority=TaskPriority.NORMAL,
    watchdog_ms=20,  # 20ms Watchdog, aber Task braucht 25ms
    watchdog_action=WatchdogAction.WARNING, 
    watchdog_sensitivity=3, 
    autostart=True
))

# Task 3: Mittel, sollte KEINEN Timeout haben
scheduler.add_task(Task(
    name="Medium_OK", 
    function=medium_task, 
    task_type=TaskType.CYCLIC, 
    interval_ms=20, 
    priority=TaskPriority.NORMAL,
    watchdog_ms=10,  # 10ms Watchdog
    watchdog_action=WatchdogAction.WARNING, 
    watchdog_sensitivity=3, 
    autostart=True
))

print("=== WATCHDOG FUNCTIONALITY TEST ===")
print("Expected: Fast_OK und Medium_OK haben KEINE Watchdog-Trigger")
print("Expected: Slow_TIMEOUT hat Watchdog-Trigger (Task braucht 25ms, Watchdog ist 20ms)")
print("\nRunning for 10 seconds...\n")

# Alle Tasks starten
scheduler.start_all()

# Laufen lassen
time.sleep(10.0)

# Status anzeigen
print("\n>>> Status aller Tasks:")
scheduler.print_status()

# Analyse
print("\n=== ANALYSE ===")
status = scheduler.get_status()
for task in status:
    name = task['name']
    wd_triggers = task['statistics']['watchdog_triggers']
    wd_pct = task['statistics']['watchdog_ratio_pct']
    
    if name == "Slow_TIMEOUT":
        if wd_triggers > 0:
            print(f"✓ {name}: Watchdog funktioniert! ({wd_triggers} triggers, {wd_pct:.1f}%)")
        else:
            print(f"✗ {name}: FEHLER - Watchdog hat nicht ausgelöst!")
    else:
        if wd_triggers == 0:
            print(f"✓ {name}: Korrekt - keine falschen Watchdog-Trigger")
        else:
            print(f"✗ {name}: FEHLER - Falsche Watchdog-Trigger! ({wd_triggers} triggers)")

# Alle stoppen
scheduler.stop_all()
print("\nTest abgeschlossen!")

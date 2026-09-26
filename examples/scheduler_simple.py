"""
Einfaches Scheduler-Beispiel: So verwendest du den IEC Scheduler
"""

from RobotLibrary.IEC_Scheduler import Task, Scheduler, TaskType, TaskPriority
import time

print("=" * 80)
print("EINFACHES SCHEDULER BEISPIEL")
print("=" * 80)
print()

# ============================================================================
# 1. EINFACHSTES BEISPIEL: Eine Task
# ============================================================================

print(">>> Beispiel 1: Eine einfache Task")
print()

counter = 0

def my_function():
    """Diese Funktion wird zyklisch ausgeführt"""
    global counter
    counter += 1
    print(f"  Task läuft... (Ausführung #{counter})")


# Task erstellen
task = Task(
    name="MyTask",                    # Name der Task
    function=my_function,             # Funktion die ausgeführt wird
    task_type=TaskType.CYCLIC,        # Zyklisch (regelmäßig)
    interval_ms=500.0,                # Alle 500ms (0.5 Sekunden)
    priority=TaskPriority.NORMAL,     # Normale Priorität
    autostart=True                    # Automatisch starten
)

# Laufen lassen
print("Task läuft für 3 Sekunden...")
time.sleep(3.0)

# Task stoppen
task.stop()
print(f"Task gestoppt. Insgesamt {counter} Ausführungen.\n")


# ============================================================================
# 2. MEHRERE TASKS MIT SCHEDULER
# ============================================================================

print("=" * 80)
print(">>> Beispiel 2: Mehrere Tasks mit verschiedenen Intervallen")
print("=" * 80)
print()

def fast_task():
    print("  [Fast] 100ms Task")

def medium_task():
    print("  [Medium] 500ms Task")

def slow_task():
    print("  [Slow] 1000ms Task")


# Scheduler erstellen
scheduler = Scheduler()

# Tasks hinzufügen
scheduler.add_task(Task("Fast", fast_task, TaskType.CYCLIC, interval_ms=100.0))
scheduler.add_task(Task("Medium", medium_task, TaskType.CYCLIC, interval_ms=500.0))
scheduler.add_task(Task("Slow", slow_task, TaskType.CYCLIC, interval_ms=1000.0))

# Alle Tasks starten
scheduler.start_all()

# Laufen lassen
time.sleep(3.0)

# Status anzeigen
print("\n>>> Status aller Tasks:")
scheduler.print_status()

# Alle stoppen
scheduler.stop_all()
print()


# ============================================================================
# 3. EVENT-GETRIGGERTE TASK
# ============================================================================

print("=" * 80)
print(">>> Beispiel 3: Event-getriggerte Task")
print("=" * 80)
print()

def event_handler():
    print("  [Event] Event wurde getriggert!")

# Event-Task erstellen
event_task = Task(
    name="EventTask",
    function=event_handler,
    task_type=TaskType.EVENT,           # Event-getriggert (nicht zyklisch!)
    priority=TaskPriority.HIGH,
    autostart=True
)

# Task wartet jetzt auf Trigger
print("Task wartet auf Events...")
time.sleep(1.0)

# Events manuell triggern
print("\nTriggere 3 Events:")
for i in range(3):
    print(f"  Trigger #{i+1}")
    event_task.trigger()
    time.sleep(0.5)

event_task.stop()
print()


# ============================================================================
# 4. TASK SUSPEND/RESUME
# ============================================================================

print("=" * 80)
print(">>> Beispiel 4: Task Pause/Resume")
print("=" * 80)
print()

counter4 = 0

def counting_task():
    global counter4
    counter4 += 1

task4 = Task("Counter", counting_task, TaskType.CYCLIC, 
             interval_ms=100.0, autostart=True)

print("Task läuft...")
time.sleep(0.5)
print(f"  Counter: {counter4}")

print("\nTask pausieren...")
task4.suspend()
time.sleep(1.0)
print(f"  Counter während Pause: {counter4} (sollte gleich bleiben)")

print("\nTask fortsetzen...")
task4.resume()
time.sleep(0.5)
print(f"  Counter nach Resume: {counter4} (sollte wieder steigen)")

task4.stop()
print()


# ============================================================================
# 5. PRIORITÄTEN
# ============================================================================

print("=" * 80)
print(">>> Beispiel 5: Task-Prioritäten")
print("=" * 80)
print()

def low_prio():
    print("  [LOW] Niedrige Priorität")

def high_prio():
    print("  [HIGH] Hohe Priorität")

def realtime_prio():
    print("  [REALTIME] Realtime Priorität")


scheduler5 = Scheduler()
scheduler5.add_task(Task("Low", low_prio, TaskType.CYCLIC, 
                        interval_ms=200.0, priority=TaskPriority.LOW))
scheduler5.add_task(Task("High", high_prio, TaskType.CYCLIC, 
                        interval_ms=200.0, priority=TaskPriority.HIGH))
scheduler5.add_task(Task("Realtime", realtime_prio, TaskType.CYCLIC, 
                        interval_ms=200.0, priority=TaskPriority.REALTIME))

scheduler5.start_all()
time.sleep(1.0)
scheduler5.stop_all()

print("\n>>> Status (sortiert nach Priorität):")
scheduler5.print_status()
print()


# ============================================================================
# 6. WATCHDOG
# ============================================================================

print("=" * 80)
print(">>> Beispiel 6: Watchdog-Überwachung")
print("=" * 80)
print()

def slow_function():
    """Diese Funktion ist absichtlich langsam"""
    time.sleep(0.15)  # 150ms

# Task mit 100ms Watchdog
watchdog_task = Task(
    name="SlowTask",
    function=slow_function,
    task_type=TaskType.CYCLIC,
    interval_ms=200.0,
    watchdog_ms=100.0,  # Watchdog-Timeout: 100ms (Task braucht aber 150ms!)
    autostart=True
)

print("Task mit Watchdog läuft (sollte Timeout-Warnung ausgeben)...")
time.sleep(1.0)

info = watchdog_task.get_info()
print(f"\nWatchdog-Trigger: {info['statistics']['watchdog_triggers']}")

watchdog_task.stop()
print()


# ============================================================================
# 7. TASK DYNAMISCH HINZUFÜGEN/ENTFERNEN
# ============================================================================

print("=" * 80)
print(">>> Beispiel 7: Tasks dynamisch verwalten")
print("=" * 80)
print()

def task_a():
    print("  [A] Task A läuft")

def task_b():
    print("  [B] Task B läuft")


scheduler7 = Scheduler()
scheduler7.add_task(Task("TaskA", task_a, TaskType.CYCLIC, 
                        interval_ms=300.0, autostart=True))

print("Scheduler mit Task A läuft...")
time.sleep(1.0)

print("\nFüge Task B hinzu...")
scheduler7.add_task(Task("TaskB", task_b, TaskType.CYCLIC, 
                        interval_ms=300.0, autostart=True))
time.sleep(1.0)

print("\nEntferne Task A...")
scheduler7.remove_task("TaskA")
time.sleep(1.0)

scheduler7.stop_all()
print()


# ============================================================================
# ZUSAMMENFASSUNG
# ============================================================================

print("=" * 80)
print("ZUSAMMENFASSUNG - SO VERWENDEST DU DEN SCHEDULER:")
print("=" * 80)
print("""
1. EINFACHE TASK:
   task = Task(name="MyTask", function=my_func, task_type=TaskType.CYCLIC,
               interval_ms=100.0, autostart=True)
   
2. MEHRERE TASKS:
   scheduler = Scheduler()
   scheduler.add_task(task1)
   scheduler.add_task(task2)
   scheduler.start_all()
   
3. EVENT-TASK:
   event_task = Task(name="Event", function=handler, task_type=TaskType.EVENT)
   event_task.trigger()  # Event auslösen
   
4. PRIORITÄTEN:
   - TaskPriority.LOW / NORMAL / HIGH / REALTIME
   - Höhere Priorität = wird bevorzugt
   
5. WATCHDOG:
   watchdog_ms=100.0  # Alarm wenn Task länger als 100ms braucht
   
6. SUSPEND/RESUME:
   task.suspend()  # Pausieren
   task.resume()   # Fortsetzen
   
7. CPU AFFINITY:
   cpu_affinity=[0, 1]  # Task auf CPU Cores 0 und 1 begrenzen
   
8. STATISTIKEN:
   scheduler.print_status()  # Zeigt alle Tasks mit Statistiken
   task.get_info()          # Info über eine Task
""")

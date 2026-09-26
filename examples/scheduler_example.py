"""
Praktisches Beispiel: IEC Scheduler für Roboter-Steuerung
Zeigt typische Anwendungsfälle mit verschiedenen Task-Typen
"""

from RobotLibrary.IEC_Scheduler import Task, Scheduler, TaskType, TaskPriority
from RobotLibrary.IEC_Types import BOOL, INT, REAL, IEC_Struct, ARRAY
import time


# ============================================================================
# 1. DATENSTRUKTUREN
# ============================================================================

class RobotData(IEC_Struct):
    """Globale Roboterdaten"""
    Position_X: REAL = REAL(0.0)
    Position_Y: REAL = REAL(0.0)
    Position_Z: REAL = REAL(0.0)
    Speed: REAL = REAL(0.0)
    IsMoving: BOOL = BOOL(False)
    ErrorCode: INT = INT(0)
    CycleCount: INT = INT(0)


class SensorData(IEC_Struct):
    """Sensor-Daten"""
    Temperature: REAL = REAL(20.0)
    Pressure: REAL = REAL(1013.0)
    ForceX: REAL = REAL(0.0)
    ForceY: REAL = REAL(0.0)
    ForceZ: REAL = REAL(0.0)


# Globale Daten-Instanzen
robot = RobotData()
sensors = SensorData()


# ============================================================================
# 2. TASK-FUNKTIONEN
# ============================================================================

def fast_control_loop():
    """
    Schnelle Regelschleife (10ms Zyklus)
    Kritische Echtzeit-Steuerung
    """
    # Simuliere Positions-Update
    robot.Position_X.value += 0.1
    robot.CycleCount.value += 1
    
    # Geschwindigkeit berechnen
    robot.Speed.value = 0.1 / 0.010  # 0.1 pro Zyklus bei 10ms
    
    # Status
    robot.IsMoving.value = robot.Speed.value > 0


def sensor_reading():
    """
    Sensor-Auslesen (50ms Zyklus)
    Moderate Priorität
    """
    import random
    
    # Simuliere Sensor-Werte
    sensors.Temperature.value = 20.0 + random.uniform(-2.0, 2.0)
    sensors.Pressure.value = 1013.0 + random.uniform(-10.0, 10.0)
    sensors.ForceX.value = random.uniform(-5.0, 5.0)
    sensors.ForceY.value = random.uniform(-5.0, 5.0)
    sensors.ForceZ.value = random.uniform(-50.0, 50.0)


def data_logging():
    """
    Daten-Logging (500ms Zyklus)
    Niedrige Priorität
    """
    # In echtem System: Daten in Datei/Datenbank schreiben
    print(f"[LOG] Pos=({float(robot.Position_X):.1f}, {float(robot.Position_Y):.1f}, "
          f"{float(robot.Position_Z):.1f}) Speed={float(robot.Speed):.1f} "
          f"Temp={float(sensors.Temperature):.1f}°C")


def safety_monitor():
    """
    Sicherheitsüberwachung (100ms Zyklus)
    Höchste Priorität
    """
    # Überwache kritische Werte
    if sensors.Temperature.value > 80.0:
        robot.ErrorCode.value = 1001  # Überhitzung
        print("[SAFETY] WARNING: Temperature too high!")
    
    if sensors.ForceZ.value > 100.0:
        robot.ErrorCode.value = 1002  # Kraft zu hoch
        print("[SAFETY] WARNING: Force too high!")
    
    if robot.Speed.value > 1000.0:
        robot.ErrorCode.value = 1003  # Geschwindigkeit zu hoch
        print("[SAFETY] WARNING: Speed too high!")


emergency_triggered = False
def emergency_stop():
    """
    Notaus (Event-getriggert)
    Realtime-Priorität
    """
    global emergency_triggered
    emergency_triggered = True
    
    print("\n" + "="*60)
    print("!!! EMERGENCY STOP !!!")
    print("="*60)
    
    # Stoppe Bewegung
    robot.Speed.value = 0.0
    robot.IsMoving.value = False
    robot.ErrorCode.value = 9999
    
    print(f"Robot stopped at position ({float(robot.Position_X):.1f}, "
          f"{float(robot.Position_Y):.1f}, {float(robot.Position_Z):.1f})")
    print("="*60 + "\n")


# ============================================================================
# 3. SCHEDULER SETUP
# ============================================================================

def setup_robot_scheduler():
    """
    Erstellt und konfiguriert den Scheduler mit allen Tasks
    """
    scheduler = Scheduler()
    
    # Task 1: Schnelle Regelschleife (10ms, Hohe Priorität)
    # - Kritisch für Echtzeit-Steuerung
    # - Watchdog: 8ms (Task muss in < 8ms fertig sein)
    # - CPU Core 0 (dedizierter Kern)
    control_task = Task(
        name="ControlLoop",
        function=fast_control_loop,
        task_type=TaskType.CYCLIC,
        interval_ms=10.0,
        priority=TaskPriority.HIGH,
        watchdog_ms=8.0,
        cpu_affinity=[0]
    )
    scheduler.add_task(control_task)
    
    # Task 2: Sicherheitsüberwachung (100ms, Realtime-Priorität)
    # - Höchste Priorität für Safety
    # - Watchdog: 50ms
    safety_task = Task(
        name="SafetyMonitor",
        function=safety_monitor,
        task_type=TaskType.CYCLIC,
        interval_ms=100.0,
        priority=TaskPriority.REALTIME,
        watchdog_ms=50.0
    )
    scheduler.add_task(safety_task)
    
    # Task 3: Sensor-Auslesen (50ms, Normal-Priorität)
    # - Regelmäßige Sensor-Aktualisierung
    # - Watchdog: 30ms
    sensor_task = Task(
        name="SensorRead",
        function=sensor_reading,
        task_type=TaskType.CYCLIC,
        interval_ms=50.0,
        priority=TaskPriority.NORMAL,
        watchdog_ms=30.0
    )
    scheduler.add_task(sensor_task)
    
    # Task 4: Daten-Logging (500ms, Niedrige Priorität)
    # - Kann verzögert werden wenn System ausgelastet
    # - Kein Watchdog (nicht zeitkritisch)
    logging_task = Task(
        name="DataLogger",
        function=data_logging,
        task_type=TaskType.CYCLIC,
        interval_ms=500.0,
        priority=TaskPriority.LOW
    )
    scheduler.add_task(logging_task)
    
    # Task 5: Notaus (Event-getriggert, Realtime-Priorität)
    # - Wird nur bei Bedarf ausgeführt
    # - Höchste Priorität
    # - Watchdog: 10ms (muss sofort reagieren)
    estop_task = Task(
        name="EmergencyStop",
        function=emergency_stop,
        task_type=TaskType.EVENT,
        priority=TaskPriority.REALTIME,
        watchdog_ms=10.0
    )
    scheduler.add_task(estop_task)
    
    return scheduler, estop_task


# ============================================================================
# 4. HAUPTPROGRAMM
# ============================================================================

def main():
    print("="*80)
    print("IEC Scheduler - Roboter Steuerung Beispiel")
    print("="*80)
    print()
    
    # Scheduler erstellen
    scheduler, estop_task = setup_robot_scheduler()
    
    # Alle Tasks starten
    print("Starting scheduler...")
    scheduler.start_all()
    print("Scheduler running...\n")
    
    # Simuliere normalen Betrieb (5 Sekunden)
    print(">>> Phase 1: Normal Operation (5s)")
    time.sleep(5.0)
    
    # Status anzeigen
    print("\n>>> Scheduler Status:")
    scheduler.print_status()
    
    # Simuliere Notaus-Event
    print("\n>>> Phase 2: Triggering Emergency Stop")
    estop_task.trigger()
    time.sleep(1.0)
    
    # Zeige was passiert ist
    print(f"\nRobot State after Emergency:")
    print(f"  Position: ({robot.Position_X.value:.1f}, {robot.Position_Y.value:.1f}, {robot.Position_Z.value:.1f})")
    print(f"  Speed: {robot.Speed.value:.1f}")
    print(f"  Error Code: {robot.ErrorCode.value}")
    print(f"  Cycle Count: {robot.CycleCount.value}")
    
    # Tasks pausieren/fortsetzen
    print("\n>>> Phase 3: Suspend/Resume Logging Task")
    logger = scheduler.get_task("DataLogger")
    if logger:
        print("Suspending DataLogger for 2 seconds...")
        logger.suspend()
        time.sleep(2.0)
        print("Resuming DataLogger...")
        logger.resume()
        time.sleep(2.0)
    
    # Finale Statistiken
    print("\n>>> Final Scheduler Status:")
    scheduler.print_status()
    
    # Scheduler stoppen
    print("\n>>> Stopping scheduler...")
    scheduler.stop_all()
    
    print("\nDone!")


# ============================================================================
# 5. ERWEITERTE ANWENDUNGEN
# ============================================================================

def example_dynamic_task_management():
    """
    Zeigt dynamisches Hinzufügen/Entfernen von Tasks
    """
    print("\n" + "="*80)
    print("Erweitert: Dynamisches Task-Management")
    print("="*80)
    
    scheduler = Scheduler()
    
    # Basis-Task
    def base_function():
        print("  [Base] Running...")
    
    base_task = Task("BaseTask", base_function, TaskType.CYCLIC, 
                     interval_ms=200.0, autostart=True)
    scheduler.add_task(base_task)
    
    print("Running with 1 task...")
    time.sleep(1.0)
    
    # Dynamisch Task hinzufügen
    def dynamic_function():
        print("  [Dynamic] Running...")
    
    dynamic_task = Task("DynamicTask", dynamic_function, TaskType.CYCLIC,
                       interval_ms=300.0, autostart=True)
    scheduler.add_task(dynamic_task)
    
    print("\nAdded dynamic task, running with 2 tasks...")
    time.sleep(1.5)
    
    # Task wieder entfernen
    scheduler.remove_task("DynamicTask")
    print("\nRemoved dynamic task, running with 1 task...")
    time.sleep(1.0)
    
    scheduler.stop_all()


def example_task_communication():
    """
    Zeigt Kommunikation zwischen Tasks über gemeinsame Daten
    """
    print("\n" + "="*80)
    print("Erweitert: Task-Kommunikation")
    print("="*80)
    
    class SharedData(IEC_Struct):
        Counter: INT = INT(0)
        Flag: BOOL = BOOL(False)
    
    shared = SharedData()
    
    def producer_task():
        """Erzeugt Daten"""
        shared.Counter.value += 1
        if int(shared.Counter) % 5 == 0:
            shared.Flag.value = True
    
    def consumer_task():
        """Verarbeitet Daten"""
        if bool(shared.Flag.value):
            print(f"  [Consumer] Flag detected at counter={int(shared.Counter.value)}")
            shared.Flag.value = False
    
    scheduler = Scheduler()
    scheduler.add_task(Task("Producer", producer_task, TaskType.CYCLIC, 100.0))
    scheduler.add_task(Task("Consumer", consumer_task, TaskType.CYCLIC, 50.0))
    
    scheduler.start_all()
    time.sleep(2.0)
    scheduler.stop_all()
    
    print(f"Final counter: {int(shared.Counter)}")


# ============================================================================
# START
# ============================================================================

if __name__ == "__main__":
    # Haupt-Beispiel
    main()
    
    # Erweiterte Beispiele (optional)
    # example_dynamic_task_management()
    # example_task_communication()

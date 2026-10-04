# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      examples.quickstart.quickstart
#  Author:      Thorsten Brach
#  Date:        2026-10-03
#
#  Description:
#    Compact example: initialize the RobotTask, switch on the robot, a few moves.
#
#  Copyright:
#    (C) 2026 Thorsten Brach. All rights reserved
#             Licensed under the MIT License.
#
#  Disclaimer:
#    This project is provided without any guarantee and can be used for
#    private and commercial purposes. Any use is at the user's
#    own risk and responsibility.
#
# -------------------------------------------------------------------------


"""SRCI quickstart: connect, switch on the robot, move, switch off - one script, top to bottom.

    python quickstart.py            robot behind the PLC gateway (THE ROBOT MOVES)
    python quickstart.py --sim      SRCI SDK simulator instead of a robot (no PLC needed)

The poses are made for a JAKA MiniCobo (zero position = arm straight up, reach 580 mm). For another
robot change READY_POSE and RECTANGLE. Try new poses with a low OVERRIDE first.
"""

import copy
import math
import sys
import time

from srci.api import SrciClient
from srci.fb import (
    MC_ChangeSpeedOverrideFB,
    MC_EnableRobotFB,
    MC_GroupResetFB,
    MC_GroupStopFB,
    MC_MoveAxesAbsoluteFB,
    MC_MoveLinearAbsoluteFB,
    MC_ReadActualPositionFB,
)
from srci.transport import TcpTransport, Transport
from srci.types import (
    ArmConfigElbow,
    ArmConfigShoulder,
    ArmConfigWrist,
    BlendingMode,
    MessageLevel,
    SyncMode,
    TurnMode,
)

# ============================================================================= settings

HOST = "192.168.2.10"  # PLC bridge (SRCI_TcpIp_Bridge, FB_SrciTcpIpBridge)
PORT = 5000
TELEGRAM_LENGTH = 256  # bytes per direction, as configured in the PLC / robot
OVERRIDE = 100.0  # speed override [%] for all moves (first run on a new robot: 30)
VELOCITY = 50.0  # velocity of each move [% of the reference velocity] -> effectively 50 %

# elbow-bent pose [deg]: shoulder (J2) and elbow (J3) bent - away from the stretched arm;
# J5 = 90 keeps the wrist away from its singularity (J5 = 0)
READY_POSE = {"J1": 0.0, "J2": 30.0, "J3": 60.0, "J4": 0.0, "J5": 90.0, "J6": 0.0}
RECTANGLE = (150.0, 150.0)  # size in X and Y [mm], horizontal, starting at the TCP of READY_POSE
# blending at the corners of the rectangle (spec table 6-9); not every RC supports every mode -
# an unsupported mode is rejected with 16#8E05 (JAKA MiniCobo, firmware 1.7.1: only
# MAX_CORNER_DEVIATION - probe it with examples/jaka_minicobo/minicobo.py blending):
#   MAX_CORNER_DEVIATION  parameter = max. deviation from the corner [mm]
#   CORNER_DISTANCE       parameter = radius [mm]
#   RAMP_OVERLAP          parameter = overlap of the ramps [%] 0..100
#   EXACT_STOP            no blending (the robot stops at every corner)
BLENDING_MODE = BlendingMode.MAX_CORNER_DEVIATION
BLENDING_PARAMETER = 50.0  # well visible; at most about half of the shorter side
# TurnMode and ConfigMode (shoulder, elbow, wrist) of the linear moves - optional parameters, not
# every RC supports every value (16#8E10 TurnMode, 16#8E09 ConfigMode not supported):
#   TurnMode:   USE_TURN_NUMBER (spec default), SAME (keep the turn numbers), FREE
#   ConfigMode: USE_CONFIG (spec default, config of the target position), SAME, FREE
# The JAKA (JSI 1.6) rejects TurnMode USE_TURN_NUMBER and SAME. 'python minicobo.py blending' in
# examples/jaka_minicobo shows which TurnMode, ConfigMode and BlendingMode a robot accepts.
TURN_MODE = TurnMode.FREE
CONFIG_MODE = 1  # 0 USE_CONFIG, 1 SAME, 2 FREE (for shoulder, elbow and wrist)
REACH = (150.0, 520.0)  # the corners must lie in this distance from the base axis [mm] (MiniCobo: 580)

SIMULATION = "--sim" in sys.argv

# ============================================================================= connection

transport: Transport
if SIMULATION:
    # SRCI SDK simulator in-process (needs the locally built SDK library, SRCI_SDK_SIM_LIB)
    from srci.sim.sdk import SdkSimulator, sdk_transport

    sim = SdkSimulator()
    sim.set_move_cycles(100)  # a simulated move takes 1 s
    transport = sdk_transport(sim, TELEGRAM_LENGTH, TELEGRAM_LENGTH)
else:
    if "--yes" not in sys.argv:
        answer = input("THE ROBOT WILL MOVE. Is the working area clear? [y/n] ")
        if answer.strip().lower() not in ("y", "yes", "j", "ja"):
            print("cancelled")
            sys.exit(0)
    transport = TcpTransport(HOST, PORT, TELEGRAM_LENGTH, TELEGRAM_LENGTH, response_timeout=0.1)

# the client runs the RobotTask cyclically in the background (like a PLC task)
client = SrciClient(transport)

# ============================================================================= RobotTask parameters (ParCfg)
# All parameters - used for the initialization. The lines commented out show the default value.

cfg = client.program.ParCfg
# fmt: off
# --- communication
cfg.Com.TelegramLengthPlcToRob = TELEGRAM_LENGTH     # [bytes] PLC -> RC, = PROFINET module size
cfg.Com.TelegramLengthRobToPlc = TELEGRAM_LENGTH     # [bytes] RC -> PLC
cfg.Com.LifeSignTimeOut = 500                        # [ms] connection lost if the LifeSign stops (default 50; JAKA: >= 300)
# cfg.Com.TwoSequences = False                       # 2nd sequence in the telegram

# --- client (PLC / Python)
# cfg.Plc.CycleTime = 10                             # [ms] cycle time of the client
# cfg.Plc.Parameter.ManufacturedID = 0               # identification of the client (information only)
# cfg.Plc.Parameter.OrderID = ""
# cfg.Plc.Parameter.SerialNumber = ""
# cfg.Plc.Parameter.FirmwareVersion = ""
# cfg.Plc.Parameter.InterfaceVersion = ""

# synchronization of the user data with the RC: [0] at the start, [1] while running
# SyncMode: NO_SYNCHRONIZATION, CLIENT_TO_SERVER, SERVER_TO_CLIENT, AUTOMATIC
sync = cfg.Plc.Parameter.SynchronizationModes
sync.Tool[0] = sync.Tool[1] = SyncMode.NO_SYNCHRONIZATION
# sync.Frame[0] = sync.Frame[1] = SyncMode.NO_SYNCHRONIZATION
# sync.Load[0] = sync.Load[1] = SyncMode.NO_SYNCHRONIZATION
# sync.WorkAreas[0] = sync.WorkAreas[1] = SyncMode.NO_SYNCHRONIZATION   # needs ReadWorkArea (not Core)
# sync.SWLimits[0] = sync.SWLimits[1] = SyncMode.NO_SYNCHRONIZATION
# sync.DefaultDynamics[0] = sync.DefaultDynamics[1] = SyncMode.NO_SYNCHRONIZATION
# sync.ReferenceDynamics[0] = sync.ReferenceDynamics[1] = SyncMode.NO_SYNCHRONIZATION
# cfg.Plc.Parameter.SyncUserInteraction.Tool = False  # synchronization needs a confirmation of the user
#                                                     # (also .Frame .Load .WorkAreas .SWLimits ...)

# optional cyclic data PLC -> RC (sent in every telegram)
# cfg.Plc.OptionalCyclic.UseCallSubprogram = False   # data for a subprogram (CallSubprogram)
# cfg.Plc.OptionalCyclic.UseCartesianPosition = False
# cfg.Plc.OptionalCyclic.UseJointPosition = False
# cfg.Plc.OptionalCyclic.UseForce = False
# cfg.Plc.OptionalCyclic.UseTwoSequences = False
# cfg.Plc.OptionalCyclic.UseCartesianPositionExt = False   # external axes E2..E6
# cfg.Plc.OptionalCyclic.UseJointPositionExt = False

# --- robot controller
cfg.Rob.Parameter.MessageLevel = MessageLevel.WARNING  # messages of the RC from: DEBUG, INFO, WARNING, ERROR
# cfg.Rob.Parameter.WaitAtBlendingZone = False       # FALSE: blending zone may be left without the next command
# cfg.Rob.Parameter.AllowSecSeqWhileSubprogram = False
# cfg.Rob.Parameter.AllowDynamicBlending = False
# cfg.Rob.Parameter.DelayTime = 0                    # [ms] wait before the 1st move of an empty queue
# cfg.Rob.Parameter.WaitForNrOfCmd = 0               # moves needed before the RC starts (blending)
# cfg.Rob.Parameter.SyncDelay = 0                    # [ms] before SyncReaction on inconsistent user data
# cfg.Rob.Parameter.SyncReaction = SyncReaction.NO_REACTION   # (srci.types) NO_AUTOMATIC_DISABLE,
#                                                    # INTERRUPT_WHEN_SEQUENCE_IS_EMPTY, IMMEDIATE_INTERRUPT

# optional cyclic data RC -> PLC (in every telegram, e.g. for MC_ReadActualPositionCyclicFB)
# cfg.Rob.OptionalCyclic.UseCartesianPosition = False
# cfg.Rob.OptionalCyclic.UseJointPosition = False
# cfg.Rob.OptionalCyclic.UseForce = False
# cfg.Rob.OptionalCyclic.UseCurrent = False          # motor currents J1..J6
# cfg.Rob.OptionalCyclic.UseCallSubprogram = False
# cfg.Rob.OptionalCyclic.UseTwoSequences = False
# cfg.Rob.OptionalCyclic.UseCartesianPositionExt = False   # also UseJointPositionExt, UseForceExt,
#                                                          # UseCurrentExt (external axes)
# fmt: on

# ============================================================================= initialize, switch on

# RobotTask: initializes the interface, reads robot data and configuration
client.wait_initialized(timeout=15.0)
robot = client.program.axes_group.State.RobotData
print(f"connected: {robot.RCManufacturer} {robot.RCOrderID}, firmware {robot.RCFirmwareVersion}")

# reset pending errors
client.execute(MC_GroupResetFB())

# switch on the robot (power, brakes released) - Enable stays TRUE until client.disable(enable)
enable = client.enable(MC_EnableRobotFB())
print(f"robot enabled: {enable.Enabled}")

# speed override for all following moves
override = MC_ChangeSpeedOverrideFB()
override.ParCmd.Override = OVERRIDE
client.execute(override)

# ============================================================================= moves

try:
    # start position (joints and TCP)
    position = client.execute(MC_ReadActualPositionFB()).OutCmd
    start = copy.deepcopy(position.ActualJointPosition)
    print("start:              J1..J6 =", " ".join(f"{getattr(start, f'J{i}'):.1f}" for i in range(1, 7)))

    # 1. joint move (PTP) into the elbow-bent pose
    ready = copy.deepcopy(start)
    for joint, angle in READY_POSE.items():
        setattr(ready, joint, angle)
    move_axes = MC_MoveAxesAbsoluteFB()
    move_axes.ParCmd.JointPosition = ready
    move_axes.ParCmd.VelocityRate = VELOCITY
    client.execute(move_axes, timeout=60.0)
    print("1. elbow-bent pose")

    # 2..5. rectangle with linear moves in the horizontal plane, orientation unchanged, blended corners
    position = client.execute(MC_ReadActualPositionFB()).OutCmd
    corner = position.ActualCartesianPosition  # TCP in the elbow-bent pose
    print(f"   TCP:             X={corner.X:.1f} Y={corner.Y:.1f} Z={corner.Z:.1f} mm")
    width, depth = RECTANGLE
    offsets = [(width, 0.0), (width, depth), (0.0, depth), (0.0, 0.0)]
    radii = [math.hypot(corner.X + dx, corner.Y + dy) for dx, dy in offsets]
    if not SIMULATION and not all(REACH[0] <= r <= REACH[1] for r in radii):
        print(f"rectangle skipped: corners {min(radii):.0f}..{max(radii):.0f} mm from the base axis, "
              f"allowed {REACH[0]:.0f}..{REACH[1]:.0f} mm - change READY_POSE or RECTANGLE")  # fmt: skip
    else:
        # client.execute() waits until a move is DONE -> the robot stops at every corner.
        # For blending, all moves are sent in advance: one function block instance per move,
        # client.start() only gives the rising edge on Execute, the RC buffers the moves
        # (AbortingMode BUFFER, the default) and blends from one into the next.
        moves = []
        for dx, dy in offsets:
            target = copy.deepcopy(corner)
            target.X += dx
            target.Y += dy
            move_linear = MC_MoveLinearAbsoluteFB()  # a new instance for every move
            move_linear.ParCmd.Position = target
            move_linear.ParCmd.VelocityRate = VELOCITY
            move_linear.ParCmd.TurnMode = TURN_MODE
            move_linear.ParCmd.ConfigMode.Shoulder = ArmConfigShoulder(CONFIG_MODE)
            move_linear.ParCmd.ConfigMode.Elbow = ArmConfigElbow(CONFIG_MODE)
            move_linear.ParCmd.ConfigMode.Wrist = ArmConfigWrist(CONFIG_MODE)
            move_linear.ParCmd.BlendingMode = BLENDING_MODE  # blend into the next move
            move_linear.ParCmd.BlendingParameter[0] = BLENDING_PARAMETER
            moves.append(move_linear)
        moves[-1].ParCmd.BlendingMode = BlendingMode.EXACT_STOP  # the last move stops exactly
        started = time.monotonic()
        for move_linear in moves:
            client.start(move_linear)  # send all moves, do not wait
        for n, move_linear in enumerate(moves, start=2):
            client.wait_done(move_linear, timeout=60.0)  # Done in this order; resets Execute
            print(
                f"{n}. linear to X={move_linear.ParCmd.Position.X:.1f} Y={move_linear.ParCmd.Position.Y:.1f}"
            )
        # compare with BLENDING_MODE = EXACT_STOP: blended corners must be clearly faster
        print(f"   rectangle in {time.monotonic() - started:.1f} s ({BLENDING_MODE.name})")

    # 6. your moves here - e.g. 50 mm up in a straight line:
    #   target = copy.deepcopy(corner)
    #   target.Z += 50.0
    #   move_linear = MC_MoveLinearAbsoluteFB()
    #   move_linear.ParCmd.Position = target
    #   move_linear.ParCmd.TurnMode = TURN_MODE
    #   move_linear.ParCmd.VelocityRate = VELOCITY
    #   client.execute(move_linear, timeout=60.0)

    # 7. joint move back to the start position
    move_axes = MC_MoveAxesAbsoluteFB()
    move_axes.ParCmd.JointPosition = start
    move_axes.ParCmd.VelocityRate = VELOCITY
    client.execute(move_axes, timeout=60.0)
    position = client.execute(MC_ReadActualPositionFB()).OutCmd
    back = position.ActualJointPosition
    print("7. back at start:   J1..J6 =", " ".join(f"{getattr(back, f'J{i}'):.1f}" for i in range(1, 7)))

except BaseException as exc:  # error or Ctrl+C: stop the robot
    print(f"\nstopping the robot: {exc!r}")
    client.execute(MC_GroupStopFB(), timeout=5.0, check=False)
    raise

finally:
    # ========================================================================= switch off
    client.disable(enable)
    print(f"robot enabled: {enable.Enabled}")
    client.close()  # stops the RobotTask and closes the connection

print("done")

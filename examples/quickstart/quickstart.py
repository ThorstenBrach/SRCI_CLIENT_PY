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

"""SRCI quickstart: initialize, switch on the robot, move, switch off.

    python quickstart.py            robot behind the PLC gateway (THE ROBOT MOVES)
    python quickstart.py --sim      SRCI SDK simulator instead of a robot (no PLC needed)

Read from top to bottom:

* ``main()``       connect, initialize the RobotTask, switch on the robot, run the program,
                   switch off
* ``configure()``  every parameter of the RobotTask (ParCfg) - the ones not needed are comments
* ``program()``    the moves: joint move into an elbow-bent pose, a rectangle with linear moves,
                   back to the start - add your own moves there
* helper functions (read the position, move)

The poses are made for a JAKA MiniCobo (zero position = arm straight up, reach 580 mm). For another
robot change READY_POSE and RECTANGLE. Try a new pose with a low OVERRIDE first.
"""

from __future__ import annotations

import copy
import math
import sys

from srci.api import SrciClient
from srci.fb import (
    MC_ChangeSpeedOverrideFB,
    MC_EnableRobotFB,
    MC_GroupResetFB,
    MC_GroupStopFB,
    MC_MoveAxesAbsoluteFB,
    MC_MoveDirectAbsoluteFB,
    MC_MoveLinearAbsoluteFB,
    MC_ReadActualPositionFB,
)
from srci.transport import TcpTransport, Transport
from srci.types import (
    MessageLevel,
    RobotCartesianPosition,
    RobotJointPosition,
    RobotTaskParCfg,
    SyncMode,
)

# ----------------------------------------------------------------------------- settings

HOST = "192.168.2.10"  # PLC gateway (TwinCAT FB_SrciTcpGateway)
PORT = 5000
TELEGRAM_LENGTH = 256  # bytes per direction, as configured in the PLC / robot
OVERRIDE = 30.0  # speed override [%] for all moves
VELOCITY = 30.0  # velocity of each move [% of the reference velocity]

# elbow-bent pose [deg] for the rectangle: shoulder (J2) and elbow (J3) bent - away from the
# stretched arm; J5 = 90 keeps the wrist away from its singularity (J5 = 0)
READY_POSE = {"J1": 0.0, "J2": 30.0, "J3": 60.0, "J4": 0.0, "J5": 90.0, "J6": 0.0}
RECTANGLE = (100.0, 80.0)  # size in X and Y [mm], horizontal, starting at the TCP of READY_POSE
REACH = (150.0, 520.0)  # the corners must lie in this distance from the base axis [mm] (MiniCobo: 580)


# ----------------------------------------------------------------------------- main: connect, switch on, run the program, switch off


def main(argv: list[str]) -> int:
    transport: Transport
    if "--sim" in argv:
        # SRCI SDK simulator in-process (needs the locally built SDK library, SRCI_SDK_SIM_LIB)
        from srci.sim.sdk import SdkSimulator, sdk_transport

        sim = SdkSimulator()
        sim.set_move_cycles(100)  # a simulated move takes 1 s
        transport = sdk_transport(sim, TELEGRAM_LENGTH, TELEGRAM_LENGTH)
    else:
        transport = TcpTransport(HOST, PORT, TELEGRAM_LENGTH, TELEGRAM_LENGTH, response_timeout=0.1)
        if (
            "--yes" not in argv
            and input("THE ROBOT WILL MOVE. Is the working area clear? [yes/no] ") != "yes"
        ):
            return 0

    with SrciClient(transport) as client:
        # 1. RobotTask: parameters before the first cycle, then wait for the initialization
        #    (the RobotTask initializes the interface and reads robot data and configuration)
        configure(client.program.config)
        client.wait_initialized(timeout=15.0)
        robot = client.program.axes_group.State.RobotData
        print(f"connected: {robot.RCManufacturer} {robot.RCOrderID}, firmware {robot.RCFirmwareVersion}")

        # 2. reset pending errors
        client.execute(MC_GroupResetFB())

        # 3. switch on the robot (power, brakes released); Enable stays TRUE until disable()
        enable = client.enable(MC_EnableRobotFB())
        print(f"robot enabled: {enable.Enabled}")

        # 4. speed override for all following moves
        override = MC_ChangeSpeedOverrideFB()
        override.ParCmd.Override = OVERRIDE
        client.execute(override)

        # 5. move - stop the robot on any error and on Ctrl+C
        try:
            program(client, check_reach="--sim" not in argv)  # the simulator has no real kinematics
        except BaseException as exc:
            print(f"\nstopping the robot: {exc!r}")
            client.execute(MC_GroupStopFB(), timeout=5.0, check=False)
            raise
        finally:
            # 6. switch off the robot
            client.disable(enable)
            print(f"robot enabled: {enable.Enabled}")
    print("done")
    return 0


# ----------------------------------------------------------------------------- RobotTask parameters


def configure(cfg: RobotTaskParCfg) -> None:
    """All parameters of the RobotTask (MC_RobotTaskFB.ParCfg). They are used for the
    initialization; the lines commented out show the default value."""
    # --- communication
    cfg.Com.TelegramLengthPlcToRob = TELEGRAM_LENGTH  # [bytes] PLC -> RC, = PROFINET module size
    cfg.Com.TelegramLengthRobToPlc = TELEGRAM_LENGTH  # [bytes] RC -> PLC
    cfg.Com.LifeSignTimeOut = (
        100  # [ms] RC: connection lost if the LifeSign stops (default 50; Python: margin)
    )
    # cfg.Com.TwoSequences = False                     # 2nd sequence in the telegram (e.g. jog while a program waits)

    # --- client (PLC / Python)
    # cfg.Plc.CycleTime = 10                           # [ms] cycle time of the client
    # cfg.Plc.Parameter.ManufacturedID = 0             # identification of the client (information only)
    # cfg.Plc.Parameter.OrderID = ""
    # cfg.Plc.Parameter.SerialNumber = ""
    # cfg.Plc.Parameter.FirmwareVersion = ""
    # cfg.Plc.Parameter.InterfaceVersion = ""

    # synchronization of the user data with the RC: [0] at the start, [1] while running
    # NO_SYNCHRONIZATION, CLIENT_TO_SERVER, SERVER_TO_CLIENT, AUTOMATIC
    sync = cfg.Plc.Parameter.SynchronizationModes
    sync.Tool[0] = sync.Tool[1] = SyncMode.NO_SYNCHRONIZATION
    # sync.Frame[0] = sync.Frame[1] = SyncMode.NO_SYNCHRONIZATION
    # sync.Load[0] = sync.Load[1] = SyncMode.NO_SYNCHRONIZATION
    # sync.WorkAreas[0] = sync.WorkAreas[1] = SyncMode.NO_SYNCHRONIZATION   # needs ReadWorkArea (not Core)
    # sync.SWLimits[0] = sync.SWLimits[1] = SyncMode.NO_SYNCHRONIZATION
    # sync.DefaultDynamics[0] = sync.DefaultDynamics[1] = SyncMode.NO_SYNCHRONIZATION
    # sync.ReferenceDynamics[0] = sync.ReferenceDynamics[1] = SyncMode.NO_SYNCHRONIZATION
    # synchronization needs a confirmation of the user
    # cfg.Plc.Parameter.SyncUserInteraction.Tool = False   # also .Frame .Load .WorkAreas .SWLimits
    #                                                      # .DefaultDynamics .ReferenceDynamics

    # optional cyclic data PLC -> RC (sent in every telegram)
    # cfg.Plc.OptionalCyclic.UseCallSubprogram = False     # data for a subprogram (CallSubprogram)
    # cfg.Plc.OptionalCyclic.UseCartesianPosition = False  # cartesian position X..Rz
    # cfg.Plc.OptionalCyclic.UseJointPosition = False      # joint position J1..J6
    # cfg.Plc.OptionalCyclic.UseForce = False              # force X..Rz
    # cfg.Plc.OptionalCyclic.UseTwoSequences = False       # two sequences
    # cfg.Plc.OptionalCyclic.UseCartesianPositionExt = False  # external axes E2..E6
    # cfg.Plc.OptionalCyclic.UseJointPositionExt = False      # external axes E2..E6

    # --- robot controller
    cfg.Rob.Parameter.MessageLevel = (
        MessageLevel.WARNING
    )  # messages of the RC from: DEBUG, INFO, WARNING, ERROR
    # cfg.Rob.Parameter.WaitAtBlendingZone = False     # FALSE: blending zone may be left without the next command
    # cfg.Rob.Parameter.AllowSecSeqWhileSubprogram = False
    # cfg.Rob.Parameter.AllowDynamicBlending = False
    # cfg.Rob.Parameter.DelayTime = 0                  # [ms] wait before the 1st move of an empty queue
    # cfg.Rob.Parameter.WaitForNrOfCmd = 0             # moves needed before the RC starts (blending)
    # cfg.Rob.Parameter.SyncDelay = 0                  # [ms] before SyncReaction on inconsistent user data
    # cfg.Rob.Parameter.SyncReaction = SyncReaction.NO_REACTION  # (srci.types) NO_AUTOMATIC_DISABLE,
    #                                                 # INTERRUPT_WHEN_SEQUENCE_IS_EMPTY, IMMEDIATE_INTERRUPT

    # optional cyclic data RC -> PLC (in every telegram, e.g. for MC_ReadActualPositionCyclicFB)
    # cfg.Rob.OptionalCyclic.UseCartesianPosition = False  # cartesian position X..Rz
    # cfg.Rob.OptionalCyclic.UseJointPosition = False      # joint position J1..J6
    # cfg.Rob.OptionalCyclic.UseForce = False              # force X..Rz
    # cfg.Rob.OptionalCyclic.UseCurrent = False            # motor currents J1..J6
    # cfg.Rob.OptionalCyclic.UseCallSubprogram = False
    # cfg.Rob.OptionalCyclic.UseTwoSequences = False
    # cfg.Rob.OptionalCyclic.UseCartesianPositionExt = False  # also UseJointPositionExt,
    # cfg.Rob.OptionalCyclic.UseForceExt = False              # UseCurrentExt (external axes)


# ----------------------------------------------------------------------------- the program


def program(client: SrciClient, check_reach: bool = True) -> None:
    """The moves. Add your own moves where it says so."""
    start, _ = read_position(client)
    show("start", client)

    # 1. joint move into the elbow-bent pose
    ready = copy.deepcopy(start)
    for joint, angle in READY_POSE.items():
        setattr(ready, joint, angle)
    move_joints(client, ready)
    show("1. elbow-bent pose", client)

    # 2..5. rectangle with linear moves in the horizontal plane, orientation unchanged
    _, corner = read_position(client)
    width, depth = RECTANGLE
    corners = []
    for dx, dy in ((width, 0.0), (width, depth), (0.0, depth), (0.0, 0.0)):
        p = copy.deepcopy(corner)
        p.X += dx
        p.Y += dy
        corners.append(p)
    radii = [math.hypot(p.X, p.Y) for p in corners]
    if check_reach and not all(REACH[0] <= r <= REACH[1] for r in radii):
        print(f"rectangle skipped: corners {min(radii):.0f}..{max(radii):.0f} mm from the base axis, "
              f"allowed {REACH[0]:.0f}..{REACH[1]:.0f} mm - change READY_POSE or RECTANGLE")  # fmt: skip
    else:
        for n, p in enumerate(corners, start=2):
            move_linear(client, p)
            show(f"{n}. linear to corner {n - 1}", client)

    # 6. your moves here, e.g. 50 mm up in a straight line and back as PTP:
    #   _, tcp = read_position(client)
    #   above = copy.deepcopy(tcp)
    #   above.Z += 50.0
    #   move_linear(client, above)
    #   move_direct(client, tcp)

    # 7. back to the start position
    move_joints(client, start)
    show("7. back at start", client)


# ----------------------------------------------------------------------------- helpers (used by program)


def read_position(client: SrciClient) -> tuple[RobotJointPosition, RobotCartesianPosition]:
    """Actual position: (joints [deg], cartesian [mm / deg])."""
    out = client.execute(MC_ReadActualPositionFB()).OutCmd
    return out.ActualJointPosition, out.ActualCartesianPosition


def move_joints(client: SrciClient, target: RobotJointPosition) -> None:
    """PTP move in joint space to ``target`` (RobotJointPosition, degrees)."""
    move = MC_MoveAxesAbsoluteFB()
    move.ParCmd.JointPosition = copy.deepcopy(target)
    move.ParCmd.VelocityRate = VELOCITY
    client.execute(move, timeout=60.0)


def move_linear(client: SrciClient, target: RobotCartesianPosition) -> None:
    """Straight line of the TCP to ``target`` (RobotCartesianPosition, mm / degrees)."""
    move = MC_MoveLinearAbsoluteFB()
    move.ParCmd.Position = copy.deepcopy(target)
    move.ParCmd.VelocityRate = VELOCITY
    client.execute(move, timeout=60.0)


def move_direct(client: SrciClient, target: RobotCartesianPosition) -> None:
    """PTP move to a cartesian ``target`` (the TCP path is not a straight line)."""
    move = MC_MoveDirectAbsoluteFB()
    move.ParCmd.Position = copy.deepcopy(target)
    move.ParCmd.VelocityRate = VELOCITY
    client.execute(move, timeout=60.0)


def show(text: str, client: SrciClient) -> None:
    joints, tcp = read_position(client)
    print(f"{text:<30} J1..J6 = " + " ".join(f"{getattr(joints, f'J{i}'):7.2f}" for i in range(1, 7))
          + f"   XYZ = {tcp.X:7.1f} {tcp.Y:7.1f} {tcp.Z:7.1f}")  # fmt: skip


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

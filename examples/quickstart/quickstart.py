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

Read from top to bottom: ``main()`` (connect, switch on the robot, run the program, switch off),
``program()`` (the moves - add your own there), the helper functions. All moves are relative to
the position of the robot at the start and end there again.
"""

from __future__ import annotations

import copy
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
from srci.types import RobotCartesianPosition, RobotJointPosition

# ----------------------------------------------------------------------------- settings

HOST = "192.168.2.10"  # PLC gateway (TwinCAT FB_SrciTcpGateway)
PORT = 5000
TELEGRAM_LENGTH = 256  # bytes per direction, as configured in the PLC / robot
OVERRIDE = 30.0  # speed override [%] for all moves
VELOCITY = 30.0  # velocity of each move [% of the reference velocity]


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
        # 1. RobotTask: configuration before the first cycle, then wait for the initialization
        client.program.config.Com.LifeSignTimeOut = 100  # [ms] margin for Python (no real-time)
        client.wait_initialized(timeout=15.0)
        robot = client.program.axes_group.State.RobotData
        print(f"connected: {robot.RCManufacturer} {robot.RCOrderID}, firmware {robot.RCFirmwareVersion}")

        # 2. reset errors, switch on the robot (power, brakes), set the speed override
        client.execute(MC_GroupResetFB())
        enable = client.enable(MC_EnableRobotFB())  # stays enabled until client.disable(enable)
        override = MC_ChangeSpeedOverrideFB()
        override.ParCmd.Override = OVERRIDE
        client.execute(override)

        # 3. move - stop the robot on any error and on Ctrl+C
        try:
            program(client)
        except BaseException as exc:
            print(f"\nstopping the robot: {exc!r}")
            client.execute(MC_GroupStopFB(), timeout=5.0, check=False)
            raise
        finally:
            # 4. switch off the robot
            client.disable(enable)
    print("done")
    return 0


# ----------------------------------------------------------------------------- the program


def program(client: SrciClient) -> None:
    """The moves. Every target is computed from the start position - change the offsets or add
    lines like these. Check the directions with a low OVERRIDE first: which way +20 deg on J2/J3
    goes depends on the robot and its start pose."""
    start_joints, _ = read_position(client)
    show("start", client)

    # 1. joint move: base (J1) +20 deg
    target = copy.deepcopy(start_joints)
    target.J1 += 20.0
    move_joints(client, target)
    show("1. J1 +20 deg", client)

    # 2. joint move: bend shoulder (J2) and elbow (J3) - the TCP moves out of the upright pose
    target.J2 += 20.0
    target.J3 += 20.0
    move_joints(client, target)
    show("2. J2/J3 +20 deg", client)

    # 3. straight line: TCP 50 mm down (Z), orientation unchanged
    _, tcp = read_position(client)
    work = copy.deepcopy(tcp)
    tcp.Z -= 50.0
    move_linear(client, tcp)
    show("3. linear Z -50 mm", client)

    # 4. cartesian PTP: back 50 mm up
    move_direct(client, work)
    show("4. direct Z +50 mm", client)

    # your moves here, e.g.:
    #   target.J6 += 30.0
    #   move_joints(client, target)

    # back to the start
    move_joints(client, start_joints)
    show("back at start", client)


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
    print(f"{text:<28} J1..J6 = " + " ".join(f"{getattr(joints, f'J{i}'):7.2f}" for i in range(1, 7))
          + f"   XYZ = {tcp.X:7.1f} {tcp.Y:7.1f} {tcp.Z:7.1f}")  # fmt: skip


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

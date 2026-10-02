# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      examples.jaka_minicobo.minicobo
#  Author:      Thorsten Brach
#  Date:        2026-10-02
#
#  Description:
#    First steps with a real robot (JAKA MiniCobo) behind a TwinCAT PLC that maps
#    the SRCI telegrams from TCP/IP to PROFINET (SRCI_TcpGateway).
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

"""First steps with a JAKA MiniCobo behind a TwinCAT PLC gateway (TCP/IP <-> PROFINET).

``python minicobo.py info``
    connect, initialize, show robot data, configuration, SW limits, position and messages.
    The robot is **not** enabled and does not move.

``python minicobo.py move --joint 6 --delta 5``
    enable the robot, move ONE joint by a few degrees relative to its current position
    (slow: override and velocity in %), move back, disable. **The robot moves.** Asks for
    confirmation unless ``--yes`` is given.

Gateway: 192.168.2.10:5000, 256 bytes per direction (change with ``--host``/``--port``/
``--length``). ``--sdk-tcp`` runs the same script against the SRCI SDK simulator behind a
local TCP gateway (dry run without robot; needs the locally built SDK library).
"""

from __future__ import annotations

import argparse
import contextlib
import copy
import dataclasses
import logging
import sys
import time
from collections.abc import Iterator
from typing import Any

from srci.api import CommandError, SrciClient, WaitTimeoutError
from srci.fb import (
    MC_ChangeSpeedOverrideFB,
    MC_EnableRobotFB,
    MC_GroupResetFB,
    MC_GroupStopFB,
    MC_MoveAxesAbsoluteFB,
    MC_ReadActualPositionFB,
    MC_ReadRobotSWLimitsFB,
)
from srci.logging_bridge import PythonLogger
from srci.transport import TcpTransport, Transport, TransportConnectError
from srci.types import MessageLevel, Severity

# ---------------------------------------------------------------------------- configuration

HOST = "192.168.2.10"  # TwinCAT PLC (FB_SrciTcpGateway)
PORT = 5000
TELEGRAM_LENGTH = 256  # bytes per direction = PROFINET module size of the robot
JOINTS = 6  # MiniCobo: 6 axes
MAX_DELTA = 30.0  # [deg] largest relative move this example accepts

# Functions of the profile "Core" in RCSupportedFunctions (spec table 5-2; CreateServerLog,
# ReadServerLog, CreateClientLog and ReadClientLog have no bit). This example only uses Core
# functions: the RobotTask (ReadRobotData, ExchangeConfiguration, ReadMessages), GroupReset,
# EnableRobot, ChangeSpeedOverride, ReadRobotSWLimits, ReadActualPosition, MoveAxesAbsolute,
# GroupStop. The synchronization of user data is off (no ReadWorkArea etc. during the init).
CORE = (
    "ReadRobotData", "EnableRobot", "GroupReset", "ReadActualPosition", "ReadActualPositionCyclic",
    "ExchangeConfiguration", "SetSequence", "ChangeSpeedOverride", "ReadMessages",
    "ReadRobotReferenceDynamics", "WriteFrameData", "WriteToolData", "WriteLoadData",
    "WriteRobotReferenceDynamics", "WriteRobotDefaultDynamics", "ReadRobotDefaultDynamics",
    "ReadFrameData", "ReadToolData", "ReadLoadData", "ReadRobotSWLimits", "GroupJog",
    "MoveLinearAbsolute", "MoveDirectAbsolute", "MoveAxesAbsolute", "GroupStop", "GroupContinue",
    "GroupInterrupt", "ReturnToPrimary",
)  # fmt: skip

# ---------------------------------------------------------------------------- output


def section(title: str) -> None:
    print(f"\n=== {title} " + "=" * max(0, 70 - len(title)))


def show(name: str, value: Any) -> None:
    print(f"  {name:<30} {value}")


def joints(pos: Any) -> str:
    return "  ".join(f"J{i}={getattr(pos, f'J{i}'):8.2f}" for i in range(1, JOINTS + 1))


def cartesian(pos: Any) -> str:
    return "  ".join(f"{n}={getattr(pos, n):8.2f}" for n in ("X", "Y", "Z", "Rx", "Ry", "Rz"))


# ---------------------------------------------------------------------------- connection


@contextlib.contextmanager
def open_transport(args: argparse.Namespace) -> Iterator[tuple[Transport, bool]]:
    """TCP connection to the PLC gateway (or to the SDK simulator for a dry run).

    The second value is True for the simulator."""
    length = args.length
    if not args.sdk_tcp:
        # response_timeout: the PLC answers within a few PLC cycles; a late answer closes the
        # connection (no framing) and the next cycle reconnects
        with TcpTransport(args.host, args.port, length, length, response_timeout=0.1) as transport:
            yield transport, False
        return

    from srci.sim.gateway import PlcGatewaySimulator
    from srci.sim.sdk import SdkNotAvailableError, SdkSimulator

    try:
        sim = SdkSimulator()
    except SdkNotAvailableError as exc:
        sys.exit(f"SDK simulator not available: {exc}")
    sim.set_move_cycles(50)  # simulated motions take 0.5 s
    with (
        sim,
        PlcGatewaySimulator(lambda telegram: sim.exchange(telegram, length), length, length) as gateway,
        TcpTransport("127.0.0.1", gateway.port, length, length, response_timeout=0.5) as transport,
    ):
        yield transport, True


def create_client(transport: Transport, args: argparse.Namespace, simulator: bool) -> SrciClient:
    client = SrciClient(transport, realtime=not (args.fast and simulator))
    cfg = client.program.config
    # Python is no real-time system (scheduler, garbage collector): more margin than the 50 ms
    # default before the RC considers the connection lost
    cfg.Com.LifeSignTimeOut = args.lifesign_ms
    # messages of the robot controller from severity WARNING on
    cfg.Rob.Parameter.MessageLevel = MessageLevel.WARNING
    if args.debug:
        client.program.external_logger = PythonLogger()  # every telegram -> logger srci.plc
        client.program.log_level = Severity.DEBUG
    return client


def initialize(client: SrciClient, transport: Transport, timeout: float) -> None:
    section("Connect and initialize")
    started = time.monotonic()
    try:
        client.wait_initialized(timeout=timeout)
    except WaitTimeoutError:
        ag = client.program.axes_group
        rt = client.program.robot_task
        print("  not initialized - diagnosis:")
        show("TelegramState", ag.Cyclic.RobToPlc.TelegramState.name)
        show("RobotTask ErrorID", f"16#{int(rt.ErrorID):04X}")
        show("transport", transport.statistics)
        print(
            "  hints: exchanges = 0, timeouts > 0 -> the gateway accepts, but does not answer\n"
            "         (gateway Connected / ErrorID, lengths in MAIN);\n"
            "         ERROR_163_TELEGRAM_LENGTH_MISMATCH -> --length must match the PROFINET module;\n"
            "         UNDEFINED with exchanges > 0 -> the PLC answers, but the RC sends nothing\n"
            "         (PROFINET mapping of RobotInData, robot in SRCI/remote mode?)"
        )
        raise
    rt_ag = client.program.axes_group.Cyclic.RobToPlc
    show("Initialized", client.program.robot_task.Initialized)
    show("TelegramState", rt_ag.TelegramState.name)
    show("SRCI version RC", f"{rt_ag.SRCIVersion.MajorVersion}.{rt_ag.SRCIVersion.MinorVersion}")
    show("time until initialized [s]", f"{time.monotonic() - started:.2f}")


# ---------------------------------------------------------------------------- info


def show_robot(client: SrciClient) -> None:
    section("Robot data (ReadRobotData, read by the RobotTask)")
    ag = client.program.axes_group
    robot = ag.State.RobotData
    show("RCManufacturer", robot.RCManufacturer)
    show("RCOrderID", robot.RCOrderID)
    show("RCSerialNumber", robot.RCSerialNumber)
    show("RASerialNumber", robot.RASerialNumber)
    show("RCFirmwareVersion", robot.RCFirmwareVersion)
    show("RCInterpreterVersion", robot.RCInterpreterVersion)
    show("InterpreterCycleTime [ms]", robot.InterpreterCycleTime)
    show_supported_functions(robot.RCSupportedFunctions)

    section("Configuration (ExchangeConfiguration)")
    config = ag.State.ConfigurationData
    show("HighestToolIndex", config.HighestToolIndex)
    show("HighestFrameIndex", config.HighestFrameIndex)
    show("HighestLoadIndex", config.HighestLoadIndex)


def show_supported_functions(functions: Any) -> None:
    """RCSupportedFunctions (spec table 6-18): the Core functions, then the number of the others."""
    core_missing = [name for name in CORE if not getattr(functions, name)]
    others = [
        f.name
        for f in dataclasses.fields(functions)
        if f.name not in CORE and not f.name.startswith(("Byte", "Reserved")) and getattr(functions, f.name)
    ]
    show("Core functions supported", f"{len(CORE) - len(core_missing)} of {len(CORE)}")
    if core_missing:
        show("Core functions missing", ", ".join(core_missing))
    if not others:
        show("other functions supported", "none (Core profile only)")
    elif len(others) <= 8:
        show("other functions supported", ", ".join(others))
    else:
        show("other functions supported", f"{len(others)} (e.g. {', '.join(others[:5])}, ...)")


def read_limits(client: SrciClient) -> Any:
    section("Software limits (ReadRobotSWLimits)")
    limits = client.execute(MC_ReadRobotSWLimitsFB()).OutCmd.LimitValues
    for j in range(1, JOINTS + 1):
        show(
            f"J{j} [deg]",
            f"{getattr(limits, f'J{j}LowerLimit'):8.2f} .. {getattr(limits, f'J{j}UpperLimit'):8.2f}",
        )
    return limits


def read_position(client: SrciClient) -> Any:
    section("Actual position (ReadActualPosition, tool 0 / frame 0)")
    out = client.execute(MC_ReadActualPositionFB()).OutCmd
    show("joints [deg]", joints(out.ActualJointPosition))
    show("cartesian [mm/deg]", cartesian(out.ActualCartesianPosition))
    return out.ActualJointPosition


def show_messages(client: SrciClient, transport: Transport) -> None:
    section("Messages of the robot controller and the client")
    messages = [m for m in client.program.message_log if m.MessageCode]
    if not messages:
        show("messages", "none")
    for m in messages[:10]:  # newest first
        show(f"{m.Severity.name} 16#{int(m.MessageCode):04X}", m.MessageText)
    section("Transport")
    stats = transport.statistics
    show("exchanges", stats.exchanges)
    show("reconnects / timeouts", f"{stats.connects - 1} / {stats.timeouts}")
    show("round trip last / max [ms]", f"{stats.last_rtt * 1000:.1f} / {stats.max_rtt * 1000:.1f}")


# ---------------------------------------------------------------------------- move


def move_joints(position: Any, velocity: float) -> MC_MoveAxesAbsoluteFB:
    move = MC_MoveAxesAbsoluteFB()
    for j in range(1, JOINTS + 1):
        setattr(move.ParCmd.JointPosition, f"J{j}", getattr(position, f"J{j}"))
    # optional parameter: % of the reference velocity, -1 = default dynamics of the RC.
    # Acceleration/deceleration stay at the default: not every RC supports them (16#8E03).
    move.ParCmd.VelocityRate = velocity
    return move


def confirm(text: str) -> bool:
    try:
        return input(f"\n{text} [yes/no] ").strip().lower() in ("y", "yes", "j", "ja")
    except EOFError:
        return False


def move_relative(client: SrciClient, args: argparse.Namespace) -> None:
    joint = f"J{args.joint}"
    limits = read_limits(client)
    start = read_position(client)
    target = copy.copy(start)
    setattr(target, joint, getattr(start, joint) + args.delta)
    lower, upper = getattr(limits, f"{joint}LowerLimit"), getattr(limits, f"{joint}UpperLimit")
    if not lower < getattr(target, joint) < upper:
        raise SystemExit(
            f"{joint} target {getattr(target, joint):.2f} outside the SW limits {lower} .. {upper}"
        )

    section("Move")
    show("joint", joint)
    show("start -> target [deg]", f"{getattr(start, joint):.2f} -> {getattr(target, joint):.2f} -> back")
    show("override / velocity [%]", f"{args.override} / {args.velocity}")
    if not args.yes and not confirm("THE ROBOT WILL MOVE. Is the working area clear?"):
        print("  cancelled")
        return

    client.execute(MC_GroupResetFB())
    enable = client.enable(MC_EnableRobotFB())
    show("EnableRobot.Enabled", enable.Enabled)
    try:
        override = MC_ChangeSpeedOverrideFB()
        override.ParCmd.Override = args.override
        client.execute(override)
        client.execute(move_joints(target, args.velocity), timeout=60.0)
        show("reached", joints(read_position_quiet(client)))
        client.execute(move_joints(start, args.velocity), timeout=60.0)
        show("back at start", joints(read_position_quiet(client)))
    except BaseException:  # also Ctrl+C: stop the robot before the connection ends
        print("\n  stopping the robot (GroupStop)")
        with contextlib.suppress(Exception):
            client.execute(MC_GroupStopFB(), timeout=5.0)
        raise
    finally:
        client.disable(enable)
        show("EnableRobot.Enabled", enable.Enabled)


def read_position_quiet(client: SrciClient) -> Any:
    return client.execute(MC_ReadActualPositionFB()).OutCmd.ActualJointPosition


# ---------------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["info", "move"])
    ap.add_argument("--host", default=HOST, help=f"IP of the PLC gateway (default {HOST})")
    ap.add_argument("--port", type=int, default=PORT, help=f"TCP port of the PLC gateway (default {PORT})")
    ap.add_argument(
        "--length", type=int, default=TELEGRAM_LENGTH, help="telegram length [bytes] per direction"
    )
    ap.add_argument(
        "--joint", type=int, default=6, choices=range(1, JOINTS + 1), help="joint to move (default 6)"
    )
    ap.add_argument("--delta", type=float, default=5.0, help="relative move [deg] (default 5)")
    ap.add_argument("--override", type=float, default=10.0, help="speed override [%%] (default 10)")
    ap.add_argument(
        "--velocity",
        type=float,
        default=10.0,
        help="velocity rate [%%] (default 10, -1 = default dynamics of the RC)",
    )
    ap.add_argument(
        "--lifesign-ms", type=int, default=100, help="LifeSign timeout of the RC [ms] (default 100)"
    )
    ap.add_argument("--timeout", type=float, default=15.0, help="time for the initialization [s]")
    ap.add_argument("--yes", action="store_true", help="move without asking")
    ap.add_argument("--debug", action="store_true", help="log every telegram (logger srci.plc)")
    ap.add_argument("--sdk-tcp", action="store_true", help="dry run against the SDK simulator (no robot)")
    ap.add_argument("--fast", action="store_true", help="simulator only: do not wait for the cycle time")
    args = ap.parse_args(argv)
    if not 0 < abs(args.delta) <= MAX_DELTA:
        ap.error(f"--delta must be between -{MAX_DELTA} and {MAX_DELTA} (and not 0)")
    if not 0 < args.override <= 100:
        ap.error("--override must be in 0 < x <= 100")
    if not (0 < args.velocity <= 100 or args.velocity == -1):
        ap.error("--velocity must be in 0 < x <= 100 or -1")

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING, format="%(name)s %(message)s")

    target = "SDK simulator" if args.sdk_tcp else f"{args.host}:{args.port}"
    print(f"SRCI gateway {target}, telegrams {args.length}/{args.length} bytes")
    try:
        with open_transport(args) as (transport, simulator):
            client = create_client(transport, args, simulator)
            try:
                initialize(client, transport, args.timeout)
                show_robot(client)
                if args.command == "info":
                    read_limits(client)
                    read_position(client)
                else:
                    move_relative(client, args)
                show_messages(client, transport)
            except (CommandError, WaitTimeoutError) as exc:
                print(f"\nERROR: {exc}")
                show_messages(client, transport)
                return 1
            finally:
                client.close()  # stops the cycle thread; the RC detects the missing LifeSign
    except TransportConnectError as exc:
        print(f"\nERROR: {exc}")
        print(
            "  is the PLC running, FB_SrciTcpGateway enabled (Listening) and the port open in the firewall?"
        )
        return 1
    print("\ndone")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

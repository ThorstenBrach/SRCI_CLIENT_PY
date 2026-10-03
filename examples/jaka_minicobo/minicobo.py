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

``python minicobo.py blending``
    which blending modes the RC accepts (tiny moves: 1 mm up / J6 +0.5 deg and back).

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
from pathlib import Path
from typing import Any

from srci.api import CommandError, SrciClient, WaitTimeoutError
from srci.fb import (
    MC_ChangeSpeedOverrideFB,
    MC_EnableRobotFB,
    MC_GroupResetFB,
    MC_GroupStopFB,
    MC_MoveAxesAbsoluteFB,
    MC_MoveLinearAbsoluteFB,
    MC_ReadActualPositionFB,
    MC_ReadRobotSWLimitsFB,
)
from srci.logging_bridge import PythonLogger
from srci.transport import TcpTransport, Transport, TransportConnectError
from srci.types import (
    ArmConfigElbow,
    ArmConfigShoulder,
    ArmConfigWrist,
    BlendingMode,
    MessageLevel,
    RobotLibraryConstants,
    Severity,
    TurnMode,
)

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
    if args.log or args.debug:
        # system log of all function blocks -> logger srci.plc (log file / console)
        client.program.external_logger = PythonLogger()
        client.program.log_level = Severity.DEBUG
    return client


_HANDLERS: list[logging.Handler] = []


def setup_logging(args: argparse.Namespace) -> None:
    """Console: warnings (everything with --debug). Log file: everything - the system log of the
    library (logger srci.plc), the transport (srci.transport) and the telegrams (srci.telegram)."""
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    for handler in _HANDLERS:  # main() called again (tests)
        root.removeHandler(handler)
        handler.close()
    _HANDLERS.clear()
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if args.debug else logging.WARNING)
    console.setFormatter(logging.Formatter("%(name)s %(message)s"))
    root.addHandler(console)
    _HANDLERS.append(console)
    if args.log:
        file = logging.FileHandler(args.log, mode="w", encoding="utf-8")
        file.setLevel(logging.DEBUG)
        file.setFormatter(
            logging.Formatter("%(asctime)s.%(msecs)03d %(levelname)-7s %(name)-14s %(message)s", "%H:%M:%S")
        )
        root.addHandler(file)
        _HANDLERS.append(file)


def trace_telegrams(transport: Transport, every: bool) -> None:
    """Log the telegrams (logger srci.telegram, level DEBUG, hex): the first 50 exchanges, then
    every change of the header (TelegramState, Control) and every 100th exchange; all of them
    with ``every``."""
    log = logging.getLogger("srci.telegram")
    exchange = transport.exchange
    count = 0
    last_key = b""

    def traced(out: bytes | bytearray) -> bytes:
        nonlocal count, last_key
        answer = exchange(out)
        count += 1
        key = bytes(out[6:7]) + answer[3:4]  # AxesGroupID/Control PLC -> RC, TelegramState RC -> PLC
        if every or count <= 50 or key != last_key or count % 100 == 0:
            log.debug("#%d PLC->RC %s", count, bytes(out).hex(" "))
            log.debug("#%d RC->PLC %s", count, bytes(answer).hex(" "))
        last_key = key
        return answer

    transport.exchange = traced  # type: ignore[method-assign]  # trace wrapper on this instance


def initialize(client: SrciClient, transport: Transport, timeout: float) -> None:
    section("Connect and initialize")
    started = time.monotonic()
    try:
        client.wait_initialized(timeout=timeout)
    except (CommandError, WaitTimeoutError):
        diagnose_initialization(client, transport)
        raise
    rt_ag = client.program.axes_group.Cyclic.RobToPlc
    show("Initialized", client.program.robot_task.Initialized)
    show("TelegramState", rt_ag.TelegramState.name)
    show("SRCI version RC", f"{rt_ag.SRCIVersion.MajorVersion}.{rt_ag.SRCIVersion.MinorVersion}")
    show("time until initialized [s]", f"{time.monotonic() - started:.2f}")


def diagnose_initialization(client: SrciClient, transport: Transport) -> None:
    """Why the RobotTask is not initialized: its step, the TelegramState and the raw headers."""
    program = client.program
    rt = program.robot_task
    rx = bytes(program._in[:18])  # last telegram RC -> PLC (header)
    tx = bytes(program._out[:18])  # last telegram PLC -> RC (header)
    print("  not initialized - diagnosis:")
    show("RobotTask step / ErrorID", f"{rt._stepCmd} / 16#{int(rt.ErrorID):04X} {rt.ErrorAddTxt}")
    show(
        "TelegramState (RC)",
        f"{rx[3] if len(rx) > 3 else '?'} {program.axes_group.Cyclic.RobToPlc.TelegramState.name}",
    )
    show("header RC -> PLC", rx.hex(" "))
    show("header PLC -> RC", tx.hex(" "))
    show("transport", transport.statistics)
    if not any(rx):
        print(
            "  -> the PLC answers, but RobotInData is all 0: the robot sends nothing over PROFINET\n"
            "     (PROFINET device in data exchange? RobotInData linked to the SRCI input module?\n"
            "      SRCI/PROFINET control active on the robot?)"
        )
    elif rx[0] == 0:
        print(
            "  -> byte 0 (SRCI version) is 0: RobotInData does not start with the SRCI telegram (module order?)"
        )
    print(
        "  hints: step 1 + ERR_TIMEOUT_CMD -> the RC never reported INITIALIZED (state above);\n"
        "         ERROR_163_TELEGRAM_LENGTH_MISMATCH -> --length must match the PROFINET module;\n"
        "         steps 2..7 -> the RC is initialized, but does not answer a command\n"
        "         (ReadMessages, ExchangeConfiguration, ReadRobotData) - run with --debug"
    )


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


# blending modes of spec table 6-9 with a typical parameter ([0], [1])
BLENDING_PROBES = [
    (BlendingMode.DEFINED_VELOCITY, (50.0, 0.0)),  # velocity at the corner [%]
    (BlendingMode.CORNER_DISTANCE, (5.0, 0.0)),  # radius [mm]
    (BlendingMode.MAX_CORNER_DEVIATION, (2.0, 0.0)),  # deviation [mm]
    (BlendingMode.CORNER_DISTANCE_2R, (5.0, 5.0)),  # radius before / after [mm]
    (BlendingMode.RAMP_OVERLAP, (50.0, 0.0)),  # overlap of the ramps [%]
    (BlendingMode.CORNER_DISTANCE_1R, (5.0, 0.0)),  # radius [mm]
]


def _probe_pair(client: SrciClient, kind: str, mode: BlendingMode, par: tuple[float, float],
                turn_mode: TurnMode, config_mode: int = 0) -> str:  # fmt: skip
    """A tiny move with ``mode`` (1 mm up / J6 +0.5 deg) and an EXACT_STOP move back; the result of
    the first one. A move the RC does not finish within 15 s is stopped (GroupStop + GroupReset)."""
    out = client.execute(MC_ReadActualPositionFB()).OutCmd
    first: Any
    back: Any
    if kind == "linear":
        start_c = copy.deepcopy(out.ActualCartesianPosition)
        up = copy.deepcopy(start_c)
        up.Z += 1.0
        first, back = MC_MoveLinearAbsoluteFB(), MC_MoveLinearAbsoluteFB()
        first.ParCmd.Position, back.ParCmd.Position = up, start_c
        first.ParCmd.TurnMode = back.ParCmd.TurnMode = turn_mode
        for move in (first, back):  # ConfigMode: 0 USE_CONFIG, 1 SAME, 2 FREE for shoulder, elbow, wrist
            move.ParCmd.ConfigMode.Shoulder = ArmConfigShoulder(config_mode)
            move.ParCmd.ConfigMode.Elbow = ArmConfigElbow(config_mode)
            move.ParCmd.ConfigMode.Wrist = ArmConfigWrist(config_mode)
    else:
        start_j = copy.deepcopy(out.ActualJointPosition)
        turned = copy.deepcopy(start_j)
        turned.J6 += 0.5
        first, back = MC_MoveAxesAbsoluteFB(), MC_MoveAxesAbsoluteFB()
        first.ParCmd.JointPosition, back.ParCmd.JointPosition = turned, start_j
    first.ParCmd.BlendingMode = mode
    first.ParCmd.BlendingParameter[0], first.ParCmd.BlendingParameter[1] = par
    client.start(first)
    client.start(back)  # BlendingMode EXACT_STOP (default)
    try:
        client.wait_done(first, timeout=15.0)
        result = "accepted"
    except CommandError as exc:
        result = f"rejected 16#{exc.error_id:04X}" + {
            0x8E05: " (BlendingMode not supported)",
            0x8E10: " (TurnMode not supported)",
        }.get(exc.error_id, "")
    except WaitTimeoutError:
        result = "no answer within 15 s"
    hanging = result.startswith("no answer")
    try:
        # after a rejected first move some RCs (JAKA) keep the move back INTERRUPTED -> stop it soon
        client.wait_done(back, timeout=15.0 if result == "accepted" else 3.0)
    except CommandError as exc:
        if result == "accepted":
            result = f"accepted, but the move back failed: {exc}"
    except WaitTimeoutError:
        hanging = True
        if result == "accepted":
            result = "accepted, but the move back did not finish within 15 s"
    if hanging:  # a move is still running on the RC: stop it
        client.execute(MC_GroupStopFB(), timeout=5.0, check=False)
    if result != "accepted":  # reset the error of the rejected command
        client.execute(MC_GroupResetFB(), timeout=5.0, check=False)
    return result


def probe_blending(client: SrciClient, args: argparse.Namespace) -> None:
    """Which TurnMode and which blending modes does the RC accept? Tiny moves (1 mm up / J6
    +0.5 deg) and back. A rejected command is not executed (16#8E05: BlendingMode, 16#8E10:
    TurnMode not supported)."""
    section("TurnMode and blending modes")
    if not args.yes and not confirm(
        "THE ROBOT WILL MOVE A LITTLE (1 mm / 0.5 deg). Is the working area clear?"
    ):
        print("  cancelled")
        return
    client.execute(MC_GroupResetFB())
    enable = client.enable(MC_EnableRobotFB())
    try:
        override = MC_ChangeSpeedOverrideFB()
        override.ParCmd.Override = args.override
        client.execute(override)
        # 1. TurnMode x ConfigMode of linear moves (without blending)
        combos: list[tuple[TurnMode, int]] = []
        for tm in TurnMode:
            for cm in (ArmConfigShoulder.USE_CONFIG, ArmConfigShoulder.SAME, ArmConfigShoulder.FREE):
                result = _probe_pair(client, "linear", BlendingMode.EXACT_STOP, (0.0, 0.0), tm, cm)
                show(f"TurnMode {tm.name}, ConfigMode {cm.name}", result)
                if result == "accepted":
                    combos.append((tm, int(cm)))
        if not combos:
            show("blending", "not tested - no TurnMode / ConfigMode works for MoveLinearAbsolute")
            return
        turn_mode, config_mode = combos[0]
        # 2. blending modes (linear with the working TurnMode, joint moves)
        supported = []
        for mode, par in BLENDING_PROBES:
            for kind in ("linear", "axes"):
                result = _probe_pair(client, kind, mode, par, turn_mode, config_mode)
                show(f"{mode.name} ({kind})", result)
                if result == "accepted":
                    supported.append(f"{mode.name} ({kind})")
        show(
            "linear: TurnMode / ConfigMode",
            ", ".join(f"{t.name}/{ArmConfigShoulder(c).name}" for t, c in combos),
        )
        show("blending supported", ", ".join(supported) if supported else "none - use EXACT_STOP")
    except BaseException:
        print("\n  stopping the robot (GroupStop)")
        with contextlib.suppress(Exception):
            client.execute(MC_GroupStopFB(), timeout=5.0)
        raise
    finally:
        client.disable(enable)


def read_position_quiet(client: SrciClient) -> Any:
    return client.execute(MC_ReadActualPositionFB()).OutCmd.ActualJointPosition


# ---------------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["info", "move", "blending"])
    ap.add_argument(
        "--srci-version",
        default="1.5",
        help="SRCI version sent to the RC in byte 0 of the header, e.g. 1.3 (default 1.5 of the library)",
    )
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
    ap.add_argument("--debug", action="store_true", help="show the whole log on the console as well")
    ap.add_argument(
        "--log", metavar="FILE", help="log file (default minicobo_<date>_<time>.log in the current folder)"
    )
    ap.add_argument("--no-log", action="store_true", help="no log file")
    ap.add_argument("--trace-all", action="store_true", help="log file: every telegram (else only changes)")
    ap.add_argument("--sdk-tcp", action="store_true", help="dry run against the SDK simulator (no robot)")
    ap.add_argument("--fast", action="store_true", help="simulator only: do not wait for the cycle time")
    args = ap.parse_args(argv)
    if not 0 < abs(args.delta) <= MAX_DELTA:
        ap.error(f"--delta must be between -{MAX_DELTA} and {MAX_DELTA} (and not 0)")
    if not 0 < args.override <= 100:
        ap.error("--override must be in 0 < x <= 100")
    if not (0 < args.velocity <= 100 or args.velocity == -1):
        ap.error("--velocity must be in 0 < x <= 100 or -1")

    try:
        major, minor = (int(part) for part in args.srci_version.split("."))
        if not (0 <= major <= 7 and 0 <= minor <= 31):
            raise ValueError
    except ValueError:
        ap.error("--srci-version must be <major>.<minor>, major 0..7, minor 0..31 (e.g. 1.3)")

    if args.no_log:
        args.log = None
    elif args.log is None:
        args.log = f"minicobo_{time.strftime('%Y%m%d_%H%M%S')}.log"
    setup_logging(args)
    if args.log:
        print(f"log file {Path(args.log).resolve()}")

    target = "SDK simulator" if args.sdk_tcp else f"{args.host}:{args.port}"
    print(f"SRCI gateway {target}, telegrams {args.length}/{args.length} bytes, SRCI version {major}.{minor}")
    # The RobotTask sends the version of the library (RobotLibraryConstants.SRCIVersion, byte 0:
    # bits 5..7 major, bits 0..4 minor). An RC with an older SRCI version (e.g. 1.3) may not
    # answer 1.5: change it for this process. The RobotTask only checks the major version of the RC.
    version = RobotLibraryConstants.SRCIVersion
    saved = (version.MajorVersion, version.MinorVersion)
    version.MajorVersion, version.MinorVersion = major, minor
    try:
        return run(args)
    finally:
        version.MajorVersion, version.MinorVersion = saved


def run(args: argparse.Namespace) -> int:
    try:
        with open_transport(args) as (transport, simulator):
            if args.log:
                trace_telegrams(transport, args.trace_all)
            client = create_client(transport, args, simulator)
            try:
                initialize(client, transport, args.timeout)
                show_robot(client)
                if args.command == "info":
                    read_limits(client)
                    read_position(client)
                elif args.command == "blending":
                    probe_blending(client, args)
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
    print("\ndone" + (f" - log file {Path(args.log).resolve()}" if args.log else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      examples.core_profile.core_profile_demo
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    SRCI example: every function of the profile "Core" (spec V1.5.9, table 5-2).
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

"""SRCI example: every function of the profile "Core" (spec V1.5.9, table 5-2).

Runs against

* the PLC gateway of a real robot:        ``python core_profile_demo.py --gateway 192.168.0.10:5000``
* the SRCI SDK simulator (in-process):    ``python core_profile_demo.py --sdk``
* the SDK simulator behind a local TCP
  gateway (same path as a real robot):     ``python core_profile_demo.py --sdk-tcp``

The SDK simulator needs the locally built SDK library (``SRCI_SDK_SIM_LIB``, not part of the
package). **With a real robot the demo moves the robot** - check the positions below first.

Explained step by step in README.md next to this file.
"""

from __future__ import annotations

import argparse
import contextlib
import logging
import sys
from collections.abc import Iterator
from typing import Any

import srci
from srci.api import CommandError, SrciClient
from srci.fb import (
    MC_ChangeSpeedOverrideFB,
    MC_EnableRobotFB,
    MC_ExchangeConfigurationFB,
    MC_GroupContinueFB,
    MC_GroupInterruptFB,
    MC_GroupJogFB,
    MC_GroupResetFB,
    MC_GroupStopFB,
    MC_MoveAxesAbsoluteFB,
    MC_MoveDirectAbsoluteFB,
    MC_MoveLinearAbsoluteFB,
    MC_ReadActualPositionCyclicFB,
    MC_ReadActualPositionFB,
    MC_ReadFrameDataFB,
    MC_ReadLoadDataFB,
    MC_ReadMessagesFB,
    MC_ReadRobotDataFB,
    MC_ReadRobotDefaultDynamicsFB,
    MC_ReadRobotReferenceDynamicsFB,
    MC_ReadRobotSWLimitsFB,
    MC_ReadToolDataFB,
    MC_ReturnToPrimaryFB,
    MC_SetSequenceFB,
    MC_WriteFrameDataFB,
    MC_WriteLoadDataFB,
    MC_WriteRobotDefaultDynamicsFB,
    MC_WriteRobotReferenceDynamicsFB,
    MC_WriteToolDataFB,
)
from srci.iec.rt import copy_into
from srci.logging_bridge import PythonLogger
from srci.transport import Transport
from srci.types import AbortingMode, JogMode, MessageLevel, SequenceFlag, Severity

TELEGRAM_LENGTH = 256  # bytes per direction, must match the gateway / robot configuration
TOOL = 1  # tool of all motions (index 0 = flange is fixed on the RC)

# ---------------------------------------------------------------------------- output


def section(title: str) -> None:
    print(f"\n=== {title} " + "=" * max(0, 70 - len(title)))


def show(name: str, value: Any) -> None:
    print(f"  {name:<28} {value}")


def joints(pos: Any) -> str:
    return "  ".join(f"J{i}={getattr(pos, f'J{i}'):8.2f}" for i in range(1, 7))


def cartesian(pos: Any) -> str:
    return "  ".join(f"{n}={getattr(pos, n):8.2f}" for n in ("X", "Y", "Z", "Rx", "Ry", "Rz"))


# ---------------------------------------------------------------------------- 1. RobotTask


def create_client(transport: Transport, realtime: bool) -> SrciClient:
    """RobotTask: the program with MC_RobotTaskFB and its configuration."""
    client = SrciClient(transport, realtime=realtime)
    cfg = client.program.config
    # cyclic position data RC -> PLC for MC_ReadActualPositionCyclicFB (spec 5.6.3)
    cfg.Rob.OptionalCyclic.UseJointPosition = True
    cfg.Rob.OptionalCyclic.UseCartesianPosition = True
    # messages of the robot controller from severity WARNING on (MC_ReadMessagesFB)
    cfg.Rob.Parameter.MessageLevel = MessageLevel.WARNING
    return client


def demo_robot_task(client: SrciClient) -> None:
    section("RobotTask - initialization")
    client.wait_initialized(timeout=10.0)
    rt = client.program.robot_task
    ag = client.program.axes_group
    show("Initialized", rt.Initialized)
    show("TelegramState", ag.Cyclic.RobToPlc.TelegramState.name)
    show(
        "SRCI version RC",
        f"{ag.Cyclic.RobToPlc.SRCIVersion.MajorVersion}.{ag.Cyclic.RobToPlc.SRCIVersion.MinorVersion}",
    )
    show("cycles until initialized", client.cycle)


# ---------------------------------------------------------------------------- 2. robot data, configuration


def demo_read_robot_data(client: SrciClient) -> None:
    section("ReadRobotData")
    rd = client.execute(MC_ReadRobotDataFB())
    out = rd.OutCmd
    show("RCManufacturer", out.RCManufacturer)
    show("RCSerialNumber", out.RCSerialNumber)
    show("RCFirmwareVersion", out.RCFirmwareVersion)
    show("RobotID", out.RobotID)
    show("InterpreterCycleTime [ms]", out.InterpreterCycleTime)
    show("J1..J6 used", all(getattr(out.AxisJointUsed, f"J{i}") for i in range(1, 7)))
    show("supports MoveLinearAbsolute", out.RCSupportedFunctions.MoveLinearAbsolute)


def demo_exchange_configuration(client: SrciClient) -> None:
    section("ExchangeConfiguration")
    # The RobotTask exchanges the configuration itself during the initialization; the block
    # can be used to read the result (and to change parameters while the robot runs).
    ex = MC_ExchangeConfigurationFB()
    copy_into(ex.ParCmd, client.program.robot_task._exchangeConfiguration.ParCmd)  # keep the config
    client.enable(ex)
    client.run_until(lambda: ex.OutCmd.HighestToolIndex > 0 or ex.Error, 5.0, "configuration")
    show("HighestToolIndex", ex.OutCmd.HighestToolIndex)
    show("HighestFrameIndex", ex.OutCmd.HighestFrameIndex)
    show("HighestLoadIndex", ex.OutCmd.HighestLoadIndex)
    show("NumberOfServerLogs", ex.OutCmd.NumberOfServerLogs)
    client.disable(ex)


def demo_read_messages(client: SrciClient) -> MC_ReadMessagesFB:
    section("ReadMessages")
    rm = MC_ReadMessagesFB()
    rm.ParCmd.MessageLevel = MessageLevel.INFO
    client.enable(rm)
    show("Valid", rm.Valid)
    show("active errors / warnings", f"{rm.OutCmd.NumberOfActiveErrors} / {rm.OutCmd.NumberOfActiveWarnings}")
    show("last message", rm.OutCmd.Text or "-")
    return rm  # stays enabled: new messages appear in OutCmd


def demo_group_reset_and_enable(client: SrciClient) -> MC_EnableRobotFB:
    section("GroupReset, EnableRobot")
    client.execute(MC_GroupResetFB())
    show("GroupReset", "done")
    enable = client.enable(MC_EnableRobotFB())
    show("EnableRobot.Enabled", enable.Enabled)
    return enable  # keep Enable = TRUE while the robot shall have power


def demo_change_speed_override(client: SrciClient, percent: float) -> None:
    section("ChangeSpeedOverride")
    ov = MC_ChangeSpeedOverrideFB()
    ov.ParCmd.Override = percent
    client.execute(ov)
    show("Override [%]", percent)


# ---------------------------------------------------------------------------- 3. positions


def demo_read_actual_position(client: SrciClient) -> None:
    section("ReadActualPosition")
    rp = client.execute(MC_ReadActualPositionFB())
    show("joints", joints(rp.OutCmd.ActualJointPosition))
    show("cartesian", cartesian(rp.OutCmd.ActualCartesianPosition))


def demo_read_actual_position_cyclic(client: SrciClient) -> MC_ReadActualPositionCyclicFB:
    section("ReadActualPositionCyclic")
    # needs the cyclic position data (config Rob.OptionalCyclic, see create_client);
    # no command: the block copies the positions of every received telegram
    cyc = MC_ReadActualPositionCyclicFB()
    cyc.ParCmd.ReadJointPosition = True
    cyc.ParCmd.ReadCartesianPosition = True
    client.enable(cyc)
    client.run(2)
    show("Enabled", cyc.Enabled)
    show("joints", joints(cyc.OutCmd.JointPosition))
    return cyc  # stays enabled: OutCmd follows the robot in every cycle


# ---------------------------------------------------------------------------- 4. tool, frame, load, dynamics


def demo_tool_frame_load(client: SrciClient) -> None:
    section("WriteToolData / ReadToolData")
    wt = MC_WriteToolDataFB()
    wt.ParCmd.ToolNo = TOOL
    wt.ParCmd.ToolData.Z = 150.0  # TCP 150 mm in front of the flange
    wt.ParCmd.ToolData.LoadNo = 1  # load of the tool
    client.execute(wt)
    rt = MC_ReadToolDataFB()
    rt.ParCmd.ToolNo = TOOL
    client.execute(rt)
    show(
        "Tool[1]",
        f"X={rt.OutCmd.ToolData.X} Y={rt.OutCmd.ToolData.Y} Z={rt.OutCmd.ToolData.Z} Load={rt.OutCmd.ToolData.LoadNo}",
    )

    section("WriteFrameData / ReadFrameData")
    wf = MC_WriteFrameDataFB()
    wf.ParCmd.FrameNo = 1
    wf.ParCmd.FrameData.X, wf.ParCmd.FrameData.Y = 500.0, -200.0  # work piece origin
    client.execute(wf)
    rf = MC_ReadFrameDataFB()
    rf.ParCmd.FrameNo = 1
    client.execute(rf)
    show("Frame[1]", f"X={rf.OutCmd.FrameData.X} Y={rf.OutCmd.FrameData.Y} Z={rf.OutCmd.FrameData.Z}")

    section("WriteLoadData / ReadLoadData")
    wl = MC_WriteLoadDataFB()
    wl.ParCmd.LoadNo = 1
    wl.ParCmd.LoadData.Mass = 2.5  # kg
    wl.ParCmd.LoadData.Z = 80.0  # center of mass 80 mm in front of the flange
    client.execute(wl)
    rl = MC_ReadLoadDataFB()
    rl.ParCmd.LoadNo = 1
    client.execute(rl)
    show("Load[1]", f"Mass={rl.OutCmd.LoadData.Mass} kg  center of mass Z={rl.OutCmd.LoadData.Z}")


def demo_limits_and_dynamics(client: SrciClient) -> None:
    section("ReadRobotSWLimits")
    sw = client.execute(MC_ReadRobotSWLimitsFB())
    lim = sw.OutCmd.LimitValues
    show("J1", f"{lim.J1LowerLimit} .. {lim.J1UpperLimit}")
    show("J2", f"{lim.J2LowerLimit} .. {lim.J2UpperLimit}")

    section("Read/WriteRobotDefaultDynamics")
    rd = client.execute(MC_ReadRobotDefaultDynamicsFB())
    show("VelocityRate [%] (read)", rd.OutCmd.DynamicValues.VelocityRate)
    wd = MC_WriteRobotDefaultDynamicsFB()
    copy_into(wd.ParCmd.DynamicValues, rd.OutCmd.DynamicValues)  # change one value, keep the others
    wd.ParCmd.DynamicValues.VelocityRate = 50.0
    client.execute(wd)
    client.execute(rd)
    show("VelocityRate [%] (new)", rd.OutCmd.DynamicValues.VelocityRate)

    section("Read/WriteRobotReferenceDynamics")
    rr = client.execute(MC_ReadRobotReferenceDynamicsFB())
    ref = rr.OutCmd.DynamicValues
    show("VelocityReference", ref.VelocityReference)
    show("AccelerationReference", ref.AccelerationReference)
    wr = MC_WriteRobotReferenceDynamicsFB()
    copy_into(wr.ParCmd.DynamicValues, ref)  # write back unchanged
    client.execute(wr)
    show("WriteRobotReferenceDynamics", "done")


# ---------------------------------------------------------------------------- 5. motion


def move_axes(j1: float, j2: float = 0.0, j3: float = 0.0, j5: float = 0.0) -> MC_MoveAxesAbsoluteFB:
    mv = MC_MoveAxesAbsoluteFB()
    pos = mv.ParCmd.JointPosition
    pos.J1, pos.J2, pos.J3, pos.J5 = j1, j2, j3, j5
    mv.ParCmd.ToolNo = TOOL  # tool written in demo_tool_frame_load
    # VelocityRate, AccelerationRate, DecelerationRate, JerkRate: default -1.0 = default dynamics
    return mv


def demo_moves(
    client: SrciClient, home: tuple[float, float, float, float], cyclic: MC_ReadActualPositionCyclicFB
) -> None:
    section("MoveAxesAbsolute")
    client.execute(move_axes(*home))
    show("at home", home)

    section("MoveDirectAbsolute (PTP to a cartesian position)")
    md = MC_MoveDirectAbsoluteFB()
    md.ParCmd.Position.X, md.ParCmd.Position.Y, md.ParCmd.Position.Z = 30.0, 10.0, 20.0
    md.ParCmd.ToolNo = TOOL
    client.execute(md)
    show("reached", cartesian(md.ParCmd.Position))

    section("MoveLinearAbsolute, buffered behind a second MoveLinearAbsolute")
    first = MC_MoveLinearAbsoluteFB()
    first.ParCmd.Position.X, first.ParCmd.Position.Y, first.ParCmd.Position.Z = 40.0, 10.0, 20.0
    first.ParCmd.ToolNo = TOOL
    first.ParCmd.VelocityRate = 50.0  # 50 % of the reference velocity
    second = MC_MoveLinearAbsoluteFB()
    second.AbortingMode = AbortingMode.BUFFER  # default: wait for the previous motion (ABORT: replace it)
    second.ParCmd.Position.X, second.ParCmd.Position.Y, second.ParCmd.Position.Z = 40.0, 30.0, 20.0
    second.ParCmd.ToolNo = TOOL
    client.start(first)
    client.start(second)  # sent in the same cycle, executed after the first one
    client.run(3)
    show("second.CommandBuffered", second.CommandBuffered)
    client.wait_done(first)
    show("first done, second active", second.Active or second.Busy)
    client.wait_done(second)
    show("second done", "yes")
    # the enabled MC_ReadActualPositionCyclicFB follows the robot in every cycle:
    show("cyclic position", cartesian(cyclic.OutCmd.CartesianPosition))


def demo_interrupt_jog_return_continue(client: SrciClient) -> None:
    section("GroupInterrupt, GroupJog, ReturnToPrimary, GroupContinue")
    mv = client.start(move_axes(60.0))
    client.idle(0.3)  # the motion is running
    client.execute(MC_GroupInterruptFB())
    show("interrupted", "primary sequence paused")

    # jogging runs in the secondary sequence while the primary sequence is interrupted
    jog = MC_GroupJogFB()
    jog.ParCmd.Mode = JogMode.JOG_AXES
    jog.ParCmd.Override = 50
    jog.ParCmd.ToolNo = TOOL
    client.enable(jog)
    jog.ParCmd.Control.Y_J2_Pos = True  # J2 + (hold-to-run like a jog key)
    client.idle(0.3)
    show("MotionActive while jogging", jog.OutCmd.MotionActive)
    jog.ParCmd.Control.Y_J2_Pos = False
    client.idle(0.1)
    client.disable(jog)

    # back to the position where the primary sequence was interrupted
    rtp = MC_ReturnToPrimaryFB()
    rtp.ParCmd.ToolNo = TOOL  # tool of the interrupted motion, else the RC refuses (16#8C26)
    client.add(rtp, Enable=True)  # Enable-type: moves while Enable = TRUE, Done at the position
    client.run_until(lambda: rtp.Done or rtp.Error, 30.0, "ReturnToPrimary")
    show("ReturnToPrimary.Progress [%]", rtp.OutCmd.Progress)
    client.disable(rtp)

    client.execute(MC_GroupContinueFB())
    client.wait_done(mv)
    show("interrupted move", "finished after GroupContinue")


def demo_group_stop(client: SrciClient) -> None:
    section("GroupStop")
    mv = client.start(move_axes(-60.0))
    client.idle(0.3)
    client.execute(MC_GroupStopFB())
    client.run_until(lambda: mv.CommandAborted or mv.Done or mv.Error, 10.0, "abort")
    show("move CommandAborted", mv.CommandAborted)
    mv.Execute = False
    client.run()


def demo_set_sequence(client: SrciClient) -> None:
    section("SetSequence")
    seq = MC_SetSequenceFB()
    seq.ParCmd.TargetSequence = SequenceFlag.SECONDARY_SEQUENCE
    client.execute(seq)
    show("active sequence", "SECONDARY")
    seq.ParCmd.TargetSequence = SequenceFlag.PRIMARY_SEQUENCE
    client.execute(seq)
    show("active sequence", "PRIMARY")


# ---------------------------------------------------------------------------- 6. logs


def demo_logs(client: SrciClient, messages: MC_ReadMessagesFB) -> None:
    section("Client log / server log / messages")
    # Client log (CreateClientLog / ReadClientLog): every block writes into the system log of
    # the axes group - the RobotTask output SystemLog (ring buffer) and the ExternalLogger.
    entries = [e for e in client.program.system_log if e]
    show("system log entries", len(entries))
    for line in entries[:3]:  # newest first
        print("   ", line.rstrip())
    # Server log (CreateServerLog / ReadServerLog): not implemented in the PLC library yet
    # (MC_CreateServerLog_ToDo, MC_ReadServerLog are empty); the RC reports the number of
    # its log entries in ExchangeConfiguration.OutCmd.NumberOfServerLogs.
    show(
        "messages of the RC",
        f"{messages.OutCmd.NumberOfActiveErrors} errors, {messages.OutCmd.NumberOfActiveWarnings} warnings",
    )


# ---------------------------------------------------------------------------- main


@contextlib.contextmanager
def open_transport(args: argparse.Namespace) -> Iterator[tuple[Transport, Any]]:
    """Transport to the robot; the second value is the SDK simulator (or None)."""
    if args.gateway:
        from srci.transport import TcpTransport

        host, _, port = args.gateway.partition(":")
        with TcpTransport(
            host, int(port or 5000), TELEGRAM_LENGTH, TELEGRAM_LENGTH, response_timeout=0.5
        ) as t:
            yield t, None
        return
    from srci.sim.sdk import SdkNotAvailableError, SdkSimulator, sdk_transport

    try:
        sim = SdkSimulator()
    except SdkNotAvailableError as exc:
        sys.exit(f"SDK simulator not available: {exc}")
    sim.set_move_cycles(80)  # simulated motions take 0.8 s
    with sim:
        if args.sdk_tcp:
            from srci.sim.gateway import PlcGatewaySimulator
            from srci.transport import TcpTransport

            def handler(telegram: bytes) -> bytes:
                return sim.exchange(telegram, TELEGRAM_LENGTH)

            with (
                PlcGatewaySimulator(handler, TELEGRAM_LENGTH, TELEGRAM_LENGTH) as gw,
                TcpTransport(
                    "127.0.0.1", gw.port, TELEGRAM_LENGTH, TELEGRAM_LENGTH, response_timeout=0.5
                ) as t,
            ):
                yield t, sim
        else:
            yield sdk_transport(sim, TELEGRAM_LENGTH, TELEGRAM_LENGTH), sim


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    target = ap.add_mutually_exclusive_group(required=True)
    target.add_argument("--gateway", metavar="HOST:PORT", help="PLC gateway of a real robot")
    target.add_argument("--sdk", action="store_true", help="SRCI SDK simulator in-process")
    target.add_argument(
        "--sdk-tcp", action="store_true", help="SRCI SDK simulator behind a local TCP gateway"
    )
    ap.add_argument("--fast", action="store_true", help="do not wait for the cycle time (simulator only)")
    ap.add_argument(
        "--debug", action="store_true", help="log every telegram of the library (logger srci.plc)"
    )
    args = ap.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING, format="%(name)s %(message)s")
    srci.configure(TOOL_MAX=16, FRAME_MAX=16, LOAD_MAX=16)  # like the library parameters in Codesys

    with open_transport(args) as (transport, sim):
        client = create_client(transport, realtime=not (args.fast and sim is not None))
        if args.debug:
            client.program.external_logger = PythonLogger()
            client.program.log_level = Severity.DEBUG
        try:
            demo_robot_task(client)
            demo_read_robot_data(client)
            demo_exchange_configuration(client)
            messages = demo_read_messages(client)
            enable = demo_group_reset_and_enable(client)
            demo_change_speed_override(client, 100.0)
            demo_read_actual_position(client)
            cyclic = demo_read_actual_position_cyclic(client)
            demo_tool_frame_load(client)
            demo_limits_and_dynamics(client)
            demo_moves(client, (0.0, 0.0, 0.0, 0.0), cyclic)
            demo_interrupt_jog_return_continue(client)
            demo_group_stop(client)
            demo_set_sequence(client)
            demo_logs(client, messages)
            section("EnableRobot - disable")
            client.disable(enable)
            show("Enabled", enable.Enabled)
        except CommandError as exc:
            print(f"\nERROR: {exc}")
            return 1
    print("\nall Core functions executed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

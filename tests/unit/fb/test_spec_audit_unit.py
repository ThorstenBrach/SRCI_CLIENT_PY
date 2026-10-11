# -------------------------------------------------------------------------
#  SRCI Robot Library - Python client
# -------------------------------------------------------------------------
#
#  Object:      tests.unit.fb.test_spec_audit_unit
#  Author:      Thorsten Brach
#  Date:        2026-09-26
#
#  Description:
#    Findings of the specification audit (docs/ST_FINDINGS.md F61 ...) without the SDK.
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

"""Findings of the specification audit (docs/ST_FINDINGS.md F61 ...) without the SDK."""

from __future__ import annotations

from srci.fb import MC_MoveAxesAbsoluteFB
from srci.types import (
    AxesGroupAcyclicAcrEntryRspBuffer,
    CmdMessageState,
    ComDirection,
    RobotLibraryErrorIdEnum,
    SequenceFlag,
    Severity,
    SystemTime,
)
from tests.helpers import Host, new_axes_group


def response(state: CmdMessageState, severity: int = 0, code: int = 0) -> AxesGroupAcyclicAcrEntryRspBuffer:
    rsp = AxesGroupAcyclicAcrEntryRspBuffer()
    rsp.Payload[0] = 0x10 | int(state)  # ParSeq 1, State (table 5-120)
    rsp.Payload[1] = severity & 0xFF
    rsp.Payload[2], rsp.Payload[3] = code >> 8, code & 0xFF
    rsp.PayloadLen = 4
    return rsp


def test_f61_state_error_without_code_is_8613() -> None:
    """F61 (B-05): response state ERROR without error code -> 16#8613, Error TRUE."""
    fb = MC_MoveAxesAbsoluteFB()
    fb.CallBack(RspData=response(CmdMessageState.ERROR), Timestamp=SystemTime())
    assert fb.ErrorID == RobotLibraryErrorIdEnum.ERR_ROBOT_ERROR_NO_ID
    assert fb.Error and not fb.Busy


def test_f61_state_error_with_warning_only_is_8613() -> None:
    """F61 (B-05): state ERROR with severity WARNING -> warning kept and 16#8613."""
    fb = MC_MoveAxesAbsoluteFB()
    fb.CallBack(RspData=response(CmdMessageState.ERROR, Severity.WARNING, 0x7001), Timestamp=SystemTime())
    assert fb.WarningID == 0x7001
    assert fb.ErrorID == RobotLibraryErrorIdEnum.ERR_ROBOT_ERROR_NO_ID and fb.Error


def test_f61_error_of_the_rc_sets_error_at_once() -> None:
    """F61 (B-01): the response with an error sets Error together with ErrorID (not one cycle
    later) and resets Busy."""
    fb = MC_MoveAxesAbsoluteFB()
    fb.Busy = True
    fb.CallBack(RspData=response(CmdMessageState.ERROR, Severity.ERROR, 0x8E03), Timestamp=SystemTime())
    assert fb.ErrorID == 0x8E03 and fb.Error and not fb.Busy


def test_f62_warning_and_info_are_held_until_reset() -> None:
    """F62 (B-06): a later response without message does not clear WarningID/InfoID."""
    fb = MC_MoveAxesAbsoluteFB()
    fb.CallBack(RspData=response(CmdMessageState.ACTIVE, Severity.WARNING, 0x7001), Timestamp=SystemTime())
    assert fb.WarningID == 0x7001
    fb.CallBack(RspData=response(CmdMessageState.ACTIVE, Severity.INFO, 0x6001), Timestamp=SystemTime())
    fb.CallBack(RspData=response(CmdMessageState.DONE), Timestamp=SystemTime())
    assert (fb.WarningID, fb.InfoID, fb.ErrorID) == (0x7001, 0x6001, 0)
    fb.Reset()
    assert (fb.WarningID, fb.InfoID) == (0, 0)


# ------------------------------------------------------------------ F63 telegram sequence areas


def areas(host: Host, direction: ComDirection) -> list[tuple[int, int]]:
    ag, _ = new_axes_group()
    return [
        (
            host.CalculateSequencePayloadStartAdr(AxesGroup=ag, Direction=direction, Sequence=s),
            host.CalculateSequencePayloadMax(AxesGroup=ag, Direction=direction, Sequence=s),
        )
        for s in (SequenceFlag.PRIMARY_SEQUENCE, SequenceFlag.SECONDARY_SEQUENCE)
    ]


def test_f63_one_sequence_area_is_the_acyclic_area() -> None:
    """F63 (A-03): one sequence: area = telegram length - cyclic data - footer."""
    host = Host()
    (start, size), (_, size2) = areas(host, ComDirection.ROB_TO_PLC)
    assert (start, size, size2) == (10, 128 - 10 - 1, 0)


def test_f63_two_sequences_halve_the_acyclic_area() -> None:
    """F63 (A-02/A-03): two sequences: the acyclic area is halved like in spec Fig. 5-205 and in
    the SDK (1st = area / 2 behind the cyclic data, 2nd = rest behind the 1st); no overlap."""
    host = Host()
    host._parCfg.Com.TwoSequences = True
    for direction, length, cyclic in ((ComDirection.ROB_TO_PLC, 128, 10), (ComDirection.PLC_TO_ROB, 64, 18)):
        (s1, n1), (s2, n2) = areas(host, direction)
        area = length - cyclic - 1
        assert (s1, n1) == (cyclic, area // 2)
        assert (s2, n2) == (cyclic + area // 2, area - area // 2)
        assert s2 + n2 == length - 1  # the footer follows


def test_f63_second_sequence_is_sent_at_its_address() -> None:
    """F63 (A-04): both sequence headers are written, the 2nd one at its own address, and both
    NewSEQ flags are reset after sending."""
    host, (ag, _) = Host(), new_axes_group()
    host._parCfg.Com.TwoSequences = True
    ag.State.SequenceCountSend = 1
    ag.State.NewSEQ[0] = ag.State.NewSEQ[1] = True
    host.Telegram.PlcToRob.Header.TelegramLengthPlcToRob = 64
    host.Telegram.PlcToRob.Sequence[0].Header.SEQ_ACK = 5
    host.Telegram.PlcToRob.Sequence[1].Header.SEQ_ACK = 6
    out = bytearray(64)
    host.CreateSendPayload(ag, out)
    (s1, _), (s2, _) = areas(host, ComDirection.PLC_TO_ROB)
    assert out[s1 : s1 + 4] == bytes.fromhex("0005 0000")
    assert out[s2 : s2 + 4] == bytes.fromhex("0006 0000")
    assert ag.State.NewSEQ == [False, False]


def recv_telegram(host: Host, acks: tuple[int, int], cmd_ids: tuple[int, int]) -> bytearray:
    data = bytearray(128)
    for idx, (ack, cmd) in enumerate(zip(acks, cmd_ids, strict=True)):
        start = areas(host, ComDirection.ROB_TO_PLC)[idx][0]
        frag = cmd.to_bytes(2, "big") + bytes([0, 1]) + (0).to_bytes(2, "big") + (4).to_bytes(2, "big")
        payload = frag + bytes([0x1A, 0, 0, 0])  # State DONE
        data[start : start + 4] = ack.to_bytes(2, "big") + len(payload).to_bytes(2, "big")
        data[start + 4 : start + 4 + len(payload)] = payload
    return data


def test_f63_responses_are_processed_in_the_order_of_the_ack() -> None:
    """F63 (A-06): both sequences acknowledged in one telegram -> the one with the lower Ack
    first (spec Fig. 5-207/5-208), independent of its position in the telegram."""
    host, (ag, acr) = Host(), new_axes_group()
    host._parCfg.Com.TwoSequences = True
    ag.State.CurrentSEQ[0], ag.State.CurrentSEQ[1] = 8, 7
    host.ParseRecvPayload(ag, recv_telegram(host, (8, 7), (0x0101, 0x0202)))
    assert [cmd for cmd, _ in acr.responses] == [0x0202, 0x0101]


def test_f63_ack_of_an_other_seq_is_ignored() -> None:
    """F63: a sequence whose Ack is not the Seq that was sent (the SDK sends Ack 0 in the
    sequence it does not process) carries no response."""
    host, (ag, acr) = Host(), new_axes_group()
    host._parCfg.Com.TwoSequences = True
    ag.State.CurrentSEQ[0], ag.State.CurrentSEQ[1] = 8, 9
    host.ParseRecvPayload(ag, recv_telegram(host, (8, 0), (0x0101, 0x0202)))
    assert [cmd for cmd, _ in acr.responses] == [0x0101]


# ------------------------------------------------------------------ F80 enum defaults like TwinCAT


def test_f80_enum_without_initial_value_starts_with_member_0() -> None:
    """F80: an enum without initial value starts with the member 0 if there is one (TwinCAT,
    checked online), otherwise with the first member: TriggerCondition -> UNDEFINED (first
    member -5), MessageLevel (no member 0) -> DEBUG."""
    from srci.types import MessageLevel, ReadMessagesParCmd, SetTriggerMotionParCmd, TriggerCondition

    par = SetTriggerMotionParCmd()
    assert par.TriggerMode_1 == par.TriggerMode_2 == TriggerCondition.UNDEFINED
    assert ReadMessagesParCmd().MessageLevel == MessageLevel.DEBUG


def test_f80_set_trigger_motion_trigger_mode_2_undefined_is_allowed() -> None:
    """F80 (spec table 6-692): TriggerMode_1 has no valid default (0 = undefined -> 16#0008);
    TriggerMode_2 = 0 (undefined) is allowed: only TriggerMode_1 is used."""
    from srci.fb import MC_SetTriggerMotionFB
    from srci.types import TriggerCondition

    ag, _ = new_axes_group()
    fb = MC_SetTriggerMotionFB()
    assert not fb.CheckParameterValid(AxesGroup=ag)
    assert fb.ErrorID == RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD
    fb = MC_SetTriggerMotionFB()
    fb.ParCmd.TriggerMode_1 = TriggerCondition.START_POSITION_TIME_MS
    fb.ParCmd.TriggerParameter_1 = 100.0
    fb.ParCmd.TriggerMode_2 = TriggerCondition.UNDEFINED
    assert fb.CheckParameterValid(AxesGroup=ag), fb.ErrorID


# ------------------------------------------------------------------ F81 / F82 (found while writing the wiki)


def test_f81_update_tool_data_stores_the_tool_in_the_plc_array() -> None:
    """F81: AxesGroupSystemDataFB.UpdateToolData (called by Write/ReadToolData) did not copy the
    tool into the ToolData array of the RobotTask (code commented out) - frames and loads were
    stored."""
    from srci.iec.rt import ADR, array_type
    from srci.types import Frame, FrameData, Tool, ToolData
    from srci.types import iec as _iec

    ag, _ = new_axes_group()
    sd = ag.SystemData
    tools = [Tool() for _ in range(4)]
    frames = [Frame() for _ in range(4)]
    sd.ToolDataPtr = ADR(tools, None, array_type(tools, _iec.StructType(Tool)))
    sd.ToolDataMin, sd.ToolDataMax = 0, 3
    sd.FrameDataPtr = ADR(frames, None, array_type(frames, _iec.StructType(Frame)))
    sd.FrameDataMin, sd.FrameDataMax = 0, 3

    sd.UpdateFrameData(FrameNo=2, FrameData=FrameData(X=12.5))
    assert frames[2].Available and frames[2].Data.X == 12.5
    sd.UpdateToolData(ToolNo=2, ToolData=ToolData(Z=150.0, LoadNo=1))
    assert tools[2].Available
    assert tools[2].Data.Z == 150.0 and tools[2].Data.LoadNo == 1
    assert not tools[1].Available and not tools[3].Available


def test_f82_read_actual_position_cyclic_joint_ext_sets_its_own_reading_flag() -> None:
    """F82: MC_ReadActualPositionCyclicFB set OutCmd.ReadingCartesianPositionExt instead of
    ReadingJointPositionExt when the extended joint position was read (copy & paste)."""
    from srci.fb import MC_ReadActualPositionCyclicFB

    ag, _ = new_axes_group()
    ag.State.CMDsEnabled = ag.State.Initialized = True
    ag.State.RobotData.RCSupportedFunctions.ReadActualPositionCyclic = True
    ag.CyclicOptional.RobToPlc.JointPositionExt.Active = True
    ag.CyclicOptional.RobToPlc.JointPositionExt.E2 = 12.5
    fb = MC_ReadActualPositionCyclicFB()
    fb.ParCmd.ReadJointPositionExt = True
    for _ in range(3):
        fb(Enable=True, AxesGroup=ag)
    assert fb.Enabled and not fb.Error, hex(fb.ErrorID)
    assert fb.OutCmd.JointPosition.E2 == 12.5
    assert fb.OutCmd.ReadingJointPositionExt
    assert not fb.OutCmd.ReadingCartesianPositionExt


# ------------------------------------------------------------------ F83 / F84 (found while writing the wiki)


def test_f83_deactivate_is_allowed_with_the_sequence_of_the_command() -> None:
    """F83: the SequenceFlag check of F69 also applied to ProcessingMode DEACTIVATE: an action
    started in a sequence (e.g. TRIGGER_BUFFERED) could not be deactivated with the same
    SequenceFlag (16#8625), WaitForTrigger (only primary / secondary allowed) not at all."""
    from srci.fb import MC_WaitForTriggerFB, MC_WriteDigitalOutputsFB
    from srci.types import ProcessingMode, SequenceFlag

    ag, _ = new_axes_group()
    wait = MC_WaitForTriggerFB()
    wait.ParCmd.ListenerID = 7
    wait.ProcessingMode = ProcessingMode.DEACTIVATE
    wait.SequenceFlag = SequenceFlag.PRIMARY_SEQUENCE
    assert wait.CheckParameterValid(AxesGroup=ag), hex(wait.ErrorID)
    out = MC_WriteDigitalOutputsFB()
    out.ParCmd.ListenerID = 7
    out.ProcessingMode = ProcessingMode.DEACTIVATE
    out.SequenceFlag = SequenceFlag.SECONDARY_SEQUENCE
    assert out.CheckParameterValid(AxesGroup=ag), hex(out.ErrorID)
    # the check itself stays: a sequence mode without sequence is still rejected
    out = MC_WriteDigitalOutputsFB()
    out.ProcessingMode = ProcessingMode.BUFFERED
    out.SequenceFlag = SequenceFlag.NO_SEQUENCE
    assert not out.CheckParameterValid(AxesGroup=ag)


def test_f84_move_linear_cam_accepts_trigger_delay_above_255_ms() -> None:
    """F84: MC_MoveLinearCamFB rejected TriggerDelay > 255 ms (16#0008), although it is a UINT
    [ms] (spec) and MC_MoveCircularCamFB accepts up to 65535."""
    from srci.fb import MC_MoveLinearCamFB

    ag, _ = new_axes_group()
    fb = MC_MoveLinearCamFB()
    fb.ParCmd.TriggerDelay = 1000
    assert fb.CheckParameterValid(AxesGroup=ag), hex(fb.ErrorID)
    fb = MC_MoveLinearCamFB()
    fb.ParCmd.TriggerDelay = 65535
    assert fb.CheckParameterValid(AxesGroup=ag), hex(fb.ErrorID)


# ------------------------------------------------------------------ F85 ... F92 (Optional blocks, wiki)


def _valid(fb: object, ag: object) -> tuple[bool, int]:
    ok = fb.CheckParameterValid(AxesGroup=ag)  # type: ignore[attr-defined]
    return ok, int(fb.ErrorID)  # type: ignore[attr-defined]


def test_f85_configure_conveyor_accepts_circular_conveyors() -> None:
    """F85: MC_ConfigureConveyorFB rejected ConveyorType CIRCULAR_CONVEYOR_TRACKING (the check compared
    LINEAR_CONVEYOR_TRACKING twice)."""
    from srci.fb import MC_ConfigureConveyorFB
    from srci.types import ConveyorType

    ag, _ = new_axes_group()
    fb = MC_ConfigureConveyorFB()
    fb.ParCmd.ConveyorType = ConveyorType.CIRCULAR_CONVEYOR_TRACKING
    fb.ParCmd.Radius = 500.0
    ok, err = _valid(fb, ag)
    assert ok, hex(err)


def test_f86_force_control_accepts_plc_sensor_algorithm() -> None:
    """F86: MC_ForceControlFB rejected ConnectionMode PLC_SENSOR_ALGORITHM (the check tested
    PLC_SENSOR_RC_ALGORITHM twice)."""
    from srci.fb import MC_ForceControlFB
    from srci.types import SensorConnectionMode

    ag, _ = new_axes_group()
    fb = MC_ForceControlFB()
    fb.ParCmd.ConnectionMode = SensorConnectionMode.PLC_SENSOR_ALGORITHM
    ok, err = _valid(fb, ag)
    assert ok, hex(err)


def test_f87_user_login_needs_a_user_name_only_with_user_name_mode() -> None:
    """F87: MC_UserLoginFB demanded a Username also in Mode PASSWORD_ONLY; with
    USERNAME_AND_PASSWORD an empty Username is still rejected."""
    from srci.fb import MC_UserLoginFB
    from srci.types import LogonMode

    ag, _ = new_axes_group()
    fb = MC_UserLoginFB()
    fb.ParCmd.Mode = LogonMode.PASSWORD_ONLY
    fb.ParCmd.Password = "secret"
    ok, err = _valid(fb, ag)
    assert ok, hex(err)
    fb = MC_UserLoginFB()
    fb.ParCmd.Mode = LogonMode.USERNAME_AND_PASSWORD
    fb.ParCmd.Password = "secret"
    assert not _valid(fb, ag)[0]


def test_f88_stop_subprogram_target_id_is_a_job_or_instance_id() -> None:
    """F88: MC_StopSubprogramFB limited TargetID to 255 although JobID / InstanceID are UINT
    (65535 = -1 in the telegram) and reported ERR_LISTENERID_MUST_BE_POSITIVE."""
    from srci.fb import MC_StopSubprogramFB

    ag, _ = new_axes_group()
    fb = MC_StopSubprogramFB()
    fb.ParCmd.TargetID = 1000
    ok, err = _valid(fb, ag)
    assert ok, hex(err)
    fb = MC_StopSubprogramFB()
    fb.ParCmd.TargetID = -2
    ok, err = _valid(fb, ag)
    assert not ok and err == RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD


def test_f89_move_superimposed_accepts_trigger_continuous() -> None:
    """F89: MC_MoveSuperImposedFB rejected ProcessingMode TRIGGER_CONTINUOUS (allowed by the spec)."""
    from srci.fb import MC_MoveSuperImposedFB
    from srci.types import ProcessingMode

    ag, _ = new_axes_group()
    fb = MC_MoveSuperImposedFB()
    fb.ProcessingMode = ProcessingMode.TRIGGER_CONTINUOUS
    fb.ParCmd.ListenerID = 5
    for name in ("VelocityDiffRate", "AccelerationDiffRate", "DecelerationDiffRate", "JerkDiffRate"):
        setattr(fb.ParCmd, name, -1.0)
    ok, err = _valid(fb, ag)
    assert ok, hex(err)


def test_f90_measuring_input_shows_the_measuring_id_while_active() -> None:
    """F90: MC_MeasuringInputFB showed the MeasuringID only at DONE, so a running measurement could
    not be aborted by its ID (MC_AbortMeasuringInputFB)."""
    from srci.fb import MC_MeasuringInputFB

    fb = MC_MeasuringInputFB()
    rsp = response(CmdMessageState.ACTIVE)
    rsp.Payload[4], rsp.Payload[5] = 0x01, 0x02  # MeasuringID (UINT)
    rsp.PayloadLen = 6
    fb.CallBack(RspData=rsp, Timestamp=SystemTime())
    assert fb._response.MeasuringID == 0x0102  # parsed by CallBack
    fb.OnApplyOutCmd(State=CmdMessageState.ACTIVE)  # step 1 of the cyclic call
    assert fb.OutCmd.MeasuringID == 0x0102


def test_f91_write_analog_output_rejects_index_0() -> None:
    """F91: MC_WriteAnalogOutputFB accepted Index 0 (spec 1..32, like MC_ReadAnalogInputFB)."""
    from srci.fb import MC_WriteAnalogOutputFB

    ag, _ = new_axes_group()
    fb = MC_WriteAnalogOutputFB()
    ok, err = _valid(fb, ag)
    assert not ok and err == RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD
    fb = MC_WriteAnalogOutputFB()
    fb.ParCmd.Index = 1
    ok, err = _valid(fb, ag)
    assert ok, hex(err)


def test_f92_unit_measurement_invalid_measuring_mode_is_a_parameter_error() -> None:
    """F92: MC_UnitMeasurementFB reported an invalid MeasuringMode as ERR_PROCESSINGMODE_NOT_ALLOWED."""
    from srci.fb import MC_UnitMeasurementFB

    ag, _ = new_axes_group()
    fb = MC_UnitMeasurementFB()
    fb.ParCmd.MeasuringMode = 7  # type: ignore[assignment]
    ok, err = _valid(fb, ag)
    assert not ok and err == RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD

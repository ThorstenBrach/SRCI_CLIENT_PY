"""Telegram coding of MC_RobotTaskFB: ``CreateSendPayload*``, ``ParseRecvPayload*``, ``Calculate*``.

``MC_RobotTaskFB`` of the PLC library has ~9000 lines. The Python port splits it by
concern into mixins; this one holds the methods that convert between the byte arrays
(``RobotOutData``/``RobotInData``) and the ``Telegram`` structure. Method names,
arguments and order of the fields are the ones of the ST code.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.fb._internal.Recv.RobotLibraryRecvDataFB import RobotLibraryRecvDataFB
from srci.fb._internal.Send.RobotLibrarySendDataFB import RobotLibrarySendDataFB
from srci.functions.Convert.Misc import ByteToVersion, CombineBytesToUint, GetHalfeByteHi, GetHalfeByteLo
from srci.iec.sizeof import SIZEOF
from srci.types import (
    AxesGroup,
    CmdMessageState,
    ComDirection,
    MessageType,
    RobotLibraryParameter,
    RobotTaskParCfg,
    SequenceFlag,
    Severity,
    SystemTime,
    Telegram,
)

__all__ = ["MC_RobotTaskFB_Telegram"]


class MC_RobotTaskFB_Telegram:
    """Telegram part of MC_RobotTaskFB (mixin)."""

    # VAR CONSTANT of MC_RobotTaskFB
    FOOTER_SIZE = 1
    PRIMARY_SEQUENCE = 0
    SECONDARY_SEQUENCE = 1

    if TYPE_CHECKING:  # provided by RobotLibraryLogFB / MC_RobotTaskFB
        SystemTime: SystemTime

        def CreateLogMessagePara1(self, **kwargs: Any) -> None: ...
        def CreateLogMessagePara2(self, **kwargs: Any) -> None: ...
        def CreateLogMessagePara3(self, **kwargs: Any) -> None: ...
        def CreateLogMessagePara4(self, **kwargs: Any) -> None: ...
        def CreateLogMessagePara5(self, **kwargs: Any) -> None: ...

    def __init__(self) -> None:
        self.Telegram = Telegram()
        self.SendData = RobotLibrarySendDataFB()
        self.RecvData = RobotLibraryRecvDataFB()
        self._parCfg = RobotTaskParCfg()
        self.ROBOT_IN_DATA_SIZE = 0
        self.ROBOT_OUT_DATA_SIZE = 0

    # ================================================================== send

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CreateSendPayload  sha256: bbc3f675b567d808
    def CreateSendPayload(self, AxesGroup: AxesGroup, RobotOutData: bytearray) -> int:
        self.ROBOT_OUT_DATA_SIZE = len(RobotOutData)
        # Call SendData FB, update payload and size
        self.SendData(Payload=RobotOutData, PayLoadSize=self.ROBOT_OUT_DATA_SIZE)
        # reset all variables and payload
        self.SendData.Reset()

        self.CreateSendPayloadHeader(AxesGroup=AxesGroup)
        self.CreateSendPayloadCyclic(AxesGroup=AxesGroup)
        self.CreateSendPayloadCyclicOptional(AxesGroup=AxesGroup)
        self.CreateSendPayloadSequence(AxesGroup=AxesGroup)
        self.CreateSendPayloadFooter(AxesGroup=AxesGroup)
        self.CreateSendPayloadLogging(AxesGroup=AxesGroup)

        # reset NewSEQ flag
        AxesGroup.State.NewSEQ[0] = False
        return 0

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CreateSendPayloadCyclic  sha256: 538f589a3a4be0dc
    def CreateSendPayloadCyclic(self, AxesGroup: AxesGroup) -> int:
        """ToolNo/FrameNo (spec table 5-90).

        ST-FIX F2: the ST code always sends these two bytes. Spec (table 5-88 bit 1) and
        SDK only expect them when "Cartesian Position" is configured in the direction
        RC -> PLC; otherwise the sequence would start two bytes too late for the RC.
        """
        if AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active:
            self.SendData.AddByte(self.Telegram.PlcToRob.Cyclic.ToolNo)
            self.SendData.AddByte(self.Telegram.PlcToRob.Cyclic.FrameNo)
        return 0

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CreateSendPayloadCyclicOptional  sha256: 25c341cc77f7fdae
    def CreateSendPayloadCyclicOptional(self, AxesGroup: AxesGroup) -> int:
        opt = AxesGroup.CyclicOptional.PlcToRob
        tel = self.Telegram.PlcToRob.CyclicOptional
        send = self.SendData

        if opt.SubProgramData.Active:
            send.AddDataBlock(tel.SubProgramData.Data)

        if opt.CartesianPosition.Active:
            pos = tel.CartesianPosition
            for value in (pos.X, pos.Y, pos.Z, pos.Rx, pos.Ry, pos.Rz):
                send.AddReal(value)
            # ST-FIX F1: Config is 2 bytes (spec table 5-97, SIZEOF of the structure);
            # the ST code only sends the first byte.
            send.AddByte(pos.Config & 0x07)
            send.AddByte(0)
            send.AddByte(pos.Turns_J2_J1)
            send.AddByte(pos.Turns_J4_J3)
            send.AddByte(pos.Turns_J6_J5)
            send.AddByte(pos.Turns_E1)
            send.AddReal(pos.E1)

        if opt.JointPosition.Active:
            j = tel.JointPosition
            for value in (j.J1, j.J2, j.J3, j.J4, j.J5, j.J6, j.E1):
                send.AddReal(value)

        if opt.Force.Active:
            f = tel.Force
            for value in (f.X, f.Y, f.Z, f.Rx, f.Ry, f.Rz):
                send.AddReal(value)

        # Telegram.PlcToRob.CyclicOptional.TwoSequences: nothing to send

        if opt.CartesianPositionExt.Active:
            c = tel.CartesianPositionExt
            for value in (c.E2, c.E3, c.E4, c.E5, c.E6):
                send.AddReal(value)

        if opt.JointPositionExt.Active:
            je = tel.JointPositionExt
            for value in (je.E2, je.E3, je.E4, je.E5, je.E6):
                send.AddReal(value)

        if opt.ForceExt.Active:
            fe = tel.ForceExt
            for value in (fe.E1, fe.E2, fe.E3, fe.E4, fe.E5, fe.E6):
                send.AddReal(value)
        return 0

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CreateSendPayloadFooter  sha256: a392248f4aa3d296
    def CreateSendPayloadFooter(self, AxesGroup: AxesGroup) -> int:
        self.SendData.SetLifeSignFooter(LifeSign=AxesGroup.Cyclic.PlcToRob.LifeSign)
        return 0

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CreateSendPayloadHeader  sha256: e998709e8b8221c1
    def CreateSendPayloadHeader(self, AxesGroup: AxesGroup) -> int:
        h = self.Telegram.PlcToRob.Header
        send = self.SendData
        send.AddByte(h.SRCIVersion)
        send.AddByte(h.FastStop_LifeSign)
        send.AddUint(h.TelegramLengthPlcToRob)
        send.AddUint(h.TelegramLengthRobToPlc)
        send.AddByte(h.AxesGroupID_Control)
        send.AddByte(h.Reserved)
        send.AddUint(h.TelegramNumberPlcToRob)
        send.AddUint(h.TelegramNumberRobToPlc)
        send.AddUint(h.ClientDate)
        send.AddTime(h.ClientTime)
        return 0

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CreateSendPayloadLogging  sha256: 17cc8c3288acceb2
    def CreateSendPayloadLogging(self, AxesGroup: AxesGroup) -> int:
        seq = self.Telegram.PlcToRob.Sequence
        if (seq[0].Header.PayloadLength > 0 and AxesGroup.State.NewSEQ[0]) or (
            seq[1].Header.PayloadLength > 0 and AxesGroup.State.NewSEQ[1]
        ):
            self.CreateLogMessagePara1(
                Timestamp=self.SystemTime,
                MessageType=MessageType.CMD,
                Severity=Severity.DEBUG,
                MessageCode=0,
                MessageText="SendData: Bytes send in total: {1}",
                Para1=str(self.SendData.PayloadLen),
            )
        return 0

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CreateSendPayloadSequence  sha256: a1b6024cc2caa8d5
    def CreateSendPayloadSequence(self, AxesGroup: AxesGroup) -> int:
        send = self.SendData
        for _seqIdx in range(AxesGroup.State.SequenceCountSend + 1):
            # Check 2nd sequence ? -> goto 2nd sequence payload address
            if _seqIdx == self.SECONDARY_SEQUENCE:
                send.PayloadPtr = self.CalculateSequencePayloadStartAdr(
                    AxesGroup=AxesGroup,
                    Direction=ComDirection.PLC_TO_ROB,
                    Sequence=SequenceFlag.SECONDARY_SEQUENCE,
                )
            seq = self.Telegram.PlcToRob.Sequence[_seqIdx]
            send.AddUint(seq.Header.SEQ_ACK)
            send.AddUint(seq.Header.PayloadLength)

            # check limit reached ?
            if send.PayloadPtr + self.FOOTER_SIZE >= self.Telegram.PlcToRob.Header.TelegramLengthPlcToRob:
                break

            for _fragIdx in range(AxesGroup.State.FragmentCountSend[_seqIdx] + 1):
                frag = seq.Fragment[_fragIdx]
                if frag.Header.PayloadLength > 0:
                    send.AddUint(frag.Header.CmdID)
                    send.AddByte(frag.Header.Reserve)
                    send.AddByte(frag.Header.FragmentAction)
                    send.AddUint(frag.Header.PayloadPointer)
                    send.AddUint(frag.Header.PayloadLength)
                    # the command header is part of the fragment payload
                    start = frag.Header.PayloadPointer
                    send.AddDataBlock(frag.Command.Payload[start : start + frag.Header.PayloadLength])
        return 0

    # ================================================================== receive

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#ParseRecvPayload  sha256: a81b149eb30d7f5e
    def ParseRecvPayload(self, AxesGroup: AxesGroup, RobotInData: bytes | bytearray) -> None:
        self.ROBOT_IN_DATA_SIZE = len(RobotInData)
        # reset all variables and payload
        self.RecvData.Reset()
        # Call RecvData FB, update payload and size
        self.RecvData(Payload=RobotInData, PayloadSize=self.ROBOT_IN_DATA_SIZE)

        # check new data to receive ?  (see docs/ST_FINDINGS.md F4: compares the ACK of the
        # previous telegram, which always equals LastACK[0] - kept as in ST)
        if self.Telegram.RobToPlc.Sequence[0].Header.SEQ_ACK != AxesGroup.State.LastACK[0]:
            # delete old telegram data
            self.Telegram.RobToPlc = type(self.Telegram.RobToPlc)()

        self.ParseRecvPayloadHeader(AxesGroup=AxesGroup)
        self.ParseRecvPayloadCyclic(AxesGroup=AxesGroup)
        self.ParseRecvPayloadCyclicOptional(AxesGroup=AxesGroup)
        self.ParseRecvPayloadSequence(AxesGroup=AxesGroup)
        self.ParseRecvPayloadFooter(AxesGroup=AxesGroup)
        self.ParseRecvPayloadLogging(AxesGroup=AxesGroup)

        AxesGroup.State.LastACK[0] = self.Telegram.RobToPlc.Sequence[0].Header.SEQ_ACK
        AxesGroup.State.LastACK[1] = self.Telegram.RobToPlc.Sequence[1].Header.SEQ_ACK

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#ParseRecvPayloadCyclic  sha256: 10e988648ea20985
    def ParseRecvPayloadCyclic(self, AxesGroup: AxesGroup) -> None:
        """Empty in ST (no fixed cyclic data from RC to PLC)."""

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#ParseRecvPayloadCyclicOptional  sha256: 335111c33908b33e
    def ParseRecvPayloadCyclicOptional(self, AxesGroup: AxesGroup) -> None:
        opt = AxesGroup.CyclicOptional.RobToPlc
        tel = self.Telegram.RobToPlc.CyclicOptional
        recv = self.RecvData

        if opt.SubProgramData.Active:
            for _idx in range(26):  # ST: FOR _idx := 0 TO 25
                tel.SubProgramData.Data[_idx] = recv.GetByte()

        if opt.CartesianPosition.Active:
            pos = tel.CartesianPosition
            pos.X = recv.GetReal()
            pos.Y = recv.GetReal()
            pos.Z = recv.GetReal()
            pos.Rx = recv.GetReal()
            pos.Ry = recv.GetReal()
            pos.Rz = recv.GetReal()
            pos.Config = recv.GetWord()
            pos.Turns_J2_J1 = recv.GetByte()
            pos.Turns_J4_J3 = recv.GetByte()
            pos.Turns_J6_J5 = recv.GetByte()
            pos.Turns_E1 = recv.GetByte()
            pos.E1 = recv.GetReal()
            pos.ToolNo = recv.GetUsint()
            pos.FrameNo = recv.GetUsint()
            pos.CurrentlyUsedToolNo = recv.GetUsint()
            pos.CurrentlyUsedFrameNo = recv.GetUsint()
            pos.Reserve_1 = recv.GetByte()
            pos.Reserve_2 = recv.GetByte()

        if opt.JointPosition.Active:
            j = tel.JointPosition
            j.J1 = recv.GetReal()
            j.J2 = recv.GetReal()
            j.J3 = recv.GetReal()
            j.J4 = recv.GetReal()
            j.J5 = recv.GetReal()
            j.J6 = recv.GetReal()
            j.E1 = recv.GetReal()
            j.E1_Reserve = recv.GetWord()

        if opt.Force.Active:
            f = tel.Force
            f.X, f.Y, f.Z = recv.GetReal(), recv.GetReal(), recv.GetReal()
            f.Rx, f.Ry, f.Rz = recv.GetReal(), recv.GetReal(), recv.GetReal()

        if opt.Current.Active:
            c = tel.Current
            c.J1, c.J2, c.J3 = recv.GetReal(), recv.GetReal(), recv.GetReal()
            c.J4, c.J5, c.J6 = recv.GetReal(), recv.GetReal(), recv.GetReal()

        if opt.CartesianPositionExt.Active:
            ce = tel.CartesianPositionExt
            ce.E2, ce.E3, ce.E4 = recv.GetReal(), recv.GetReal(), recv.GetReal()
            ce.E5, ce.E6 = recv.GetReal(), recv.GetReal()

        if opt.JointPositionExt.Active:
            je = tel.JointPositionExt
            je.E2, je.E3, je.E4 = recv.GetReal(), recv.GetReal(), recv.GetReal()
            je.E5, je.E6 = recv.GetReal(), recv.GetReal()

        if opt.ForceExt.Active:
            fe = tel.ForceExt
            fe.E1, fe.E2, fe.E3 = recv.GetReal(), recv.GetReal(), recv.GetReal()
            fe.E4, fe.E5, fe.E6 = recv.GetReal(), recv.GetReal(), recv.GetReal()

        if opt.CurrentExt.Active:
            cx = tel.CurrentExt
            cx.E1, cx.E2, cx.E3 = recv.GetReal(), recv.GetReal(), recv.GetReal()
            cx.E4, cx.E5, cx.E6 = recv.GetReal(), recv.GetReal(), recv.GetReal()

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#ParseRecvPayloadFooter  sha256: fead5ac00118c5dc
    def ParseRecvPayloadFooter(self, AxesGroup: AxesGroup) -> None:
        self.Telegram.RobToPlc.Footer.LifeSign = self.RecvData.GetLifeSignFooter()

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#ParseRecvPayloadHeader  sha256: e7eefb56da6258d6
    def ParseRecvPayloadHeader(self, AxesGroup: AxesGroup) -> None:
        h = self.Telegram.RobToPlc.Header
        recv = self.RecvData
        h.SRCIVersion = ByteToVersion(recv.GetByte())  # Version
        h.LifeSign = recv.GetHalfeByte2(IncPayloadPtr=True)  # Connection alive signal
        h.Reserved = recv.GetByte()  # Reserved byte
        h.TelegramState = type(h.TelegramState)(recv.GetUsint())  # Initialization / telegram control state
        h.StatusRobotArm = recv.GetDword()  # Combination of various RA related states
        h.Override = recv.GetUint()  # Actual override in percentage encoding

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#ParseRecvPayloadLogging  sha256: 59a2d4c272755ee5
    def ParseRecvPayloadLogging(self, AxesGroup: AxesGroup) -> None:
        """Returns immediately in ST (logging moved to ParseRecvPayloadSequence)."""
        return

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#ParseRecvPayloadSequence  sha256: d880d1a33819c63e
    def ParseRecvPayloadSequence(self, AxesGroup: AxesGroup) -> None:
        recv = self.RecvData
        _seqCount = 0
        if self._parCfg.Com.TwoSequences:
            _seqCount += 1

        for _seqIdx in range(_seqCount + 1):
            # ST-FIX F5: ST keeps _fragIdx / _seqPayloadPtr of the first sequence for the second one
            _fragIdx = 0
            _seqPayloadPtr = 0
            # Check 2nd sequence ? -> goto 2nd sequence payload address
            if _seqIdx == self.SECONDARY_SEQUENCE:
                recv.PayloadPtr = self.CalculateSequencePayloadStartAdr(
                    AxesGroup=AxesGroup,
                    Direction=ComDirection.ROB_TO_PLC,
                    Sequence=SequenceFlag.SECONDARY_SEQUENCE,
                )
            seq = self.Telegram.RobToPlc.Sequence[_seqIdx]
            seq.Header.SEQ_ACK = recv.GetUint()
            seq.Header.PayloadLength = recv.GetUint()

            # check new data available ?
            if seq.Header.SEQ_ACK == AxesGroup.State.LastACK[_seqIdx] or seq.Header.PayloadLength == 0:
                continue

            if seq.Header.PayloadLength > self._parCfg.Com.TelegramLengthRobToPlc:
                self.CreateLogMessagePara2(
                    Timestamp=self.SystemTime,
                    MessageType=MessageType.CMD,
                    Severity=Severity.DEBUG,
                    MessageCode=0,
                    MessageText="Invalid sequence payload length, Sequence = {1}, PayloadLength = {2} ",
                    Para1=str(_seqIdx),
                    Para2=str(seq.Header.PayloadLength),
                )
                return
            self.CreateLogMessagePara4(
                Timestamp=self.SystemTime,
                MessageType=MessageType.CMD,
                Severity=Severity.DEBUG,
                MessageCode=0,
                MessageText="RecvData: ACK = {1}, received Sequence [{2}] with PayloadLength = {3}, Lifesign = {4}",
                Para1=str(seq.Header.SEQ_ACK),
                Para2=str(_seqIdx),
                Para3=str(seq.Header.PayloadLength),
                Para4=str(self.Telegram.RobToPlc.Header.LifeSign),
            )

            # processing sequence payload
            while _seqPayloadPtr < seq.Header.PayloadLength:
                frag = seq.Fragment[_fragIdx]
                frag.Header.CmdID = recv.GetUint()
                frag.Header.Reserve = recv.GetByte()
                frag.Header.FragmentAction = recv.GetByte()
                frag.Header.PayloadPointer = recv.GetUint()
                frag.Header.PayloadLength = recv.GetUint()
                # add header size to payload pointer
                _seqPayloadPtr += SIZEOF(frag.Header)

                if frag.Header.PayloadLength > 0:
                    if frag.Header.PayloadLength > self._parCfg.Com.TelegramLengthRobToPlc:
                        self.CreateLogMessagePara2(
                            Timestamp=self.SystemTime,
                            MessageType=MessageType.CMD,
                            Severity=Severity.DEBUG,
                            MessageCode=0,
                            MessageText="Invalid fragment payload length, Sequence = {1}, PayloadLength = {2} ",
                            Para1=str(_seqIdx),
                            Para2=str(frag.Header.PayloadLength),
                        )
                        return
                    # Fill Response payload
                    for _idx in range(frag.Header.PayloadLength):
                        _payLoadPtr = frag.Header.PayloadPointer + _idx
                        if 0 <= _payLoadPtr <= RobotLibraryParameter.RESPONSE_PAYLOAD_MAX:
                            frag.Command.Payload[_payLoadPtr] = recv.GetByte()
                            _seqPayloadPtr += 1
                        else:
                            self.CreateLogMessagePara3(
                                Timestamp=self.SystemTime,
                                MessageType=MessageType.CMD,
                                Severity=Severity.DEBUG,
                                MessageCode=0,
                                MessageText="Invalid fragment payload pointer, Sequence = {1}, Fragment = {2}, "
                                "PayloadPointer = {3} ",
                                Para1=str(_seqIdx),
                                Para2=str(_fragIdx),
                                Para3=str(_payLoadPtr),
                            )
                            return

                    # Add Response to ACR
                    AxesGroup.Acyclic.ActiveCommandRegister.AddRsp(frag)

                    # Only for debugging - header is part of the payload itself
                    payload = frag.Command.Payload
                    frag.Command.Header.State = CmdMessageState(GetHalfeByteLo(Value=payload[0]))
                    frag.Command.Header.ParSeq = GetHalfeByteHi(Value=payload[0])
                    frag.Command.Header.AlarmMessageSeverity = (
                        payload[1] - 256 if payload[1] > 127 else payload[1]
                    )
                    frag.Command.Header.AlarmMessageCode = CombineBytesToUint(
                        HiByte=payload[2], LoByte=payload[3]
                    )

                    self.CreateLogMessagePara5(
                        Timestamp=self.SystemTime,
                        MessageType=MessageType.CMD,
                        Severity=Severity.DEBUG,
                        MessageCode=0,
                        MessageText="RecvData: received Fragment [{1}] with PayloadLength = {2}, CmdID <{3}> , "
                        "CmdState: {4}, Fragment-Action Bits: {5}",
                        Para1=str(_seqIdx),
                        Para2=str(frag.Header.PayloadLength),
                        Para3=str(frag.Header.CmdID),
                        Para4=frag.Command.Header.State.name,
                        Para5=f"{frag.Header.FragmentAction:08b}",
                    )

                # Check still payload left ? -> goto next fragment
                if _seqPayloadPtr < seq.Header.PayloadLength:
                    _fragIdx += 1

                # Check fragment index limit reached ?
                if _fragIdx > RobotLibraryParameter.FRAGMENT_MAX:
                    self.CreateLogMessagePara1(
                        Timestamp=self.SystemTime,
                        MessageType=MessageType.CMD,
                        Severity=Severity.DEBUG,
                        MessageCode=0,
                        MessageText="Fragment index out of range, _fragIdx = {1} ",
                        Para1=str(_fragIdx),
                    )
                    return

    # ================================================================== lengths

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CalculateCyclicDataLength  sha256: cb65667947d482e7
    def CalculateCyclicDataLength(self, AxesGroup: AxesGroup, Direction: ComDirection) -> int:
        ROB_TO_PLC_HEADER_SIZE = 10  # SIZEOF(Header) is 12 because of VersionStruct
        length = 0
        if Direction == ComDirection.PLC_TO_ROB:
            plc = AxesGroup.CyclicOptional.PlcToRob
            tel = self.Telegram.PlcToRob
            length += SIZEOF(tel.Header)
            # ST-FIX F2: ToolNo/FrameNo only with "Cartesian Position" RC -> PLC (see CreateSendPayloadCyclic)
            if AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active:
                length += SIZEOF(tel.Cyclic)
            plc_parts: tuple[tuple[bool, object], ...] = (
                (plc.SubProgramData.Active, tel.CyclicOptional.SubProgramData),
                (plc.CartesianPosition.Active, tel.CyclicOptional.CartesianPosition),
                (plc.JointPosition.Active, tel.CyclicOptional.JointPosition),
                (plc.Force.Active, tel.CyclicOptional.Force),
                (plc.CartesianPositionExt.Active, tel.CyclicOptional.CartesianPositionExt),
                (plc.JointPositionExt.Active, tel.CyclicOptional.JointPositionExt),
                (plc.ForceExt.Active, tel.CyclicOptional.ForceExt),
            )
            for active, part in plc_parts:
                if active:
                    length += SIZEOF(part)
        if Direction == ComDirection.ROB_TO_PLC:
            rob = AxesGroup.CyclicOptional.RobToPlc
            opt = self.Telegram.RobToPlc.CyclicOptional
            length += ROB_TO_PLC_HEADER_SIZE
            rob_parts: tuple[tuple[bool, object], ...] = (
                (rob.SubProgramData.Active, opt.SubProgramData),
                (rob.CartesianPosition.Active, opt.CartesianPosition),
                (rob.JointPosition.Active, opt.JointPosition),
                (rob.Force.Active, opt.Force),
                (rob.Current.Active, opt.Current),
                (rob.CartesianPositionExt.Active, opt.CartesianPositionExt),
                (rob.JointPositionExt.Active, opt.JointPositionExt),
                (rob.ForceExt.Active, opt.ForceExt),
                (rob.CurrentExt.Active, opt.CurrentExt),
            )
            for active, part in rob_parts:
                if active:
                    length += SIZEOF(part)
        return length

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CalculateSequencePayloadMax  sha256: f8407eefc3f19950
    def CalculateSequencePayloadMax(
        self, AxesGroup: AxesGroup, Direction: ComDirection, Sequence: SequenceFlag
    ) -> int:
        _cyclicDataLength = self.CalculateCyclicDataLength(AxesGroup=AxesGroup, Direction=Direction)
        total = (
            self._parCfg.Com.TelegramLengthPlcToRob
            if Direction == ComDirection.PLC_TO_ROB
            else self._parCfg.Com.TelegramLengthRobToPlc
        )
        if Sequence == SequenceFlag.PRIMARY_SEQUENCE:
            return total - _cyclicDataLength
        if Sequence == SequenceFlag.SECONDARY_SEQUENCE:
            return (total - _cyclicDataLength) // 2
        return 0

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CalculateSequencePayloadStartAdr  sha256: c19d7e4cfb757b6b
    def CalculateSequencePayloadStartAdr(
        self, AxesGroup: AxesGroup, Direction: ComDirection, Sequence: SequenceFlag
    ) -> int:
        _cyclicDataLength = self.CalculateCyclicDataLength(AxesGroup=AxesGroup, Direction=Direction)
        if Sequence == SequenceFlag.PRIMARY_SEQUENCE:
            return _cyclicDataLength
        if Sequence == SequenceFlag.SECONDARY_SEQUENCE:
            _sequencePayloadLength = self.CalculateSequencePayloadMax(
                AxesGroup=AxesGroup, Direction=Direction, Sequence=Sequence
            )
            return _cyclicDataLength + _sequencePayloadLength
        return 0

    # ST-Source: POUs/General/MC_RobotTask/MC_RobotTaskFB.st#CalculateTelegramLengthPlcToRob  sha256: 705dba25faa31299
    def CalculateTelegramLengthPlcToRob(self, AxesGroup: AxesGroup) -> int:
        """Note F8: SIZEOF(Footer) is 2 (structure), the footer on the wire is 1 byte - kept as in ST."""
        _cyclicDataLength = self.CalculateCyclicDataLength(
            AxesGroup=AxesGroup, Direction=ComDirection.PLC_TO_ROB
        )
        seq = self.Telegram.PlcToRob.Sequence
        length = (
            _cyclicDataLength
            + SIZEOF(seq[self.PRIMARY_SEQUENCE].Header)
            + seq[self.PRIMARY_SEQUENCE].Header.PayloadLength
            + SIZEOF(self.Telegram.PlcToRob.Footer)
        )
        if self._parCfg.Com.TwoSequences:
            length += (
                SIZEOF(seq[self.SECONDARY_SEQUENCE].Header)
                + seq[self.SECONDARY_SEQUENCE].Header.PayloadLength
            )
        return length

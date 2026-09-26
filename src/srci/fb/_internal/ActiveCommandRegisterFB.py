"""ActiveCommandRegisterFB

ST-Source: POUs/_internal/ActiveCommandRegisterFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
from srci.fb._internal.BaseFBs.RobotLibraryLogFB import RobotLibraryLogFB
from srci.functions.Convert.Misc import ByteToFragmentAction, CombineBytesToUint, GetHalfeByteLo
from srci.functions.Convert.TO_STRING.CMD_MESSAGE_STATE_TO_STRING import CMD_MESSAGE_STATE_TO_STRING
from srci.functions.Convert.TO_STRING.CMD_TYPE_TO_STRING import CMD_TYPE_TO_STRING
from srci.functions.Swap.SwapUint import SwapUint
from srci.iec.conv import DINT_TO_REAL, DINT_TO_STRING, DINT_TO_UINT, REAL_TO_STRING, UINT_TO_STRING
from srci.iec.rt import ADR, ADR_ELEM, ADR_VALUE, SysDepMemCpy, SysDepMemSet, copy_into, mem_read, st_for_end, type_size, wrap
from srci.iec.standard import R_TRIG
from srci.types import ActiveCommandRegisterState, AlarmMessage, AxesGroupAcyclicAcrEntry, AxesGroupAcyclicAcrEntryCmdBuffer, AxesGroupAcyclicAcrEntryRspBuffer, BufferStateCmd, BufferStateRsp, CmdMessageState, CmdType, FragmentAction, MessageType, RobotLibraryConstants, RobotLibraryErrorIdEnum, RobotLibraryParameter, Severity, SystemTime, TelegramRobToPlcFragment

if TYPE_CHECKING:
    from srci.fb._internal.BaseFBs.RobotLibraryBaseFB import RobotLibraryBaseFB
    from srci.interfaces.IMessageLogger import IMessageLogger

__all__ = ['ActiveCommandRegisterFB']


class ActiveCommandRegisterFB(RobotLibraryLogFB):

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Active Command Register
        self.Register: _iec.IecArray[AxesGroupAcyclicAcrEntry] = _iec.IecArray(1, [AxesGroupAcyclicAcrEntry() for _ in range(_iec.array_len(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX')))])
        # System Time
        self.SystemTime: SystemTime = SystemTime()
        # usable size of the arc register
        self.RegisterSize: int = RobotLibraryParameter.ACTIVE_CMD_REGISTER_ENTRIES_MAX
        # VAR_OUTPUT
        # Execution Order List
        self.ExecutionOrderList: _iec.IecArray[int] = _iec.IecArray(1, [0] * _iec.array_len(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX')))
        # Current amount of used registers
        self.CurrentAcrUsageCount: int = 0
        # Current percent of used registers
        self.CurrentAcrUsagePercent: float = 0.0
        # VAR
        # temporarty Active Command Register
        self.TmpRegister: _iec.IecArray[AxesGroupAcyclicAcrEntry] = _iec.IecArray(1, [AxesGroupAcyclicAcrEntry() for _ in range(_iec.array_len(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX')))])
        # last used unique ID
        self.LastUniqueID: int = 0
        # Warning for ACR usage at 80%
        self.WarningAcrUsage: R_TRIG = R_TRIG()
        # VAR CONSTANT
        # Active command
        self.ACTIVE_CMD: int = 1
        # Buffered command
        self.BUFFER_CMD: int = 2
        # Empty ACR entry
        self.EMPTY_ACR_ENTRY: AxesGroupAcyclicAcrEntry = AxesGroupAcyclicAcrEntry(State=ActiveCommandRegisterState.IS_FREE)
        # Empty command entry
        self.EMPTY_CMD_ENTRY: AxesGroupAcyclicAcrEntryCmdBuffer = AxesGroupAcyclicAcrEntryCmdBuffer(State=BufferStateCmd.EMPTY)
        # constant for byte index of priority in payload
        self.PRIORITY_IDX: int = 3
        # bitmask to mask the priority out of the halfbyte
        self.PRIORITY_BIT_MASK: int = 15

    def __call__(self, *, Register: _iec.IecArray[AxesGroupAcyclicAcrEntry] | None = None, SystemTime: SystemTime | None = None, RegisterSize: int | None = None, InternalLogger: IMessageLogger | None = None, ExternalLogger: IMessageLogger | None = None, LogLevel: Severity | None = None) -> None:
        if Register is not None:
            copy_into(self.Register, Register)
        if SystemTime is not None:
            copy_into(self.SystemTime, SystemTime)
        if RegisterSize is not None:
            self.RegisterSize = RegisterSize
        if InternalLogger is not None:
            self.InternalLogger = InternalLogger
        if ExternalLogger is not None:
            self.ExternalLogger = ExternalLogger
        if LogLevel is not None:
            self.LogLevel = Severity(LogLevel)
        self.__body()

    def __body(self) -> None:
        self.ManageRegister()

        self.UpdateExecutionOrderList()

    def AddCmd(self, *, pCommandFB: RobotLibraryBaseFB | None = None) -> int:  # PUBLIC
        AddCmd: int = 0
        # internal index for loops
        _regIdx: int = 0
        # internal command type
        _cmdType: CmdType = CmdType.RobotTask
        # log message
        _messageLog: AlarmMessage = AlarmMessage()
        # flag for free register found
        _freeRegisterFound: bool = False
        # internal Acr error
        _errorAcrEntry: int = RobotLibraryErrorIdEnum.ERR_NO_FREE_ACR_ENTRY

        # calculate the used length of the ACR
        for _regIdx in range(1, self.RegisterSize + 1):
            if self.Register[_regIdx].State == ActiveCommandRegisterState.IS_FREE:
                self.Register[_regIdx].State = ActiveCommandRegisterState.IS_PROCESSING
                self.Register[_regIdx].UniqueID = DINT_TO_UINT(_regIdx)
                self.Register[_regIdx].pCommandFB = pCommandFB

                # check pointer to command FB
                if self.Register[_regIdx].pCommandFB is not None:
                    copy_into(self.Register[_regIdx].Command[RobotLibraryConstants.ACTIVE_CMD].Timestamp, self.SystemTime)

                    copy_into(self.Register[_regIdx].Command[RobotLibraryConstants.ACTIVE_CMD].Payload, pCommandFB.CommandData.Payload)
                    self.Register[_regIdx].Command[RobotLibraryConstants.ACTIVE_CMD].PayloadLen = pCommandFB.CommandData.PayloadLen
                    self.Register[_regIdx].Command[RobotLibraryConstants.ACTIVE_CMD].PayLoadPtr = 0
                    self.Register[_regIdx].Command[RobotLibraryConstants.ACTIVE_CMD].State = BufferStateCmd.CREATED

                # set flag for free register found
                _freeRegisterFound = True

                # Increment Current used register counter
                self.CurrentAcrUsageCount = self.CurrentAcrUsageCount + 1

                # return Unique ID
                AddCmd = self.Register[_regIdx].UniqueID

                # Get CmdType from payload
                _cmdType = mem_read(ADR(pCommandFB.CommandData, 'Payload', _iec.ArrayType(0, _iec.Param('PARAMETER_PAYLOAD_MAX'), _iec.BYTE)), _iec.EnumType(CmdType), 2, _cmdType)

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ACR-ID [{1}]: Added  Command-Payload of CmdType <{2}>', Para1=DINT_TO_STRING(_regIdx), Para2=CMD_TYPE_TO_STRING(Value=CmdType(SwapUint(Value=_cmdType))))
                break

        # Check a free register could be found ?
        if not _freeRegisterFound:
            # set error in Command FB
            if pCommandFB is not None:
                _adr__errorAcrEntry = ADR_VALUE(_errorAcrEntry, _iec.WORD)  # ADR(_errorAcrEntry)
                SysDepMemCpy(pDest=ADR(pCommandFB, 'ErrorID', _iec.WORD), pSrc=_adr__errorAcrEntry, DataLen=2)
                _errorAcrEntry = _adr__errorAcrEntry.value

            # Create log entry
            self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.FATAL_ERROR, MessageCode=0, MessageText='Not possible to add CMD <{1}> to ACR - NO FREE REGISTER FOUND ! -> STOPPING SRCI INTERFACE...', Para1=CMD_TYPE_TO_STRING(Value=CmdType(SwapUint(Value=_cmdType))))
        return AddCmd

    def AddRsp(self, *, Rsp: TelegramRobToPlcFragment | None = None) -> int:
        if Rsp is None:
            Rsp = TelegramRobToPlcFragment()
        AddRsp: int = 0
        # internal index for loops
        _Idx: int = 0
        # internal registen index
        _regIdx: int = 0
        # internal command type
        _cmdType: CmdType = CmdType.RobotTask
        # internal FragmentAction
        _fragmentAction: FragmentAction = FragmentAction()
        # internal command message state
        _cmdMessageState: CmdMessageState = CmdMessageState.EMPTY
        # internal flag for CmdID found
        _found: bool = False

        for _regIdx in range(1, self.RegisterSize + 1):
            if self.Register[_regIdx].UniqueID == Rsp.Header.CmdID:
                # CmdID was found in the ACR
                _found = True
                # convert to fragment action
                copy_into(_fragmentAction, ByteToFragmentAction(FragmentAction_=Rsp.Header.FragmentAction))

                # delete response
                if _fragmentAction.Clear:
                    SysDepMemSet(pDest=ADR_ELEM(self.Register[_regIdx].Response, self.ACTIVE_CMD, _iec.StructType(AxesGroupAcyclicAcrEntryRspBuffer)), Value=0, DataLen=type_size(_iec.StructType(AxesGroupAcyclicAcrEntryRspBuffer)))

                # add payload to response
                for _Idx in range(Rsp.Header.PayloadPointer, Rsp.Header.PayloadPointer + Rsp.Header.PayloadLength - 1 + 1):
                    copy_into(self.Register[_regIdx].Response[self.ACTIVE_CMD].Timestamp, self.SystemTime)
                    self.Register[_regIdx].Response[self.ACTIVE_CMD].State = BufferStateRsp.RECEIVING
                    self.Register[_regIdx].Response[self.ACTIVE_CMD].PayloadLen = wrap(self.Register[_regIdx].Response[self.ACTIVE_CMD].PayloadLen + 1, 'UDINT')
                    self.Register[_regIdx].Response[self.ACTIVE_CMD].Payload[_Idx] = Rsp.Command.Payload[_Idx]

                # Get current message state
                _cmdMessageState = CmdMessageState(GetHalfeByteLo(Value=self.Register[_regIdx].Response[self.ACTIVE_CMD].Payload[0]))
                # Get command type from payload
                _cmdType = CmdType(CombineBytesToUint(HiByte=self.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[0], LoByte=self.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[1]))

                # Create log entry
                self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ACR-ID [{1}]: Added Response-Payload of CmdType <{2}> with State = {3}', Para1=DINT_TO_STRING(_regIdx), Para2=CMD_TYPE_TO_STRING(Value=_cmdType), Para3=CMD_MESSAGE_STATE_TO_STRING(Value=_cmdMessageState))

                if _fragmentAction.Complete:
                    # set response state
                    self.Register[_regIdx].Response[self.ACTIVE_CMD].State = BufferStateRsp.RECEIVED

                    # Check current message state and tag the register state as IS_FINAL, if needed
                    if _cmdMessageState >= CmdMessageState.DONE:
                        self.Register[_regIdx].State = ActiveCommandRegisterState.IS_FINAL

                        # get command type from payload
                        _cmdType = CmdType(CombineBytesToUint(HiByte=self.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[0], LoByte=self.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[1]))

                        # Create log entry
                        self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ACR-ID [{1}]: Detected Response-Payload of CmdType <{2}> has reached final state <{3}>', Para1=DINT_TO_STRING(_regIdx), Para2=CMD_TYPE_TO_STRING(Value=_cmdType), Para3=CMD_MESSAGE_STATE_TO_STRING(Value=_cmdMessageState))
                        # Exit the loop

                # Check Response received complete ?
                if self.Register[_regIdx].Response[self.ACTIVE_CMD].State == BufferStateRsp.RECEIVED:
                    # update state
                    self.Register[_regIdx].Response[self.ACTIVE_CMD].State = BufferStateRsp.PROCESSED
                    # callback CommandFB
                    self.Register[_regIdx].pCommandFB.CallBack(RspData=self.Register[_regIdx].Response[self.ACTIVE_CMD], Timestamp=self.SystemTime)

                break

        # Check CmdID was found in the ACR ?
        if not _found:
            # Create log entry
            self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.WARNING, MessageCode=0, MessageText='ACR-ID [?]: Response-Payload of CmdID <{1}> with State = {2} received, but no matching ACR entry found', Para1=UINT_TO_STRING(Rsp.Header.CmdID), Para2=CMD_MESSAGE_STATE_TO_STRING(Value=_cmdMessageState))
        return AddRsp

    def FB_init(self, *, bInitRetains: bool = False, bInCopyCode: bool = False) -> bool:
        FB_init: bool = False

        self.MyType = 'ActiveCommandRegisterFB'
        return FB_init

    def ManageRegister(self) -> None:  # PRIVATE
        # internal index
        _regIdx: int = 0
        # internal command type
        _cmdType: CmdType = CmdType.RobotTask
        # internal command message state
        _cmdMessageState: CmdMessageState = CmdMessageState.EMPTY

        for _regIdx in range(1, self.RegisterSize + 1):
            # Check pointer to command FB is valid ?
            if self.Register[_regIdx].pCommandFB is not None:
                # Check apply Cmd parameter update ?
                if self.Register[_regIdx].Command[self.ACTIVE_CMD].State == BufferStateCmd.PROCESSED and self.Register[_regIdx].Command[self.BUFFER_CMD].State == BufferStateCmd.UPDATE_AVAILABLE:
                    copy_into(self.Register[_regIdx].Command[self.ACTIVE_CMD], self.Register[_regIdx].Command[self.BUFFER_CMD])
                    copy_into(self.Register[_regIdx].Command[self.BUFFER_CMD], self.EMPTY_CMD_ENTRY)

                    # get command type from payload
                    _cmdType = CmdType(CombineBytesToUint(HiByte=self.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[0], LoByte=self.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[1]))

                    # Create log entry
                    self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ACR-ID [{1}]: Moved BUFFER_CMD to ACTIVE_CMD, CmdType <{2}>', Para1=DINT_TO_STRING(_regIdx), Para2=CMD_TYPE_TO_STRING(Value=_cmdType))

                # // Check Response received ?
                # IF ( Register[_regIdx].Response[ACTIVE_CMD].State = BufferStateRsp.RECEIVED)
                # THEN
                #   // update state
                #   Register[_regIdx].Response[ACTIVE_CMD].State := BufferStateRsp.PROCESSED;
                #   // callback CommandFB
                #   Register[_regIdx].pCommandFB^.CallBack(RspData := Register[_regIdx].Response[ACTIVE_CMD],TimeStamp := SystemTime);
                # END_IF
                # delete entries with State.IS_Final
                if self.Register[_regIdx].State == ActiveCommandRegisterState.IS_FINAL:
                    # get command type from payload
                    _cmdType = CmdType(CombineBytesToUint(HiByte=self.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[0], LoByte=self.Register[_regIdx].Command[self.ACTIVE_CMD].Payload[1]))

                    # Get current message state
                    _cmdMessageState = CmdMessageState(GetHalfeByteLo(Value=self.Register[_regIdx].Response[self.ACTIVE_CMD].Payload[0]))

                    # Create log entry
                    self.CreateLogMessagePara3(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ACR-ID [{1}]: Deleted ACR-Entry of CmdType <{2}> with State = {3}, because of Final-State was reached', Para1=DINT_TO_STRING(_regIdx), Para2=CMD_TYPE_TO_STRING(Value=_cmdType), Para3=CMD_MESSAGE_STATE_TO_STRING(Value=_cmdMessageState))

                    # delete register entry
                    copy_into(self.Register[_regIdx], self.EMPTY_ACR_ENTRY)

                    # decrement current used register counter
                    self.CurrentAcrUsageCount = self.CurrentAcrUsageCount - 1

        # Calculate percent of register usage
        if self.CurrentAcrUsageCount > 0:
            self.CurrentAcrUsagePercent = DINT_TO_REAL(self.CurrentAcrUsageCount) / DINT_TO_REAL(self.RegisterSize) * 100.0
        else:
            self.CurrentAcrUsagePercent = 0.0

        # build rising edge for arc usage over 80%
        self.WarningAcrUsage(CLK=self.CurrentAcrUsagePercent > RobotLibraryParameter.ACR_USAGE_WARNING_LIMIT)

        if self.WarningAcrUsage.Q:
            # Create log entry
            self.CreateLogMessagePara4(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.WARNING, MessageCode=0, MessageText='ACR Register usage has reached the warning limit ({1}): {2}/{3} = {4}%', Para1=REAL_TO_STRING(RobotLibraryParameter.ACR_USAGE_WARNING_LIMIT), Para2=DINT_TO_STRING(self.CurrentAcrUsageCount), Para3=DINT_TO_STRING(self.RegisterSize), Para4=REAL_TO_STRING(self.CurrentAcrUsagePercent))

    def OnOnlineChange(self, *, UniqueID: int = 0, pCommandFB: RobotLibraryBaseFB | None = None) -> int:  # PUBLIC
        OnOnlineChange: int = 0
        # internal index for loops
        _regIdx: int = 0

        OnOnlineChange = -1

        # Check command FB pointer is valid ?
        if pCommandFB is not None:
            for _regIdx in range(1, self.RegisterSize + 1):
                # check unique ID found ?
                if self.Register[_regIdx].UniqueID == UniqueID:
                    # update pointer to command FB
                    self.Register[_regIdx].pCommandFB = pCommandFB
                    # Return result OK
                    OnOnlineChange = RobotLibraryConstants.OK
                    break
        return OnOnlineChange

    def RemoveCmd(self, *, UniqueID: int = 0) -> int:  # PUBLIC
        RemoveCmd: int = 0
        # internal index
        _regIdx: int = 0
        # internal command type
        _cmdType: CmdType = CmdType.RobotTask

        RemoveCmd = RobotLibraryConstants.HAS_ERROR

        if UniqueID == 0:
            UniqueID = UniqueID

        for _regIdx in range(1, self.RegisterSize + 1):
            # check unique ID found and not yet sended ?
            if self.Register[_regIdx].UniqueID == UniqueID and self.Register[_regIdx].Command[self.ACTIVE_CMD].State < BufferStateCmd.UPDATE_AVAILABLE:
                # Get CmdType from payload
                _cmdType = mem_read(ADR(self.Register[_regIdx].Command[self.ACTIVE_CMD], 'Payload', _iec.ArrayType(0, _iec.Param('PARAMETER_PAYLOAD_MAX'), _iec.BYTE)), _iec.EnumType(CmdType), 2, _cmdType)
                # delete register entry
                SysDepMemSet(pDest=ADR_ELEM(self.Register, _regIdx, _iec.StructType(AxesGroupAcyclicAcrEntry)), Value=0, DataLen=type_size(_iec.StructType(AxesGroupAcyclicAcrEntry)))
                # decrement current used register counter
                self.CurrentAcrUsageCount = self.CurrentAcrUsageCount - 1
                # Command successfull removed
                RemoveCmd = RobotLibraryConstants.OK

                # Create log entry
                self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ACR-ID [{1}]: Removed CmdType <{2}>', Para1=DINT_TO_STRING(_regIdx), Para2=CMD_TYPE_TO_STRING(Value=CmdType(SwapUint(Value=_cmdType))))
                break
        return RemoveCmd

    def Reset(self) -> None:  # PUBLIC
        SysDepMemSet(pDest=ADR(self, 'Register', _iec.ArrayType(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX'), _iec.StructType(AxesGroupAcyclicAcrEntry))), Value=0, DataLen=type_size(_iec.ArrayType(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX'), _iec.StructType(AxesGroupAcyclicAcrEntry))))

        self.CurrentAcrUsageCount = 0
        self.CurrentAcrUsagePercent = 0.0

        # Create log entry
        self.CreateLogMessagePara1(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ACR Registers has been reset and all entries deleted by Reset method call', Para1='')

    def UpdateExecutionOrderList(self) -> None:  # PRIVATE
        # temporary Active Command Register entry
        TmpRegisterEntry: AxesGroupAcyclicAcrEntry = AxesGroupAcyclicAcrEntry()
        # temporary index
        TmpIndex: int = 0
        # internal index
        i: int = 0
        # internal index
        j: int = 0

        # Reset temporary register
        SysDepMemSet(pDest=ADR(self, 'TmpRegister', _iec.ArrayType(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX'), _iec.StructType(AxesGroupAcyclicAcrEntry))), Value=0, DataLen=type_size(_iec.ArrayType(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX'), _iec.StructType(AxesGroupAcyclicAcrEntry))))
        # Reset Execution Order List
        SysDepMemSet(pDest=ADR(self, 'ExecutionOrderList', _iec.ArrayType(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX'), _iec.DINT)), Value=0, DataLen=type_size(_iec.ArrayType(1, _iec.Param('ACTIVE_CMD_REGISTER_ENTRIES_MAX'), _iec.DINT)))
        # pre-set temporary register index
        j = 1

        for i in range(1, self.RegisterSize + 1):
            # add only entries which are not in status free and where datas must be processed
            if (self.Register[i].State > ActiveCommandRegisterState.IS_FREE and self.Register[i].Command[self.ACTIVE_CMD].State != BufferStateCmd.EMPTY) and self.Register[i].Command[self.ACTIVE_CMD].State != BufferStateCmd.PROCESSED:
                # copy register entry
                copy_into(self.TmpRegister[j], self.Register[i])
                # store index of the entry from the ACR
                self.ExecutionOrderList[j] = i
                # inc temporar register index
                j = j + 1
        else:
            i = st_for_end(1, self.RegisterSize)

        # Bubble Sort to sort the priorities from the active command register
        for i in range(1, self.RegisterSize + 1):
            for j in range(1, self.RegisterSize - 1 + 1):
                # check list entry is not empty ?
                if self.TmpRegister[i].State == ActiveCommandRegisterState.IS_FREE or self.TmpRegister[j + 1].State == ActiveCommandRegisterState.IS_FREE:
                    break

                if self.TmpRegister[j].Command[self.ACTIVE_CMD].Payload[self.PRIORITY_IDX] & self.PRIORITY_BIT_MASK > self.TmpRegister[j + 1].Command[self.ACTIVE_CMD].Payload[self.PRIORITY_IDX] & self.PRIORITY_BIT_MASK:
                    # swap position of register entry
                    copy_into(TmpRegisterEntry, self.TmpRegister[j])
                    copy_into(self.TmpRegister[j], self.TmpRegister[j + 1])
                    copy_into(self.TmpRegister[j + 1], TmpRegisterEntry)

                    # swap position of index in the Execution Order List
                    TmpIndex = self.ExecutionOrderList[j]
                    self.ExecutionOrderList[j] = self.ExecutionOrderList[j + 1]
                    self.ExecutionOrderList[j + 1] = TmpIndex
            else:
                j = st_for_end(1, self.RegisterSize - 1)
        else:
            i = st_for_end(1, self.RegisterSize)

        # Bubble Sort to sort the Timestamp from the pre-sorted active command register
        for i in range(1, self.RegisterSize + 1):
            for j in range(1, self.RegisterSize - 1 + 1):
                # check list entry is not empty ?
                if self.TmpRegister[i].State == ActiveCommandRegisterState.IS_FREE or self.TmpRegister[j + 1].State == ActiveCommandRegisterState.IS_FREE:
                    break

                # Priority is higher
                # Date is greater
                # Date is the same, but Time is greater
                if self.TmpRegister[j].Command[self.ACTIVE_CMD].Payload[self.PRIORITY_IDX] & self.PRIORITY_BIT_MASK >= self.TmpRegister[j + 1].Command[self.ACTIVE_CMD].Payload[self.PRIORITY_IDX] & self.PRIORITY_BIT_MASK and (self.TmpRegister[j].Command[self.ACTIVE_CMD].Timestamp.SystemDate > self.TmpRegister[j + 1].Command[self.ACTIVE_CMD].Timestamp.SystemDate or (self.TmpRegister[j].Command[self.ACTIVE_CMD].Timestamp.SystemDate == self.TmpRegister[j + 1].Command[self.ACTIVE_CMD].Timestamp.SystemDate and self.TmpRegister[j].Command[self.ACTIVE_CMD].Timestamp.SystemTime > self.TmpRegister[j + 1].Command[self.ACTIVE_CMD].Timestamp.SystemTime)):
                    # swap position of register entry
                    copy_into(TmpRegisterEntry, self.TmpRegister[j])
                    copy_into(self.TmpRegister[j], self.TmpRegister[j + 1])
                    copy_into(self.TmpRegister[j + 1], TmpRegisterEntry)

                    # swap position of index in the Execution Order List
                    TmpIndex = self.ExecutionOrderList[j]
                    self.ExecutionOrderList[j] = self.ExecutionOrderList[j + 1]
                    self.ExecutionOrderList[j + 1] = TmpIndex

    def _set_NotifyParameterChanged(self, NotifyParameterChanged: int) -> None:
        # internal register index
        _regIdx: int = 0
        # internal command type
        _cmdType: CmdType = CmdType.RobotTask

        for _regIdx in range(1, RobotLibraryParameter.ACTIVE_CMD_REGISTER_ENTRIES_MAX + 1):
            # check unique ID found ?
            if self.Register[_regIdx].UniqueID == NotifyParameterChanged:
                if self.Register[_regIdx].Command[self.ACTIVE_CMD].State != BufferStateCmd.SENDING and self.Register[_regIdx].Command[self.ACTIVE_CMD].State != BufferStateCmd.PROCESSED:
                    # Check pointer is valid ?
                    if self.Register[_regIdx].pCommandFB is not None:
                        # add to send register
                        copy_into(self.Register[_regIdx].Command[self.ACTIVE_CMD].Timestamp, self.SystemTime)
                        self.Register[_regIdx].Command[self.ACTIVE_CMD].State = BufferStateCmd.UPDATE_AVAILABLE
                        copy_into(self.Register[_regIdx].Command[self.ACTIVE_CMD].Payload, self.Register[_regIdx].pCommandFB.CommandData.Payload)
                        self.Register[_regIdx].Command[self.ACTIVE_CMD].PayloadLen = self.Register[_regIdx].pCommandFB.CommandData.PayloadLen

                        # get command type from payload
                        _cmdType = CmdType(CombineBytesToUint(HiByte=self.Register[_regIdx].pCommandFB.CommandData.Payload[0], LoByte=self.Register[_regIdx].pCommandFB.CommandData.Payload[1]))

                        # Create log entry
                        self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ACR-ID [{1}]: Updated Cmd-Parameter of CmdType <{2}> -> written to ACTIVE_CMD Index', Para1=DINT_TO_STRING(_regIdx), Para2=CMD_TYPE_TO_STRING(Value=_cmdType))
                else:
                    # Check pointer is valid ?
                    if self.Register[_regIdx].pCommandFB is not None:
                        # add to buffer register
                        copy_into(self.Register[_regIdx].Command[self.BUFFER_CMD].Timestamp, self.SystemTime)
                        self.Register[_regIdx].Command[self.BUFFER_CMD].State = BufferStateCmd.UPDATE_AVAILABLE
                        copy_into(self.Register[_regIdx].Command[self.BUFFER_CMD].Payload, self.Register[_regIdx].pCommandFB.CommandData.Payload)
                        self.Register[_regIdx].Command[self.BUFFER_CMD].PayloadLen = self.Register[_regIdx].pCommandFB.CommandData.PayloadLen

                        # get command type from payload
                        _cmdType = CmdType(CombineBytesToUint(HiByte=self.Register[_regIdx].pCommandFB.CommandData.Payload[0], LoByte=self.Register[_regIdx].pCommandFB.CommandData.Payload[1]))

                        # Create log entry
                        self.CreateLogMessagePara2(Timestamp=self.SystemTime, MessageType=MessageType.CMD, Severity=Severity.INFO, MessageCode=0, MessageText='ACR-ID [{1}]: Updated Cmd-Parameter of CmdType <{2}> -> written to BUFFER_CMD Index', Para1=DINT_TO_STRING(_regIdx), Para2=CMD_TYPE_TO_STRING(Value=_cmdType))

    NotifyParameterChanged = property(None, _set_NotifyParameterChanged)  # PUBLIC

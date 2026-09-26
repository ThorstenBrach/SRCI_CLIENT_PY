"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ActiveCommandRegisterFB
Author:      Thorsten Brach
Date:        2026-01-01

Description:

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""
import copy
from typing import Any
from RobotLibrary.Enumerations.State.BufferStateRsp import BufferStateRsp
from RobotLibrary.IEC_Types import  DINT, ARRAY, UDINT, UINT, WORD
from RobotLibrary.IEC_Standard import R_TRIG
from RobotLibrary.Functions.ToString import INT_TO_STRING
from RobotLibrary.Functions.Convert import ByteToFragmentAction
from RobotLibrary.Constants import OK,HAS_ERROR, ACTIVE_CMD, BUFFER_CMD
from RobotLibrary.Parameter import ACTIVE_CMD_REGISTER_ENTRIES_MAX, ACR_USAGE_WARNING_LIMIT
from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseFB import RobotLibraryBaseFB
from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryLogFB import RobotLibraryLogFB
from RobotLibrary.Structures.AxesGroup.Acyclic.AxesGroupAcyclicAcrEntryRspBuffer import AxesGroupAcyclicAcrEntryRspBuffer
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from RobotLibrary.Structures.AxesGroup.Acyclic.AxesGroupAcyclicAcrEntry import AxesGroupAcyclicAcrEntry
from RobotLibrary.Structures.AxesGroup.Acyclic.AxesGroupAcyclicAcrEntryCmdBuffer import AxesGroupAcyclicAcrEntryCmdBuffer
from RobotLibrary.Structures.Miscellaneous.FragmentAction import FragmentAction
from RobotLibrary.Structures.Telegram.RobToPlc.Fragment.TelegramRobToPlcFragment import TelegramRobToPlcFragment
from RobotLibrary.Enumerations.State.CmdMessageState import CmdMessageState
from RobotLibrary.Enumerations.State.ActiveCommandRegisterState import ActiveCommandRegisterState
from RobotLibrary.Enumerations.Type.CmdType import CmdType
from RobotLibrary.Enumerations.State.BufferStateCmd import BufferStateCmd
from RobotLibrary.Enumerations.Events.ErrorIdEnum  import ErrorIdEnum as RobotErrorIdEnum 
from RobotLibrary.Enumerations.Type.MessageType import MessageType as MessageTypeEnum
from RobotLibrary.Enumerations.Miscellaneous.Severity  import Severity as SeverityEnum
from RobotLibrary.Structures.Miscellaneous.AlarmMessage import AlarmMessage

class ActiveCommandRegisterFB(RobotLibraryLogFB):
    
    #region VAR_INPUT
    Register: ARRAY[AxesGroupAcyclicAcrEntry] = ARRAY(1, ACTIVE_CMD_REGISTER_ENTRIES_MAX, AxesGroupAcyclicAcrEntry)
    """ Active Command Register"""
    _systemTime : SystemTime
    """System Time"""
    _registerSize : int = int(ACTIVE_CMD_REGISTER_ENTRIES_MAX)
    """usable size of the arc register"""
    #endregion
    

    #region VAR_OUTPUT
    ExecutionOrderList: ARRAY[DINT] = ARRAY(1, ACTIVE_CMD_REGISTER_ENTRIES_MAX, DINT)
    """ Execution Order List """
    CurrentAcrUsageCount : int
    """ Current amount of used registers """
    CurrentAcrUsagePercent : float
    """ Current percent of used registers """
    #endregion


    #region VAR
    TmpRegister: ARRAY[AxesGroupAcyclicAcrEntry] = ARRAY(1, ACTIVE_CMD_REGISTER_ENTRIES_MAX, AxesGroupAcyclicAcrEntry)
    """ temporarty Active Command Register"""
    LastUniqueID : UINT = UINT(0)
    """ last used unique ID """
    WarningAcrUsage : R_TRIG
    """ Warning for ACR usage at 80% """
    #endregion

    #region VAR CONSTANT
    EMPTY_ACR_ENTRY      : AxesGroupAcyclicAcrEntry = AxesGroupAcyclicAcrEntry()
    """ Empty ACR entry """
    EMPTY_CMD_ENTRY      : AxesGroupAcyclicAcrEntryCmdBuffer = AxesGroupAcyclicAcrEntryCmdBuffer()
    """ Empty command entry """
    #endregion    
    
    #-------------------------------------------------------------------------
    # __init__ - Constructor / Initialization
    #-------------------------------------------------------------------------
    def __init__(self) -> None:
        self.EMPTY_ACR_ENTRY.State = ActiveCommandRegisterState.IS_FREE
        self.EMPTY_CMD_ENTRY.State = BufferStateCmd.EMPTY
        self.MyType = self.__class__.__name__
        # initialize runtime counters and helpers
        self.CurrentAcrUsageCount   = 0
        self.CurrentAcrUsagePercent = 0.0
        self.WarningAcrUsage        = R_TRIG()


    #-------------------------------------------------------------------------
    # __call__ - main execution ( FB body )
    #-------------------------------------------------------------------------
    def __call__(self,
                 SystemTime   : SystemTime,
                 RegisterSize : int,
                 *args: Any, **kwds: Any) -> Any:

        self._systemTime = SystemTime   
        self._registerSize = RegisterSize

        self.ManageRegister()
        self.UpdateExecutionOrderList()


    #-------------------------------------------------------------------------
    #  AddCmd - Add command to ACR
    #-------------------------------------------------------------------------
    def AddCmd(self, pCommandFB: RobotLibraryBaseFB) -> int:
        
        # return value of method        
        AddCmd : int = 0
        
        # region local variables
        
        # internal index for loops
        _regIdx : int = 0
        # internal command type 
        _cmdType : CmdType = CmdType(0)
        # log message
        _messageLog : AlarmMessage = AlarmMessage()
        # flag for free register found
        _freeRegisterFound : bool = False
        # internal Acr error 
        _errorAcrEntry : WORD = RobotErrorIdEnum.ERR_NO_FREE_ACR_ENTRY.TypeValue

        # endregion

        # calculate the used length of the ACR 
        for _regIdx in range(1, self._registerSize):
            
            if ( self.Register[_regIdx].State == ActiveCommandRegisterState.IS_FREE ):
                
                self.Register[_regIdx].State          =  ActiveCommandRegisterState.IS_PROCESSING
                self.Register[_regIdx].UniqueID.value = _regIdx
                self.Register[_regIdx].pCommandFB     =  pCommandFB
                # check pointer to command FB
                if ( self.Register[_regIdx].pCommandFB is not None ):

                    self.Register[_regIdx].Command[ACTIVE_CMD].Timestamp  = self._systemTime
                    self.Register[_regIdx].Command[ACTIVE_CMD].Payload    = pCommandFB.CommandData.Payload 
                    self.Register[_regIdx].Command[ACTIVE_CMD].PayloadLen = pCommandFB.CommandData.PayloadLen
                    self.Register[_regIdx].Command[ACTIVE_CMD].PayLoadPtr = UINT(0)
                    self.Register[_regIdx].Command[ACTIVE_CMD].State      = BufferStateCmd.CREATED
                # set flag for free register found
                _freeRegisterFound = True                
                # Increment Current used register counter
                self.CurrentAcrUsageCount +=1

                # return Unique ID
                AddCmd = self.Register[_regIdx].UniqueID.value

                # Get CmdType from payload
                _cmdType = self.Register[_regIdx].Command[ACTIVE_CMD].GetCmdHeaderFromPayload().CmdTyp

                # Create log entry
                self.CreateLogMessage( 
                    Timestamp   = self._systemTime,
                    MessageType = MessageTypeEnum.CMD,
                    Severity    = SeverityEnum.INFO,
                    MessageCode = 0,
                    MessageText = 'ACR-ID [{1}]: Added  Command-Payload of CmdType <{2}>',
                    Para1       =  INT_TO_STRING(_regIdx),
                    Para2       =  _cmdType.toString()
                )

                break # exit for loop


        # Check a free register could be found ? 
        if ( not _freeRegisterFound ):

            # set error in Command FB   
            if ( pCommandFB is not None ):

                pCommandFB.ErrorID = int(RobotErrorIdEnum.ERR_NO_FREE_ACR_ENTRY)

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self._systemTime,
                MessageType = MessageTypeEnum.CMD,
                Severity    = SeverityEnum.FATAL_ERROR,
                MessageCode = 0,
                MessageText = 'Not possible to add CMD <{1}> to ACR - NO FREE REGISTER FOUND ! -> STOPPING SRCI INTERFACE...',
                Para1       =  _cmdType.toString()
            )                          


        return AddCmd


    #-------------------------------------------------------------------------
    #  AddRsp - Add response to ACR
    #-------------------------------------------------------------------------
    def AddRsp(self, Rsp : TelegramRobToPlcFragment) -> int:
        
        # return value of method
        AddRspCmd        : int = 0
        
        #region local variables
        
        # internal index for loops
        _Idx             : int = 0
        # internal register index
        _regIdx          : int = 0
        # internal command type
        _cmdType         : CmdType = CmdType(0)
        # internal FragmentAction
        _fragmentAction  : FragmentAction = FragmentAction()
        # internal command message state
        _cmdMessageState : CmdMessageState = CmdMessageState(0)

        # internal flag for CmdID found
        _found           : bool = False
        
        #endregion
                
        for _regIdx in range(1, self._registerSize):
        
            if ( self.Register[_regIdx].UniqueID == Rsp.Header.CmdID ):
            
                # CmdID was found in the ACR
                _found = True
                # convert to fragment action 
                _fragmentAction = ByteToFragmentAction(Rsp.Header.FragmentAction)

                # delete response 
                if ( _fragmentAction.Clear ):

                    # delete response
                    self.Register[_regIdx].Response[ACTIVE_CMD] = AxesGroupAcyclicAcrEntryRspBuffer()


                # add payload to response
                for _idx in range( Rsp.Header.PayloadPointer.value,  Rsp.Header.PayloadLength.value -1 ):
                
                    self.Register[_regIdx].Response[ACTIVE_CMD].Timestamp     = self._systemTime
                    self.Register[_regIdx].Response[ACTIVE_CMD].State         = BufferStateRsp.RECEIVING
                    self.Register[_regIdx].Response[ACTIVE_CMD].PayloadLen    = UDINT(self.Register[_regIdx].Response[ACTIVE_CMD].PayloadLen.value + 1)
                    self.Register[_regIdx].Response[ACTIVE_CMD].Payload[_idx] = Rsp.Command.Payload[_idx]

                # Get current message state 
                _cmdMessageState = self.Register[_regIdx].Response[ACTIVE_CMD].GetRspHeaderFromPayload().State
                # Get command type from payload
                _cmdType         = self.Register[_regIdx].Command[ACTIVE_CMD].GetCmdHeaderFromPayload().CmdTyp


                # Create log entry
                self.CreateLogMessage( 
                    Timestamp   = self._systemTime,
                    MessageType = MessageTypeEnum.CMD,
                    Severity    = SeverityEnum.INFO,
                    MessageCode = 0,
                    MessageText = 'ACR-ID [{1}]: Added Response-Payload of CmdType <{2}> with State = {3}',
                    Para1       =  INT_TO_STRING(_regIdx),
                    Para2       =  _cmdType.toString(),
                    Para3       =  _cmdMessageState.toString()
                )

                if ( _fragmentAction.Complete ) :
                
                    # set response state
                    self.Register[_regIdx].Response[ACTIVE_CMD].State = BufferStateRsp.RECEIVED

                    # Check current message state and tag the register state as IS_FINAL, if needed 
                    if ( _cmdMessageState >= CmdMessageState.DONE) :
                    
                        self.Register[_regIdx].State = ActiveCommandRegisterState.IS_FINAL
                        
                        # get command type from payload
                        _cmdType = self.Register[_regIdx].Command[ACTIVE_CMD].GetCmdHeaderFromPayload().CmdTyp


                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self._systemTime,
                            MessageType = MessageTypeEnum.CMD,
                            Severity    = SeverityEnum.INFO,
                            MessageCode = 0,
                            MessageText = 'ACR-ID [{1}]: Detected Response-Payload of CmdType <{2}> has reached final state <{3}>',
                            Para1       =  INT_TO_STRING(_regIdx),
                            Para2       =  _cmdType.toString(),
                            Para3       =  _cmdMessageState.toString()
                        )


                # Check Response received complete ? 
                if ( self.Register[_regIdx].Response[ACTIVE_CMD].State == BufferStateRsp.RECEIVED) :
                
                    # update state
                    self.Register[_regIdx].Response[ACTIVE_CMD].State = BufferStateRsp.PROCESSED
                    # callback CommandFB    
                    self.Register[_regIdx].pCommandFB.CallBack(RspData=self.Register[_regIdx].Response[ACTIVE_CMD], Timestamp=self._systemTime)

                break # exit for loop


        # Check CmdID was found in the ACR ? 
        if ( not _found ):

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = self._systemTime,
                MessageType = MessageTypeEnum.CMD,
                Severity    = SeverityEnum.WARNING,
                MessageCode = 0,
                MessageText = 'ACR-ID [?]: Response-Payload of CmdID <{1}> with State = {2} received, but no matching ACR entry found',
                Para1       =  Rsp.Header.CmdID.toString(),
                Para2       =  _cmdMessageState.toString()
            )

        return AddRspCmd 


    @property
    def NotifyParameterChanged(self) -> int:
        """Notify that parameters have changed"""
        return 0 # no value to return
        
    @NotifyParameterChanged.setter
    def NotifyParameterChanged(self, value : int) -> None:
        
        #region local variables

        # internal register index
        _regIdx  : int = 0
        # internal command type
        _cmdType : CmdType = CmdType(0)
        
        #endregion
        
        
        for _regIdx in range( 1,ACTIVE_CMD_REGISTER_ENTRIES_MAX) :
        
            # check unique ID found ?
            if ( self.Register[_regIdx].UniqueID.value == value ):
            
                if (( self.Register[_regIdx].Command[ACTIVE_CMD].State != BufferStateCmd.SENDING   ) and
                    ( self.Register[_regIdx].Command[ACTIVE_CMD].State != BufferStateCmd.PROCESSED )):
                
                    if ( self.Register[_regIdx].pCommandFB is not None ):
                
                        # add to send register
                        self.Register[_regIdx].Command[ACTIVE_CMD].Timestamp  = self._systemTime
                        self.Register[_regIdx].Command[ACTIVE_CMD].State      = BufferStateCmd.UPDATE_AVAILABLE
                        self.Register[_regIdx].Command[ACTIVE_CMD].Payload    = self.Register[_regIdx].pCommandFB.CommandData.Payload
                        self.Register[_regIdx].Command[ACTIVE_CMD].PayloadLen = self.Register[_regIdx].pCommandFB.CommandData.PayloadLen

                        # get command type from payload
                        _cmdType = self.Register[_regIdx].Command[ACTIVE_CMD].GetCmdHeaderFromPayload().CmdTyp
                    
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self._systemTime,
                            MessageType = MessageTypeEnum.CMD,
                            Severity    = SeverityEnum.INFO,
                            MessageCode = 0,
                            MessageText = 'ACR-ID [{1}]: Updated Cmd-Parameter of CmdType <{2}> -> written to ACTIVE_CMD Index',
                            Para1       =  INT_TO_STRING(_regIdx),
                            Para2       =  _cmdType.toString()
                        )

                else:
                    # Check pointer is valid ? 
                    if ( self.Register[_regIdx].pCommandFB is not None ) :
                    
                        # add to buffer register
                        self.Register[_regIdx].Command[BUFFER_CMD].Timestamp  = self._systemTime
                        self.Register[_regIdx].Command[BUFFER_CMD].State      = BufferStateCmd.UPDATE_AVAILABLE
                        self.Register[_regIdx].Command[BUFFER_CMD].Payload    = self.Register[_regIdx].pCommandFB.CommandData.Payload
                        self.Register[_regIdx].Command[BUFFER_CMD].PayloadLen = self.Register[_regIdx].pCommandFB.CommandData.PayloadLen

                        # get command type from payload
                        _cmdType = self.Register[_regIdx].Command[BUFFER_CMD].GetCmdHeaderFromPayload().CmdTyp
                        
                        # Create log entry
                        self.CreateLogMessage( 
                            Timestamp   = self._systemTime,
                            MessageType = MessageTypeEnum.CMD,
                            Severity    = SeverityEnum.INFO,
                            MessageCode = 0,
                            MessageText = 'ACR-ID [{1}]: Updated Cmd-Parameter of CmdType <{2}> -> written to BUFFER_CMD Index',
                            Para1       =  INT_TO_STRING(_regIdx),
                            Para2       =  _cmdType.toString()
                        )


    #-------------------------------------------------------------------------
    #  ManageRegister - Manage the Active Command Register
    #-------------------------------------------------------------------------
    def ManageRegister(self) -> None:
        
        #region local variables
        
        # internal index
        _regIdx          : int = 0
        # internal command type
        _cmdType         : CmdType = CmdType(0)
        # internal command message state
        _cmdMessageState : CmdMessageState = CmdMessageState(0)
        
        #endregion

        for _regIdx in range(1 , self._registerSize) :
        
            # Check pointer to command FB is valid ? 
            if ( self.Register[_regIdx].pCommandFB is not None) :
            
            
                # Check apply Cmd parameter update ?  
                if (( self.Register[_regIdx].Command[ACTIVE_CMD].State == BufferStateCmd.PROCESSED        ) and
                    ( self.Register[_regIdx].Command[BUFFER_CMD].State == BufferStateCmd.UPDATE_AVAILABLE )) :
                
                    self.Register[_regIdx].Command[ACTIVE_CMD] = self.Register[_regIdx].Command[BUFFER_CMD]
                    self.Register[_regIdx].Command[BUFFER_CMD] = copy.deepcopy(self.EMPTY_CMD_ENTRY)
                
                    # get command type from payload
                    _cmdType = self.Register[_regIdx].Command[ACTIVE_CMD].GetCmdHeaderFromPayload().CmdTyp
                
                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = self._systemTime,
                        MessageType = MessageTypeEnum.CMD,
                        Severity    = SeverityEnum.INFO,
                        MessageCode = 0,
                        MessageText = 'ACR-ID [{1}]: Moved BUFFER_CMD to ACTIVE_CMD, CmdType <{2}>',
                        Para1       =  INT_TO_STRING(_regIdx),
                        Para2       =  _cmdType.toString()
                    )
                
                    
                """
                # Check Response received ? 
                if ( self.Register[_regIdx].Response[ACTIVE_CMD].State == BufferStateRsp.RECEIVED) :
                
                    # update state
                    self.Register[_regIdx].Response[ACTIVE_CMD].State = BufferStateRsp.PROCESSED
                    # callback CommandFB    
                    self.Register[_regIdx].pCommandFB.CallBack(RspData = self.Register[_regIdx].Response[ACTIVE_CMD],Timestamp = self.SystemTime)
                """
                
                # delete entries with State.IS_Final 
                if ( self.Register[_regIdx].State == ActiveCommandRegisterState.IS_FINAL ):
                
                    # get command type from payload
                    _cmdType = self.Register[_regIdx].Command[ACTIVE_CMD].GetCmdHeaderFromPayload().CmdTyp                              
                
                    # Get current message state 
                    _cmdMessageState = self.Register[_regIdx].Response[ACTIVE_CMD].GetRspHeaderFromPayload().State

                    # Create log entry
                    self.CreateLogMessage(
                        Timestamp   = self._systemTime,
                        MessageType = MessageTypeEnum.CMD,
                        Severity    = SeverityEnum.INFO,
                        MessageCode = 0,
                        MessageText = 'ACR-ID [{1}]: Deleted ACR-Entry of CmdType <{2}> with State = {3}, because of Final-State was reached',
                        Para1       =  INT_TO_STRING(_regIdx),
                        Para2       =  _cmdType.toString(),
                        Para3       =  _cmdMessageState.toString()
                    )


                    # delete register 
                    self.Register[_regIdx] = copy.deepcopy(self.EMPTY_ACR_ENTRY)

                    # decrement current used register counter
                    self.CurrentAcrUsageCount -= 1


        # Calculate percent of register usage
        if ( self.CurrentAcrUsageCount > 0):
        
            self.CurrentAcrUsagePercent =  self.CurrentAcrUsageCount / self._registerSize * 100.0
        else:
            self.CurrentAcrUsagePercent = 0.0


        # build rising edge for arc usage over 80% 
        self.WarningAcrUsage( CLK = (self.CurrentAcrUsagePercent > ACR_USAGE_WARNING_LIMIT))

        if ( self.WarningAcrUsage.Q ) :
        
            # Create log entry
            self.CreateLogMessage(
                Timestamp   = self._systemTime,
                MessageType = MessageTypeEnum.CMD,
                Severity    = SeverityEnum.WARNING,
                MessageCode = 0,
                MessageText = 'ACR Register usage has reached the warning limit ({1}): {2}/{3} = {4}%',
                Para1       =  str(ACR_USAGE_WARNING_LIMIT),
                Para2       =  str(self.CurrentAcrUsageCount),
                Para3       =  str(self._registerSize),
                Para4       =  str(self.CurrentAcrUsagePercent)
            )


    #-------------------------------------------------------------------------
    #  OnOnlineChange - Handle online change
    #-------------------------------------------------------------------------
    def OnOnlineChange(self, UniqueID : UDINT, pCommandFB : RobotLibraryBaseFB) -> int:
        """Handle online change"""
        
        # internal index for loops
        _regIdx : int = 0        
        
        OnOnlineChange = HAS_ERROR

        # Check command FB pointer is valid ?
        if ( pCommandFB is not None):
        
            for _regIdx  in range (1, self._registerSize):
            
                # check unique ID found ?
                if ( self.Register[_regIdx].UniqueID == UniqueID ) :
                    
                    # update pointer to command FB
                    self.Register[_regIdx].pCommandFB = pCommandFB
                    # Return result OK
                    OnOnlineChange = OK
                    break
            
        return OnOnlineChange


    #-------------------------------------------------------------------------
    #  RemoveCmd - Remove command from ACR
    #-------------------------------------------------------------------------
    def RemoveCmd(self, UniqueID: int) -> int:
        
        # return value of method
        RemoveCmd : int = 0
        
        #region local variables
        
        # internal index
        _regIdx : int = 0
        # internal command type 
        _cmdType : CmdType = CmdType(0)

        #endregion
        
        
        RemoveCmd = HAS_ERROR

        # just for break point in debugger
        if (UniqueID == 0):
        
            UniqueID = UniqueID


        for _regIdx in range(1, self._registerSize):
        
            # check unique ID found and not yet sended ?
            if (( self.Register[_regIdx].UniqueID.value           == UniqueID                        ) and
                ( self.Register[_regIdx].Command[ACTIVE_CMD].State < BufferStateCmd.UPDATE_AVAILABLE )):       
            
                # Get CmdType from payload
                _cmdType = self.Register[_regIdx].Command[ACTIVE_CMD].GetCmdHeaderFromPayload().CmdTyp                
                # delete register entry
                self.Register[_regIdx] = copy.deepcopy(self.EMPTY_ACR_ENTRY)
                
                # decrement current used register counter
                self.CurrentAcrUsageCount -= 1
                # Command successfull removed
                RemoveCmd = OK
                
                
                # Create log entry
                self.CreateLogMessage(  
                    Timestamp   = self._systemTime,
                    MessageType = MessageTypeEnum.CMD,
                    Severity    = SeverityEnum.INFO,
                    MessageCode = 0,
                    MessageText = 'ACR-ID [{1}]: Removed CmdType <{2}>',
                    Para1       =  INT_TO_STRING(_regIdx),                 
                    Para2       =  _cmdType.toString()
                )
                
                break # exit for loop
            
        return RemoveCmd


    #-------------------------------------------------------------------------
    #  Reset - Reset internal variables
    #-------------------------------------------------------------------------
    def Reset(self) -> None:
        """Reset internal variables"""
        
        # internal index for loops
        _idx : int = 0

        # reset usage counters
        self.CurrentAcrUsageCount   = 0
        self.CurrentAcrUsagePercent = 0.0
        self.LastUniqueID           = UINT(0)
        
        # reset ACR register
        for _idx in range(1, ACTIVE_CMD_REGISTER_ENTRIES_MAX):
            self.Register[_idx] = copy.deepcopy(self.EMPTY_ACR_ENTRY)
            self.ExecutionOrderList[_idx] = DINT(0)
            
        # Create log entry
        self.CreateLogMessage(
            Timestamp   = self._systemTime,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.INFO,
            MessageCode = 0,
            MessageText = 'ACR Registers has been reset and all entries deleted by Reset method call',
            Para1       =  ''
            )


    #-------------------------------------------------------------------------
    #  UpdateExecutionOrderList - Update the execution order list based on priorities
    #-------------------------------------------------------------------------
    def UpdateExecutionOrderList(self) -> None:
        
        #region local variables
        
        # temporary Active Command Register entry
        TmpRegisterEntry  : AxesGroupAcyclicAcrEntry = AxesGroupAcyclicAcrEntry()
        # temporary index
        TmpIndex          : int = 0
        # internal index
        i                 : int = 0
        # internal index
        j                 : int = 0  
        #constant for byte index of priority in payload 
        PRIORITY_IDX      : int = 3
        # bitmask to mask the priority out of the halfbyte
        PRIORITY_BIT_MASK : int = int(0b00001111)

        #end region
                
        for i in range ( 1, self._registerSize):
            # Reset temporary register
            self.TmpRegister[i] = copy.deepcopy(self.EMPTY_ACR_ENTRY)   
            # Reset Execution Order List
            self.ExecutionOrderList[i] = DINT(0)


        # pre-set temporary register index 
        j = 1

        for i in range ( 1, self._registerSize):
        
            # add only entries which are not in status free and where datas must be processed
            if (( self.Register[i].State                      > ActiveCommandRegisterState.IS_FREE ) and
                ( self.Register[i].Command[ACTIVE_CMD].State != BufferStateCmd.EMPTY               ) and
                ( self.Register[i].Command[ACTIVE_CMD].State != BufferStateCmd.PROCESSED           )):
            
                # copy register entry 
                self.TmpRegister[j] = self.Register[i]
                # store index of the entry from the ACR
                self.ExecutionOrderList[j] = i
                # inc temporar register index
                j = j + 1

        # Bubble Sort to sort the priorities from the active command register
        for i in range(1, self._registerSize):
        
            for j in range(1, self._registerSize - 1):
              
                # check list entry is not empty ? 
                if (( self.TmpRegister[i  ].State == ActiveCommandRegisterState.IS_FREE ) or
                    ( self.TmpRegister[j+1].State == ActiveCommandRegisterState.IS_FREE )):
                
                    break

                if (( self.TmpRegister[j].Command[ACTIVE_CMD].Payload[PRIORITY_IDX] & PRIORITY_BIT_MASK ) > ( self.TmpRegister[j+1].Command[ACTIVE_CMD].Payload[PRIORITY_IDX] & PRIORITY_BIT_MASK )):

                    # swap position of register entry  
                    TmpRegisterEntry = self.TmpRegister[j]
                    self.TmpRegister[j] = self.TmpRegister[j+1]
                    self.TmpRegister[j+1] = TmpRegisterEntry
                
                    # swap position of index in the Execution Order List  
                    TmpIndex = self.ExecutionOrderList[j].value
                    self.ExecutionOrderList[j].value = self.ExecutionOrderList[j+1].value
                    self.ExecutionOrderList[j+1].value = TmpIndex

        # Bubble Sort to sort the Timestamp from the pre-sorted active command register
        for i  in range(1, self._registerSize):
        
            for j in range(1, self._registerSize - 1):

                # check list entry is not empty ? 
                if (( self.TmpRegister[i  ].State == ActiveCommandRegisterState.IS_FREE ) or
                    ( self.TmpRegister[j+1].State == ActiveCommandRegisterState.IS_FREE )):
                
                    break

                # Priority is higher
                if (
                   (( self.TmpRegister[j].Command[ACTIVE_CMD].Payload[PRIORITY_IDX] & PRIORITY_BIT_MASK ) >= ( self.TmpRegister[j+1].Command[ACTIVE_CMD].Payload[PRIORITY_IDX] & PRIORITY_BIT_MASK )) and
                    # Date is greater 
                    (( self.TmpRegister[j].Command[ACTIVE_CMD].Timestamp.SystemDate.value                 >   self.TmpRegister[j+1].Command[ACTIVE_CMD].Timestamp.SystemDate.value                 )  or 
                    # Date is the same, but Time is greater
                    (( self.TmpRegister[j].Command[ACTIVE_CMD].Timestamp.SystemDate.value                 ==  self.TmpRegister[j+1].Command[ACTIVE_CMD].Timestamp.SystemDate.value                 )  and 
                     ( self.TmpRegister[j].Command[ACTIVE_CMD].Timestamp.SystemTime.value                 >   self.TmpRegister[j+1].Command[ACTIVE_CMD].Timestamp.SystemTime.value                 )))
                  ):
                    # swap position of register entry  
                    TmpRegisterEntry = self.TmpRegister[j]
                    self.TmpRegister[j] = self.TmpRegister[j+1]
                    self.TmpRegister[j+1] = TmpRegisterEntry

                    # swap position of index in the Execution Order List  
                    TmpIndex = self.ExecutionOrderList[j].value
                    self.ExecutionOrderList[j]   = self.ExecutionOrderList[j+1]
                    self.ExecutionOrderList[j+1] = TmpIndex
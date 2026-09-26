"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_ReadActualPositionFB
Author:      Thorsten Brach
Date:        2026-01-25

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
#region Imports
import copy

from RobotLibrary.IEC_Standard import SetTimeout
from RobotLibrary.Constants import RUNNING, OK

from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseExecuteFB import RobotLibraryBaseExecuteFB
from RobotLibrary.POUs._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from RobotLibrary.POUs._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB

from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from RobotLibrary.Structures.AxesGroup.AxesGroup import AxesGroup

from RobotLibrary.Enumerations.State import CmdMessageState
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Enumerations.Type.MessageType import MessageType
from RobotLibrary.Enumerations.Events.ErrorIdEnum import ErrorIdEnum as RobotLibraryErrorIdEnum
from RobotLibrary.Enumerations.Type.CmdType import CmdType
from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode
from RobotLibrary.Enumerations.Mode.ProcessingMode import ProcessingMode as ProcessingModeEnum
from RobotLibrary.Enumerations.Flag.SequenceFlag import SequenceFlag as SequenceFlagEnum

from .Structures.ReadActualPositionParCmd import ReadActualPositionParCmd
from .Structures.ReadActualPositionOutCmd import ReadActualPositionOutCmd
from .Structures.ReadActualPositionRecvData import ReadActualPositionRecvData
from .Structures.ReadActualPositionSendData import ReadActualPositionSendData
#endregion

class MC_ReadActualPositionFB( RobotLibraryBaseExecuteFB):
    """Function block to move axes to absolute positions."""
    
    #VAR_INPUT
    ProcessingMode     : ProcessingModeEnum
    """Processing mode - For more information see chapter 5.6.4.5."""

    SequenceFlag       : SequenceFlagEnum
    """Defines the target sequence in which the command will be executed"""
    
    ParCmd             : ReadActualPositionParCmd
    """command parameter"""
    
    #VAR_OUTPUT
    CommandBuffered    : bool
    """Command is transferred and confirmed by the RC"""
    
    Valid              : bool
    """
    TRUE, while the following outputs return valid values
     • ActualCartesianPosition
     • ToolNoReturn
     • FrameNoReturn
     • ActualJointPosition
     """

    CommandAborted     : bool
    """The command was aborted by another command."""

    CommandInterrupted : bool
    """TRUE, while command is interrupted during execution and can be continued."""
    
    ParameterAccepted  : bool
    """Receiving of input parameter values has been acknowledged by RC"""

    OutCmd             : ReadActualPositionOutCmd
    """command outputs"""

    #VAR
    _parCmd            : ReadActualPositionParCmd
    """ internal copy of command parameter """
    _command           : ReadActualPositionSendData
    """ command data to send """
    _response          : ReadActualPositionRecvData
    """ response data received """

    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        
        super().__init__()
        
        # Initialize Base
        self.MyType   = self.__class__.__name__
        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        self.ProcessingMode = ProcessingModeEnum.PARALLEL
        self.SequenceFlag = SequenceFlagEnum.PRIMARY_SEQUENCE
        # Initialize VAR_INPUT
        self.ParCmd          = ReadActualPositionParCmd()
        
        # Initialize VAR_OUTPUT
        self.CommandBuffered    = False
        self.Active             = False
        self.CommandAborted     = False
        self.CommandInterrupted = False
        self.OutCmd             = ReadActualPositionOutCmd()
        
        # Initialize VAR
        self._parCmd            = ReadActualPositionParCmd()
        self._command           = ReadActualPositionSendData()
        self._response          = ReadActualPositionRecvData()


    #--------------------------------------------------------
    # CheckAddParameter - check if parameter must be added
    #--------------------------------------------------------
    def CheckAddParameter(self, PayloadPtr: int) -> bool:
        """
        Checks if the remaining payload is not empty and the parameter must be added
        """        
        # Get payload as bytes 
        Payload : bytearray = self._command.GetBytes()

        return any(Payload[PayloadPtr:])


    #--------------------------------------------------------
    # CheckFunctionSupported - check if function is supported by RC
    #--------------------------------------------------------
    def CheckFunctionSupported(self, AxesGroup: AxesGroup) -> bool:
        """
        Check if the function is supported by the connected robot controller
        """
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.ReadActualPosition.value

        if ( not CheckFunctionSupported ):

            # call base implementation for set error and create log entry
            super().CheckFunctionSupported(AxesGroup = AxesGroup)

        return CheckFunctionSupported


    #--------------------------------------------------------
    # CheckParameterChanged - check if parameter changed
    #--------------------------------------------------------
    def CheckParameterChanged(self, AxesGroup : AxesGroup) -> bool:

        # Check ParCmd Size is > 0, because MemCmp does not work correctly with size = 0
        if ((self.ParCmd.sizeof() == 0) or (self._stepCmd == 0)) :

            return False

        # compare memory 
        self._parameterChanged = self.ParCmd != self._parCmd

        # check parameter valid ?
        self._parameterValid   = self.CheckParameterValid( AxesGroup = AxesGroup )

        if (((  self._parameterChanged        )  and 
             (  self._parameterValid          )) or
             (  self._parameterUpdateInternal ))  :

            # Create log entry for parameter changed event
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.DEBUG,
                MessageCode = 0,
                MessageText = 'NotifyParameterChanged Event {1}',
                Para1       =  ''
            )

            # reset internal flag for send parameter update
            self._parameterUpdateInternal = False
            # update internal copy of parameters 
            self._parCmd = copy.deepcopy(self.ParCmd)
            # inc parameter sequence
            self._command.ParSeq.value += 1
            # update command data  
            self.CommandData = self.CreateCommandPayload(AxesGroup = AxesGroup) # ( Access via reference to rCommandFB in ACR )
            # notify active command register 
            AxesGroup.Acyclic.ActiveCommandRegister.NotifyParameterChanged = self._uniqueID
            # Reset Valid output of the FB 
            self.Valid = False
            # Reset parameter accepted flag
            self.ParameterAccepted = False

        return self._parameterChanged 


    #--------------------------------------------------------
    # CheckParameterValid - check if parameter is valid
    #--------------------------------------------------------
    def CheckParameterValid(self, AxesGroup : AxesGroup) -> bool:
        """
        Check if the input parameters are valid
        """

        CheckParameterValid : bool = True

        # Check ParCmd.ProcessingMode defined ? 
        if (( self.ProcessingMode < ProcessingModeEnum.BUFFERED         ) and 
            ( self.ProcessingMode > ProcessingModeEnum.TRIGGER_MULTIPLE )) :

            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_DEFINED, Overwrite = True )
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.ProcessingMode = {1}',
                Para1       = str(self.ProcessingMode)
            )
            return CheckParameterValid


        # Check ProcessingMode valid ? 
        if (( self.ProcessingMode != ProcessingModeEnum.BUFFERED           ) and  
            ( self.ProcessingMode != ProcessingModeEnum.ABORTING           ) and  
            ( self.ProcessingMode != ProcessingModeEnum.PARALLEL           ) and
            ( self.ProcessingMode != ProcessingModeEnum.CONTINUOUS         ) and
            ( self.ProcessingMode != ProcessingModeEnum.DEACTIVATE         ) and
            ( self.ProcessingMode != ProcessingModeEnum.TRIGGER_ONCE       ) and
            ( self.ProcessingMode != ProcessingModeEnum.TRIGGER_CONTINUOUS ) and
            ( self.ProcessingMode != ProcessingModeEnum.TRIGGER_MULTIPLE   )) :
        
            #Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite = True )
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ProcessingMode = {1}',
                Para1       =  str(self.ProcessingMode)
            )
            return CheckParameterValid


        # Check SequenceFlag valid ? 
        if (( self.SequenceFlag != SequenceFlagEnum.       NO_SEQUENCE ) and  
            ( self.SequenceFlag != SequenceFlagEnum.  PRIMARY_SEQUENCE ) and  
            ( self.SequenceFlag != SequenceFlagEnum.SECONDARY_SEQUENCE )):
        
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite = True )
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter SequenceFlag = {1}',
                Para1       =  str(self.SequenceFlag)
            )
            return CheckParameterValid


        # Check ParCmd.ToolNo valid ? 
        if (( self.ParCmd.ToolNo <  -1                                                ) or  
            ( self.ParCmd.ToolNo > 254                                                ) or
            ( self.ParCmd.ToolNo > AxesGroup.State.ConfigurationData.HighestToolIndex ) or
            ( self.ParCmd.ToolNo > AxesGroup.State.UnifiedToolIndex                   )):
        
            # Parameter not valid
            CheckParameterValid = False
            
            # Check ToolNo available on RC ? 
            if ( self.ParCmd.ToolNo > AxesGroup.State.ConfigurationData.HighestToolIndex ) :
                
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_TOOLNO_UNAVAILABLE, Overwrite = True )
            else:
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_TOOLNO_RANGE, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.ToolNo = {1}',
                Para1       =  str(self.ParCmd.ToolNo)
            )
            return CheckParameterValid


        # Check ParCmd.FrameNo valid ? 
        if (( self.ParCmd.FrameNo <  -1                                                 ) or  
            ( self.ParCmd.FrameNo > 254                                                 ) or
            ( self.ParCmd.FrameNo > AxesGroup.State.ConfigurationData.HighestFrameIndex ) or
            ( self.ParCmd.FrameNo > AxesGroup.State.UnifiedFrameIndex                   )) :

            # Parameter not valid
            CheckParameterValid = False
            
            # Check FrameNo available on RC ? 
            if ( self.ParCmd.FrameNo > AxesGroup.State.ConfigurationData.HighestFrameIndex ) :
                
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_FRAMENO_UNAVAILABLE, Overwrite = True )                
                
            else:
                
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_FRAMENO_RANGE, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.FrameNo = {1}',
                Para1       =  str(self.ParCmd.FrameNo)
            )
            return CheckParameterValid


        # Check ParCmd.ListenerID valid ? 
        if (( self.ParCmd.ListenerID <   0 ) or  
            ( self.ParCmd.ListenerID > 127 )):
        
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.ListenerID = {1}',
                Para1       =  str(self.ParCmd.ListenerID)
            )
            return CheckParameterValid

        return CheckParameterValid


    #--------------------------------------------------------
    # CreateCommandPayload - create command payload
    #--------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup : AxesGroup) -> RobotLibraryCommandDataFB:
        
        # Parameter count
        _parameterCnt : int = 0

        #region Mapping table
        
        # Table 6-38: Sent CMD payload (PLC to RC) of "ReadActualPosition"
        # --------------------------
        # Header
        # --------------------------
        # Byte 00 : UINT  - Type HB     
        # Byte 01 :       - Type LB    
        # Byte 02 : USINT - Reserve | ExecutionMode
        # Byte 03 : USINT - ParSeq  | Priority
        # --------------------------
        # Datablock
        # --------------------------
        # Byte 04 : SINT  EmitterID[0];
        # Byte 05 : SINT  EmitterID[1];
        # Byte 06 : SINT  EmitterID[2];
        # Byte 07 : SINT  EmitterID[3];
        # Byte 08 : SINT  ListenerID;
        # Byte 09 : BYTE  Reserved;
        # Byte 10 : USINT ToolNo
        # Byte 11 : USINT FrameNo
        # --------------------------
        # endregion

        # set command parameter 
        self._command.CmdTyp                      = CmdType.ReadActualPosition
        self._command.ExecMode                    = self. ExecMode
        self._command.ParSeq                      = self._command.ParSeq
        self._command.Priority                    = self. Priority
         
        self._command.EmitterID[0].value          = 0
        self._command.EmitterID[1].value          = 0
        self._command.EmitterID[2].value          = 0
        self._command.EmitterID[3].value          = 0
        self._command.Reserve.value               = 0
        self._command.ListenerID.value            = self._parCmd.ListenerID
        self._command.ToolNo.value                = self._parCmd.ToolNo
        self._command.FrameNo.value               = self._parCmd.FrameNo


        if (self._parCmd.ToolNo == -1 ) :
            self._command.ToolNo.value = 255 # -1 is mapped to 255, see specification

        if (self._parCmd.FrameNo == -1 ) :
            self._command.FrameNo.value = 255 # -1 is mapped to 255, see specification


        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


        for _idx in range(0, 4 ) :
        
            # Check parameter must be added ? 
            if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)) :
                
                # add command.EmitterID[x]
                self.CommandData.AddSint(self._command.EmitterID[_idx])
                # inc parameter counter
                _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ListenerID
            self.CommandData.AddSint(self._command.ListenerID)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.Reserve
            self.CommandData.AddSint(self._command.Reserve)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolNo
            self.CommandData.AddUsint(self._command.ToolNo)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.FrameNo
            self.CommandData.AddUsint(self._command.FrameNo)
            # inc parameter counter
            _parameterCnt += 1


        #return command data
        return self.CommandData
    
    
    #--------------------------------------------------------
    # CreateCommandPayloadLog - create log entry for created command payload
    #--------------------------------------------------------
    def CreateCommandPayloadLog(self, AxesGroup : AxesGroup, ParameterCnt : int) -> None:
        """
        Create log entry for created command payload
        """

        # Create log entry for Parameter start
        self.CreateLogMessage (
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Create command payload with {1} parameter(s) :',
            Para1       = str(ParameterCnt)
        )

        for _idx in range(0, 4 ) :
            # Return if no parameter is remaining...
            if ( ParameterCnt == 0 ) : return #noqa
            
            # dec remaining parameter(s)
            ParameterCnt -= 1
            # Create log entry for MsgID
            self.CreateLogMessage (
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.DEBUG,
                MessageCode = 0,
                MessageText = 'Command.EmitterID[{2}] = {1}',
                Para1       =  str(self._command.EmitterID[_idx]),
                Para2       =  str(_idx)
            )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for MsgID
        self.CreateLogMessage (
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Command.ListenerID = {1}',
            Para1       =  str(self._command.ListenerID)
        )
        

        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for MsgID
        self.CreateLogMessage (
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Command.Reserve = {1}',
            Para1       =  str(self._command.Reserve)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for MsgID
        self.CreateLogMessage (
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Command.ToolNo = {1}',
            Para1       =  str(self._command.ToolNo)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for MsgID
        self.CreateLogMessage (
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Command.FrameNo = {1}',
            Para1       =  str(self._command.FrameNo)
        )


    #--------------------------------------------------------
    # OnApplyOutCmd - apply output command data
    #--------------------------------------------------------
    def OnApplyOutCmd(self, State : CmdMessageState) -> None:
        """
        Apply output command data received from robot controller
        """

        if ( State == CmdMessageState.EMPTY ) :

            # Reset command outputs
            self.OutCmd = ReadActualPositionOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :

            # Update results
            self.OutCmd.OriginID                = self._response.OriginID.value
            self.OutCmd.InvocationCounter       = self._response.InvocationCounter.value
            self.OutCmd.ToolNoReturn            = self._response.ToolNoReturn.value
            self.OutCmd.FrameNoReturn           = self._response.FrameNoReturn.value
            self.OutCmd.ActualCartesianPosition = self._response.ActualCartesianPosition
            self.OutCmd.ActualJointPosition     = self._response.ActualJointPosition


    #--------------------------------------------------------
    # OnExecRun  - executed during execution
    #--------------------------------------------------------
    def OnExecRun(self, AxesGroup: AxesGroup) -> int:

        OnExecRun : int = RUNNING
        
        # call base implementation
        super().OnExecRun(AxesGroup = AxesGroup)

        match self._stepCmd :
        
            case 0: 
                
                if ( self._execute_R.Q ) and ( not self.Error) :

                    # Check function is supported and parameter are valid ?
                    if (( self.CheckFunctionSupported( AxesGroup = AxesGroup )) and
                        ( self.CheckParameterValid   ( AxesGroup = AxesGroup ))):

                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        self.OutCmd = ReadActualPositionOutCmd()
                        # apply command parameter
                        self._parCmd = copy.deepcopy(self.ParCmd)
                        # init parameter sequence
                        self._command.ParSeq.value = 1
                        # create command data
                        self.CommandData = self.CreateCommandPayload(AxesGroup = AxesGroup)
                        # Add command to active command register
                        self._uniqueID = AxesGroup.Acyclic.ActiveCommandRegister.AddCmd( pCommandFB = self)
                        # set timeout
                        SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                        # inc step counter
                        self._stepCmd += 1

            case 1:
                
                # Wait for responce received
                if ( self._responseReceived ) :
                
                    # reset response received flag
                    self._responseReceived = False
                    # update state flags
                    self.OnUpdateStateFlags(self._response.State)
                    # update state flags
                    self.OnApplyOutCmd(self._response.State)
                            
                    # Done, Aborted or Error ?
                    if (self._response.State >= CmdMessageState.DONE ) :
                        
                        # set timeout
                        SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                        # inc step counter
                        self._stepCmd += 1 


            case 2:
                
                if ( not self.Execute ) :

                    self.Reset()
                    # reset step counter
                    self._stepCmd = 0
                    # finish OK
                    OnExecRun = OK


            case _:
                # invalid step
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite = True )


        # Reset FB
        if ( not self.Execute ) :

            self.Reset()

        return OnExecRun


    #--------------------------------------------------------
    # OnUpdateStateFlags - update state flags
    #--------------------------------------------------------
    def OnUpdateStateFlags(self, State : CmdMessageState) -> None:
        """
        Update state flags according to received state
        """

        # Reset State flags
        self.CommandAborted = False
        self.CommandInterrupted = False
        self.Done = False

        match State:

            # No operation or process is active
            case CmdMessageState.EMPTY:
                pass

            # Created but not yet started
            case CmdMessageState.CREATED:
                pass

            # Buffered and awaiting execution
            case CmdMessageState.BUFFERED :
                self.CommandBuffered    = True
                self.ParameterAccepted  = True

            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER : 
                self.CommandBuffered    = True
                self.ParameterAccepted  = True

            # Currently active and in progress
            case CmdMessageState.ACTIVE: 
                pass

            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED:
                self.CommandInterrupted = True

            # Requested for abort
            case CmdMessageState.ABORT_REQUEST:
                pass

            # Successfully completed
            case CmdMessageState.DONE : 
                self.Done = True
                self.Busy = False

            # Aborted before completion
            case CmdMessageState.ABORTED:
                self.CommandAborted = True
                self.Busy = False

            # Encountered an error during execution
            case CmdMessageState.ERROR:
                self.Error = True
                self.Busy = False


    #--------------------------------------------------------#
    # ParseResponsePayload - parse response payload
    #--------------------------------------------------------#                
    def ParseResponsePayload(self, ResponseData : RobotLibraryResponseDataFB, Timestamp : SystemTime ) -> int:
        """
        Parse response payload received from robot controller
        """

        #region Mapping table

        # Table 6-39: Received CMD payload (RC to PLC) of "ReadActualPosition"
        # --------------------------
        # Header
        # --------------------------
        # Byte 00 : USINT   - ParSeq | State     
        # Byte 01 : SINT    - AlarmMessageSeverity    
        # Byte 02 : UINT    - AlarmMessageCode HB
        # Byte 03 :         - AlarmMessageCode LB
        # --------------------------
        # Datablock
        # --------------------------
        # Byte 04 : USINT   - InvocationCounter;
        # Byte 05 : SINT    - Reserved;
        # Byte 06 : INT     - OriginID HW HB;
        # Byte 07 :         - OriginID HW LB;
        # Byte 08 : USINT   - ToolNoReturn;
        # Byte 09 : USINT   - FrameNoReturn;
        # Byte 10 : REAL    - ActualCartesianPosition.X HW HB;
        # Byte 11 :         - ActualCartesianPosition.X HW LB;
        # Byte 12 :         - ActualCartesianPosition.X LW HB;
        # Byte 13 :         - ActualCartesianPosition.X LW LB;
        # Byte 14 : REAL    - ActualCartesianPosition.Y HW HB;
        # Byte 15 :         - ActualCartesianPosition.Y HW LB;
        # Byte 16 :         - ActualCartesianPosition.Y LW HB;
        # Byte 17 :         - ActualCartesianPosition.Y LW LB;
        # Byte 18 : REAL    - ActualCartesianPosition.Z HW HB;
        # Byte 19 :         - ActualCartesianPosition.Z HW LB;
        # Byte 20 :         - ActualCartesianPosition.Z LW HB;
        # Byte 21 :         - ActualCartesianPosition.Z LW LB;
        # Byte 22 : REAL    - ActualCartesianPosition.RX HW HB;
        # Byte 23 :         - ActualCartesianPosition.RX HW LB;
        # Byte 24 :         - ActualCartesianPosition.RX LW HB;
        # Byte 25 :         - ActualCartesianPosition.RX LW LB;
        # Byte 26 : REAL    - ActualCartesianPosition.RY HW HB;
        # Byte 27 :         - ActualCartesianPosition.RY HW LB;
        # Byte 28 :         - ActualCartesianPosition.RY LW HB;
        # Byte 29 :         - ActualCartesianPosition.RY LW LB;
        # Byte 30 : REAL    - ActualCartesianPosition.RZ HW HB;
        # Byte 31 :         - ActualCartesianPosition.RZ HW LB;
        # Byte 32 :         - ActualCartesianPosition.RZ LW HB;
        # Byte 33 :         - ActualCartesianPosition.RZ LW LB;
        # Byte 34 : BYTE    - W E S;
        # Byte 35 : BYTE    - Reserved;
        # Byte 36 : BYTE    - ActualCartesianPosition.TurnNumber[0];
        # Byte 37 : BYTE    - ActualCartesianPosition.TurnNumber[1];
        # Byte 38 : BYTE    - ActualCartesianPosition.TurnNumber[2];
        # Byte 39 : BYTE    - ActualCartesianPosition.TurnNumber[3];
        # Byte 40 : REAL    - ActualCartesianPosition.E1 HW HB;
        # Byte 41 :         - ActualCartesianPosition.E1 HW LB;
        # Byte 42 :         - ActualCartesianPosition.E1 LW HB;
        # Byte 43 :         - ActualCartesianPosition.E1 LW LB;
        # Byte 44 : REAL    - ActualJointPosition.J1 HW HB;
        # Byte 45 :         - ActualJointPosition.J1 HW LB;
        # Byte 46 :         - ActualJointPosition.J1 LW HB;
        # Byte 47 :         - ActualJointPosition.J1 LW LB;
        # Byte 48 : REAL    - ActualJointPosition.J2 HW HB;
        # Byte 49 :         - ActualJointPosition.J2 HW LB;
        # Byte 50 :         - ActualJointPosition.J2 LW HB;
        # Byte 51 :         - ActualJointPosition.J2 LW LB;
        # Byte 52 : REAL    - ActualJointPosition.J3 HW HB;
        # Byte 53 :         - ActualJointPosition.J3 HW LB;
        # Byte 54 :         - ActualJointPosition.J3 LW HB;
        # Byte 55 :         - ActualJointPosition.J3 LW LB;
        # Byte 56 : REAL    - ActualJointPosition.J4 HW HB;
        # Byte 57 :         - ActualJointPosition.J4 HW LB;
        # Byte 58 :         - ActualJointPosition.J4 LW HB;
        # Byte 59 :         - ActualJointPosition.J4 LW LB;
        # Byte 60 : REAL    - ActualJointPosition.J5 HW HB;
        # Byte 61 :         - ActualJointPosition.J5 HW LB;
        # Byte 62 :         - ActualJointPosition.J5 LW HB;
        # Byte 63 :         - ActualJointPosition.J5 LW LB;
        # Byte 64 : REAL    - ActualJointPosition.J6 HW HB;
        # Byte 65 :         - ActualJointPosition.J6 HW LB;
        # Byte 66 :         - ActualJointPosition.J6 LW HB;
        # Byte 67 :         - ActualJointPosition.J6 LW LB;
        # Byte 68 : REAL    - ActualCartesianPosition.E2 HW HB;
        # Byte 69 :         - ActualCartesianPosition.E2 HW LB;
        # Byte 70 :         - ActualCartesianPosition.E2 LW HB;
        # Byte 71 :         - ActualCartesianPosition.E2 LW LB;
        # Byte 72 : REAL    - ActualCartesianPosition.E3 HW HB;
        # Byte 73 :         - ActualCartesianPosition.E3 HW LB;
        # Byte 74 :         - ActualCartesianPosition.E3 LW HB;
        # Byte 75 :         - ActualCartesianPosition.E3 LW LB;
        # Byte 76 : REAL    - ActualCartesianPosition.E4 HW HB;
        # Byte 77 :         - ActualCartesianPosition.E4 HW LB;
        # Byte 78 :         - ActualCartesianPosition.E4 LW HB;
        # Byte 79 :         - ActualCartesianPosition.E4 LW LB;
        # Byte 80 : REAL    - ActualCartesianPosition.E5 HW HB;
        # Byte 81 :         - ActualCartesianPosition.E5 HW LB;
        # Byte 82 :         - ActualCartesianPosition.E5 LW HB;
        # Byte 83 :         - ActualCartesianPosition.E5 LW LB;
        # Byte 84 : REAL    - ActualCartesianPosition.E6 HW HB;
        # Byte 85 :         - ActualCartesianPosition.E6 HW LB;
        # Byte 86 :         - ActualCartesianPosition.E6 LW HB;
        # Byte 87 :         - ActualCartesianPosition.E6 LW LB;
        # Byte 88 : REAL    - ActualJointPosition.E1 HW HB;
        # Byte 89 :         - ActualJointPosition.E1 HW LB;
        # Byte 90 :         - ActualJointPosition.E1 LW HB;
        # Byte 91 :         - ActualJointPosition.E1 LW LB;
        # Byte 92 : REAL    - ActualJointPosition.E2 HW HB;
        # Byte 93 :         - ActualJointPosition.E2 HW LB;
        # Byte 94 :         - ActualJointPosition.E2 LW HB;
        # Byte 95 :         - ActualJointPosition.E2 LW LB;
        # Byte 96 : REAL    - ActualJointPosition.E3 HW HB;
        # Byte 97 :         - ActualJointPosition.E3 HW LB;
        # Byte 98 :         - ActualJointPosition.E3 LW HB;
        # Byte 99 :         - ActualJointPosition.E3 LW LB;
        # Byte 100: REAL    - ActualJointPosition.E4 HW HB;
        # Byte 101:         - ActualJointPosition.E4 HW LB;
        # Byte 102:         - ActualJointPosition.E4 LW HB;
        # Byte 103:         - ActualJointPosition.E4 LW LB;
        # Byte 104: REAL    - ActualJointPosition.E5 HW HB;
        # Byte 105:         - ActualJointPosition.E5 HW LB;
        # Byte 106:         - ActualJointPosition.E5 LW HB;
        # Byte 107:         - ActualJointPosition.E5 LW LB;
        # Byte 108: REAL    - ActualJointPosition.E6 HW HB;
        # Byte 109:         - ActualJointPosition.E6 HW LB;
        # Byte 110:         - ActualJointPosition.E6 LW HB;
        # Byte 111:         - ActualJointPosition.E6 LW LB;
        # --------------------------
        #endregion


        # Parameter count
        _parameterCnt : int = 0
        
        # call base implementation to parse the header from payload buffer
        ResponseData.PayloadPtr.value = super().ParseResponsePayload(ResponseData = ResponseData, Timestamp = Timestamp)

        # copy parsed header to response
        self._response.ParSeq               = self._rspHeader.ParSeq
        self._response.State                = self._rspHeader.State
        self._response.AlarmMessageSeverity = self._rspHeader.AlarmMessageSeverity
        self._response.AlarmMessageCode     = self._rspHeader.AlarmMessageCode


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.InvocationCounter
            self._response.InvocationCounter = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Reserve
            self._response.Reserve = ResponseData.GetSint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.OriginID
            self._response.OriginID = ResponseData.GetInt()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ToolNoReturn
            self._response.ToolNoReturn = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.FrameNoReturn
            self._response.FrameNoReturn = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.X
            self._response.ActualCartesianPosition.X = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.Y
            self._response.ActualCartesianPosition.Y = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.Z
            self._response.ActualCartesianPosition.Z = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.Rx
            self._response.ActualCartesianPosition.Rx = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.Ry
            self._response.ActualCartesianPosition.Ry = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.Rz
            self._response.ActualCartesianPosition.Rz = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.Config
            self._response.ActualCartesianPosition.Config = ResponseData.GetArmConfig()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.TurnNumber
            self._response.ActualCartesianPosition.TurnNumber = ResponseData.GetTurnNumbers()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.E1
            self._response.ActualCartesianPosition.E1 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.J1
            self._response.ActualJointPosition.J1 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.J2
            self._response.ActualJointPosition.J2 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.J3
            self._response.ActualJointPosition.J3 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.J4
            self._response.ActualJointPosition.J4 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.J5
            self._response.ActualJointPosition.J5 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1
            

        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.J6
            self._response.ActualJointPosition.J6 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.E2
            self._response.ActualCartesianPosition.E2 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.E3
            self._response.ActualCartesianPosition.E3 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.E4
            self._response.ActualCartesianPosition.E4 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.E5
            self._response.ActualCartesianPosition.E5 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualCartesianPosition.E6
            self._response.ActualCartesianPosition.E6 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.E1
            self._response.ActualJointPosition.E1 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.E2
            self._response.ActualJointPosition.E2 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.E3
            self._response.ActualJointPosition.E3 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.E4
            self._response.ActualJointPosition.E4 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.E5
            self._response.ActualJointPosition.E5 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ActualJointPosition.E6
            self._response.ActualJointPosition.E6 = ResponseData.GetReal().value
            # inc parameter counter
            _parameterCnt += 1


        # Create logging
        self.ParseResponsePayloadLog(ResponseData = ResponseData, Timestamp = Timestamp, ParameterCnt = _parameterCnt)
        
        # return updated payload pointer
        return ResponseData.PayloadPtr.value


    #--------------------------------------------------------#
    # ParseResponsePayloadLog - create log entry for parsed response payload
    #--------------------------------------------------------#
    def ParseResponsePayloadLog(self, ResponseData : RobotLibraryResponseDataFB,
                                      Timestamp    : SystemTime, 
                                      ParameterCnt : int                        ) -> None:

        # Create log entry for Parameter start
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = '{1} parameter(s) to parse from the response data:',
            Para1       = str(ParameterCnt)
        )
        

        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.InvocationCounter = {1}',
            Para1       =  str(self._response.InvocationCounter)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.Reserve = {1}',
            Para1       =  str(self._response.Reserve)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.OriginID = {1}',
            Para1       =  str(self._response.OriginID)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ToolNoReturn = {1}',
            Para1       =  str(self._response.ToolNoReturn)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.FrameNoReturn = {1}',
            Para1       =  str(self._response.FrameNoReturn)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.X = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.X)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.Y = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.Y)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.Z = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.Z)
        )

        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.Rx = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.Rx)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.Ry = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.Ry)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.Rz = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.Rz)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.Config = {1};{2};{3}',
            Para1       =  str(self._response.ActualCartesianPosition.Config.Shoulder),
            Para2       =  str(self._response.ActualCartesianPosition.Config.Elbow),
            Para3       =  str(self._response.ActualCartesianPosition.Config.Wrist)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.TurnNumber.J1Turns = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.TurnNumber.J1Turns)
        )

        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.TurnNumber.J2Turns = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.TurnNumber.J2Turns)
        )

        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.TurnNumber.J3Turns = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.TurnNumber.J3Turns)
        )

        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.TurnNumber.J4Turns = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.TurnNumber.J4Turns)
        )

        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.TurnNumber.J5Turns = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.TurnNumber.J5Turns)
        )

        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.TurnNumber.J6Turns = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.TurnNumber.J6Turns)
        )

        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.TurnNumber.E1Turns = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.TurnNumber.E1Turns)
        )
        

        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.E1 = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.E1)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.J1 = {1}',
            Para1       =  str(self._response.ActualJointPosition.J1)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.J2 = {1}',
            Para1       =  str(self._response.ActualJointPosition.J2)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.J3 = {1}',
            Para1       =  str(self._response.ActualJointPosition.J3)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.J4 = {1}',
            Para1       =  str(self._response.ActualJointPosition.J4)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.J5 = {1}',
            Para1       =  str(self._response.ActualJointPosition.J5)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.J6 = {1}',
            Para1       =  str(self._response.ActualJointPosition.J6)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.E2 = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.E2)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.E3 = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.E3)
        )
        
        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.E4 = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.E4)
        )
        
        
        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.E5 = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.E5)
        )

        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualCartesianPosition.E6 = {1}',
            Para1       =  str(self._response.ActualCartesianPosition.E6)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.E1 = {1}',
            Para1       =  str(self._response.ActualJointPosition.E1)
        )



        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.E2 = {1}',
            Para1       =  str(self._response.ActualJointPosition.E2)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.E3 = {1}',
            Para1       =  str(self._response.ActualJointPosition.E3)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.E4 = {1}',
            Para1       =  str(self._response.ActualJointPosition.E4)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.E5 = {1}',
            Para1       =  str(self._response.ActualJointPosition.E5)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enabled
        self.CreateLogMessage(  
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ActualJointPosition.E6 = {1}',
            Para1       =  str(self._response.ActualJointPosition.E6)
        )

    #--------------------------------------------------------
    # Reset - reset internal variables
    #--------------------------------------------------------
    def Reset(self) -> int:
        """ Reset internal variables """

        self.Done               = False
        self.Busy               = False
        self.Valid              = False
        self.CommandBuffered    = False
        self.CommandAborted     = False
        self.CommandInterrupted = False

        return super().Reset()
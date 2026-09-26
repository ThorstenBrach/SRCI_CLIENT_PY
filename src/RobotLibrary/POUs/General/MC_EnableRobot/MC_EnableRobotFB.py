"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_EnableRobotFB
Author:      Thorsten Brach
Date:        2025-12-22

Description:

Copyright:
    (C) 2025 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""
#region Imports
import copy
from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel
from RobotLibrary.Functions.ToString import STEP_MODE_TO_STRING, BOOL_TO_STRING, INT_TO_STRING
from RobotLibrary.IEC_Types import BOOL, BYTE, DWORD
from RobotLibrary.IEC_Standard import SetTimeout,CheckTimeout
from RobotLibrary.Constants import OK, RUNNING, HAS_ERROR
from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseEnableFB import RobotLibraryBaseEnableFB
from RobotLibrary.POUs._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from RobotLibrary.POUs._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode
from RobotLibrary.Enumerations.Type.MessageType import MessageType
from RobotLibrary.Enumerations.Type.MessageType import MessageType as MessageTypeEnum
from RobotLibrary.Enumerations.Type.CmdType import CmdType
from RobotLibrary.Enumerations.Events.ErrorIdEnum import ErrorIdEnum as RobotErrorIdEnum
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity as SeverityEnum
from RobotLibrary.Enumerations.Mode.StepMode import StepMode
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode as ExecutionModeEnum
from RobotLibrary.Enumerations.State.CmdMessageState import CmdMessageState
from RobotLibrary.Structures.AxesGroup.AxesGroup import AxesGroup
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from .Structures.EnableRobotParCmd import EnableRobotParCmd
from .Structures.EnableRobotOutCmd import EnableRobotOutCmd
from .Structures.EnableRobotSendData import EnableRobotSendData 
from .Structures.EnableRobotRecvData import EnableRobotRecvData
#endregion
    
# ------------------------------------------------------------
# Vollständiger Funktionsbaustein
# ------------------------------------------------------------
class MC_EnableRobotFB(RobotLibraryBaseEnableFB):
    """
    Python‑Abbildung des IEC‑Funktionsbausteins
    MC_EnableRobotFB EXTENDS RobotLibraryBaseEnableFB
    """

    # VAR_INPUT
    ParCmd                   : EnableRobotParCmd
    """Command parameter"""

    # VAR_OUTPUT
    CommandBuffered          : bool
    """Command is transferred and confirmed by the RC"""
    ParameterAccepted        : bool
    """Receiving of input parameter values has been acknowledged by RC"""
    OutCmd                   : EnableRobotOutCmd 
    """command results"""

    # VAR (lokal)
    _parCmd                  : EnableRobotParCmd
    """internal copy of command parameter"""
    _command                 : EnableRobotSendData
    """command data to send"""
    _response                : EnableRobotRecvData
    """response data received"""
    _synchronizationValid    : bool
    """internal flag for synchronisation valid"""

    # --------------------------------------------------------
    # __init__ - Contructor + initialization
    # --------------------------------------------------------
    def __init__(self):
        """Initialization of class instance"""
        
        self.MyType   = self.__class__.__name__
        self.ExecMode = ExecutionModeEnum.PARALLEL
        self.Priority = PriorityLevel.NORMAL
        
        # call base implementation
        super().__init__()


    # --------------------------------------------------------
    # __call__ - main execution ( FB body )
    # --------------------------------------------------------
    def __call__(self,Name     : str          ,
                      ExecMode : ExecutionMode,
                      Priority : PriorityLevel,
                      AxesGroup: AxesGroup      ) -> None:
        
        # call base implementation
        super().__call__(Name      = Name,
                         ExecMode  = ExecMode,
                         Priority  = Priority,
                         AxesGroup = AxesGroup)


    # --------------------------------------------------------
    # CheckAddParameter - check if parameter must be added to payload
    # --------------------------------------------------------
    def CheckAddParameter(self, PayloadPtr: int) -> bool:
        """
        Checks if the remaining payload is not empty and the parameter must be added
        """        
        # Get payload as bytes 
        Payload : bytearray = self._command.GetBytes()

        return any(Payload[PayloadPtr:])


    # --------------------------------------------------------
    # CheckFunctionSupported - check if function is supported by robot controller
    # --------------------------------------------------------
    def CheckFunctionSupported(self, AxesGroup: AxesGroup) -> bool:
        """Check if function is supported by robot controller"""
        
        # internal flag to indicate function supported
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.EnableRobot.value
        
        if not CheckFunctionSupported:
            # call base implementation for error handling
            super().CheckFunctionSupported(AxesGroup = AxesGroup)
            
        return CheckFunctionSupported


    # --------------------------------------------------------
    # CheckParameterChanged - check if parameters have changed
    # --------------------------------------------------------
    def CheckParameterChanged(self, AxesGroup: AxesGroup) -> bool:
        """Check if command parameters have changed"""
        
        # check Parameter is assigned and step is not initial
        if self.ParCmd is None or self._stepCmd == 0:
            return False

        # compare types ( data must be apply with deep copy )
        self._parameterChanged = ( self._parCmd != self.ParCmd) 
        # Check parameter valid ? 
        self._parameterValid = self.CheckParameterValid(AxesGroup = AxesGroup)
        # Check synchronization valid ?
        self._synchronizationValid = self.CheckSynchronizationValid(AxesGroup = AxesGroup)

        if (
           (( self._parameterChanged        ) and 
            ( self._parameterValid          ) and 
            ( self._synchronizationValid    )) or
            ( self._parameterUpdateInternal )
           ):
        
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
            # Reset parameter accepted flag
            self.ParameterAccepted = False

        return self._parameterChanged


    # --------------------------------------------------------
    # CheckParameterValid - check if parameters are valid
    # --------------------------------------------------------
    def CheckParameterValid(self, AxesGroup: AxesGroup) -> bool:
        """
        Check if command parameters are valid
        """

        # internal flag to indicate parameter valid
        CheckParameterValid : bool = True
                
        # Check ParCmd.HoldToRun
        # -> no plausibility check for boolean

        # Check ParCmd.StepMode valid ? 
        if (( self.ParCmd.StepMode != StepMode.DEACTIVATE ) and
            ( self.ParCmd.StepMode != StepMode.BLENDING   ) and  
            ( self.ParCmd.StepMode != StepMode.EXACT_STOP )):  
        
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite = True )
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = DWORD(self.ErrorID),
                MessageText = 'Invalid Parameter ParCmd.StepMode = {1}',
                Para1       =  STEP_MODE_TO_STRING(self.ParCmd.StepMode))
            
            # return validation result
            return CheckParameterValid

        # Check ParCmd.ManualStep
        # -> no plausibility check for boolean
        return CheckParameterValid


    # --------------------------------------------------------
    # CreateCommandPayload - create command payload
    # --------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup: AxesGroup) -> RobotLibraryCommandDataFB:
        """Create command payload data"""

        # internal parameter counter
        _parameterCnt : int = 0

        #region Mapping table
        
        # Table 6-25: Sent CMD payload (PLC to RC) of "EnableRobot"
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
        # Byte 04 : BOOL  - Enable
        # Byte 05 : BOOL  - HoldToRun
        # Byte 06 : USINT - StepMode
        # Byte 07 : BOOL  - ManualStep
        # --------------------------
        # endregion

        # update command data
        self._command.CmdTyp            = CmdType.EnableRobot
        self._command.ExecMode          = self. ExecMode
        self._command.ParSeq            = self._command.ParSeq
        self._command.Priority          = self. Priority
        self._command.Enable            = BOOL(self.Enable)
        self._command.HoldToRun.value   = self._parCmd.HoldToRun
        self._command.StepMode          = self._parCmd.StepMode
        self._command.ManualStep.value  = self._parCmd.ManualStep

        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
            
            # add command.Enable
            self.CommandData.AddBool(self._command.Enable)
            # inc parameter counter
            _parameterCnt += 1  


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
            
            # add command.StepMode
            self.CommandData.AddUsint(self._command.StepMode.TypeValue)
            # inc parameter counter
            _parameterCnt += 1  


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.HoldToRun
            self.CommandData.AddBool(self._command.HoldToRun)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ManualStep
            self.CommandData.AddBool(self._command.ManualStep)
            # inc parameter counter
            _parameterCnt += 1


        # Create logging
        self.CreateCommandPayloadLog(AxesGroup = AxesGroup, ParameterCnt = _parameterCnt)

        return self.CommandData


    # --------------------------------------------------------
    # CreateCommandPayloadLog - create logging of command payload
    # --------------------------------------------------------
    def CreateCommandPayloadLog(self, AxesGroup: AxesGroup, ParameterCnt: int) -> None:
        """Create command payload log entry"""
        
        # Create log entry for Parameter start
        self.CreateLogMessage( 
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Create command payload with {1} parameter(s) :',
            Para1       = str(ParameterCnt))


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
                       
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for Enable
        self.CreateLogMessage(
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Command.Enable = {1}',
            Para1       =  str(self._command.Enable))


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -=1
        # Create log entry for StepMode
        self.CreateLogMessage( 
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Command.StepMode = {1}',
            Para1       =  str(self._command.StepMode)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -=1
        # Create log entry for HoldToRun
        self.CreateLogMessage( 
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Command.HoldToRun = {1}',
            Para1       =  str(self._command.HoldToRun)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -=1
        # Create log entry for ManualStep
        self.CreateLogMessage( 
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Command.ManualStep = {1}',
            Para1       =  str(self._command.ManualStep)
        )


    # --------------------------------------------------------
    # OnExecCancel - IEC execution when cancel requested
    # --------------------------------------------------------    
    def OnExecCancel(self, AxesGroup: AxesGroup) -> int:
        # internal return value
        _retVal : int

        OnExecCancel : int = RUNNING

        match self._stepCancel :
                    
            case 0:
                
                 # set busy flag
                self.Busy = True
                
                # Create log entry
                self.CreateLogMessage( 
                    Timestamp   = AxesGroup.State.SystemTime,
                    MessageType = MessageTypeEnum.CMD,
                    Severity    = SeverityEnum.DEBUG,
                    MessageCode = 0,
                    MessageText = 'Execution of {1} cancelled',
                    Para1       = self.MyType
                )                 
                
                # try to remove cmd
                _retVal = AxesGroup.Acyclic.ActiveCommandRegister.RemoveCmd(self._uniqueID)
            
                # check result of removement       
                if ( _retVal == OK ):

                    # Reset step counter
                    self._stepCancel = 0
                    # finished okay
                    OnExecCancel = OK

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = AxesGroup.State.SystemTime,
                        MessageType = MessageTypeEnum.CMD,
                        Severity    = SeverityEnum.DEBUG,
                        MessageCode = 0,
                        MessageText = '{1} successfully removed from ACR',
                        Para1       = self.MyType
                    )
                else:
                    # set timeout
                    SetTimeout(PT = self._timeoutCancel, Timer = self._timerCancel)
                    # inc step counter
                    self._stepCancel += 1

                    # Create log entry
                    self.CreateLogMessage( 
                        Timestamp   = AxesGroup.State.SystemTime,
                        MessageType = MessageTypeEnum.CMD,
                        Severity    = SeverityEnum.DEBUG,
                        MessageCode = 0,
                        MessageText = '{1} was not removed from ACR because execution was already in progress',
                        Para1       = self.MyType
                    )


            case 1:  # call clear error 
                OnExecCancel = self.OnExecErrorClear(AxesGroup = AxesGroup)
            
                if ( OnExecCancel == OK):
                
                    # Reset busy flag
                    self.Busy = False
                    # Reset step counter
                    self._stepCancel = 0
                    # finished okay
                    OnExecCancel = OK


            case _:
                # invalid step
                self.SetError( ErrorID = RobotErrorIdEnum.ERR_INVALID_STEP, Overwrite = True )


        # reset step counter
        if (OnExecCancel != RUNNING):
        
            # Reset FB variables
            self.Reset()
            # Reset step counter
            self._stepCancel = 0


        return OnExecCancel


    # --------------------------------------------------------
    # OnExecErrorClear - IEC execution when error clear requested
    # --------------------------------------------------------
    def OnExecErrorClear(self, AxesGroup: AxesGroup) -> int:

        OnExecErrorClear : int = RUNNING

        match self._stepClearError :

            case 0:
                # set busy flag
                self.Busy = True
                # trigger parameter update to disable FB
                self._parameterUpdateInternal = True
                # call Check Parameter changed method to trigger the parameter update to disable the function
                self.CheckParameterChanged(AxesGroup = AxesGroup)
                # set timeout
                SetTimeout(PT = self._timeoutClearError, Timer = self._timerClearError)
                # inc step counter
                self._stepClearError += 1

            case 1:
                if (self._responseReceived):
                    # reset response received flag
                    self._responseReceived = False
                    # reset step counter
                    self._stepClearError = 0
                    # finished
                    OnExecErrorClear = OK
                else:
                    # timeout exceeded ? 
                    if (CheckTimeout(self._timerClearError) == OK) :
                    
                        OnExecErrorClear = HAS_ERROR

            case _ :
                # invalid step
                self.SetError( ErrorID = RobotErrorIdEnum.ERR_INVALID_STEP, Overwrite = True )


        # reset step counter
        if (OnExecErrorClear != RUNNING):
        
            # Reset 
            self.Reset()     
            # reset step counter
            self._stepClearError = 0


        return OnExecErrorClear


    # --------------------------------------------------------
    # OnApplyOutCmd - Applying command output
    # --------------------------------------------------------
    def OnApplyOutCmd(self, State: CmdMessageState):
        
        pass


    # --------------------------------------------------------
    # OnExecRun  - executed during execution
    # --------------------------------------------------------
    def OnExecRun(self, AxesGroup: AxesGroup)-> int:

        OnExecRun : int = super().OnExecRun(AxesGroup = AxesGroup)

        match self._stepCmd :
        
            case 0:
                if ( self._enable_R.Q ) and ( not self.Error) :
                
                    # reset the rising edge
                    self._enable_R()

                    # Check function is supported and parameter are valid ?
                    if (( self.CheckFunctionSupported   ( AxesGroup = AxesGroup )) and
                        ( self.CheckParameterValid      ( AxesGroup = AxesGroup )) and
                        ( self.CheckSynchronizationValid( AxesGroup = AxesGroup ))) : 

                        # Reset all internal flags
                        self.Reset()
                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        self.OutCmd = EnableRobotOutCmd()
                        # apply command parameter
                        self._parCmd = copy.deepcopy(self.ParCmd)
                        # init parameter sequence
                        self._command.ParSeq = BYTE(1)
                        # create command data
                        self.CommandData = self.CreateCommandPayload(AxesGroup = AxesGroup)
                        # Add command to active command register
                        self._uniqueID = AxesGroup.Acyclic.ActiveCommandRegister.AddCmd( pCommandFB = self )
                        # set timeout
                        SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                        # inc step counter
                        self._stepCmd += 1


            case 1:  
                
                # Wait for responce received
                if ( self._responseReceived ):

                    # reset response received flag
                    self._responseReceived = False
                    # update state flags
                    self.OnUpdateStateFlags(self._response.State)
                    # update state flags
                    self.OnApplyOutCmd(self._response.State)


                # do not abort directly, so that the ParSeq update can be send
                if ( self._enable_F.Q ):
                    # Set Busy flag
                    self.Busy = True
                    # trigger parameter update to disable FB
                    self._parameterUpdateInternal = True        
                    # reset the falling edge
                    self._enable_F()
                    # set timeout
                    SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                    # inc step counter
                    self._stepCmd += 1


            case 2: 
                # Wait for response received or timeout or not Initialized
                if (
                    ((     self._responseReceived             )  or
                     (     CheckTimeout(self._timerCmd) == OK )) or 
                    (( not AxesGroup.State.Initialized        )  and
                     ( not AxesGroup.State.Synchronized       ))
                   ):
                
                    self.Reset()


            case _:
                # invalid step
                self.SetError( ErrorID = RobotErrorIdEnum.ERR_INVALID_STEP, Overwrite = True )


        # Reset FB
        if (( self._enable_R.Q ) or
            ( self._enable_F.Q )):
        
            self.Reset()

        return OnExecRun


    #--------------------------------------------------------
    # OnUpdateStateFlags - update state flags
    #--------------------------------------------------------
    def OnUpdateStateFlags(self, State: CmdMessageState) -> None:
        """Update state flags from response data"""
        
        # Reset State flags        

        # Update results
        self.Enabled = self._response.Enabled.value

        match State:

            # No operation or process is active
            case CmdMessageState.EMPTY : 
                pass

            # Created but not yet started
            case CmdMessageState.CREATED : 
                pass

            # Buffered and awaiting execution
            case CmdMessageState.BUFFERED : 
                self.CommandBuffered = True
                self.ParameterAccepted  = True

            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER : 
                self.CommandBuffered = True
                self.ParameterAccepted  = True

            # Currently active and in progress
            case CmdMessageState.ACTIVE : 
                if (self.Enabled == self.Enable):
                    self.Busy = False   

            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED :
                pass

            # Requested for abort
            case CmdMessageState.ABORT_REQUEST :
                pass

            # Successfully completed
            case CmdMessageState.DONE : 
                self.Busy = False

            # Aborted before completion
            case CmdMessageState.ABORTED : 
                self.Busy = False

            # Encountered an error during execution
            case CmdMessageState.ERROR :
                self.Error = True
                self.Busy = False


    #--------------------------------------------------------#
    # ParseResponsePayload - parse response payload
    #--------------------------------------------------------#
    def ParseResponsePayload(self, ResponseData : RobotLibraryResponseDataFB, Timestamp: SystemTime) -> int:
               
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
        if ( ResponseData.IsPayloadRemaining):
        
            # Get Response.Enabled
            self._response.Enabled = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt += 1

        # Create logging
        self.ParseResponsePayloadLog(ResponseData = ResponseData, Timestamp = Timestamp, ParameterCnt = _parameterCnt)

        # return updated payload pointer
        return ResponseData.PayloadPtr.value


    #--------------------------------------------------------#
    # ParseResponsePayloadLog - parse response payload log
    #--------------------------------------------------------#
    def ParseResponsePayloadLog(self, ResponseData: RobotLibraryResponseDataFB, Timestamp: SystemTime, ParameterCnt: int) -> None:
        
        # Create log entry for Parameter start
        self.CreateLogMessage( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = '{1} parameter(s) to parse from the response data:',
            Para1       = INT_TO_STRING(ParameterCnt)
        )

        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1

        # Create log entry for Enabled
        self.CreateLogMessage( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.Enabled = {1}',
            Para1       =  BOOL_TO_STRING(self._response.Enabled)
        )


    # --------------------------------------------------------
    # Reset - resets internal variables
    # --------------------------------------------------------
    def Reset(self) -> int:
        
        # call base implementation
        Reset : int = super().Reset()

        self.Done               = False
        self.Busy               = False
        self.Valid              = False
        self.ParameterAccepted  = False
        self.CommandBuffered    = False
        self.CommandAborted     = False
        self.CommandInterrupted = False

        return Reset
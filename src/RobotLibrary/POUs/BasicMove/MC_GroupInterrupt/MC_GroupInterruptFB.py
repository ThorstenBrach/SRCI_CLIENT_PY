"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_GroupInterruptFB
Author:      Thorsten Brach
Date:        2026-01-24

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

from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel
from RobotLibrary.IEC_Standard import SetTimeout
from RobotLibrary.Constants import OK, RUNNING
from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseExecuteFB import RobotLibraryBaseExecuteFB
from RobotLibrary.POUs._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from RobotLibrary.POUs._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode
from RobotLibrary.Enumerations.Type.MessageType import MessageType
from RobotLibrary.Enumerations.Type.MessageType import MessageType as MessageTypeEnum
from RobotLibrary.Enumerations.Type.CmdType import CmdType
from RobotLibrary.Enumerations.Events.ErrorIdEnum import ErrorIdEnum as RobotLibraryErrorIdEnum

from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity as SeverityEnum
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode as ExecutionModeEnum
from RobotLibrary.Enumerations.State.CmdMessageState import CmdMessageState
from RobotLibrary.Structures.AxesGroup.AxesGroup import AxesGroup
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from .Structures.GroupInterruptParCmd import GroupInterruptParCmd
from .Structures.GroupInterruptOutCmd import GroupInterruptOutCmd
from .Structures.GroupInterruptSendData import GroupInterruptSendData 
from .Structures.GroupInterruptRecvData import GroupInterruptRecvData
#endregion 
    
# ------------------------------------------------------------
# Vollständiger Funktionsbaustein
# ------------------------------------------------------------
class MC_GroupInterruptFB(RobotLibraryBaseExecuteFB):
    """
    Python‑Abbildung des IEC‑Funktionsbausteins
    MC_GroupInterruptFB EXTENDS RobotLibraryBaseEnableFB
    """

    # VAR_INPUT
    ParCmd                   : GroupInterruptParCmd
    """Command parameter"""

    # VAR_OUTPUT
    CommandBuffered          : bool
    """Receiving of input parameter values has been acknowledged by RC"""

    Active                   : bool
    """The command takes control of the motion of the according axis group."""
    
    OutCmd                   : GroupInterruptOutCmd 
    """command results"""

    # VAR (lokal)
    _parCmd                  : GroupInterruptParCmd
    """internal copy of command parameter"""
    _command                 : GroupInterruptSendData
    """command data to send"""
    _response                : GroupInterruptRecvData

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
    # CheckAddParameter - check if parameter must be added
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
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.GroupInterrupt.value
        
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
        self._parameterChanged =  ( self._parCmd != self.ParCmd) 
        # Check parameter valid ? 
        self._parameterValid = self.CheckParameterValid(AxesGroup = AxesGroup)

        if (
           (( self._parameterChanged        ) and 
            ( self._parameterValid          )) or
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
                

        # No parameter to check
        return CheckParameterValid


    # --------------------------------------------------------
    # CreateCommandPayload - create command payload
    # --------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup: AxesGroup) -> RobotLibraryCommandDataFB:
        """Create command payload data"""

        # internal parameter counter
        _parameterCnt : int = 0

        #region Mapping table
        
        # Table 6-273: Sent CMD payload (PLC to RC) of "GroupInterrupt"
        # --------------------------
        # Header
        # --------------------------
        # Byte 00 : UINT  - Type HB     
        # Byte 01 :       - Type LB    
        # Byte 02 : USINT - Reserve | ExecutionMode
        # Byte 03 : USINT - ParSeq  | Priority
        # --------------------------
        # endregion



        # update command data
        self._command.CmdTyp            = CmdType.EnableRobot
        self._command.ExecMode          = self. ExecMode
        self._command.ParSeq            = self._command.ParSeq
        self._command.Priority          = self. Priority


        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


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


    # --------------------------------------------------------
    # OnApplyOutCmd - Applying command output
    # --------------------------------------------------------
    def OnApplyOutCmd(self, State: CmdMessageState):
        
        pass


    # --------------------------------------------------------
    # OnExecRun  - executed during execution
    # --------------------------------------------------------
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
                        self.OutCmd = GroupInterruptOutCmd()
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
    def OnUpdateStateFlags(self, State: CmdMessageState) -> None:
        """Update state flags from response data"""
        
        # Reset State flags        
        self.Done = False
        self.Active = False

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

            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER : 
                self.CommandBuffered = True

            # Currently active and in progress
            case CmdMessageState.ACTIVE : 
                 self.Active = True
                 
            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED :
                pass

            # Requested for abort
            case CmdMessageState.ABORT_REQUEST :
                pass

            # Successfully completed
            case CmdMessageState.DONE : 
                self.Done = True
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
            Para1       = str(ParameterCnt)
        )


    # --------------------------------------------------------
    # Reset - resets internal variables
    # --------------------------------------------------------
    def Reset(self) -> int:
        
        # call base implementation
        Reset : int = super().Reset()

        self.Done               = False
        self.Busy               = False
        self.Active             = False
        self.CommandBuffered    = False

        return Reset
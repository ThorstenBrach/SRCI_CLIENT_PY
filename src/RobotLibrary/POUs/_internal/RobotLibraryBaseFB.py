"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotLibraryBaseFB
Author:      Thorsten Brach
Date:        2024-06-01

Description:
  Base function block for robot library commands

Copyright:
    (C) 2024 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from RobotLibrary.Structures.AxesGroup.AxesGroup import AxesGroup

from typing import Any

from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryLogFB import RobotLibraryLogFB
from RobotLibrary.IEC_Types import  WORD, TIME, DWORD, BYTE, UINT, USINT
from RobotLibrary.IEC_Standard import R_TRIG, TON, CONCAT
from RobotLibrary.Functions.ToString import INT_TO_STRING_HEX, MESSAGE_CODE_TO_STRING
from RobotLibrary.Constants import OK
from RobotLibrary.Structures.Common.CmdHeader import CmdHeader
from RobotLibrary.Structures.Common.RspHeader import RspHeader
from RobotLibrary.Enumerations.State.CmdMessageState import CmdMessageState
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode
from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel
from RobotLibrary.Enumerations.Type.MessageType import MessageType as MessageTypeEnum 
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Enumerations.Events.ErrorIdEnum import ErrorIdEnum as RobotErrorIdEnum
from RobotLibrary.Enumerations.Events.WarningIdEnum import WarningIdEnum as RobotWarningIdEnum
from RobotLibrary.Enumerations.Events.InfoIdEnum import InfoIdEnum as RobotInfoIdEnum
from RobotLibrary.POUs._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB
from RobotLibrary.POUs._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB


class RobotLibraryBaseFB(RobotLibraryLogFB):

    """
    Base function block for robot library commands.
    Provides common functionality for command execution, error handling,
    and response processing.
    """
    
    #region VAR_INPUT
    Name: str
    """User defined command name"""
    
    ExecMode: ExecutionMode
    """Execution Mode"""
    
    Priority: PriorityLevel
    """Priority"""
    #endregion
    
    #region VAR_OUTPUT
    CommandData: RobotLibraryCommandDataFB
    """Command data"""
    
    ResponseData: RobotLibraryResponseDataFB
    """Response data"""
    
    Error: bool
    """An error occurred during the execution of the command"""
    
    ErrorID: int
    """ErrorID reported by RC for error identification according to Table 7-1"""
    
    ErrorIdEnum: RobotErrorIdEnum  
    """Error ID as enum"""    
    
    ErrorAddTxt: str
    """Additional error text"""
    
    WarningID: int
    """WarningID for warning identification reported during execution"""
    
    WarningIdEnum: RobotWarningIdEnum  
    """Warning ID as enum"""
    
    InfoID: int
    """InfoID for info identification reported during execution"""
    
    InfoIdEnum: RobotInfoIdEnum 
    """Info ID as enum"""
    
    #endregion
    
    #region VAR 
    _error_R: R_TRIG
    """Rising edge for error"""
    
    _warning_R: R_TRIG
    """Rising edge for warning"""
    
    _info_R: R_TRIG
    """Rising edge for information"""
    
    _clearError: bool
    """Clear error active"""
    
    _cancel: bool
    """Cancel active"""
    
    _uniqueID: int
    """Unique ID"""
    
    _responseReceived: bool
    """Flag for response received"""
    
    _stepCmd: int
    """Internal step counter"""
    
    _timerCmd: TON
    """Internal timer"""
    
    _timeoutCmd: TIME = TIME(5000)
    """Internal timeout in ms"""
    
    _stepClearError: int
    """Internal step counter for ClearError"""
    
    _timerClearError: TON
    """Internal timer for ClearError"""
    
    _timeoutClearError: TIME = TIME(5000)
    """Internal timeout in ms for ClearError"""
    
    _stepCancel: int
    """Internal step counter for Cancel"""
    
    _timerCancel: TON
    """Internal timer for Cancel"""
    
    _timeoutCancel: TIME = TIME(5000)
    """Internal timeout in ms for Cancel"""
    
    _cmdHeader: CmdHeader
    """Internal command header"""
    
    _rspHeader: RspHeader
    """Internal response header"""
    
    _parameterUpdateInternal: bool
    """Internal flag for send a parameter update"""
    
    _parameterChanged: bool
    """Internal flag for parameter has changed"""
    
    _parameterValid: bool
    """Internal flag for parameter are valid"""
        
    #endregion
        
    def __init__(self, **kwargs: Any) -> None:
        """Initialize the base FB"""
        super().__init__(**kwargs)
        # Initialize default timeout values
        # self._timeoutCmd = TIME(5000)  # T#5S = 5000ms
        # self._timeoutClearError = TIME(5000)
        # self._timeoutCancel = TIME(5000)
        
        self._parameterValid = False

        self._error_R   = R_TRIG() # ToDo : should be initialized as new instance within the declaration?
        self._warning_R = R_TRIG() # ToDo : should be initialized as new instance within the declaration?
        self._info_R    = R_TRIG() # ToDo : should be initialized as new instance within the declaration?


    # Main execution methods
    def __call__(self, AxesGroup: AxesGroup) -> None:
        """Main execution - called cyclically like ST implementation"""
        self.OnCall(AxesGroup)
        self.OnExecRun(AxesGroup)
        self.CheckParameterChanged(AxesGroup)
        
        # Check for online change
        if AxesGroup.State.OnlineChange_R.Q:
            self.OnOnlineChange(AxesGroup)


    # --------------------------------------------------------
    # CallBack - called when response is received in (A)ctive (C)ommand (R)egister
    # --------------------------------------------------------
    def CallBack(self, RspData: Any, Timestamp: Any) -> int:        
        """Callback when response is received"""
        
        # Create log entry
        self.CreateLogMessage(
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = DWORD(0),
            MessageText = 'Callback received in FB {1} <{2}>',
            Para1       = str(self.MyType), 
            Para2       = str(self.Name)
         )
        
        # Reset and populate response data
        self.ResponseData.Reset()
        self.ResponseData.Payload = RspData.Payload
        self.ResponseData.PayloadLen = RspData.PayloadLen
        self.ParseResponsePayload(self.ResponseData, Timestamp)
        
        # Set flag for response received
        self._responseReceived = True
        return 0


    # --------------------------------------------------------------
    # CheckFunctionSupported - must be overridden in derived classes
    # ---------------------------------------------------------------
    def CheckFunctionSupported(self, AxesGroup: AxesGroup) -> bool:
        """Check if function is supported by robot controller"""
        
        self.Error = True
        self.ErrorID = RobotErrorIdEnum.ERR_FUNCTION_NOT_SUPPORTED
        self.ErrorAddTxt   = f"{self._myType} {self.Name}"
        
        # Create log entry
        self.CreateLogMessage(
             Timestamp   = AxesGroup.State.SystemTime,
             MessageType = MessageTypeEnum.CMD,
             Severity    = Severity.DEBUG,
             MessageCode = DWORD(0),
             MessageText = str(f'Execution canceled, function <{self._myType}> not supported'),
             Para1       = str(self._myType)
        )
        return False


    # --------------------------------------------------------------
    # CheckFunctionSupported - must be overridden in derived classes
    # ---------------------------------------------------------------
    def CheckParameterChanged(self, AxesGroup: AxesGroup) -> bool:
        """Check if parameters have changed - base implementation must be called in derived classes"""
                
        if self._parameterChanged:
            AxesGroup.Acyclic.ActiveCommandRegister.NotifyParameterChanged = self._uniqueID

        return self._parameterChanged


    # --------------------------------------------------------------
    # CheckFunctionSupported - must be overridden in derived classes
    # ---------------------------------------------------------------
    def CheckParameterValid(self, AxesGroup: AxesGroup) -> bool:
        """Check if parameters are valid - override in derived classes"""
        return True


    # --------------------------------------------------------------
    # CreateCommandPayload - must be overridden in derived classes
    # ---------------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup: AxesGroup) -> Any:
        """Create command payload - override in derived classes - base implementation must be called in derived classes"""
        # Reset all variables
        self.CommandData.Reset()
        # Add CmdType
        self.CommandData.AddUint( self._cmdHeader.CmdTyp.TypeValue)
        # Add Reserve_ExecMode
        self.CommandData.AddHalfBytes(BYTE(0), self._cmdHeader.ExecMode.TypeValue)
        # Add ParSeq_Priority
        self.CommandData.AddHalfBytes(self._cmdHeader.ParSeq, self._cmdHeader.Priority.TypeValue)
        # Return command data
        return self.CommandData


    # --------------------------------------------------------------
    # HasError - Check if error is present
    # ---------------------------------------------------------------
    @property
    def HasError(self) -> bool:
        """Check if error is present"""
        return bool(self.ErrorID != RobotErrorIdEnum.NO_ERROR)


    # --------------------------------------------------------------
    # HasWarning - Check if warning is present
    # ---------------------------------------------------------------
    @property
    def HasWarning(self) -> bool:
        """Check if warning is present"""
        return bool(self.WarningID != RobotWarningIdEnum.NO_WARNING)


    # --------------------------------------------------------------
    # HasInfo - Check if info is present
    # ---------------------------------------------------------------
    @property
    def HasInfo(self) -> bool:
        """Check if info is present"""
        return bool(self.InfoID != RobotInfoIdEnum.NO_INFO)


    # --------------------------------------------------------------
    # OnApplyOutCmd - must be overridden in derived classes
    # ---------------------------------------------------------------
    def OnApplyOutCmd(self, State: CmdMessageState) -> None:
        """Hook called when applying output command"""
        pass


    # --------------------------------------------------------------
    # OnCall - called on each cycle
    # ---------------------------------------------------------------
    def OnCall(self, AxesGroup: AxesGroup) -> None:
        """Called on each cycle"""
        # Map numeric value to enum for tooltip display
        self.ErrorIdEnum.value = self.ErrorID # type: ignore
        self.WarningIdEnum.value = self.WarningID # type: ignore
        self.InfoIdEnum.value = self.InfoID # type: ignore
        
        self.Error = self.ErrorID != OK 
        
        # Setup logging
        self.InternalLogger = AxesGroup.MessageLog
        self.ExternalLogger = AxesGroup.MessageLog.ExternalLogger
        self.LogLevel = AxesGroup.MessageLog.LogLevel
        
        # Build rising edges for error, warning, info detection
        self.  _error_R(CLK=self.ErrorID   != OK)
        self._warning_R(CLK=self.WarningID != OK)
        self.   _info_R(CLK=self.InfoID    != OK)
        
        # Log events if configured
    
        # Log Command events to message log 
        if (( self.LogLevel < self._rspHeader.AlarmMessageSeverity ) and
           (( self._error_R  .Q                                    ) or 
            ( self._warning_R.Q                                    ) or 
            ( self._info_R   .Q                                    ))
           ):
        
            # Add command message to message buffer       
            AxesGroup.MessageLog.AddMessageLogByParameter( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageTypeEnum.CMD,
                MessageCode = self._rspHeader.AlarmMessageCode,
                MessageText = CONCAT(self.MyType, CONCAT(' : ' , MESSAGE_CODE_TO_STRING(self._rspHeader.AlarmMessageCode.value))),
                Severity    = self._rspHeader.AlarmMessageSeverity 
            )


        if ( self._error_R.Q):
            # Create log entry
            self.CreateLogMessage(
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageTypeEnum.CMD,
                Severity    = Severity.DEBUG,
                MessageCode = 0,
                MessageText = 'Error with ID: 16#{1} in FB {2} received ',
                Para1       = INT_TO_STRING_HEX(self.ErrorID),
                Para2       = self.MyType
            )


        if ( self._warning_R.Q):
            # Create log entry
            self.CreateLogMessage(
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageTypeEnum.CMD,
                Severity    = Severity.DEBUG,
                MessageCode = 0,
                MessageText = 'Warning with ID: 16#{1} in FB {2} received ',
                Para1       = INT_TO_STRING_HEX(self.WarningID),
                Para2       = self.MyType
            )


        if ( self._info_R.Q) :
            # Create log entry
            self.CreateLogMessage(
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageTypeEnum.CMD,
                Severity    = Severity.DEBUG,
                MessageCode = 0,
                MessageText = 'Info with ID: 16#{1} in FB {2} received ',
                Para1       = INT_TO_STRING_HEX(self.InfoID),
                Para2       = self.MyType
            )


    # --------------------------------------------------------------
    # OnExecRun - execute run - must be overridden in derived classes
    # ---------------------------------------------------------------
    def OnExecRun(self, AxesGroup: AxesGroup) -> int:
        """Execute run - override in derived classes"""
        return 0


    # --------------------------------------------------------------
    # OnOnlineChange - handle online change event
    # ---------------------------------------------------------------
    def OnOnlineChange(self, AxesGroup: AxesGroup) -> int:
        """Handle online change event"""
        
        #ToDo : implementation needed? We do not have online changes in Python
        # Update pointer to command FB
        #    AxesGroup.Acyclic.ActiveCommandRegister.OnOnlineChange(
        #         UniqueID=self._uniqueID,
        #         pCommandFB=id(self)  # Python object id as pointer substitute
            
        return 0


    # --------------------------------------------------------------
    # OnUpdateStateFlags - must be overridden in derived classes
    # ---------------------------------------------------------------
    def OnUpdateStateFlags(self, State: CmdMessageState) -> None:
        """Hook called when updating state flags"""
        pass 


    # --------------------------------------------------------------
    # ParseResponsePayload - parse response payload header - must be overridden in derived classes
    # ---------------------------------------------------------------
    def ParseResponsePayload(self, ResponseData : RobotLibraryResponseDataFB, Timestamp: Any) -> int:
        """Parse response payload"""
        # Reset message IDs
        self.InfoID = 0 
        self.WarningID = 0 
        self.ErrorID = 0 
        
        # Get State
        self._rspHeader.State = CmdMessageState(ResponseData.GetHalfeByte1(IncPayloadPtr=False).value)
        # Get ParSeq
        self._rspHeader.ParSeq = USINT(ResponseData.GetHalfeByte2(IncPayloadPtr=True).value) 
        # Get AlarmMessageSeverity
        self._rspHeader.AlarmMessageSeverity = Severity(ResponseData.GetSint().value) 
        # Get AlarmMessageCode
        self._rspHeader.AlarmMessageCode = ResponseData.GetUint() 
        
        # Update InfoID / WarningID / ErrorID based on severity         
        match self._rspHeader.AlarmMessageSeverity:

            case Severity.INFO:
                self.SetInfo(InfoID = self._rspHeader.AlarmMessageCode.value, Overwrite=True)

            case Severity.WARNING:
                self.SetWarning(WarningID = self._rspHeader.AlarmMessageCode.value, Overwrite=True)

            case Severity.ERROR:
                self.SetError(ErrorID = self._rspHeader.AlarmMessageCode.value, Overwrite=True)

            case Severity.FATAL_ERROR:
                self.SetError(ErrorID = self._rspHeader.AlarmMessageCode.value, Overwrite=True)

        # return current payload pointer
        return ResponseData.PayloadPtr.value


    # --------------------------------------------------------------
    # Reset - reset internal variables
    # ---------------------------------------------------------------
    def Reset(self) -> int:
        """Reset function block"""
        self._parameterUpdateInternal = False 
        self._responseReceived = False 
        self._uniqueID = 0 
        self._stepCmd = 0
        self.Error = False
        self.ErrorID = 0 
        self.WarningID = 0 
        self.InfoID = 0 
        return OK 


    # --------------------------------------------------------------
    # SetError - set error ID
    # ---------------------------------------------------------------
    def SetError(self, ErrorID: int | UINT | WORD, Overwrite: bool = False) -> None:
        """Set error ID"""
        if not self.HasError or Overwrite:
            
            if (isinstance(ErrorID, int)):
                self.ErrorID = ErrorID 
                        
            if (isinstance(ErrorID, UINT)):
                self.ErrorID = ErrorID.value

            if (isinstance(ErrorID, WORD)):
                self.ErrorID = ErrorID.value


    # --------------------------------------------------------------
    # SetWarning - set warning ID
    # ---------------------------------------------------------------
    def SetWarning(self, WarningID: int | UINT | WORD, Overwrite: bool = False) -> None:
        """Set warning ID"""
        if not self.HasWarning or Overwrite:
            
            if (isinstance(WarningID, int)):
                self.WarningID = WarningID 
                        
            if (isinstance(WarningID, UINT)):
                self.WarningID = WarningID.value 

            if (isinstance(WarningID, WORD)):
                self.WarningID = WarningID.value


    # --------------------------------------------------------------
    # SetInfo - set info ID
    # ---------------------------------------------------------------
    def SetInfo(self, InfoID: int | UINT | WORD, Overwrite: bool = False) -> None:
        """Set info ID"""
        if not self.HasInfo or Overwrite:
            
            if (isinstance(InfoID, int)):
                self.InfoID = InfoID 
                        
            if (isinstance(InfoID, UINT)):
                self.InfoID = InfoID.value 

            if (isinstance(InfoID, WORD)):
                self.InfoID = InfoID.value
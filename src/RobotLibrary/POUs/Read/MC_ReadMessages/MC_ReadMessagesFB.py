"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_ReadRobotDataFB
Author:      Thorsten Brach
Date:        2026-01-11

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

from RobotLibrary.Functions.Convert import IEC_DATE_TO_STRING, IEC_TIME_TO_STRING, IEC_TIMESTAMP_TO_SYSTEMTIME
from RobotLibrary.IEC_Standard import SetTimeout, CheckTimeout
from RobotLibrary.Constants import RUNNING, OK, HAS_ERROR
from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Enumerations.State import CmdMessageState
from RobotLibrary.Enumerations.Type.MessageType import MessageType
from RobotLibrary.Enumerations.Events.ErrorIdEnum import ErrorIdEnum as RobotLibraryErrorIdEnum
from RobotLibrary.Enumerations.Level.MessageLevel  import MessageLevel
from RobotLibrary.Enumerations.Type.CmdType import CmdType

from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseEnableFB import RobotLibraryBaseEnableFB
from RobotLibrary.POUs._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from RobotLibrary.POUs._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB

from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from RobotLibrary.Structures.AxesGroup.AxesGroup import AxesGroup

from .Structures.ReadMessagesParCmd import ReadMessagesParCmd
from .Structures.ReadMessagesOutCmd import ReadMessagesOutCmd
from .Structures.ReadMessagesSendData import ReadMessagesSendData
from .Structures.ReadMessagesRecvData import ReadMessagesRecvData

#endregion

class MC_ReadMessagesFB( RobotLibraryBaseEnableFB):
    """Function block to read messages from the robot controller."""
    
    #region VAR_INPUT
    ParCmd : ReadMessagesParCmd
    """command parameter"""
    #endregion
    
    #region VAR_OUTPUT
    Valid : bool    
    """
    TRUE, while the following outputs return valid values:
     • Values
     """
     
    CommandBuffered : bool
    """ Command is transferred and confirmed by the RC"""

    OutCmd : ReadMessagesOutCmd
    """command outputs"""
    #endregion
    
    #region VAR
    _parCmd             : ReadMessagesParCmd
    """internal copy of command parameter"""
    _command            : ReadMessagesSendData
    """command data to send"""
    _response           : ReadMessagesRecvData
    """response data received"""

    #endregion
    
    
    #------------------------------------------------------------
    # Initialization of Function Block
    #------------------------------------------------------------
    def __init__(self):
        
        super().__init__()
        
        self.MyType   = self.__class__.__name__
        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL

        # Initialize VAR_INPUT
        self.ParCmd = ReadMessagesParCmd()

        # Initialize VAR_OUTPUT
        self.Valid = False
        self.CommandBuffered = False
        self.OutCmd = ReadMessagesOutCmd()

        # Initialize VAR
        self._parCmd   = ReadMessagesParCmd()
        self._command  = ReadMessagesSendData()
        self._response = ReadMessagesRecvData()






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
        CheckFunctionSupported : bool = True # Function is mandatory 

        return CheckFunctionSupported

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ReadMessages.value

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

        return self._parameterChanged 
    
    #--------------------------------------------------------
    # CheckParameterValid - check if parameter is valid
    #--------------------------------------------------------
    def CheckParameterValid(self, AxesGroup : AxesGroup) -> bool:
        """
        Check if the input parameters are valid
        """
        CheckParameterValid : bool = True

        # Check ParCmd.MsgID valid ? 
        if (( self.ParCmd.MsgID <   0 ) or
            ( self.ParCmd.MsgID > 255 )) :
            
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
                MessageText = 'Invalid Parameter ParCmd.MsgID = {1}',
                Para1       =  str(self.ParCmd.MsgID)
            )
            return CheckParameterValid


        # Check ParCmd.MessageLevel valid ? 
        if (( self.ParCmd.MessageLevel != MessageLevel.DEBUG   ) and 
            ( self.ParCmd.MessageLevel != MessageLevel.INFO    ) and
            ( self.ParCmd.MessageLevel != MessageLevel.WARNING ) and
            ( self.ParCmd.MessageLevel != MessageLevel.ERROR   )):
            
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
                MessageText = 'Invalid Parameter ParCmd.MessageLevel = {1}',
                Para1       =  self.ParCmd.MessageLevel.toString()
            )
            
        return CheckParameterValid



    #--------------------------------------------------------
    # CreateCommandPayload - create command payload
    #--------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup : AxesGroup) -> RobotLibraryCommandDataFB:
        
        # Parameter count
        _parameterCnt : int = 0

        # region Mapping table
        
        # Table 6-107: Sent CMD payload (PLC to RC) of "ReadMessages"
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
        # Byte 04 : USINT  MsgID;
        # Byte 05 : BOOL   Enable;
        # Byte 06 : USINT  MessageLevel;
        # --------------------------
        #endregion

        # set command parameter 
        self._command.CmdTyp       = CmdType.ReadMessages
        self._command.ExecMode     = self. ExecMode
        self._command.ParSeq       = self._command.ParSeq
        self._command.Priority     = self. Priority
        self._command.MsgID.value  = self._parCmd.MsgID
        self._command.Enable.value = self.Enable
        self._command.MessageLevel = self._parCmd.MessageLevel.TypeValue


        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.MsgID
            self.CommandData.AddUsint(self._command.MsgID)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.Enable
            self.CommandData.AddBool(self._command.Enable)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.MessageLevel
            self.CommandData.AddUsint(self._command.MessageLevel)
            # inc parameter counter
            _parameterCnt += 1

        # Create logging
        self.CreateCommandPayloadLog(AxesGroup = AxesGroup, ParameterCnt = _parameterCnt)

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
            MessageText = 'Command.MsgID = {1}',
            Para1       =  str(self._command.MsgID)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Enable
        self.CreateLogMessage (
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Command.Enable = {1}',
            Para1       =  str(self._command.Enable)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for MessageLevel
        self.CreateLogMessage (
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Command.MessageLevel = {1}',
            Para1       = str(self._command.MessageLevel)
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
            self.OutCmd = ReadMessagesOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :

            # Update results
            self.OutCmd.MsgId                  =             self._response.MsgId.value
            self.OutCmd.NumberOfActiveErrors   =             self._response.NumberOfActiveErrors.value
            self.OutCmd.NumberOfActiveWarnings =             self._response.NumberOfActiveWarnings.value
            self.OutCmd.Timestamp              =             self._response.Timestamp
            self.OutCmd.MsgType                = MessageType(self._response.MsgType.value)
            self.OutCmd.Severity               = Severity   (self._response.Severity.value)
            self.OutCmd.ErrorCode              =             self._response.ErrorCode.value
            self.OutCmd.Text                   =             self._response.Text.toString()


    #--------------------------------------------------------
    # OnExecCancel - executed when command is cancelled
    #--------------------------------------------------------
    def OnExecCancel(self, AxesGroup : AxesGroup) -> int:
        """
        Executed when the command is cancelled
        """

        # internal return value 
        _retVal : int = 0

        OnExecCancel : int = RUNNING

        match self._stepCancel :

            case 0:
                
                # set busy flag
                self.Busy = True
                
                # Create log entry
                self.CreateLogMessage ( 
                    Timestamp   = AxesGroup.State.SystemTime,
                    MessageType = MessageType.CMD,
                    Severity    = Severity.DEBUG,
                    MessageCode = 0,
                    MessageText = 'Execution of {1} cancelled',
                    Para1       = self.MyType
                )

                # try to remove cmd
                _retVal = AxesGroup.Acyclic.ActiveCommandRegister.RemoveCmd(self._uniqueID)

                # check result of removement       
                if ( _retVal ==  OK ):

                    # Reset step counter
                    self._stepCancel = 0
                    # finished okay
                    OnExecCancel = OK
                    
                    # Create log entry
                    self.CreateLogMessage ( 
                        Timestamp   = AxesGroup.State.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
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
                    self.CreateLogMessage ( 
                        Timestamp   = AxesGroup.State.SystemTime,
                        MessageType = MessageType.CMD,
                        Severity    = Severity.DEBUG,
                        MessageCode = 0,
                        MessageText = '{1} was not removed from ACR because execution was already in progress',
                        Para1       = self.MyType)


            case 1 :
                # call clear error 
                OnExecCancel = self.OnExecErrorClear(AxesGroup = AxesGroup)  

                if ( OnExecCancel == OK) : 
                
                    # Reset busy flag
                    self.Busy = False
                    # Reset step counter
                    self._stepCancel = 0
                    # finished okay
                    OnExecCancel = OK


            case _:
                # invalid step
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite = True )


        # reset step counter
        if (OnExecCancel != RUNNING) :
            # Reset FB variables
            self.Reset()
            # Reset step counter
            self._stepCancel = 0

        return OnExecCancel


    #--------------------------------------------------------
    # OnExecErrorClear - executed when an error is cleared
    #--------------------------------------------------------
    def OnExecErrorClear(self, AxesGroup : AxesGroup) -> int:
        """
        Executed when an error is cleared
        """

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
                if ( self._responseReceived ):
                
                    # reset response received flag
                    self._responseReceived = False
                    # reset step counter
                    self._stepClearError = 0
                    # finished
                    OnExecErrorClear = OK
                else:
                    # timeout exceeded ? 
                    if (CheckTimeout(self._timerClearError) == OK):
                        
                        OnExecErrorClear = HAS_ERROR

            case _:
                # invalid step
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite = True )


        # reset step counter
        if (OnExecErrorClear != RUNNING):
            # Reset 
            self.Reset()     
            # reset step counter
            self._stepClearError = 0

        return OnExecErrorClear
    
    
    #--------------------------------------------------------
    # OnExecRun  - executed during execution
    #--------------------------------------------------------
    def OnExecRun(self, AxesGroup : AxesGroup) -> int:
        """
        Executed during cyclic execution
        """
        
        #    internal index for loops
        _idx : int = 0


        OnExecRun : int = super().OnExecRun(AxesGroup = AxesGroup)


        match self._stepCmd :

            case 0:
                if ( self._enable_R.Q ) and ( not self.Error) :
                
                    # reset the rising edge
                    self._enable_R()
                    
                    # Check function is supported and parameter are valid ?
                    if (( self.CheckFunctionSupported( AxesGroup = AxesGroup )) and
                        ( self.CheckParameterValid   ( AxesGroup = AxesGroup ))) : 

                        # Reset all internal flags
                        self.Reset()
                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        self.OutCmd = ReadMessagesOutCmd()
                        # apply command parameter
                        self._parCmd = copy.deepcopy(self.ParCmd)
                        # init parameter sequence
                        self._command.ParSeq.value = 1
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

                    if ( self.Valid ):
                    
                        # Add message to message buffer       
                        AxesGroup.MessageLog.AddMessageLogByParameter(
                            Timestamp   = IEC_TIMESTAMP_TO_SYSTEMTIME(self.OutCmd.Timestamp),
                            MessageType =                             self.OutCmd.MsgType,
                            MessageCode =                             self.OutCmd.ErrorCode,
                            MessageText =                             self.OutCmd.Text,
                            Severity    =                             self.OutCmd.Severity
                        )

                # do not abort directly, so that the ParSeq update can be send
                if ( self._enable_F.Q ) :
                
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
                if ((( self._responseReceived                  )  or 
                     (      CheckTimeout(self._timerCmd) == OK )) or 
                    (( not AxesGroup.State.Initialized         )  and
                     ( not AxesGroup.State.Synchronized        ))) :

                    self.Reset()

            case _:
                # invalid step
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite = True )


        # Reset FB
        if (( self._enable_R.Q ) or
            ( self._enable_F.Q )):

            self.Reset()

        #return result
        return OnExecRun
    
    
    #--------------------------------------------------------
    # OnUpdateStateFlags - update state flags
    #--------------------------------------------------------
    def OnUpdateStateFlags(self, State : CmdMessageState) -> None:
        """
        Update state flags according to received state
        """

        # Reset State flags
        self.Valid = False

        # Update results
        self.Enabled = self._response.Enabled.value

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

            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER : 
                self.CommandBuffered    = True

            # Currently active and in progress
            case CmdMessageState.ACTIVE: 
                self.Valid = True

            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED:
                pass

            # Requested for abort
            case CmdMessageState.ABORT_REQUEST:
                pass

            # Successfully completed
            case CmdMessageState.DONE : 
                self.Busy = False

            # Aborted before completion
            case CmdMessageState.ABORTED:
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

        # Table 6-108: Received CMD payload (RC to PLC) of "ReadMessages"
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
        # Byte 04 : USINT       MsgID;
        # Byte 05 : BOOL        Enabled;
        # Byte 06 : USINT       NumberOfActiveErrors;
        # Byte 07 : USINT       NumberOfActiveWarnings;
        # Byte 08 : DATE        Date HW HB;
        # Byte 09 :             Date HW LB;
        # Byte 10 : TIME_OF_DAY Time HW HB;
        # Byte 11 :             Time HW LB;
        # Byte 12 :             Time LW HB;
        # Byte 13 :             Time LW LB;
        # Byte 14 : USINT       MsgType;
        # Byte 15 : SINT        Severity;
        # Byte 16 : DWORD       ErrorCode HW HB;
        # Byte 17 :             ErrorCode HW LB;
        # Byte 18 :             ErrorCode LW HB;
        # Byte 19 :             ErrorCode LW LB;
        # Byte 20 : CHAR        Text[0];
        # Byte 21 : CHAR        Text[1];
        # Byte 22 : CHAR        Text[2];
        # Byte 23 : CHAR        Text[3];
        # Byte 24 : CHAR        Text[4];
        # Byte 25 : CHAR        Text[5];
        # Byte 26 : CHAR        Text[6];
        # Byte 27 : CHAR        Text[7];
        # Byte 28 : CHAR        Text[8];
        # Byte 29 : CHAR        Text[9];
        # Byte 30 : CHAR        Text[10];
        # Byte 31 : CHAR        Text[11];
        # Byte 32 : CHAR        Text[12];
        # Byte 33 : CHAR        Text[13];
        # Byte 34 : CHAR        Text[14];
        # Byte 35 : CHAR        Text[15];
        # Byte 36 : CHAR        Text[16];
        # Byte 37 : CHAR        Text[17];
        # Byte 38 : CHAR        Text[18];
        # Byte 39 : CHAR        Text[19];
        # Byte 40 : CHAR        Text[20];
        # Byte 41 : CHAR        Text[21];
        # Byte 42 : CHAR        Text[22];
        # Byte 43 : CHAR        Text[23];
        # Byte 44 : CHAR        Text[24];
        # Byte 45 : CHAR        Text[25];
        # Byte 46 : CHAR        Text[26];
        # Byte 47 : CHAR        Text[27];
        # Byte 48 : CHAR        Text[28];
        # Byte 49 : CHAR        Text[29];
        # Byte 50 : CHAR        Text[30];
        # Byte 51 : CHAR        Text[31];
        # Byte 52 : CHAR        Text[32];
        # Byte 53 : CHAR        Text[33];
        # Byte 54 : CHAR        Text[34];
        # Byte 55 : CHAR        Text[35];
        # Byte 56 : CHAR        Text[36];
        # Byte 57 : CHAR        Text[37];
        # Byte 58 : CHAR        Text[38];
        # Byte 59 : CHAR        Text[39];
        # Byte 60 : CHAR        Text[40];
        # Byte 61 : CHAR        Text[41];
        # Byte 62 : CHAR        Text[42];
        # Byte 63 : CHAR        Text[43];
        # Byte 64 : CHAR        Text[44];
        # Byte 65 : CHAR        Text[45];
        # Byte 66 : CHAR        Text[46];
        # Byte 67 : CHAR        Text[47];
        # Byte 68 : CHAR        Text[48];
        # Byte 69 : CHAR        Text[49];
        # Byte 70 : CHAR        Text[50];
        # Byte 71 : CHAR        Text[51];
        # Byte 72 : CHAR        Text[52];
        # Byte 73 : CHAR        Text[53];
        # Byte 74 : CHAR        Text[54];
        # Byte 75 : CHAR        Text[55];
        # Byte 76 : CHAR        Text[56];
        # Byte 77 : CHAR        Text[57];
        # Byte 78 : CHAR        Text[58];
        # Byte 79 : CHAR        Text[59];
        # Byte 80 : CHAR        Text[60];
        # Byte 81 : CHAR        Text[61];
        # Byte 82 : CHAR        Text[62];
        # Byte 83 : CHAR        Text[63];
        # Byte 84 : CHAR        Text[64];
        # Byte 85 : CHAR        Text[65];
        # Byte 86 : CHAR        Text[66];
        # Byte 87 : CHAR        Text[67];
        # Byte 88 : CHAR        Text[68];
        # Byte 89 : CHAR        Text[69];
        # Byte 90 : CHAR        Text[70];
        # Byte 91 : CHAR        Text[71];
        # Byte 92 : CHAR        Text[72];
        # Byte 93 : CHAR        Text[73];
        # Byte 94 : CHAR        Text[74];
        # Byte 95 : CHAR        Text[75];
        # Byte 96 : CHAR        Text[76];
        # Byte 97 : CHAR        Text[77];
        # Byte 98 : CHAR        Text[78];
        # Byte 99 : CHAR        Text[79];
        # Byte 100: CHAR        Text[80];
        # Byte 101: CHAR        Text[81];
        # Byte 102: CHAR        Text[82];
        # Byte 103: CHAR        Text[83];
        # Byte 104: CHAR        Text[84];
        # Byte 105: CHAR        Text[85];
        # Byte 106: CHAR        Text[86];
        # Byte 107: CHAR        Text[87];
        # Byte 108: CHAR        Text[88];
        # Byte 109: CHAR        Text[89];
        # Byte 110: CHAR        Text[90];
        # Byte 111: CHAR        Text[91];
        # Byte 112: CHAR        Text[92];
        # Byte 113: CHAR        Text[93];
        # Byte 114: CHAR        Text[94];
        # Byte 115: CHAR        Text[95];
        # Byte 116: CHAR        Text[96];
        # Byte 117: CHAR        Text[97];
        # Byte 118: CHAR        Text[98];
        # Byte 119: CHAR        Text[99];
        # Byte 120: CHAR        Text[100];
        # Byte 121: CHAR        Text[101];
        # Byte 122: CHAR        Text[102];
        # Byte 123: CHAR        Text[103];
        # Byte 124: CHAR        Text[104];
        # Byte 125: CHAR        Text[105];
        # Byte 126: CHAR        Text[106];
        # Byte 127: CHAR        Text[107];
        # Byte 128: CHAR        Text[108];
        # Byte 129: CHAR        Text[109];
        # Byte 130: CHAR        Text[110];
        # Byte 131: CHAR        Text[111];
        # Byte 132: CHAR        Text[112];
        # Byte 133: CHAR        Text[113];
        # Byte 134: CHAR        Text[114];
        # Byte 135: CHAR        Text[115];
        # Byte 136: CHAR        Text[116];
        # Byte 137: CHAR        Text[117];
        # Byte 138: CHAR        Text[118];
        # Byte 139: CHAR        Text[119];
        # Byte 140: CHAR        Text[120];
        # Byte 141: CHAR        Text[121];
        # Byte 142: CHAR        Text[122];
        # Byte 143: CHAR        Text[123];
        # Byte 144: CHAR        Text[124];
        # Byte 145: CHAR        Text[125];
        # Byte 146: CHAR        Text[126];
        # Byte 147: CHAR        Text[127];
        # Byte 148: CHAR        Text[128];
        # Byte 149: CHAR        Text[129];
        # Byte 150: CHAR        Text[130];
        # Byte 151: CHAR        Text[131];
        # Byte 152: CHAR        Text[132];
        # Byte 153: CHAR        Text[133];
        # Byte 154: CHAR        Text[134];
        # Byte 155: CHAR        Text[135];
        # Byte 156: CHAR        Text[136];
        # Byte 157: CHAR        Text[137];
        # Byte 158: CHAR        Text[138];
        # Byte 159: CHAR        Text[139];
        # Byte 160: CHAR        Text[140];
        # Byte 161: CHAR        Text[141];
        # Byte 162: CHAR        Text[142];
        # Byte 163: CHAR        Text[143];
        # Byte 164: CHAR        Text[144];
        # Byte 165: CHAR        Text[145];
        # Byte 166: CHAR        Text[146];
        # Byte 167: CHAR        Text[147];
        # Byte 168: CHAR        Text[148];
        # Byte 169: CHAR        Text[149];
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
            # Get Response.MsgID
            self._response.MsgID = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Enabled
            self._response.Enabled = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.NumberOfActiveErrors
            self._response.NumberOfActiveErrors = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.NumberOfActiveWarnings
            self._response.NumberOfActiveWarnings = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Timestamp.IEC_DATE
            self._response.Timestamp.IEC_DATE = ResponseData.GetIecDate()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Timestamp.IEC_TIME
            self._response.Timestamp.IEC_TIME = ResponseData.GetIecTime()
            # inc parameter counter
            _parameterCnt += 1

        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.MsgType
            self._response.MsgType = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Severity
            self._response.Severity = ResponseData.GetSint()
            # inc parameter counter
            _parameterCnt += 1
        
        
        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.ErrorCode
            self._response.ErrorCode = ResponseData.GetDword()
            # inc parameter counter
            _parameterCnt += 1

        
        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.Text
            self._response.Text.fromBytes( ResponseData.GetDataBlock(Size = self._response.Text.Size, IsString = True))

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
            MessageText = 'Response.Enabled = {1}',
            Para1       =  str(self._response.Enabled)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for MsgID
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.MsgId = {1}',
            Para1       =  str(self._response.MsgId)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for NumberOfActiveErrors
        self.CreateLogMessage (
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.NumberOfActiveErrors = {1}',
            Para1       =  str(self._response.NumberOfActiveErrors)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for NumberOfActiveWarnings
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.NumberOfActiveWarnings = {1}',
            Para1       = str(self._response.NumberOfActiveWarnings)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Timestamp.IEC_DATE
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.Timestamp.IEC_DATE = {1}',
            Para1       =  IEC_DATE_TO_STRING(self._response.Timestamp.IEC_DATE)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Timestamp.IEC_TIME
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.Timestamp.IEC_TIME = {1}',
            Para1       =  IEC_TIME_TO_STRING(self._response.Timestamp.IEC_TIME)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for MsgType
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.MsgType = {1}',
            Para1       = MessageType(self._response.MsgType.value).toString()
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Severity
        self.CreateLogMessage( 
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.Severity = {1}',
            Para1       =  self._response.Severity.toString()
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for ErrorCode
        self.CreateLogMessage( 
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.ErrorCode = {1}',
            Para1       =  str(self._response.ErrorCode)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return #noqa
        # dec remaining parameter(s)
        ParameterCnt -= 1
        # Create log entry for Text
        self.CreateLogMessage( 
            Timestamp   = Timestamp,
            MessageType = MessageType.CMD,
            Severity    = Severity.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.Text = {1}',
            Para1       =  str(self._response.Text)
        )


    #--------------------------------------------------------
    # Reset - reset internal variables
    #--------------------------------------------------------
    def Reset(self) -> int:
        """ Reset internal variables """

        self.Busy               = False
        self.Valid              = False
        self.CommandBuffered    = False

        return super().Reset()
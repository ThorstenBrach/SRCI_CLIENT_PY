"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_ReadRobotDataFB
Author:      Thorsten Brach
Date:        2026-01-05

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

from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel
from RobotLibrary.Functions.ToString import INT_TO_STRING, BYTE_TO_STRING_BIN
from RobotLibrary.Functions.Convert import ByteToAxisJointUsed, ByteToAxisExternalUsed, ByteToAxisJointUnit, ByteToAxisExternalUnit, BytesToRCSupportedFunctions
from RobotLibrary.IEC_Types import BOOL, BYTE
from RobotLibrary.IEC_Standard import SetTimeout,CONCAT
from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseExecuteFB import RobotLibraryBaseExecuteFB
from RobotLibrary.POUs._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from RobotLibrary.POUs._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB
from RobotLibrary.Enumerations.Type.MessageType import MessageType as MessageTypeEnum
from RobotLibrary.Enumerations.Type.CmdType import CmdType
from RobotLibrary.Enumerations.Events.ErrorIdEnum import ErrorIdEnum as RobotErrorIdEnum
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity as SeverityEnum
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode as ExecutionModeEnum
from RobotLibrary.Enumerations.State.CmdMessageState import CmdMessageState
from RobotLibrary.Structures.AxesGroup.AxesGroup import AxesGroup
from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from .Structures.ReadRobotDataParCmd import ReadRobotDataParCmd
from .Structures.ReadRobotDataOutCmd import ReadRobotDataOutCmd
from .Structures.ReadRobotDataSendData import ReadRobotDataSendData 
from .Structures.ReadRobotDataRecvData import ReadRobotDataRecvData

import copy
#endregion

# ------------------------------------------------------------
# Vollständiger Funktionsbaustein
# ------------------------------------------------------------
class MC_ReadRobotDataFB(RobotLibraryBaseExecuteFB):
    """
    Python‑Abbildung des IEC‑Funktionsbausteins
    MC_ReadRobotDataFB EXTENDS RobotLibraryBaseExecuteFB
    """

    # VAR_INPUT
    ParCmd                   : ReadRobotDataParCmd
    """Command parameter"""

    # VAR_OUTPUT
    CommandBuffered          : bool
    """Receiving of input parameter values has been acknowledged by RC"""
    OutCmd                   : ReadRobotDataOutCmd 
    """command results"""

    # VAR (lokal)
    _parCmd                  : ReadRobotDataParCmd
    """internal copy of command parameter"""
    _command                 : ReadRobotDataSendData
    """command data to send"""
    _response                : ReadRobotDataRecvData
    """response data received"""

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
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.ReadRobotData.value
        
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
                MessageType = MessageTypeEnum.CMD,
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


        return CheckParameterValid


    # --------------------------------------------------------
    # CreateCommandPayload - create command payload
    # --------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup: AxesGroup) -> RobotLibraryCommandDataFB:
        """Create command payload data"""

        # internal parameter counter
        _parameterCnt : int = 0

        # update command data
        self._command.CmdTyp            = CmdType.ReadRobotData
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
        
        if ( State == CmdMessageState.EMPTY ) :
        
            # Reset command outputs
            self.OutCmd = ReadRobotDataOutCmd()
        

        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :
            
            # Update results
            self.OutCmd.RCManufacturer       =                              self._response.RCManufacturer
            self.OutCmd.RCOrderID            =                              self._response.RCOrderID
            self.OutCmd.RCSerialNumber       =                              self._response.RCSerialNumber
            self.OutCmd.RASerialNumber       =                              self._response.RASerialNumber
            self.OutCmd.RCFirmwareVersion    =                              self._response.RCFirmwareVersion
            self.OutCmd.RCInterpreterVersion =                              self._response.RCInterpreterVersion
            self.OutCmd.AxisJointUsed        =  ByteToAxisJointUsed        (self._response.AxisJointUsed)
            self.OutCmd.AxisExternalUsed     =  ByteToAxisExternalUsed     (self._response.AxisExternalUsed)
            self.OutCmd.AxisJointUnit        =  ByteToAxisJointUnit        (self._response.AxisJointUnit)
            self.OutCmd.AxisExternalUnit     =  ByteToAxisExternalUnit     (self._response.AxisExternalUnit)
            self.OutCmd.RCSupportedFunctions =  BytesToRCSupportedFunctions(self._response.RCSupportedFunctions)
            self.OutCmd.RobotID              =                              self._response.RobotID
            self.OutCmd.InterpreterCycleTime =                              self._response.InterpreterCycleTime
            
            # must be always true, because this command is part of the interface initialization
            self.OutCmd.RCSupportedFunctions.ExchangeConfiguration = BOOL(True)
            self.OutCmd.RCSupportedFunctions.ReadRobotData         = BOOL(True)
            self.OutCmd.RCSupportedFunctions.ReadMessages          = BOOL(True)

    # --------------------------------------------------------
    # OnExecRun  - executed during execution
    # --------------------------------------------------------
    def OnExecRun(self, AxesGroup: AxesGroup)-> int:

        OnExecRun : int = super().OnExecRun(AxesGroup = AxesGroup)

        match self._stepCmd :
        
            case 00:
                if ( self._execute_R.Q ) and ( not self.Error) :

                    # Check function is supported and parameter are valid ?
                    if (( self.CheckFunctionSupported   ( AxesGroup = AxesGroup )) and
                        ( self.CheckParameterValid      ( AxesGroup = AxesGroup ))) : 

                        # Reset all internal flags
                        self.Reset()
                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        self.OutCmd = ReadRobotDataOutCmd()
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


                    # Done, Aborted or Error ?
                    if ( self._response.State >= CmdMessageState.DONE ):
                        # set timeout
                        SetTimeout(PT = self._timeoutCmd, Timer = self._timerCmd)
                        # inc step counter
                        self._stepCmd += 1 


            case 2: 
                # Wait for execution finished 
                if ( not self.Execute ):
                
                    self.Reset()


            case _:
                # invalid step
                self.SetError( ErrorID = RobotErrorIdEnum.ERR_INVALID_STEP, Overwrite = True )


        # Reset FB
        if (not self.Execute):
        
            self.Reset()

        return OnExecRun
    
    
    def OnUpdateStateFlags(self, State: CmdMessageState) -> None:
        """Update state flags from response data"""
        
        # Reset State flags        

        # Update results
        self.Done = False

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
                pass
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
        if ( ResponseData.IsPayloadRemaining ) :
        
            # Get _response.RCManufacturer
            self._response.RCManufacturer.fromBytes( ResponseData.GetDataBlock(Size = self._response.RCManufacturer.Size, IsString = True))
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
        
            # Get _response.RCOrderID
            self._response.RCOrderID.fromBytes( ResponseData.GetDataBlock(Size = self._response.RCOrderID.Size, IsString = True))
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :

            # Get _response.RCSerialNumber
            self._response.RCSerialNumber.fromBytes( ResponseData.GetDataBlock(Size = self._response.RCSerialNumber.Size, IsString = True))
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.RASerialNumber
            self._response.RASerialNumber.fromBytes( ResponseData.GetDataBlock(Size = self._response.RASerialNumber.Size, IsString = True))
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.RCFirmwareVersion
            self._response.RCFirmwareVersion.fromBytes( ResponseData.GetDataBlock(Size = self._response.RCFirmwareVersion.Size, IsString = True))
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.RCInterpreterVersion
            # self._response.RCInterpreterVersion.fromBytes( ResponseData.GetDataBlock( Size = self._response.RCInterpreterVersion.Size, IsString = True )

            # This adaption was made because of Stäubli - check with other robot brands...
            
            # Get _response.RCInterpreterVersion
            self._response.RCInterpreterVersion = ''
            self._response.RCInterpreterVersion = CONCAT(self._response.RCInterpreterVersion, ResponseData.GetByte().toString())
            self._response.RCInterpreterVersion = CONCAT(self._response.RCInterpreterVersion, '.')
            self._response.RCInterpreterVersion = CONCAT(self._response.RCInterpreterVersion, ResponseData.GetByte().toString())
            self._response.RCInterpreterVersion = CONCAT(self._response.RCInterpreterVersion, '.')
            self._response.RCInterpreterVersion = CONCAT(self._response.RCInterpreterVersion, ResponseData.GetByte().toString())
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :

            # Get _response.Reserve
            self._response.Reserve = ResponseData.GetByte() 
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
        
            # Get _response.AxisJointUsed
            self._response.AxisJointUsed = ResponseData.GetByte() 
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
        
            # Get _response.AxisExternalUsed
            self._response.AxisExternalUsed = ResponseData.GetByte() 
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
        
            # Get _response.AxisJointUnit
            self._response.AxisJointUnit = ResponseData.GetByte() 
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
        
            # Get _response.AxisExternalUnit
            self._response.AxisExternalUnit = ResponseData.GetByte() 
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
        
            # Get _response.RCSupportedFunctions
            self._response.RCSupportedFunctions = bytearray(ResponseData.GetDataBlock( Size = len(self._response.RCSupportedFunctions), IsString = False ))
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
        
            # Get _response.Reserve2
            self._response.Reserve2 = ResponseData.GetByte() 
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
        
            # Get _response.RobotID
            self._response.RobotID.fromBytes( ResponseData.GetDataBlock( Size= self._response.RobotID.Size, IsString = True ) )           # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
        
            # Get _response.InterpreterCycleTime
            self._response.InterpreterCycleTime = ResponseData.GetUsint() 
            # inc parameter counter
            _parameterCnt += 1


        # Create logging
        self.ParseResponsePayloadLog(ResponseData = ResponseData, Timestamp = Timestamp, ParameterCnt = _parameterCnt)

        # return updated payload pointer
        return ResponseData.PayloadPtr.value


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
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for RCManufacturer
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.RCManufacturer = {1}',
            Para1       = self._response.RCManufacturer
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for RCOrderID
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.RCOrderID = {1}',
            Para1       = self._response.RCOrderID
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for RCSerialNumber
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.RCSerialNumber = {1}',
            Para1       = self._response.RCSerialNumber
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for RASerialNumber
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.RASerialNumber = {1}',
            Para1       = self._response.RASerialNumber
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for RCFirmwareVersion
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.RCFirmwareVersion = {1}',
            Para1       = self._response.RCFirmwareVersion
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for RCInterpreterVersion
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.RCInterpreterVersion = {1}',
            Para1       = self._response.RCInterpreterVersion
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for Reserve
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.Reserve = {1}',
            Para1       =  self._response.Reserve.toString()
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for AxisJointUsed
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.AxisJointUsed = {1}',
            Para1       =  BYTE_TO_STRING_BIN(self._response.AxisJointUsed)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for AxisExternalUsed
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.AxisExternalUsed = {1}',
            Para1       =  BYTE_TO_STRING_BIN(self._response.AxisExternalUsed)
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for AxisJointUnit
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.AxisJointUnit = {1}',
            Para1       =  self._response.AxisJointUnit.toString()
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for AxisExternalUnit
        self.CreateLogMessage ( 
            Timestamp   = Timestamp,
            MessageType = MessageTypeEnum.CMD,
            Severity    = SeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Response.AxisExternalUnit = {1}',
            Para1       =  self._response.AxisExternalUnit.toString()
        )
        
        
        for  _idx in range( 0, 19):

            # Return if no parameter is remaining...
            if ( ParameterCnt == 0 ) : return  # noqa: E701
            # dec remaining parameter(s)                        
            ParameterCnt -= 1
            # Create log entry for RCSupportedFunctions
            self.CreateLogMessage (
                Timestamp   = Timestamp,
                MessageType = MessageTypeEnum.CMD,
                Severity    = SeverityEnum.DEBUG,
                MessageCode = 0,
                MessageText = 'Response.RCSupportedFunctions[{2}] = {1}',
                Para1       =  CONCAT( '2#', BYTE_TO_STRING_BIN(self._response.RCSupportedFunctions[_idx])),
                Para2       =  INT_TO_STRING(_idx)
            )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for Reserve2
        self.CreateLogMessage ( Timestamp   = Timestamp,
                                MessageType = MessageTypeEnum.CMD,
                                Severity    = SeverityEnum.DEBUG,
                                MessageCode = 0,
                                MessageText = 'Response.Reserve2 = {1}',
                                Para1       = self._response.Reserve2.toString()
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for RobotID
        self.CreateLogMessage ( Timestamp   = Timestamp,
                                MessageType = MessageTypeEnum.CMD,
                                Severity    = SeverityEnum.DEBUG,
                                MessageCode = 0,
                                MessageText = 'Response.RobotID = {1}',
                                Para1       =  self._response.RobotID
        )


        # Return if no parameter is remaining...
        if ( ParameterCnt == 0 ) : return  # noqa: E701
        # dec remaining parameter(s)                        
        ParameterCnt -= 1
        # Create log entry for InterpreterCycleTime
        self.CreateLogMessage ( Timestamp   = Timestamp,
                                MessageType = MessageTypeEnum.CMD,
                                Severity    = SeverityEnum.DEBUG,
                                MessageCode = 0,
                                MessageText = 'Response.InterpreterCycleTime = {1}',
                                Para1       =  self._response.InterpreterCycleTime.toString()
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
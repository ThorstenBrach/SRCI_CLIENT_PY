"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_ReadLoadDataFB
Author:      Thorsten Brach
Date:        2026-01-20

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


from .Structures.ReadLoadDataParCmd import ReadLoadDataParCmd
from .Structures.ReadLoadDataOutCmd import ReadLoadDataOutCmd
from .Structures.ReadLoadDataRecvData import ReadLoadDataRecvData
from .Structures.ReadLoadDataSendData import ReadLoadDataSendData

#endregion


class MC_ReadLoadDataFB(RobotLibraryBaseExecuteFB):
    """Function block to read load data from the robot controller."""
    
    #VAR_INPUT
    ParCmd          : ReadLoadDataParCmd
    """command parameter"""
    
    #VAR_OUTPUT
    CommandBuffered : bool
    """Command is transferred and confirmed by the RC"""
    OutCmd          : ReadLoadDataOutCmd
    """command outputs"""

    #VAR
    _parCmd          : ReadLoadDataParCmd
    """ internal copy of command parameter """
    _command         : ReadLoadDataSendData
    """ command data to send """
    _response        : ReadLoadDataRecvData
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

        # Initialize VAR_INPUT
        self.ParCmd          = ReadLoadDataParCmd()
        
        # Initialize VAR_OUTPUT
        self.CommandBuffered = False
        self.OutCmd          = ReadLoadDataOutCmd()
        
        # Initialize VAR
        self._parCmd         = ReadLoadDataParCmd()
        self._command        = ReadLoadDataSendData()
        self._response       = ReadLoadDataRecvData()


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
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.ReadLoadData.value

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
        if (( self.ParCmd.LoadNo < -1                                                  ) or
            ( self.ParCmd.LoadNo == 0                                                  ) or
            ( self.ParCmd.LoadNo >  254                                                ) or
            ( self.ParCmd.LoadNo >  AxesGroup.State.ConfigurationData.HighestLoadIndex ) or
            ( self.ParCmd.LoadNo >  AxesGroup.State.UnifiedLoadIndex                   )) :
            
            # Parameter not valid
            CheckParameterValid = False
            
            # Check LoadNo available on RC ? 
            if ( self.ParCmd.LoadNo > AxesGroup.State.ConfigurationData.HighestLoadIndex ) :

                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_LOADNO_UNAVAILABLE, Overwrite = True )
            else:

                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_LOADNO_RANGE, Overwrite = True )

            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.LoadNo = {1}',
                Para1       =  str(self.ParCmd.LoadNo)
            )

        return CheckParameterValid

    #--------------------------------------------------------
    # CreateCommandPayload - create command payload
    #--------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup : AxesGroup) -> RobotLibraryCommandDataFB:
        
        # Parameter count
        _parameterCnt : int = 0

        #region Mapping table
        
        # Table 6-171: Sent CMD payload (PLC to RC) of "ReadLoadData"
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
        # Byte 04 : USINT - LoadNo
        # --------------------------
        # endregion

        # set command parameter 
        self._command.CmdTyp       = CmdType.ReadLoadData
        self._command.ExecMode     = self. ExecMode
        self._command.ParSeq       = self._command.ParSeq
        self._command.Priority     = self. Priority
        self._command.LoadNo.value = self._parCmd.LoadNo

        if ( self._parCmd.LoadNo == -1) :

            self._command.LoadNo.value = 255 # -1 is mapped to 255, see specification

        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadNo
            self.CommandData.AddUsint(self._command.LoadNo)
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
            MessageText = 'Command.LoadNo = {1}',
            Para1       =  str(self._command.LoadNo)
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
            self.OutCmd = ReadLoadDataOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :

            # Update results
            self.OutCmd.LoadData     = self._response.LoadData
            self.OutCmd.LoadNoReturn = self._response.LoadNoReturn.value


    #--------------------------------------------------------
    # OnUpdateStateFlags - update state flags
    #--------------------------------------------------------
    def OnUpdateStateFlags(self, State : CmdMessageState) -> None:
        """
        Update state flags according to received state
        """

        # Reset State flags
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

            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER : 
                self.CommandBuffered    = True

            # Currently active and in progress
            case CmdMessageState.ACTIVE: 
                pass

            # Interrupted and awaiting continuation
            case CmdMessageState.INTERRUPTED:
                pass

            # Requested for abort
            case CmdMessageState.ABORT_REQUEST:
                pass

            # Successfully completed
            case CmdMessageState.DONE : 
                self.Done = True
                self.Busy = False

            # Aborted before completion
            case CmdMessageState.ABORTED:
                self.Busy = False

            # Encountered an error during execution
            case CmdMessageState.ERROR:
                self.Error = True
                self.Busy = False


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
                        self.OutCmd = ReadLoadDataOutCmd()
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
                        
                        # Update the LoadData in user defined system data 
                        AxesGroup.SystemData.UpdateLoadData( Caller     = self,
                                                             SystemTime = AxesGroup.State.SystemTime,
                                                             LoadNo     = self.OutCmd.LoadNoReturn, 
                                                             LoadData   = self.OutCmd.LoadData)
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


    #--------------------------------------------------------#
    # ParseResponsePayload - parse response payload
    #--------------------------------------------------------#                
    def ParseResponsePayload(self, ResponseData : RobotLibraryResponseDataFB, Timestamp : SystemTime ) -> int:
        """
        Parse response payload received from robot controller
        """

        #region Mapping table

        # Table 6-172: Received CMD payload (RC to PLC) of "ReadLoadData"
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
        # Byte 04 : DATE    - LoadData.Date LW HB;
        # Byte 05 :         - LoadData.Date LW LB;
        # Byte 06 : TOD     - LoadData.Time LW HB;
        # Byte 07 :         - LoadData.Time LW LB;
        # Byte 08 :         - LoadData.Time LW HB;
        # Byte 09 :         - LoadData.Time LW LB;
        # Byte 10 : REAL    - LoadData.X HW HB;
        # Byte 11 :         - LoadData.X HW LB;
        # Byte 12 :         - LoadData.X LW HB;
        # Byte 13 :         - LoadData.X LW LB;
        # Byte 14 : REAL    - LoadData.Y HW HB;
        # Byte 15 :         - LoadData.Y HW LB;
        # Byte 16 :         - LoadData.Y LW HB;
        # Byte 17 :         - LoadData.Y LW LB;
        # Byte 18 : REAL    - LoadData.Z HW HB;
        # Byte 19 :         - LoadData.Z HW LB;
        # Byte 20 :         - LoadData.Z LW HB;
        # Byte 21 :         - LoadData.Z LW LB;
        # Byte 22 : REAL    - LoadData.RX HW HB;
        # Byte 23 :         - LoadData.RX HW LB;
        # Byte 24 :         - LoadData.RX LW HB;
        # Byte 25 :         - LoadData.RX LW LB;
        # Byte 26 : REAL    - LoadData.RY HW HB;
        # Byte 27 :         - LoadData.RY HW LB;
        # Byte 28 :         - LoadData.RY LW HB;
        # Byte 29 :         - LoadData.RY LW LB;
        # Byte 30 : REAL    - LoadData.RZ HW HB;
        # Byte 31 :         - LoadData.RZ HW LB;
        # Byte 32 :         - LoadData.RZ LW HB;
        # Byte 33 :         - LoadData.RZ LW LB;
        # Byte 34 : REAL    - LoadData.Mass HW HB;
        # Byte 35 :         - LoadData.Mass HW LB;
        # Byte 36 :         - LoadData.Mass LW HB;
        # Byte 37 :         - LoadData.Mass LW LB;
        # Byte 38 : REAL    - LoadData.IX HW HB;
        # Byte 39 :         - LoadData.IX HW LB;
        # Byte 40 :         - LoadData.IX LW HB;
        # Byte 41 :         - LoadData.IX LW LB;
        # Byte 42 : REAL    - LoadData.IY HW HB;
        # Byte 43 :         - LoadData.IY HW LB;
        # Byte 44 :         - LoadData.IY LW HB;
        # Byte 45 :         - LoadData.IY LW LB;
        # Byte 46 : REAL    - LoadData.IZ HW HB;
        # Byte 47 :         - LoadData.IZ HW LB;
        # Byte 48 :         - LoadData.IZ LW HB;
        # Byte 49 :         - LoadData.IZ LW LB;
        # Byte 50 : USINT   - LoadNo;
        # Byte 51 : BOOL    - DataChanged;
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
            # Get Response.LoadData.Timestamp.IEC_DATE
            self._response.LoadData.Timestamp.IEC_DATE = ResponseData.GetIecDate()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.Timestamp.IEC_TIME
            self._response.LoadData.Timestamp.IEC_TIME = ResponseData.GetIecTime()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.X
            self._response.LoadData.X = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.Y
            self._response.LoadData.Y = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.Z
            self._response.LoadData.Z = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.Rx
            self._response.LoadData.Rx = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.Ry
            self._response.LoadData.Ry = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.Rz
            self._response.LoadData.Rz = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.Mass
            self._response.LoadData.Mass = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.Ix
            self._response.LoadData.Ix = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.Iy
            self._response.LoadData.Iy = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadData.Iz
            self._response.LoadData.Iz = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LoadNoReturn
            self._response.LoadNoReturn = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.DataChanged
            self._response.DataChanged = ResponseData.GetBool()
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
            MessageText = 'Response.LoadData.Timestamp.IEC_DATE = {1}',
            Para1       =  str(self._response.LoadData.Timestamp.IEC_DATE)
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
            MessageText = 'Response.LoadData.Timestamp.IEC_TIME = {1}',
            Para1       =  str(self._response.LoadData.Timestamp.IEC_TIME)
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
            MessageText = 'Response.LoadData.X = {1}',
            Para1       =  str(self._response.LoadData.X)
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
            MessageText = 'Response.LoadData.Y = {1}',
            Para1       =  str(self._response.LoadData.Y)
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
            MessageText = 'Response.LoadData.Z = {1}',
            Para1       =  str(self._response.LoadData.Z)
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
            MessageText = 'Response.LoadData.Rx = {1}',
            Para1       =  str(self._response.LoadData.Rx)
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
            MessageText = 'Response.LoadData.Ry = {1}',
            Para1       =  str(self._response.LoadData.Ry)
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
            MessageText = 'Response.LoadData.Rz = {1}',
            Para1       =  str(self._response.LoadData.Rz)
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
            MessageText = 'Response.LoadData.Mass = {1}',
            Para1       =  str(self._response.LoadData.Mass)
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
            MessageText = 'Response.LoadData.Ix = {1}',
            Para1       =  str(self._response.LoadData.Ix)
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
            MessageText = 'Response.LoadData.Iy = {1}',
            Para1       =  str(self._response.LoadData.Iy)
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
            MessageText = 'Response.LoadData.Iz = {1}',
            Para1       =  str(self._response.LoadData.Iz)
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
            MessageText = 'Response.LoadNoReturn = {1}',
            Para1       =  str(self._response.LoadNoReturn)
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
            MessageText = 'Response.DataChanged = {1}',
            Para1       =  str(self._response.DataChanged)
        )


    #--------------------------------------------------------
    # Reset - reset internal variables
    #--------------------------------------------------------
    def Reset(self) -> int:
        """ Reset internal variables """

        self.Done               = False
        self.Busy               = False
        self.CommandBuffered    = False

        return super().Reset()
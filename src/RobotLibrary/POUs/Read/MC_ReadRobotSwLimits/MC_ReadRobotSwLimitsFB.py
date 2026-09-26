"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_ReadRobotSwLimitsFB
Author:      Thorsten Brach
Date:        2026-01-16 

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

from .Structures.ReadRobotSwLimitsParCmd import ReadRobotSwLimitsParCmd
from .Structures.ReadRobotSwLimitsOutCmd import ReadRobotSwLimitsOutCmd
from .Structures.ReadRobotSwLimitsRecvData import ReadRobotSwLimitsRecvData
from. Structures.ReadRobotSwLimitsSendData import ReadRobotSwLimitsSendData

#endregion


class MC_ReadRobotSwLimitsFB( RobotLibraryBaseExecuteFB):
    """Function block to read messages from the robot controller."""
    
    """Function block to read software limits from the robot controller."""
    
    #VAR_INPUT
    ParCmd          : ReadRobotSwLimitsParCmd
    """command parameter"""
    
    #VAR_OUTPUT
    CommandBuffered : bool
    """Command is transferred and confirmed by the RC"""
    OutCmd          : ReadRobotSwLimitsOutCmd
    """command outputs"""

    #VAR
    _parCmd          : ReadRobotSwLimitsParCmd
    """ internal copy of command parameter """
    _command         : ReadRobotSwLimitsSendData
    """ command data to send """
    _response        : ReadRobotSwLimitsRecvData
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
        self.ParCmd          = ReadRobotSwLimitsParCmd()
        
        # Initialize VAR_OUTPUT
        self.CommandBuffered = False
        self.OutCmd          = ReadRobotSwLimitsOutCmd()
        
        # Initialize VAR
        self._parCmd         = ReadRobotSwLimitsParCmd()
        self._command        = ReadRobotSwLimitsSendData()
        self._response       = ReadRobotSwLimitsRecvData()



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
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.ReadRobotSWLimits.value

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

        # No ParCmd to check

        return CheckParameterValid

    #--------------------------------------------------------
    # CreateCommandPayload - create command payload
    #--------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup : AxesGroup) -> RobotLibraryCommandDataFB:
        
        # Parameter count
        _parameterCnt : int = 0

        #region Mapping table
        
        # Table 6-159: Sent CMD payload (PLC to RC) of "ReadRobotSwLimits"
        # --------------------------
        # Header
        # --------------------------
        # Byte 00 : UINT  - Type HB     
        # Byte 01 :       - Type LB    
        # Byte 02 : USINT - Reserve | ExecutionMode
        # Byte 03 : USINT - ParSeq  | Priority
        # --------------------------
        # endregion

        # set command parameter 
        self._command.CmdTyp        = CmdType.ReadRobotSWLimits
        self._command.ExecMode      = self. ExecMode
        self._command.ParSeq        = self._command.ParSeq
        self._command.Priority      = self. Priority


        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)

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


    #--------------------------------------------------------
    # OnApplyOutCmd - apply output command data
    #--------------------------------------------------------
    def OnApplyOutCmd(self, State : CmdMessageState) -> None:
        """
        Apply output command data received from robot controller
        """

        if ( State == CmdMessageState.EMPTY ) :

            # Reset command outputs
            self.OutCmd = ReadRobotSwLimitsOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :

            # Update results
            self.OutCmd.LimitValues = self._response.LimitValues


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
                        self.OutCmd = ReadRobotSwLimitsOutCmd()
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
                        
                        # Update the SW limits in user defined system datas 
                        AxesGroup.SystemData.UpdateSWLimits( LimitValues = self.OutCmd.LimitValues)
                        
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


    #--------------------------------------------------------#
    # ParseResponsePayload - parse response payload
    #--------------------------------------------------------#                
    def ParseResponsePayload(self, ResponseData : RobotLibraryResponseDataFB, Timestamp : SystemTime ) -> int:
        """
        Parse response payload received from robot controller
        """

        #region Mapping table

        # Table 6-179: Received CMD payload (RC to PLC) of "WriteRobotSWLimits"
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
        # Byte 04 : IEC_DATE -  Date HW HB;
        # Byte 05 :             Date HW LB;
        # Byte 06 : IED_TIME -  Time HW HB;
        # Byte 07 :             Time HW LB;
        # Byte 08 :             Time LW HB;
        # Byte 09 :             Time LW LB;
        # Byte 10 : REAL        J1LowerLimit HW HB;
        # Byte 11 :             J1LowerLimit HW LB;
        # Byte 12 :             J1LowerLimit LW HB;
        # Byte 13 :             J1LowerLimit LW LB;
        # Byte 14 : REAL        J2LowerLimit HW HB;
        # Byte 15 :             J2LowerLimit HW LB;
        # Byte 16 :             J2LowerLimit LW HB;
        # Byte 17 :             J2LowerLimit LW LB;
        # Byte 18 : REAL        J3LowerLimit HW HB;
        # Byte 19 :             J3LowerLimit HW LB;
        # Byte 20 :             J3LowerLimit LW HB;
        # Byte 21 :             J3LowerLimit LW LB;
        # Byte 22 : REAL        J4LowerLimit HW HB;
        # Byte 23 :             J4LowerLimit HW LB;
        # Byte 24 :             J4LowerLimit LW HB;
        # Byte 25 :             J4LowerLimit LW LB;
        # Byte 26 : REAL        J5LowerLimit HW HB;
        # Byte 27 :             J5LowerLimit HW LB;
        # Byte 28 :             J5LowerLimit LW HB;
        # Byte 29 :             J5LowerLimit LW LB;
        # Byte 30 : REAL        J6LowerLimit HW HB;
        # Byte 31 :             J6LowerLimit HW LB;
        # Byte 32 :             J6LowerLimit LW HB;
        # Byte 33 :             J6LowerLimit LW LB;
        # Byte 34 : REAL        E1LowerLimit HW HB;
        # Byte 35 :             E1LowerLimit HW LB;
        # Byte 36 :             E1LowerLimit LW HB;
        # Byte 37 :             E1LowerLimit LW LB;
        # Byte 38 : REAL        J1UpperLimit HW HB;
        # Byte 39 :             J1UpperLimit HW LB;
        # Byte 40 :             J1UpperLimit LW HB;
        # Byte 41 :             J1UpperLimit LW LB;
        # Byte 42 : REAL        J2UpperLimit HW HB;
        # Byte 43 :             J2UpperLimit HW LB;
        # Byte 44 :             J2UpperLimit LW HB;
        # Byte 45 :             J2UpperLimit LW LB;
        # Byte 46 : REAL        J3UpperLimit HW HB;
        # Byte 47 :             J3UpperLimit HW LB;
        # Byte 48 :             J3UpperLimit LW HB;
        # Byte 49 :             J3UpperLimit LW LB;
        # Byte 50 : REAL        J4UpperLimit HW HB;
        # Byte 51 :             J4UpperLimit HW LB;
        # Byte 52 :             J4UpperLimit LW HB;
        # Byte 53 :             J4UpperLimit LW LB;
        # Byte 54 : REAL        J5UpperLimit HW HB;
        # Byte 55 :             J5UpperLimit HW LB;
        # Byte 56 :             J5UpperLimit LW HB;
        # Byte 57 :             J5UpperLimit LW LB;
        # Byte 58 : REAL        J6UpperLimit HW HB;
        # Byte 59 :             J6UpperLimit HW LB;
        # Byte 60 :             J6UpperLimit LW HB;
        # Byte 61 :             J6UpperLimit LW LB;
        # Byte 62 : REAL        E1UpperLimit HW HB;
        # Byte 63 :             E1UpperLimit HW LB;
        # Byte 64 :             E1UpperLimit LW HB;
        # Byte 65 :             E1UpperLimit LW LB;
        # Byte 66 : REAL        E2LowerLimit HW HB;
        # Byte 67 :             E2LowerLimit HW LB;
        # Byte 68 :             E2LowerLimit LW HB;
        # Byte 69 :             E2LowerLimit LW LB;
        # Byte 70 : REAL        E3LowerLimit HW HB;
        # Byte 71 :             E3LowerLimit HW LB;
        # Byte 72 :             E3LowerLimit LW HB;
        # Byte 73 :             E3LowerLimit LW LB;
        # Byte 74 : REAL        E4LowerLimit HW HB;
        # Byte 75 :             E4LowerLimit HW LB;
        # Byte 76 :             E4LowerLimit LW HB;
        # Byte 77 :             E4LowerLimit LW LB;
        # Byte 78 : REAL        E5LowerLimit HW HB;
        # Byte 79 :             E5LowerLimit HW LB;
        # Byte 80 :             E5LowerLimit LW HB;
        # Byte 81 :             E5LowerLimit LW LB;
        # Byte 82 : REAL        E6LowerLimit HW HB;
        # Byte 83 :             E6LowerLimit HW LB;
        # Byte 84 :             E6LowerLimit LW HB;
        # Byte 85 :             E6LowerLimit LW LB;
        # Byte 86 : REAL        E2UpperLimit HW HB;
        # Byte 87 :             E2UpperLimit HW LB;
        # Byte 88 :             E2UpperLimit LW HB;
        # Byte 89 :             E2UpperLimit LW LB;
        # Byte 90 : REAL        E3UpperLimit HW HB;
        # Byte 91 :             E3UpperLimit HW LB;
        # Byte 92 :             E3UpperLimit LW HB;
        # Byte 93 :             E3UpperLimit LW LB;
        # Byte 94 : REAL        E4UpperLimit HW HB;
        # Byte 95 :             E4UpperLimit HW LB;
        # Byte 96 :             E4UpperLimit LW HB;
        # Byte 97 :             E4UpperLimit LW LB;
        # Byte 98 : REAL        E5UpperLimit HW HB;
        # Byte 99 :             E5UpperLimit HW LB;
        # Byte 100:             E5UpperLimit LW HB;
        # Byte 101:             E5UpperLimit LW LB;
        # Byte 102: REAL        E6UpperLimit HW HB;
        # Byte 103:             E6UpperLimit HW LB;
        # Byte 104:             E6UpperLimit LW HB;
        # Byte 105:             E6UpperLimit LW LB;
        # Byte 106: BOOL        DataChanged;
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
            # Get Response.LimitValues.Timestamp.IEC_DATE
            self._response.LimitValues.Timestamp.IEC_DATE = ResponseData.GetIecDate()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.Timestamp.IEC_TIME
            self._response.LimitValues.Timestamp.IEC_TIME = ResponseData.GetIecTime()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J1LowerLimit
            self._response.LimitValues.J1LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J2LowerLimit
            self._response.LimitValues.J2LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J3LowerLimit
            self._response.LimitValues.J3LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J4LowerLimit
            self._response.LimitValues.J4LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J5LowerLimit
            self._response.LimitValues.J5LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J6LowerLimit
            self._response.LimitValues.J6LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E1LowerLimit
            self._response.LimitValues.E1LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J1UpperLimit
            self._response.LimitValues.J1UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J2UpperLimit
            self._response.LimitValues.J2UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J3UpperLimit
            self._response.LimitValues.J3UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J4UpperLimit
            self._response.LimitValues.J4UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J5UpperLimit
            self._response.LimitValues.J5UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.J6UpperLimit
            self._response.LimitValues.J6UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E1UpperLimit
            self._response.LimitValues.E1UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E2LowerLimit
            self._response.LimitValues.E2LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E3LowerLimit
            self._response.LimitValues.E3LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E4LowerLimit
            self._response.LimitValues.E4LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E5LowerLimit
            self._response.LimitValues.E5LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E6LowerLimit
            self._response.LimitValues.E6LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E2UpperLimit
            self._response.LimitValues.E2UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E3UpperLimit
            self._response.LimitValues.E3UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E4UpperLimit
            self._response.LimitValues.E4UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E5UpperLimit
            self._response.LimitValues.E5UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LimitValues.E6UpperLimit
            self._response.LimitValues.E6UpperLimit = ResponseData.GetReal()
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
            MessageText = 'Response.LimitValues.Timestamp.IEC_DATE = {1}',
            Para1       =  str(self._response.LimitValues.Timestamp.IEC_DATE)
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
            MessageText = 'Response.LimitValues.Timestamp.IEC_TIME = {1}',
            Para1       =  str(self._response.LimitValues.Timestamp.IEC_TIME)
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
            MessageText = 'Response.LimitValues.J1LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.J1LowerLimit)
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
            MessageText = 'Response.LimitValues.J2LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.J2LowerLimit)
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
            MessageText = 'Response.LimitValues.J3LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.J3LowerLimit)
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
            MessageText = 'Response.LimitValues.J4LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.J4LowerLimit)
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
            MessageText = 'Response.LimitValues.J5LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.J5LowerLimit)
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
            MessageText = 'Response.LimitValues.J6LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.J6LowerLimit)
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
            MessageText = 'Response.LimitValues.E1LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.E1LowerLimit)
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
            MessageText = 'Response.LimitValues.J1UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.J1UpperLimit)
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
            MessageText = 'Response.LimitValues.J2UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.J2UpperLimit)
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
            MessageText = 'Response.LimitValues.J3UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.J3UpperLimit)
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
            MessageText = 'Response.LimitValues.J4UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.J4UpperLimit)
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
            MessageText = 'Response.LimitValues.J5UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.J5UpperLimit)
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
            MessageText = 'Response.LimitValues.J6UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.J6UpperLimit)
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
            MessageText = 'Response.LimitValues.E1UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.E1UpperLimit)
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
            MessageText = 'Response.LimitValues.E2LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.E2LowerLimit)
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
            MessageText = 'Response.LimitValues.E3LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.E3LowerLimit)
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
            MessageText = 'Response.LimitValues.E4LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.E4LowerLimit)
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
            MessageText = 'Response.LimitValues.E5LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.E5LowerLimit)
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
            MessageText = 'Response.LimitValues.E6LowerLimit = {1}',
            Para1       =  str(self._response.LimitValues.E6LowerLimit)
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
            MessageText = 'Response.LimitValues.E2UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.E2UpperLimit)
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
            MessageText = 'Response.LimitValues.E3UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.E3UpperLimit)
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
            MessageText = 'Response.LimitValues.E4UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.E4UpperLimit)
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
            MessageText = 'Response.LimitValues.E5UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.E5UpperLimit)
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
            MessageText = 'Response.LimitValues.E6UpperLimit = {1}',
            Para1       =  str(self._response.LimitValues.E6UpperLimit)
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
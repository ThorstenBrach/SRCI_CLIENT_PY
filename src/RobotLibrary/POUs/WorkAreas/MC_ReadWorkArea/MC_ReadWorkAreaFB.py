"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_ReadWorkAreaFB
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
from RobotLibrary.Enumerations.Type.AreaType import AreaType
from RobotLibrary.Enumerations.Mode.WorkAreaReactionMode import WorkAreaReactionMode
from RobotLibrary.Enumerations.Mode.DefinitionMode import DefinitionMode
from .Structures.ReadWorkAreaParCmd import ReadWorkAreaParCmd
from .Structures.ReadWorkAreaOutCmd import ReadWorkAreaOutCmd
from .Structures.ReadWorkAreaRecvData import ReadWorkAreaRecvData
from .Structures.ReadWorkAreaSendData import ReadWorkAreaSendData
#endregion

class MC_ReadWorkAreaFB( RobotLibraryBaseExecuteFB):
    """Function block to read work area data from the robot controller."""
    
    #VAR_INPUT
    ParCmd          : ReadWorkAreaParCmd
    """command parameter"""
    
    #VAR_OUTPUT
    CommandBuffered : bool
    """Command is transferred and confirmed by the RC"""
    OutCmd          : ReadWorkAreaOutCmd
    """command outputs"""

    #VAR
    _parCmd          : ReadWorkAreaParCmd
    """ internal copy of command parameter """
    _command         : ReadWorkAreaSendData
    """ command data to send """
    _response        : ReadWorkAreaRecvData
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
        self.ParCmd          = ReadWorkAreaParCmd()
        
        # Initialize VAR_OUTPUT
        self.CommandBuffered = False
        self.OutCmd          = ReadWorkAreaOutCmd()
        
        # Initialize VAR
        self._parCmd         = ReadWorkAreaParCmd()
        self._command        = ReadWorkAreaSendData()
        self._response       = ReadWorkAreaRecvData()



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
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.ReadWorkArea.value

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

        # Check ParCmd.WorkAreaNo valid ? 
        if (( self.ParCmd.WorkAreaNo < 0                                                      ) or
            ( self.ParCmd.WorkAreaNo > 254                                                    ) or
            ( self.ParCmd.WorkAreaNo > AxesGroup.State.ConfigurationData.HighestWorkAreaIndex ) or
            ( self.ParCmd.WorkAreaNo > AxesGroup.State.UnifiedWorkAreaIndex                   )) :

            # Parameter not valid
            CheckParameterValid = False
            
            # Check LoadNo available on RC ? 
            if ( self.ParCmd.WorkAreaNo > AxesGroup.State.ConfigurationData.HighestWorkAreaIndex ):
                
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_WORKAREANO_UNAVAILABLE, Overwrite = True )
            else:
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_WORKAREANO_RANGE, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.WorkAreaNo = {1}',
                Para1       = str(self.ParCmd.WorkAreaNo)
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
        
        # Table 6-199: Sent CMD payload (PLC to RC) of "ReadWorkArea"
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
        # Byte 04 : USINT  WorkAreaNo
        # --------------------------
        # endregion

        # set command parameter 
        self._command.CmdTyp           = CmdType.ReadWorkArea
        self._command.ExecMode         = self. ExecMode
        self._command.ParSeq           = self._command.ParSeq
        self._command.Priority         = self. Priority
        self._command.WorkAreaNo.value = self._parCmd.WorkAreaNo


        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.WorkAreaNo
            self.CommandData.AddUsint(self._command.WorkAreaNo)
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
            MessageText = 'Command.WorkAreaNo = {1}',
            Para1       =  str(self._command.WorkAreaNo)
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
            self.OutCmd = ReadWorkAreaOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :

            # Update results
            self.OutCmd.WorkAreaData     = self._response.WorkAreaData
            self.OutCmd.WorkAreaNoReturn = self._response.WorkAreaNoReturn.value


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
                        self.OutCmd = ReadWorkAreaOutCmd()
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
                        
                        # Update the WorAreas in user defined system datas 
                        AxesGroup.SystemData.UpdateWorkAreas( Caller       = self,
                                                              SystemTime   = AxesGroup.State.SystemTime,
                                                              WorkAreaNo   = self.OutCmd.WorkAreaNoReturn, 
                                                              WorkAreaData = self.OutCmd.WorkAreaData)
                        
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
                self.CommandBuffered = True

            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER : 
                self.CommandBuffered = True

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

        # Table 6-200: Received CMD payload (RC to PLC) of "ReadWorkArea"
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
        # Byte 04 : USINT    - WorkAreaNo;
        # Byte 05 : BYTE     - Reserved;
        # Byte 06 : DATE     - Data.Date HW HB;
        # Byte 07 :          - Data.Date HW LB;
        # Byte 08 : IED_TIME - Data.Time HW HB;
        # Byte 09 :          - Data.Time HW LB;
        # Byte 10 :          - Data.Time LW HB;
        # Byte 11 :          - Data.Time LW LB;
        # Byte 12 : USINT    - Data.AreaType;
        # Byte 13 : BOOL     - Data.AreaMode;
        # Byte 14 : USINT    - Data.ReactionMode;
        # Byte 15 : BOOL     - Data.ActiveModification;
        # Byte 16 : USINT    - Data.DefinitionMode;
        # Byte 17 : USINT    - Data.FrameNo;
        # Byte 18 : REAL     - Data.ZeroPointX HW HB;
        # Byte 19 :          - Data.ZeroPointX HW LB;
        # Byte 20 :          - Data.ZeroPointX LW HB;
        # Byte 21 :          - Data.ZeroPointX LW LB;
        # Byte 22 : REAL     - Data.ZeroPointY HW HB;
        # Byte 23 :          - Data.ZeroPointY HW LB;
        # Byte 24 :          - Data.ZeroPointY LW HB;
        # Byte 25 :          - Data.ZeroPointY LW LB;
        # Byte 26 : REAL     - Data.ZeroPointZ HW HB;
        # Byte 27 :          - Data.ZeroPointZ HW LB;
        # Byte 28 :          - Data.ZeroPointZ LW HB;
        # Byte 29 :          - Data.ZeroPointZ LW LB;
        # Byte 30 : REAL     - Data.X1 HW HB;
        # Byte 31 :          - Data.X1 HW LB;
        # Byte 32 :          - Data.X1 LW HB;
        # Byte 33 :          - Data.X1 LW LB;
        # Byte 34 : REAL     - Data.X2 HW HB;
        # Byte 35 :          - Data.X2 HW LB;
        # Byte 36 :          - Data.X2 LW HB;
        # Byte 37 :          - Data.X2 LW LB;
        # Byte 38 : REAL     - Data.Y1 HW HB;
        # Byte 39 :          - Data.Y1 HW LB;
        # Byte 40 :          - Data.Y1 LW HB;
        # Byte 41 :          - Data.Y1 LW LB;
        # Byte 42 : REAL     - Data.Y2 HW HB;
        # Byte 43 :          - Data.Y2 HW LB;
        # Byte 44 :          - Data.Y2 LW HB;
        # Byte 45 :          - Data.Y2 LW LB;
        # Byte 46 : REAL     - Data.Z1 HW HB;
        # Byte 47 :          - Data.Z1 HW LB;
        # Byte 48 :          - Data.Z1 LW HB;
        # Byte 49 :          - Data.Z1 LW LB;
        # Byte 50 : REAL     - Data.Z2 HW HB;
        # Byte 51 :          - Data.Z2 HW LB;
        # Byte 52 :          - Data.Z2 LW HB;
        # Byte 53 :          - Data.Z2 LW LB;
        # Byte 54 : REAL     - Data.Radius HW HB;
        # Byte 55 :          - Data.Radius HW LB;
        # Byte 56 :          - Data.Radius LW HB;
        # Byte 57 :          - Data.Radius LW LB;
        # Byte 58 : REAL     - Data.JointLowerLimit.J1 HW HB;
        # Byte 59 :          - Data.JointLowerLimit.J1 HW LB;
        # Byte 60 :          - Data.JointLowerLimit.J1 LW HB;
        # Byte 61 :          - Data.JointLowerLimit.J1 LW LB;
        # Byte 62 : REAL     - Data.JointLowerLimit.J2 HW HB;
        # Byte 63 :          - Data.JointLowerLimit.J2 HW LB;
        # Byte 64 :          - Data.JointLowerLimit.J2 LW HB;
        # Byte 65 :          - Data.JointLowerLimit.J2 LW LB;
        # Byte 66 : REAL     - Data.JointLowerLimit.J3 HW HB;
        # Byte 67 :          - Data.JointLowerLimit.J3 HW LB;
        # Byte 68 :          - Data.JointLowerLimit.J3 LW HB;
        # Byte 69 :          - Data.JointLowerLimit.J3 LW LB;
        # Byte 70 : REAL     - Data.JointLowerLimit.J4 HW HB;
        # Byte 71 :          - Data.JointLowerLimit.J4 HW LB;
        # Byte 72 :          - Data.JointLowerLimit.J4 LW HB;
        # Byte 73 :          - Data.JointLowerLimit.J4 LW LB;
        # Byte 74 : REAL     - Data.JointLowerLimit.J5 HW HB;
        # Byte 75 :          - Data.JointLowerLimit.J5 HW LB;
        # Byte 76 :          - Data.JointLowerLimit.J5 LW HB;
        # Byte 77 :          - Data.JointLowerLimit.J5 LW LB;
        # Byte 78 : REAL     - Data.JointLowerLimit.J6 HW HB;
        # Byte 79 :          - Data.JointLowerLimit.J6 HW LB;
        # Byte 80 :          - Data.JointLowerLimit.J6 LW HB;
        # Byte 81 :          - Data.JointLowerLimit.J6 LW LB;
        # Byte 82 : REAL     - Data.JointLowerLimit.E1 HW HB;
        # Byte 83 :          - Data.JointLowerLimit.E1 HW LB;
        # Byte 84 :          - Data.JointLowerLimit.E1 LW HB;
        # Byte 85 :          - Data.JointLowerLimit.E1 LW LB;
        # Byte 86 : REAL     - Data.JointUpperLimit.J1 HW HB;
        # Byte 87 :          - Data.JointUpperLimit.J1 HW LB;
        # Byte 88 :          - Data.JointUpperLimit.J1 LW HB;
        # Byte 89 :          - Data.JointUpperLimit.J1 LW LB;
        # Byte 90 : REAL     - Data.JointUpperLimit.J2 HW HB;
        # Byte 91 :          - Data.JointUpperLimit.J2 HW LB;
        # Byte 92 :          - Data.JointUpperLimit.J2 LW HB;
        # Byte 93 :          - Data.JointUpperLimit.J2 LW LB;
        # Byte 94 : REAL     - Data.JointUpperLimit.J3 HW HB;
        # Byte 95 :          - Data.JointUpperLimit.J3 HW LB;
        # Byte 96 :          - Data.JointUpperLimit.J3 LW HB;
        # Byte 97 :          - Data.JointUpperLimit.J3 LW LB;
        # Byte 98 : REAL     - Data.JointUpperLimit.J4 HW HB;
        # Byte 99 :          - Data.JointUpperLimit.J4 HW LB;
        # Byte 100:          - Data.JointUpperLimit.J4 LW HB;
        # Byte 101:          - Data.JointUpperLimit.J4 LW LB;
        # Byte 102: REAL     - Data.JointUpperLimit.J5 HW HB;
        # Byte 103:          - Data.JointUpperLimit.J5 HW LB;
        # Byte 104:          - Data.JointUpperLimit.J5 LW HB;
        # Byte 105:          - Data.JointUpperLimit.J5 LW LB;
        # Byte 106: REAL     - Data.JointUpperLimit.J6 HW HB;
        # Byte 107:          - Data.JointUpperLimit.J6 HW LB;
        # Byte 108:          - Data.JointUpperLimit.J6 LW HB;
        # Byte 109:          - Data.JointUpperLimit.J6 LW LB;
        # Byte 110: REAL     - Data.JointUpperLimit.E1 HW HB;
        # Byte 111:          - Data.JointUpperLimit.E1 HW LB;
        # Byte 112:          - Data.JointUpperLimit.E1 LW HB;
        # Byte 113:          - Data.JointUpperLimit.E1 LW LB;
        # Byte 114: REAL     - Data.JointLowerLimit.E2 HW HB;
        # Byte 115:          - Data.JointLowerLimit.E2 HW LB;
        # Byte 116:          - Data.JointLowerLimit.E2 LW HB;
        # Byte 117:          - Data.JointLowerLimit.E2 LW LB;
        # Byte 118: REAL     - Data.JointLowerLimit.E3 HW HB;
        # Byte 119:          - Data.JointLowerLimit.E3 HW LB;
        # Byte 120:          - Data.JointLowerLimit.E3 LW HB;
        # Byte 121:          - Data.JointLowerLimit.E3 LW LB;
        # Byte 122: REAL     - Data.JointLowerLimit.E4 HW HB;
        # Byte 123:          - Data.JointLowerLimit.E4 HW LB;
        # Byte 124:          - Data.JointLowerLimit.E4 LW HB;
        # Byte 125:          - Data.JointLowerLimit.E4 LW LB;
        # Byte 126: REAL     - Data.JointLowerLimit.E5 HW HB;
        # Byte 127:          - Data.JointLowerLimit.E5 HW LB;
        # Byte 128:          - Data.JointLowerLimit.E5 LW HB;
        # Byte 129:          - Data.JointLowerLimit.E5 LW LB;
        # Byte 130: REAL     - Data.JointLowerLimit.E6 HW HB;
        # Byte 131:          - Data.JointLowerLimit.E6 HW LB;
        # Byte 132:          - Data.JointLowerLimit.E6 LW HB;
        # Byte 133:          - Data.JointLowerLimit.E6 LW LB;
        # Byte 134: REAL     - Data.JointUpperLimit.E2 HW HB;
        # Byte 135:          - Data.JointUpperLimit.E2 HW LB;
        # Byte 136:          - Data.JointUpperLimit.E2 LW HB;
        # Byte 137:          - Data.JointUpperLimit.E2 LW LB;
        # Byte 138: REAL     - Data.JointUpperLimit.E3 HW HB;
        # Byte 139:          - Data.JointUpperLimit.E3 HW LB;
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
            # Get Response.WorkAreaNoReturn
            self._response.WorkAreaNoReturn = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Reserve
            self._response.Reserve = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.Timestamp.IEC_DATE
            self._response.WorkAreaData.Timestamp.IEC_DATE = ResponseData.GetIecDate()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.Timestamp.IEC_TIME
            self._response.WorkAreaData.Timestamp.IEC_TIME = ResponseData.GetIecTime()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.AreaType
            self._response.WorkAreaData.AreaType = AreaType(ResponseData.GetUsint().value)
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Reserve
            self._response.Reserve = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.AreaMode
            self._response.WorkAreaData.AreaMode = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.ReactionMode
            self._response.WorkAreaData.ReactionMode = WorkAreaReactionMode(ResponseData.GetUsint().value)
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.ActiveModification
            self._response.WorkAreaData.ActiveModification = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.DefinitionMode
            self._response.WorkAreaData.DefinitionMode = DefinitionMode(ResponseData.GetUsint().value)
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.FrameNo
            self._response.WorkAreaData.FrameNo = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.ZeroPointX
            self._response.WorkAreaData.ZeroPointX = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.ZeroPointY
            self._response.WorkAreaData.ZeroPointY = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.ZeroPointZ
            self._response.WorkAreaData.ZeroPointZ = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.X.LowerLimit
            self._response.WorkAreaData.X.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.X.UpperLimit
            self._response.WorkAreaData.X.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.Y.LowerLimit
            self._response.WorkAreaData.Y.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.Y.UpperLimit
            self._response.WorkAreaData.Y.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.Z.LowerLimit
            self._response.WorkAreaData.Z.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.Z.UpperLimit
            self._response.WorkAreaData.Z.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.Radius
            self._response.WorkAreaData.Radius = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J1Limit.LowerLimit
            self._response.WorkAreaData.J1Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J2Limit.LowerLimit
            self._response.WorkAreaData.J2Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J3Limit.LowerLimit
            self._response.WorkAreaData.J3Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J4Limit.LowerLimit
            self._response.WorkAreaData.J4Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J5Limit.LowerLimit
            self._response.WorkAreaData.J5Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J6Limit.LowerLimit
            self._response.WorkAreaData.J6Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E1Limit.LowerLimit
            self._response.WorkAreaData.E1Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J1Limit.UpperLimit
            self._response.WorkAreaData.J1Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J2Limit.UpperLimit
            self._response.WorkAreaData.J2Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J3Limit.UpperLimit
            self._response.WorkAreaData.J3Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J4Limit.UpperLimit
            self._response.WorkAreaData.J4Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J5Limit.UpperLimit
            self._response.WorkAreaData.J5Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.J6Limit.UpperLimit
            self._response.WorkAreaData.J6Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E1Limit.UpperLimit
            self._response.WorkAreaData.E1Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E2Limit.LowerLimit
            self._response.WorkAreaData.E2Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E3Limit.LowerLimit
            self._response.WorkAreaData.E3Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E4Limit.LowerLimit
            self._response.WorkAreaData.E4Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E5Limit.LowerLimit
            self._response.WorkAreaData.E5Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E6Limit.LowerLimit
            self._response.WorkAreaData.E6Limit.LowerLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E2Limit.UpperLimit
            self._response.WorkAreaData.E2Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E3Limit.UpperLimit
            self._response.WorkAreaData.E3Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E4Limit.UpperLimit
            self._response.WorkAreaData.E4Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E5Limit.UpperLimit
            self._response.WorkAreaData.E5Limit.UpperLimit = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.WorkAreaData.E6Limit.UpperLimit
            self._response.WorkAreaData.E6Limit.UpperLimit = ResponseData.GetReal()
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
            MessageText = 'Response.WorkAreaNoReturn = {1}',
            Para1       =  str(self._response.WorkAreaNoReturn)
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
            MessageText = 'Response.WorkAreaData.Timestamp.IEC_DATE = {1}',
            Para1       =  str(self._response.WorkAreaData.Timestamp.IEC_DATE)
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
            MessageText = 'Response.WorkAreaData.Timestamp.IEC_TIME = {1}',
            Para1       =  str(self._response.WorkAreaData.Timestamp.IEC_TIME)
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
            MessageText = 'Response.WorkAreaData.AreaType = {1}',
            Para1       =  str(self._response.WorkAreaData.AreaType)
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
            MessageText = 'Response.WorkAreaData.AreaMode = {1}',
            Para1       =  str(self._response.WorkAreaData.AreaMode)
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
            MessageText = 'Response.WorkAreaData.ReactionMode = {1}',
            Para1       =  str(self._response.WorkAreaData.ReactionMode)
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
            MessageText = 'Response.WorkAreaData.ActiveModification = {1}',
            Para1       =  str(self._response.WorkAreaData.ActiveModification)
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
            MessageText = 'Response.WorkAreaData.DefinitionMode = {1}',
            Para1       =  str(self._response.WorkAreaData.DefinitionMode)
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
            MessageText = 'Response.WorkAreaData.FrameNo = {1}',
            Para1       =  str(self._response.WorkAreaData.FrameNo)
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
            MessageText = 'Response.WorkAreaData.ZeroPointX = {1}',
            Para1       =  str(self._response.WorkAreaData.ZeroPointX)
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
            MessageText = 'Response.WorkAreaData.ZeroPointY = {1}',
            Para1       =  str(self._response.WorkAreaData.ZeroPointY)
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
            MessageText = 'Response.WorkAreaData.ZeroPointZ = {1}',
            Para1       =  str(self._response.WorkAreaData.ZeroPointZ)
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
            MessageText = 'Response.WorkAreaData.X.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.X.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.X.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.X.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.Y.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.Y.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.Y.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.Y.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.Z.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.Z.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.Z.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.Z.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.Radius = {1}',
            Para1       =  str(self._response.WorkAreaData.Radius)
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
            MessageText = 'Response.WorkAreaData.J1Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J1Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.J2Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J2Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.J3Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J3Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.J4Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J4Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.J5Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J5Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.J6Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J6Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.E1Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E1Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.J1Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J1Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.J2Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J2Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.J3Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J3Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.J4Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J4Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.J5Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J5Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.J6Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.J6Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.E1Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E1Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.E2Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E2Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.E3Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E3Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.E4Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E4Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.E5Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E5Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.E6Limit.LowerLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E6Limit.LowerLimit)
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
            MessageText = 'Response.WorkAreaData.E2Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E2Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.E3Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E3Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.E4Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E4Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.E5Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E5Limit.UpperLimit)
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
            MessageText = 'Response.WorkAreaData.E6Limit.UpperLimit = {1}',
            Para1       =  str(self._response.WorkAreaData.E6Limit.UpperLimit)
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
"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_WriteLoadDataFB
Author:      Thorsten Brach
Date:        2026-01-21

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
import math

from RobotLibrary.Functions.ToString import VALID_REAL_TO_STRING
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


from .Structures.WriteLoadDataParCmd import WriteLoadDataParCmd
from .Structures.WriteLoadDataOutCmd import WriteLoadDataOutCmd
from .Structures.WriteLoadDataRecvData import WriteLoadDataRecvData
from .Structures.WriteLoadDataSendData import WriteLoadDataSendData
#endregion


class MC_WriteLoadDataFB( RobotLibraryBaseExecuteFB):
    """Function block to write load data to the robot controller."""
    
    #VAR_INPUT

    ProcessingMode  : ProcessingModeEnum
    """Processing Mode"""

    SequenceFlag    : SequenceFlagEnum
    """Defines the target sequence in which the command will be executed"""
    
    ParCmd          : WriteLoadDataParCmd
    """command parameter"""
    
    #VAR_OUTPUT
    CommandBuffered : bool
    """Command is transferred and confirmed by the RC"""
    CommandAborted  : bool
    """The command was aborted by another command"""
    CommandInterrupted : bool
    """TRUE, while command is interrupted during execution and can be continued."""


    OutCmd          : WriteLoadDataOutCmd
    """command outputs"""

    #VAR
    _parCmd          : WriteLoadDataParCmd
    """ internal copy of command parameter """
    _command         : WriteLoadDataSendData
    """ command data to send """
    _response        : WriteLoadDataRecvData
    """ response data received """
    
    
    #------------------------------------------------------------
    # Constructor + Initialization
    #------------------------------------------------------------
    def __init__(self):
        
        super().__init__()
        
        # Initialize Base
        self.MyType   = self.__class__.__name__
        self.ExecMode = ExecutionMode.PARALLEL
        self.Priority = PriorityLevel.NORMAL

        # Initialize VAR_INPUT
        self.ProcessingMode  = ProcessingModeEnum.PARALLEL
        self.SequenceFlag    = SequenceFlagEnum.PRIMARY_SEQUENCE
        self.ParCmd          = WriteLoadDataParCmd()
        
        # Initialize VAR_OUTPUT
        self.CommandBuffered = False
        self.OutCmd          = WriteLoadDataOutCmd()
        
        # Initialize VAR
        self._parCmd         = WriteLoadDataParCmd()
        self._command        = WriteLoadDataSendData()
        self._response       = WriteLoadDataRecvData()


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
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.WriteLoadData.value

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
                Para1       = self.ProcessingMode.toString()
            )
            return CheckParameterValid


        # Check ProcessingModea valid ? 
        if (( self.ProcessingMode != ProcessingModeEnum.BUFFERED ) and
            ( self.ProcessingMode != ProcessingModeEnum.ABORTING ) and 
            ( self.ProcessingMode != ProcessingModeEnum.PARALLEL )) : 
                    
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_PROCESSINGMODE_NOT_ALLOWED, Overwrite = True )
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ProcessingMode = {1}',
                Para1       = self.ProcessingMode.toString()
            )
            return CheckParameterValid


        # Check SequenceFlag valid ? 
        if (( self.SequenceFlag != SequenceFlagEnum.NO_SEQUENCE        ) and
            ( self.SequenceFlag != SequenceFlagEnum.PRIMARY_SEQUENCE   ) and
            ( self.SequenceFlag != SequenceFlagEnum.SECONDARY_SEQUENCE )) :
            
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_SEQFLAG_NOT_ALLOWED, Overwrite = True )
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter SequenceFlag = {1}',
                Para1       = self.SequenceFlag.toString()
            )
            return CheckParameterValid


        # Check ParCmd.LoadNo valid ? 
        if (( self.ParCmd.LoadNo <= 0                                                  ) or
            ( self.ParCmd.LoadNo >  254                                                ) or
            ( self.ParCmd.LoadNo >  AxesGroup.State.ConfigurationData.HighestLoadIndex ) or
            ( self.ParCmd.LoadNo >  AxesGroup.State.UnifiedLoadIndex                   )) :
        
            # Parameter not valid
            CheckParameterValid = False

            # Check LoadNo available on RC ? 
            if ( self.ParCmd.LoadNo > AxesGroup.State.ConfigurationData.HighestLoadIndex ):
                
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
                Para1       = str(self.ParCmd.LoadNo)
            )
            return CheckParameterValid


        # Check ParCmd.LoadData.X ? 
        if ( not math.isfinite(self.ParCmd.LoadData.X.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LoadData.X = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LoadData.X)
            )
            return CheckParameterValid


        # Check ParCmd.LoadData.Y ? 
        if ( not math.isfinite(self.ParCmd.LoadData.Y.value) ) :
            
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
                MessageText = 'Invalid Parameter ParCmd.LoadData.Y = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LoadData.Y)
            )
            return CheckParameterValid


        # Check ParCmd.LoadData.Z ? 
        if ( not math.isfinite(self.ParCmd.LoadData.Z.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LoadData.Z = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LoadData.Z)
            )
            return CheckParameterValid                          


        # Check ParCmd.LoadData.Rx ? 
        if ( not math.isfinite(self.ParCmd.LoadData.Rx.value) ) :

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
                MessageText = 'Invalid Parameter ParCmd.LoadData.Rx = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LoadData.Rx)
            )
            return CheckParameterValid


        # Check ParCmd.LoadData.Ry ? 
        if ( not math.isfinite(self.ParCmd.LoadData.Ry.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LoadData.Ry = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LoadData.Ry)
            )
            return CheckParameterValid                          


        # Check ParCmd.LoadData.Rz ? 
        if ( not math.isfinite(self.ParCmd.LoadData.Rz.value) ) :

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
                MessageText = 'Invalid Parameter ParCmd.LoadData.Rz = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LoadData.Rz)
            )
            return CheckParameterValid                          


        # Check ParCmd.LoadData.Mass ? 
        if ( not math.isfinite(self.ParCmd.LoadData.Mass.value) ) :

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
                MessageText = 'Invalid Parameter ParCmd.LoadData.Mass = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LoadData.Mass)
            )
            return CheckParameterValid                          


        # Check ParCmd.LoadData.Ix ? 
        if ( not math.isfinite(self.ParCmd.LoadData.Ix.value) ) :

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
                MessageText = 'Invalid Parameter ParCmd.LoadData.Ix = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LoadData.Ix)
            )
            return CheckParameterValid                          


        # Check ParCmd.LoadData.Iy ? 
        if ( not math.isfinite(self.ParCmd.LoadData.Iy.value) ) :

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
                MessageText = 'Invalid Parameter ParCmd.LoadData.Iy = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LoadData.Iy)
            )
            return CheckParameterValid                          


        # Check ParCmd.LoadData.Iz ? 
        if ( not math.isfinite(self.ParCmd.LoadData.Iz.value) ) :

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
                MessageText = 'Invalid Parameter ParCmd.LoadData.Iz = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LoadData.Iz)
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
        
        # Table 6-132: Sent CMD payload (PLC to RC) of "WriteLoadData"
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
        # Byte 04 : DATE LoadData.Date
        # Byte 05 : 
        # Byte 06 : TIME_OF_DAY LoadData.Time
        # Byte 07 : 
        # Byte 08 : 
        # Byte 09 : REAL LoadData.X
        # Byte 10 : 
        # Byte 11 : 
        # Byte 12 : 
        # Byte 13 : REAL LoadData.Y
        # Byte 14 : 
        # Byte 15 : 
        # Byte 16 : 
        # Byte 17 : REAL LoadData.Z
        # Byte 18 : 
        # Byte 19 : 
        # Byte 20 : 
        # Byte 21 : REAL LoadData.RX
        # Byte 22 : 
        # Byte 23 : 
        # Byte 24 : 
        # Byte 25 : REAL LoadData.RY
        # Byte 26 : 
        # Byte 27 : 
        # Byte 28 : 
        # Byte 29 : REAL LoadData.RZ
        # Byte 30 : 
        # Byte 31 : 
        # Byte 32 : 
        # Byte 33 : REAL LoadData.Mass
        # Byte 34 : 
        # Byte 35 : 
        # Byte 36 : 
        # Byte 37 : REAL LoadData.IX
        # Byte 38 : 
        # Byte 39 : 
        # Byte 40 : 
        # Byte 41 : REAL LoadData.IY
        # Byte 42 : 
        # Byte 43 : 
        # Byte 44 : 
        # Byte 45 : REAL LoadData.IZ
        # Byte 46 : 
        # Byte 47 : 
        # Byte 48 : 
        # Byte 49 : USINT LoadNo
        # --------------------------
        # endregion

        # set command parameter 
        self._command.CmdTyp        = CmdType.WriteFrameData
        self._command.ExecMode      = self. ExecMode
        self._command.ParSeq        = self._command.ParSeq
        self._command.Priority      = self. Priority
        self._command.LoadData      = self._parCmd.LoadData
        self._command.LoadNo.value  = self._parCmd.LoadNo

        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Timestamp.IEC_DATE
            self.CommandData.AddIecDate(self._command.LoadData.Timestamp.IEC_DATE)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Timestamp.IEC_TIME
            self.CommandData.AddIecTime(self._command.LoadData.Timestamp.IEC_TIME)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.X
            self.CommandData.AddReal(self._command.LoadData.X)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Y
            self.CommandData.AddReal(self._command.LoadData.Y)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Z
            self.CommandData.AddReal(self._command.LoadData.Z)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Rx
            self.CommandData.AddReal(self._command.LoadData.Rx)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Ry
            self.CommandData.AddReal(self._command.LoadData.Ry)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Rz
            self.CommandData.AddReal(self._command.LoadData.Rz)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Mass
            self.CommandData.AddReal(self._command.LoadData.Mass)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Ix
            self.CommandData.AddReal(self._command.LoadData.Ix)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Iy
            self.CommandData.AddReal(self._command.LoadData.Iy)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LoadData.Iz
            self.CommandData.AddReal(self._command.LoadData.Iz)
            # inc parameter counter
            _parameterCnt += 1


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
            MessageText = 'Command.LoadData.Timestamp.IEC_DATE = {1}',
            Para1       =  str(self._command.LoadData.Timestamp.IEC_DATE)
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
            MessageText = 'Command.LoadData.Timestamp.IEC_TIME = {1}',
            Para1       =  str(self._command.LoadData.Timestamp.IEC_TIME)
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
            MessageText = 'Command.LoadData.X = {1}',
            Para1       =  str(self._command.LoadData.X)
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
            MessageText = 'Command.LoadData.Y = {1}',
            Para1       =  str(self._command.LoadData.Y)
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
            MessageText = 'Command.LoadData.Z = {1}',
            Para1       =  str(self._command.LoadData.Z)
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
            MessageText = 'Command.LoadData.Rx = {1}',
            Para1       =  str(self._command.LoadData.Rx)
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
            MessageText = 'Command.LoadData.Ry = {1}',
            Para1       =  str(self._command.LoadData.Ry)
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
            MessageText = 'Command.LoadData.Rz = {1}',
            Para1       =  str(self._command.LoadData.Rz)
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
            MessageText = 'Command.LoadData.Mass = {1}',
            Para1       =  str(self._command.LoadData.Mass)
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
            MessageText = 'Command.LoadData.Ix = {1}',
            Para1       =  str(self._command.LoadData.Ix)
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
            MessageText = 'Command.LoadData.Iy = {1}',
            Para1       =  str(self._command.LoadData.Iy)
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
            MessageText = 'Command.LoadData.Iz = {1}',
            Para1       =  str(self._command.LoadData.Iz)
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
            MessageText = 'Command.LoadData.LoadNo = {1}',
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
            self.OutCmd = WriteLoadDataOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :

            # Update results
            pass


    #--------------------------------------------------------
    # OnUpdateStateFlags - update state flags
    #--------------------------------------------------------
    def OnUpdateStateFlags(self, State : CmdMessageState) -> None:
        """
        Update state flags according to received state
        """

        # Reset State flags
        self.CommandAborted     = False
        self.CommandInterrupted = False
        self.Done               = False

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
                        self.OutCmd = WriteLoadDataOutCmd()
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
                                                             LoadNo     = self._parCmd.LoadNo, 
                                                             LoadData   = self._parCmd.LoadData)
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

        # Table 6-133: Received CMD payload (RC to PLC) of "WriteLoadData"
        # --------------------------
        # Header
        # --------------------------
        # Byte 00 : USINT   - ParSeq | State     
        # Byte 01 : SINT    - AlarmMessageSeverity    
        # Byte 02 : UINT    - AlarmMessageCode HB
        # Byte 03 :         - AlarmMessageCode LB
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


    #--------------------------------------------------------
    # Reset - reset internal variables
    #--------------------------------------------------------
    def Reset(self) -> int:
        """ Reset internal variables """

        self.Done               = False
        self.Busy               = False
        self.CommandBuffered    = False
        self.CommandAborted     = False
        self.CommandInterrupted = False

        return super().Reset()
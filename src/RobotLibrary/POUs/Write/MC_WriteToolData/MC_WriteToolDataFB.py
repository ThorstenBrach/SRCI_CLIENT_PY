"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_WriteToolDataFB
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


from .Structures.WriteToolDataParCmd import WriteToolDataParCmd
from .Structures.WriteToolDataOutCmd import WriteToolDataOutCmd
from .Structures.WriteToolDataRecvData import WriteToolDataRecvData
from .Structures.WriteToolDataSendData import WriteToolDataSendData
#endregion


class MC_WriteToolDataFB( RobotLibraryBaseExecuteFB):
    """Function block to write tool data to the robot controller."""
    
    #VAR_INPUT

    ProcessingMode  : ProcessingModeEnum
    """Processing Mode"""

    SequenceFlag    : SequenceFlagEnum
    """Defines the target sequence in which the command will be executed"""
    
    ParCmd          : WriteToolDataParCmd
    """command parameter"""
    
    #VAR_OUTPUT
    CommandBuffered : bool
    """Command is transferred and confirmed by the RC"""
    CommandAborted  : bool
    """The command was aborted by another command"""
    CommandInterrupted : bool
    """TRUE, while command is interrupted during execution and can be continued."""


    OutCmd          : WriteToolDataOutCmd
    """command outputs"""

    #VAR
    _parCmd          : WriteToolDataParCmd
    """ internal copy of command parameter """
    _command         : WriteToolDataSendData
    """ command data to send """
    _response        : WriteToolDataRecvData
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
        self.ParCmd          = WriteToolDataParCmd()
        
        # Initialize VAR_OUTPUT
        self.CommandBuffered = False
        self.OutCmd          = WriteToolDataOutCmd()
        
        # Initialize VAR
        self._parCmd         = WriteToolDataParCmd()
        self._command        = WriteToolDataSendData()
        self._response       = WriteToolDataRecvData()


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
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.WriteToolData.value

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


        # Check ParCmd.ToolNo valid ? 
        if (( self.ParCmd.ToolNo < 0                                                  ) or
            ( self.ParCmd.ToolNo > 254                                                ) or
            ( self.ParCmd.ToolNo > AxesGroup.State.ConfigurationData.HighestToolIndex ) or
            ( self.ParCmd.ToolNo > AxesGroup.State.UnifiedToolIndex                   )) :
        
            # Parameter not valid
            CheckParameterValid = False

            # Check ToolNo available on RC ? 
            if ( self.ParCmd.ToolNo > AxesGroup.State.ConfigurationData.HighestToolIndex ):
                
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
                Para1       = str(self.ParCmd.ToolNo)
            )
            return CheckParameterValid


        # Check ParCmd.LoadNo valid ? 
        if (( self.ParCmd.ToolData.LoadNo.value < 0   ) or
            ( self.ParCmd.ToolData.LoadNo.value > 254 )) :
        
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
                MessageText = 'Invalid Parameter ParCmd.ToolData.LoadNo = {1}',
                Para1       = str(self.ParCmd.ToolData.LoadNo)
            )
            return CheckParameterValid


        # Check ParCmd.LoadData.X ? 
        if ( not math.isfinite(self.ParCmd.ToolData.X.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.ToolData.X = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.ToolData.X)
            )
            return CheckParameterValid


        # Check ParCmd.ToolData.Y ? 
        if ( not math.isfinite(self.ParCmd.ToolData.Y.value) ) :
            
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
                MessageText = 'Invalid Parameter ParCmd.ToolData.Y = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.ToolData.Y)
            )
            return CheckParameterValid


        # Check ParCmd.ToolData.Z ? 
        if ( not math.isfinite(self.ParCmd.ToolData.Z.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.ToolData.Z = {1}',
                Para1       = str(self.ParCmd.ToolData.Z)
            )
            return CheckParameterValid                          


        # Check ParCmd.ToolData.Rx ? 
        if ( not math.isfinite(self.ParCmd.ToolData.Rx.value) ) :

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
                MessageText = 'Invalid Parameter ParCmd.ToolData.Rx = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.ToolData.Rx)
            )
            return CheckParameterValid


        # Check ParCmd.ToolData.Ry ? 
        if ( not math.isfinite(self.ParCmd.ToolData.Ry.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.ToolData.Ry = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.ToolData.Ry)
            )
            return CheckParameterValid                          


        # Check ParCmd.ToolData.Rz ? 
        if ( not math.isfinite(self.ParCmd.ToolData.Rz.value) ) :

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
                MessageText = 'Invalid Parameter ParCmd.ToolData.Rz = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.ToolData.Rz)
            )
            return CheckParameterValid

        # Check ParCmd.ToolData.ID valid ? 
        if (( self.ParCmd.ToolData.ID.value < 0   ) or
            ( self.ParCmd.ToolData.ID.value > 255 )) :
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
                MessageText = 'Invalid Parameter ParCmd.ToolData.ID = {1}',
                Para1       = str(self.ParCmd.ToolData.ID)
            )
            return CheckParameterValid


        # Check ParCmd.ToolData.ExternalTCP valid ? 
        if (( self.ParCmd.ToolData.ExternalTCP.value != False ) and #noqa
            ( self.ParCmd.ToolData.ExternalTCP.value != True  )) :  #noqa
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
                MessageText = 'Invalid Parameter ParCmd.ToolData.ExternalTCP = {1}',
                Para1       = str(self.ParCmd.ToolData.ExternalTCP)
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
        
        # Table 6-126: Sent CMD payload (PLC to RC) of "WriteToolData"
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
        # Byte 04 : DATE ToolData.Date
        # Byte 05 : 
        # Byte 06 : TIME_OF_DAY ToolData.Time
        # Byte 07 : 
        # Byte 08 : 
        # Byte 09 : 
        # Byte 10 : REAL ToolData.X
        # Byte 11 : 
        # Byte 12 : 
        # Byte 13 : 
        # Byte 14 : REAL ToolData.Y
        # Byte 15 : 
        # Byte 16 : 
        # Byte 17 :
        # Byte 18 : REAL ToolData.Z
        # Byte 19 : 
        # Byte 20 : 
        # Byte 21 : 
        # Byte 22 : REAL ToolData.RX
        # Byte 23 : 
        # Byte 24 :
        # Byte 25 : 
        # Byte 26 : REAL ToolData.RY
        # Byte 27 : 
        # Byte 28 :
        # Byte 29 : 
        # Byte 30 : REAL ToolData.RZ
        # Byte 31 : 
        # Byte 32 :
        # Byte 33 : 
        # Byte 34 : USINT ToolData.ID
        # Byte 35 : USINT ToolData.LoadNo
        # Byte 36 : BOOL ToolData.ExternalTCP
        # Byte 37 : BYTE Reserved
        # Byte 38 : USINT ToolNo
        # --------------------------
        # endregion

        # set command parameter 
        self._command.CmdTyp        = CmdType.WriteFrameData
        self._command.ExecMode      = self. ExecMode
        self._command.ParSeq        = self._command.ParSeq
        self._command.Priority      = self. Priority
        self._command.ToolData      = self._parCmd.ToolData
        self._command.ToolNo.value  = self._parCmd.ToolNo

        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.Timestamp.IEC_DATE
            self.CommandData.AddIecDate(self._command.ToolData.Timestamp.IEC_DATE)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.Timestamp.IEC_TIME
            self.CommandData.AddIecTime(self._command.ToolData.Timestamp.IEC_TIME)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.X
            self.CommandData.AddReal(self._command.ToolData.X)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.Y
            self.CommandData.AddReal(self._command.ToolData.Y)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.Z
            self.CommandData.AddReal(self._command.ToolData.Z)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.Rx
            self.CommandData.AddReal(self._command.ToolData.Rx)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.Ry
            self.CommandData.AddReal(self._command.ToolData.Ry)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.Rz
            self.CommandData.AddReal(self._command.ToolData.Rz)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.ID
            self.CommandData.AddUsint(self._command.ToolData.ID)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.LoadNo
            self.CommandData.AddUsint(self._command.ToolData.LoadNo)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolData.ExternalTCP
            self.CommandData.AddBool(self._command.ToolData.ExternalTCP)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.Reserve
            self.CommandData.AddByte(self._command.Reserve)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolNo
            self.CommandData.AddUsint(self._command.ToolNo)
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
            MessageText = 'Command.ToolData.Timestamp.IEC_DATE = {1}',
            Para1       =  str(self._command.ToolData.Timestamp.IEC_DATE)
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
            MessageText = 'Command.ToolData.Timestamp.IEC_TIME = {1}',
            Para1       =  str(self._command.ToolData.Timestamp.IEC_TIME)
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
            MessageText = 'Command.ToolData.X = {1}',
            Para1       =  str(self._command.ToolData.X)
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
            MessageText = 'Command.ToolData.Y = {1}',
            Para1       =  str(self._command.ToolData.Y)
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
            MessageText = 'Command.ToolData.Z = {1}',
            Para1       =  str(self._command.ToolData.Z)
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
            MessageText = 'Command.ToolData.Rx = {1}',
            Para1       =  str(self._command.ToolData.Rx)
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
            MessageText = 'Command.ToolData.Ry = {1}',
            Para1       =  str(self._command.ToolData.Ry)
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
            MessageText = 'Command.ToolData.Rz = {1}',
            Para1       =  str(self._command.ToolData.Rz)
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
            MessageText = 'Command.ToolData.ID = {1}',
            Para1       =  str(self._command.ToolData.ID)
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
            MessageText = 'Command.ToolData.LoadNo = {1}',
            Para1       =  str(self._command.ToolData.LoadNo)
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
            MessageText = 'Command.ToolData.ExternalTCP = {1}',
            Para1       =  str(self._command.ToolData.ExternalTCP)
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
            MessageText = 'Command.ToolData.Reserve = {1}',
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
            MessageText = 'Command.ToolData.ToolNo = {1}',
            Para1       =  str(self._command.ToolNo)
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
            self.OutCmd = WriteToolDataOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :

            # Update results
            pass


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
                        self.OutCmd = WriteToolDataOutCmd()
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
                        AxesGroup.SystemData.UpdateToolData( Caller     = self,
                                                             SystemTime = AxesGroup.State.SystemTime,
                                                             ToolNo     = self._parCmd.ToolNo, 
                                                             ToolData   = self._parCmd.ToolData)
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
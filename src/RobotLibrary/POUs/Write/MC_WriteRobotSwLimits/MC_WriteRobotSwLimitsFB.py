"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_WriteRobotSwLimitsFB
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


from .Structures.WriteRobotSwLimitsParCmd import WriteRobotSwLimitsParCmd
from .Structures.WriteRobotSwLimitsOutCmd import WriteRobotSwLimitsOutCmd
from .Structures.WriteRobotSwLimitsRecvData import WriteRobotSwLimitsRecvData
from .Structures.WriteRobotSwLimitsSendData import WriteRobotSwLimitsSendData
#endregion


class MC_WriteRobotSwLimitsFB( RobotLibraryBaseExecuteFB):
    """Function block to write software limits data to the robot controller."""
    
    #VAR_INPUT
    
    ParCmd          : WriteRobotSwLimitsParCmd
    """command parameter"""
    
    #VAR_OUTPUT
    CommandBuffered : bool
    """Command is transferred and confirmed by the RC"""

    OutCmd          : WriteRobotSwLimitsOutCmd
    """command outputs"""

    #VAR
    _parCmd          : WriteRobotSwLimitsParCmd
    """ internal copy of command parameter """
    _command         : WriteRobotSwLimitsSendData
    """ command data to send """
    _response        : WriteRobotSwLimitsRecvData
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
        self.ParCmd          = WriteRobotSwLimitsParCmd()
        
        # Initialize VAR_OUTPUT
        self.CommandBuffered = False
        self.OutCmd          = WriteRobotSwLimitsOutCmd()
        
        # Initialize VAR
        self._parCmd         = WriteRobotSwLimitsParCmd()
        self._command        = WriteRobotSwLimitsSendData()
        self._response       = WriteRobotSwLimitsRecvData()


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
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.WriteRobotSWLimits.value

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


        # Check ParCmd.LimitValues.J1LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J1LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J1LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J1LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J1UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J1UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J1UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J1UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J2LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J2LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J2LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J2LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J2UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J2UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J2UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J2UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J3LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J3LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J3LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J3LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J3UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J3UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J3UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J3UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J4LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J4LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J4LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J4LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J4UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J4UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J4UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J4UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J5LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J5LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J5LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J5LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J5UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J5UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J5UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J5UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J6LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J6LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J6LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J6LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.J6UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.J6UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.J6UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.J6UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E1LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E1LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E1LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E1LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E1UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E1UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E1UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E1UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E2LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E2LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E2LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E2LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E2UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E2UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E2UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E2UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E3LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E3LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E3LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E3LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E3UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E3UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E3UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E3UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E4LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E4LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E4LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E4LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E4UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E4UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E4UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E4UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E5LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E5LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E5LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E5LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E5UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E5UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E5UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E5UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E6LowerLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E6LowerLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E6LowerLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E6LowerLimit)
            )
            return CheckParameterValid


        # Check ParCmd.LimitValues.E6UpperLimit ?
        if ( not math.isfinite(self.ParCmd.LimitValues.E6UpperLimit.value) ) :
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
                MessageText = 'Invalid Parameter ParCmd.LimitValues.E6UpperLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.LimitValues.E6UpperLimit)
            )
            return CheckParameterValid


        # Check ParCmd.ResetToFactoryDefaults ?
        if (( self.ParCmd.ResetToFactoryDefaults != False) and #noqa
            ( self.ParCmd.ResetToFactoryDefaults != True )) :  #noqa
            
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
                MessageText = 'Invalid Parameter ParCmd.ResetToFactoryDefaults = {1}',
                Para1       = str(self.ParCmd.ResetToFactoryDefaults)
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
        
        # Table 6-185: Sent CMD payload (PLC to RC) of "WriteRobotSWLimits"
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
        # Byte 04 : DATE Date
        # Byte 05 : 
        # Byte 06 : TIME_OF_DAY Time
        # Byte 07 : 
        # Byte 08 : 
        # Byte 09 : REAL J1LowerLimit
        # Byte 10 : 
        # Byte 11 : 
        # Byte 12 : REAL J2LowerLimit
        # Byte 13 : 
        # Byte 14 : 
        # Byte 15 : REAL J3LowerLimit
        # Byte 16 : 
        # Byte 17 : 
        # Byte 18 : REAL J4LowerLimit
        # Byte 19 : 
        # Byte 20 : 
        # Byte 21 : REAL J5LowerLimit
        # Byte 22 : 
        # Byte 23 : 
        # Byte 24 : REAL J6LowerLimit
        # Byte 25 : 
        # Byte 26 : 
        # Byte 27 : REAL E1LowerLimit
        # Byte 28 : 
        # Byte 29 : 
        # Byte 30 : REAL J1UpperLimit
        # Byte 31 : 
        # Byte 32 : 
        # Byte 33 : REAL J2UpperLimit
        # Byte 34 : 
        # Byte 35 : 
        # Byte 36 : REAL J3UpperLimit
        # Byte 37 : 
        # Byte 38 : 
        # Byte 39 : REAL J4UpperLimit
        # Byte 40 : 
        # Byte 41 : 
        # Byte 42 : REAL J5UpperLimit
        # Byte 43 : 
        # Byte 44 : 
        # Byte 45 : REAL J6UpperLimit
        # Byte 46 : 
        # Byte 47 : 
        # Byte 48 : REAL E1UpperLimit
        # Byte 49 : 
        # Byte 50 : 
        # Byte 51 : REAL E2LowerLimit
        # Byte 52 : 
        # Byte 53 : 
        # Byte 54 : REAL E3LowerLimit
        # Byte 55 : 
        # Byte 56 : 
        # Byte 57 : REAL E4LowerLimit
        # Byte 58 : 
        # Byte 59 : 
        # Byte 60 : REAL E5LowerLimit
        # Byte 61 : 
        # Byte 62 : 
        # Byte 63 : REAL E6LowerLimit
        # Byte 64 : 
        # Byte 65 : 
        # Byte 66 : REAL E2UpperLimit
        # Byte 67 : 
        # Byte 68 : 
        # Byte 69 : REAL E3UpperLimit
        # Byte 70 : 
        # Byte 71 : 
        # Byte 72 : REAL E4UpperLimit
        # Byte 73 : 
        # Byte 74 : 
        # Byte 75 : REAL E5UpperLimit
        # Byte 76 : 
        # Byte 77 : 
        # Byte 78 : REAL E6UpperLimit
        # Byte 79 : 
        # Byte 80 : 
        # Byte 81 : 
        # Byte 82 : BOOL ResetToFactoryDefault
        # --------------------------
        # endregion

        # set command parameter 
        self._command.CmdTyp                       = CmdType.WriteFrameData
        self._command.ExecMode                     = self. ExecMode
        self._command.ParSeq                       = self._command.ParSeq
        self._command.Priority                     = self. Priority
        self._command.LimitValues                  = self._parCmd.LimitValues
        self._command.ResetToFactoryDefaults.value = self._parCmd.ResetToFactoryDefaults

        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.Timestamp.IEC_DATE
            self.CommandData.AddIecDate(self._command.LimitValues.Timestamp.IEC_DATE)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.Timestamp.IEC_TIME
            self.CommandData.AddIecTime(self._command.LimitValues.Timestamp.IEC_TIME)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J1LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.J1LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J2LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.J2LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J3LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.J3LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J4LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.J4LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J5LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.J5LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J6LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.J6LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E1LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.E1LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J1UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.J1UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J2UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.J2UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J3UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.J3UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J4UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.J4UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J5UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.J5UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.J6UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.J6UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E1UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.E1UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E2LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.E2LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E3LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.E3LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E4LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.E4LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E5LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.E5LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E6LowerLimit
            self.CommandData.AddReal(self._command.LimitValues.E6LowerLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E2UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.E2UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E3UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.E3UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E4UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.E4UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E5UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.E5UpperLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LimitValues.E6UpperLimit
            self.CommandData.AddReal(self._command.LimitValues.E6UpperLimit)
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
            MessageText = 'Command.LimitValues.Timestamp.IEC_DATE = {1}',
            Para1       =  str(self._command.LimitValues.Timestamp.IEC_DATE)
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
            MessageText = 'Command.LimitValues.Timestamp.IEC_TIME = {1}',
            Para1       =  str(self._command.LimitValues.Timestamp.IEC_TIME)
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
            MessageText = 'Command.LimitValues.J1LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.J1LowerLimit)
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
            MessageText = 'Command.LimitValues.J2LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.J2LowerLimit)
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
            MessageText = 'Command.LimitValues.J3LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.J3LowerLimit)
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
            MessageText = 'Command.LimitValues.J4LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.J4LowerLimit)
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
            MessageText = 'Command.LimitValues.J5LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.J5LowerLimit)
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
            MessageText = 'Command.LimitValues.J6LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.J6LowerLimit)
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
            MessageText = 'Command.LimitValues.E1LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.E1LowerLimit)
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
            MessageText = 'Command.LimitValues.J1UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.J1UpperLimit)
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
            MessageText = 'Command.LimitValues.J2UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.J2UpperLimit)
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
            MessageText = 'Command.LimitValues.J3UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.J3UpperLimit)
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
            MessageText = 'Command.LimitValues.J4UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.J4UpperLimit)
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
            MessageText = 'Command.LimitValues.J5UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.J5UpperLimit)
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
            MessageText = 'Command.LimitValues.J6UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.J6UpperLimit)
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
            MessageText = 'Command.LimitValues.E1UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.E1UpperLimit)
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
            MessageText = 'Command.LimitValues.E2LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.E2LowerLimit)
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
            MessageText = 'Command.LimitValues.E3LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.E3LowerLimit)
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
            MessageText = 'Command.LimitValues.E4LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.E4LowerLimit)
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
            MessageText = 'Command.LimitValues.E5LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.E5LowerLimit)
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
            MessageText = 'Command.LimitValues.E6LowerLimit = {1}',
            Para1       =  str(self._command.LimitValues.E6LowerLimit)
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
            MessageText = 'Command.LimitValues.E2UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.E2UpperLimit)
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
            MessageText = 'Command.LimitValues.E3UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.E3UpperLimit)
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
            MessageText = 'Command.LimitValues.E4UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.E4UpperLimit)
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
            MessageText = 'Command.LimitValues.E5UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.E5UpperLimit)
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
            MessageText = 'Command.LimitValues.E6UpperLimit = {1}',
            Para1       =  str(self._command.LimitValues.E6UpperLimit)
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
            self.OutCmd = WriteRobotSwLimitsOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :

            # Update results            
            self.OutCmd.RestartRequested  = self._response.RestartRequested.value


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
                        self.OutCmd = WriteRobotSwLimitsOutCmd()
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
                        
                        # Update the RobotSwLimits in user defined system data 
                        AxesGroup.SystemData.UpdateSWLimits( LimitValues = self._parCmd.LimitValues )
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

        # Table 6-186: Received CMD payload (RC to PLC) of "WriteRobotSWLimits"
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
        # Byte 04 : BOOL       - RestartRequested
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
        if ( ResponseData.IsPayloadRemaining ):

            # Get Response.RestartRequested
            self._response.RestartRequested.value = ResponseData.GetBool().value
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
            MessageText = 'Response.RestartRequested = {1}',
            Para1       =  str(self._response.RestartRequested)
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
"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_MoveAxesAbsoluteFB
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
import math

from RobotLibrary.Functions.ToString import VALID_REAL_TO_STRING
from RobotLibrary.Functions.Convert import PERCENT_UINT_TO_REAL, REAL_TO_PERCENT_UINT
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
from RobotLibrary.Enumerations.Mode.BlendingMode import BlendingMode as BlendingModeEnum
from RobotLibrary.Enumerations.Mode.AbortingMode import AbortingMode as AbortingModeEnum
from RobotLibrary.Enumerations.Flag.SequenceFlag import SequenceFlag as SequenceFlagEnum


from .Structures.MoveAxesAbsoluteParCmd import MoveAxesAbsoluteParCmd
from .Structures.MoveAxesAbsoluteOutCmd import MoveAxesAbsoluteOutCmd
from .Structures.MoveAxesAbsoluteRecvData import MoveAxesAbsoluteRecvData
from .Structures.MoveAxesAbsoluteSendData import MoveAxesAbsoluteSendData
#endregion

class MC_MoveAxesAbsoluteFB( RobotLibraryBaseExecuteFB):
    """Function block to move axes to absolute positions."""
    
    #VAR_INPUT
    AbortingMode       : AbortingModeEnum
    """Parameter which determines the behavior towards the previously sent and still active or buffered commands"""
    SequenceFlag       : SequenceFlagEnum
    """Defines the target sequence in which the command will be executed"""
    
    ParCmd             : MoveAxesAbsoluteParCmd
    """command parameter"""
    
    #VAR_OUTPUT
    CommandBuffered    : bool
    """Command is transferred and confirmed by the RC"""
    
    Active             : bool
    """The command takes control of the motion of the according axis group"""

    CommandAborted     : bool
    """The command was aborted by another command."""

    CommandInterrupted : bool
    """TRUE, while command is interrupted during execution and can be continued"""

    OutCmd             : MoveAxesAbsoluteOutCmd
    """command outputs"""

    #VAR
    _parCmd            : MoveAxesAbsoluteParCmd
    """ internal copy of command parameter """
    _command           : MoveAxesAbsoluteSendData
    """ command data to send """
    _response          : MoveAxesAbsoluteRecvData
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
        self.AbortingMode = AbortingModeEnum.BUFFER
        self.SequenceFlag = SequenceFlagEnum.PRIMARY_SEQUENCE
        # Initialize VAR_INPUT
        self.ParCmd          = MoveAxesAbsoluteParCmd()
        
        # Initialize VAR_OUTPUT
        self.CommandBuffered    = False
        self.Active             = False
        self.CommandAborted     = False
        self.CommandInterrupted = False
        self.OutCmd             = MoveAxesAbsoluteOutCmd()
        
        # Initialize VAR
        self._parCmd            = MoveAxesAbsoluteParCmd()
        self._command           = MoveAxesAbsoluteSendData()
        self._response          = MoveAxesAbsoluteRecvData()


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
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.MoveAxesAbsolute.value

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

        # Check AbortingMode valid ? 
        if (( self.AbortingMode != AbortingModeEnum.BUFFER ) and
            ( self.AbortingMode != AbortingModeEnum.ABORT  )) :
        
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_ABORTINGMODE_INVALID, Overwrite = True )
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter AbortingMode = {1}',
                Para1       = str(self.AbortingMode)
            )
            return CheckParameterValid


        # Check SequenceFlag valid ? 
        if (( self.SequenceFlag != SequenceFlagEnum.PRIMARY_SEQUENCE   ) and
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
                Para1       = str(self.SequenceFlag)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.J1 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.J1) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.J1 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.J1)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.J2 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.J2) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.J2 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.J2)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.J3 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.J3) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.J3 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.J3)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.J4 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.J4) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.J4 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.J4)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.J5 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.J5) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.J5 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.J5)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.J6 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.J6) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.J6 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.J6)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.E1 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.E1) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.E1 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.E1)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.E2 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.E2) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.E2 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.E2)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.E3 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.E3) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.E3 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.E3)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.E4 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.E4) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.E4 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.E4)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.E5 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.E5) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.E5 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.E5)
            )
            return CheckParameterValid


        # Check ParCmd.JointPosition.E6 valid ?
        if ( not math.isfinite(self.ParCmd.JointPosition.E6) ) :
        
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
                MessageText = 'Invalid Parameter ParCmd.JointPosition.E6 = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JointPosition.E6)
            )
            return CheckParameterValid


        # Check ParCmd.VelocityRate valid ? 
        if  (( math.isfinite(self.ParCmd.VelocityRate) == False )  or #noqa
            ((               self.ParCmd.VelocityRate  <      0 )  and
             (               self.ParCmd.VelocityRate  !=    -1 )) or
             (               self.ParCmd.VelocityRate  >    100 )) :
            
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_VELOCITY_INVALID, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.VelocityRate = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.VelocityRate)
            )
            return CheckParameterValid


        # Check ParCmd.AccelerationRate valid ? 
        if  (( math.isfinite(self.ParCmd.AccelerationRate) == False )  or #noqa
            ((               self.ParCmd.AccelerationRate  <      0 )  and
             (               self.ParCmd.AccelerationRate  !=    -1 )) or
             (               self.ParCmd.AccelerationRate  >    100 )) :
            
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_ACCELERATION_INVALID, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.AccelerationRate = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.AccelerationRate)
            )
            return CheckParameterValid


        # Check ParCmd.DecelerationRate valid ? 
        if  (( math.isfinite(self.ParCmd.DecelerationRate) == False )  or #noqa
            ((               self.ParCmd.DecelerationRate  <      0 )  and
             (               self.ParCmd.DecelerationRate  !=    -1 )) or
             (               self.ParCmd.DecelerationRate  >    100 )) :
            
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_DECELERATION_INVALID, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.DecelerationRate = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.DecelerationRate)
            )
            return CheckParameterValid


        # Check ParCmd.JerkRate valid ? 
        if  (( math.isfinite(self.ParCmd.JerkRate) == False )  or #noqa
            ((               self.ParCmd.JerkRate  <      0 )  and
             (               self.ParCmd.JerkRate  !=    -1 )) or
             (               self.ParCmd.JerkRate  >    100 )) :
            
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_JERK_INVALID, Overwrite = True )
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.JerkRate = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.JerkRate)
            )
            return CheckParameterValid


        # Check ParCmd.ToolNo valid ? 
        if (( self.ParCmd.ToolNo <   0                                                ) or  
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


        # Check ParCmd.BlendingMode valid ? 
        if (( self.ParCmd.BlendingMode != BlendingModeEnum.EXACT_STOP           ) and   
            ( self.ParCmd.BlendingMode != BlendingModeEnum.DEFINED_VELOCITY     ) and
            ( self.ParCmd.BlendingMode != BlendingModeEnum.CORNER_DISTANCE      ) and
            ( self.ParCmd.BlendingMode != BlendingModeEnum.MAX_CORNER_DEVIATION ) and
            ( self.ParCmd.BlendingMode != BlendingModeEnum.CORNER_DISTANCE_2R   ) and
            ( self.ParCmd.BlendingMode != BlendingModeEnum.RAMP_OVERLAP         ) and
            ( self.ParCmd.BlendingMode != BlendingModeEnum.CORNER_DISTANCE_1R   )) :
            
            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_PAR_CMD, Overwrite = True )
            # Create log entry
            self.CreateLogMessage (
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.BlendingMode = {1}',
                Para1       = str(self.ParCmd.BlendingMode)
            )
            return CheckParameterValid


        for _idx in range(0, 2):
        
            # Check ParCmd.BlendingParameter valid ? 
            if  ( not math.isfinite(self.ParCmd.BlendingParameter[_idx]) ) :
            
                # Parameter not valid
                CheckParameterValid = False
                # Set error
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_JERK_INVALID, Overwrite = True )
                # Create log entry
                self.CreateLogMessage ( 
                    Timestamp   = AxesGroup.State.SystemTime,
                    MessageType = MessageType.CMD,
                    Severity    = Severity.ERROR,
                    MessageCode = self.ErrorID,
                    MessageText = 'Invalid Parameter ParCmd.BlendingParameter[{2}] = {1}',
                    Para1       = VALID_REAL_TO_STRING(self.ParCmd.BlendingParameter[_idx]), 
                    Para2       = str(_idx)
                )
                
                return CheckParameterValid
                break


        # Check ParCmd.MoveTime valid ? 
        if  ( self.ParCmd.MoveTime < 0 ):
        
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
                MessageText = 'Invalid Parameter ParCmd.MoveTime = {1}',
                Para1       = str(self.ParCmd.MoveTime)
            )

            return CheckParameterValid


        # Check ParCmd.Manipulation
        # -> no plausibility check for boolean

        for _idx  in  range(0, 4):
        
            # Check ParCmd.EmitterID valid ? 
            if  (( self.ParCmd.EmitterID[_idx] < -127 ) or
                 ( self.ParCmd.EmitterID[_idx] >  127 )) :

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
                    MessageText = 'Invalid Parameter ParCmd.EmitterID[{2}] = {1}',
                    Para1       = str(self.ParCmd.EmitterID[_idx]),
                    Para2       = str(_idx)
                )
                return CheckParameterValid
                break
            
        return CheckParameterValid

    #--------------------------------------------------------
    # CreateCommandPayload - create command payload
    #--------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup : AxesGroup) -> RobotLibraryCommandDataFB:
        
        # Parameter count
        _parameterCnt : int = 0

        #region Mapping table
        
        # Table 6-261: Sent CMD payload (PLC to RC) of "MoveAxesAbsolute
        # --------------------------
        # Header
        # --------------------------
        # --------------------------
        # Datablock
        # --------------------------
        # Byte 00 : UINT  - Type HB     
        # Byte 01 :       - Type LB    
        # Byte 02 : USINT - Reserve | ExecutionMode
        # Byte 03 : USINT - ParSeq  | Priority
        # --------------------------
        # Datablock
        # --------------------------
        # Byte 04 : SINT       - EmitterID[0]
        # Byte 05 : SINT       - EmitterID[1]
        # Byte 06 : SINT       - EmitterID[2]
        # Byte 07 : SINT       - EmitterID[3]
        # Byte 08 : SINT       - ListenerID
        # Byte 09 : BYTE       - Reserved
        # Byte 10 : UINT       - VelocityRate HW HB
        # Byte 11 :            - VelocityRate HW LB
        # Byte 12 : UINT       - AccelerationRate HW HB
        # Byte 13 :            - AccelerationRate HW LB
        # Byte 14 : UINT       - DecelerationRate HW HB
        # Byte 15 :            - DecelerationRate HW LB
        # Byte 16 : UINT       - JerkRate HW HB
        # Byte 17 :            - JerkRate HW LB
        # Byte 18 : USINT      - ToolNo
        # Byte 19 : USINT      - BlendingMode
        # Byte 20 : REAL       - BlendingParameter[0] HW HB
        # Byte 21 :            - BlendingParameter[0] HW LB
        # Byte 22 :            - BlendingParameter[0] LW HB
        # Byte 23 :            - BlendingParameter[0] LW LB
        # Byte 24 : REAL       - BlendingParameter[1] HW HB
        # Byte 25 :            - BlendingParameter[1] HW LB
        # Byte 26 :            - BlendingParameter[1] LW HB
        # Byte 27 :            - BlendingParameter[1] LW LB
        # Byte 28 : REAL       - JointPosition.J1 HW HB
        # Byte 29 :            - JointPosition.J1 HW LB
        # Byte 30 :            - JointPosition.J1 LW HB
        # Byte 31 :            - JointPosition.J1 LW LB
        # Byte 32 : REAL       - JointPosition.J2 HW HB
        # Byte 33 :            - JointPosition.J2 HW LB
        # Byte 34 :            - JointPosition.J2 LW HB
        # Byte 35 :            - JointPosition.J2 LW LB
        # Byte 36 : REAL       - JointPosition.J3 HW HB
        # Byte 37 :            - JointPosition.J3 HW LB
        # Byte 38 :            - JointPosition.J3 LW HB
        # Byte 39 :            - JointPosition.J3 LW LB
        # Byte 40 : REAL       - JointPosition.J4 HW HB
        # Byte 41 :            - JointPosition.J4 HW LB
        # Byte 42 :            - JointPosition.J4 LW HB
        # Byte 43 :            - JointPosition.J4 LW LB
        # Byte 44 : REAL       - JointPosition.J5 HW HB
        # Byte 45 :            - JointPosition.J5 HW LB
        # Byte 46 :            - JointPosition.J5 LW HB
        # Byte 47 :            - JointPosition.J5 LW LB
        # Byte 48 : REAL       - JointPosition.J6 HW HB
        # Byte 49 :            - JointPosition.J6 HW LB
        # Byte 50 :            - JointPosition.J6 LW HB
        # Byte 51 :            - JointPosition.J6 LW LB
        # Byte 52 : REAL       - JointPosition.E1 HW HB
        # Byte 53 :            - JointPosition.E1 HW LB
        # Byte 54 :            - JointPosition.E1 LW HB
        # Byte 55 :            - JointPosition.E1 LW LB
        # Byte 56 : BOOL       - Manipulation
        # Byte 57 : BYTE       - Reserve
        # Byte 58 : UINT       - Time HW HB
        # Byte 59 :            - Time HW LB
        # Byte 60 : REAL       - JointPosition.E2 HW HB
        # Byte 61 :            - JointPosition.E2 HW LB
        # Byte 62 :            - JointPosition.E2 LW HB
        # Byte 63 :            - JointPosition.E2 LW LB
        # Byte 64 : REAL       - JointPosition.E3 HW HB
        # Byte 65 :            - JointPosition.E3 HW LB
        # Byte 66 :            - JointPosition.E3 LW HB
        # Byte 67 :            - JointPosition.E3 LW LB
        # Byte 68 : REAL       - JointPosition.E4 HW HB
        # Byte 69 :            - JointPosition.E4 HW LB
        # Byte 70 :            - JointPosition.E4 LW HB
        # Byte 71 :            - JointPosition.E4 LW LB
        # Byte 72 : REAL       - JointPosition.E5 HW HB
        # Byte 73 :            - JointPosition.E5 HW LB
        # Byte 74 :            - JointPosition.E5 LW HB
        # Byte 75 :            - JointPosition.E5 LW LB
        # Byte 76 : REAL       - JointPosition.E6 HW HB
        # Byte 77 :            - JointPosition.E6 HW LB
        # Byte 78 :            - JointPosition.E6 LW HB
        # Byte 79 :            - JointPosition.E6 LW LB
        # endregion

        # set command parameter 
        self._command.CmdTyp                      = CmdType.MoveAxesAbsolute
        self._command.ExecMode                    = self. ExecMode
        self._command.ParSeq                      = self._command.ParSeq
        self._command.Priority                    = self. Priority

        self._command.EmitterID[0].value          = self._parCmd.EmitterID[0]
        self._command.EmitterID[1].value          = self._parCmd.EmitterID[1]
        self._command.EmitterID[2].value          = self._parCmd.EmitterID[2]
        self._command.EmitterID[3].value          = self._parCmd.EmitterID[3]
        self._command.ListenerID.value            = 0 
        self._command.Reserve.value               = 0

        self._command.VelocityRate                = REAL_TO_PERCENT_UINT(self._parCmd.VelocityRate     , IsOptional = False)
        self._command.AccelerationRate            = REAL_TO_PERCENT_UINT(self._parCmd.AccelerationRate , IsOptional = False)
        self._command.JerkRate                    = REAL_TO_PERCENT_UINT(self._parCmd.JerkRate         , IsOptional = True )
        self._command.DecelerationRate            = REAL_TO_PERCENT_UINT(self._parCmd.DecelerationRate , IsOptional = True )

        self._command.ToolNo.value                = self._parCmd.ToolNo
        self._command.BlendingMode                = self._parCmd.BlendingMode
        self._command.BlendingParameter[0].value  = self._parCmd.BlendingParameter[0]
        self._command.BlendingParameter[1].value  = self._parCmd.BlendingParameter[1]
        
        self._command.JointPosition               = self._parCmd.JointPosition
        self._command.Manipulation.value          = self._parCmd.Manipulation
        self._command.MoveTime.value              = self._parCmd.MoveTime


        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


        for _idx in range(0, 4 ) :
        
            # Check parameter must be added ? 
            if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)) :
                
                # add command.EmitterID[x]
                self.CommandData.AddSint(self._command.EmitterID[_idx])
                # inc parameter counter
                _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ListenerID
            self.CommandData.AddSint(self._command.ListenerID)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.Reserve
            self.CommandData.AddSint(self._command.Reserve)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.VelocityRate
            self.CommandData.AddUint(self._command.VelocityRate)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.AccelerationRate
            self.CommandData.AddUint(self._command.AccelerationRate)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.DecelerationRate
            self.CommandData.AddUint(self._command.DecelerationRate)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JerkRate
            self.CommandData.AddUint(self._command.JerkRate)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.ToolNo
            self.CommandData.AddUsint(self._command.ToolNo)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.BlendingMode
            self.CommandData.AddUsint(self._command.BlendingMode.TypeValue)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.BlendingParameter[0]
            self.CommandData.AddReal(self._command.BlendingParameter[0])
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.BlendingParameter[1]
            self.CommandData.AddReal(self._command.BlendingParameter[1])
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.J1
            self.CommandData.AddReal(self._command.JointPosition.J1)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.J2
            self.CommandData.AddReal(self._command.JointPosition.J2)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.J3
            self.CommandData.AddReal(self._command.JointPosition.J3)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.J4
            self.CommandData.AddReal(self._command.JointPosition.J4)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.J5
            self.CommandData.AddReal(self._command.JointPosition.J5)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.J6
            self.CommandData.AddReal(self._command.JointPosition.J6)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.E1
            self.CommandData.AddReal(self._command.JointPosition.E1)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.Manipulation
            self.CommandData.AddBool(self._command.Manipulation)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.Reserve2
            self.CommandData.AddByte(self._command.Reserve2)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.MoveTime
            self.CommandData.AddUint(self._command.MoveTime)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.E2
            self.CommandData.AddReal(self._command.JointPosition.E2)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.E3
            self.CommandData.AddReal(self._command.JointPosition.E3)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.E4
            self.CommandData.AddReal(self._command.JointPosition.E4)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.E5
            self.CommandData.AddReal(self._command.JointPosition.E5)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.JointPosition.E6
            self.CommandData.AddReal(self._command.JointPosition.E6)
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

        for _idx in range(0, 4 ) :
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
                MessageText = 'Command.EmitterID[{2}] = {1}',
                Para1       =  str(self._command.EmitterID[_idx]),
                Para2       =  str(_idx)
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
            MessageText = 'Command.ListenerID = {1}',
            Para1       =  str(self._command.ListenerID)
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
            MessageText = 'Command.Reserve = {1}',
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
            MessageText = 'Command.VelocityRate = {1}',
            Para1       =  str(self._command.VelocityRate)
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
            MessageText = 'Command.AccelerationRate = {1}',
            Para1       =  str(self._command.AccelerationRate)
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
            MessageText = 'Command.DecelerationRate = {1}',
            Para1       =  str(self._command.DecelerationRate)
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
            MessageText = 'Command.JerkRate = {1}',
            Para1       =  str(self._command.JerkRate)
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
            MessageText = 'Command.ToolNo = {1}',
            Para1       =  str(self._command.ToolNo)
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
            MessageText = 'Command.BlendingMode = {1}',
            Para1       =  str(self._command.BlendingMode)
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
            MessageText = 'Command.BlendingParameter[0] = {1}',
            Para1       =  str(self._command.BlendingParameter[0])
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
            MessageText = 'Command.BlendingParameter[1] = {1}',
            Para1       =  str(self._command.BlendingParameter[1])
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
            MessageText = 'Command.JointPosition.J1 = {1}',
            Para1       =  str(self._command.JointPosition.J1)
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
            MessageText = 'Command.JointPosition.J2 = {1}',
            Para1       =  str(self._command.JointPosition.J2)
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
            MessageText = 'Command.JointPosition.J3 = {1}',
            Para1       =  str(self._command.JointPosition.J3)
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
            MessageText = 'Command.JointPosition.J4 = {1}',
            Para1       =  str(self._command.JointPosition.J4)
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
            MessageText = 'Command.JointPosition.J5 = {1}',
            Para1       =  str(self._command.JointPosition.J5)
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
            MessageText = 'Command.JointPosition.J6 = {1}',
            Para1       =  str(self._command.JointPosition.J6)
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
            MessageText = 'Command.JointPosition.E1 = {1}',
            Para1       =  str(self._command.JointPosition.E1)
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
            MessageText = 'Command.Manipulation = {1}',
            Para1       =  str(self._command.Manipulation)
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
            MessageText = 'Command.Reserve2 = {1}',
            Para1       =  str(self._command.Reserve2)
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
            MessageText = 'Command.MoveTime = {1}',
            Para1       =  str(self._command.MoveTime)
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
            MessageText = 'Command.JointPosition.E2 = {1}',
            Para1       =  str(self._command.JointPosition.E2)
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
            MessageText = 'Command.JointPosition.E3 = {1}',
            Para1       =  str(self._command.JointPosition.E3)
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
            MessageText = 'Command.JointPosition.E4 = {1}',
            Para1       =  str(self._command.JointPosition.E4)
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
            MessageText = 'Command.JointPosition.E5 = {1}',
            Para1       =  str(self._command.JointPosition.E5)
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
            MessageText = 'Command.JointPosition.E6 = {1}',
            Para1       =  str(self._command.JointPosition.E6)
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
            self.OutCmd = MoveAxesAbsoluteOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :

            # Update results
            self.OutCmd.FollowID = self._response.OriginID.value
            self.OutCmd.Progress = PERCENT_UINT_TO_REAL( Value = self._response.Progress.value, IsOptional = True).value


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
                        self.OutCmd = MoveAxesAbsoluteOutCmd()
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
    def OnUpdateStateFlags(self, State : CmdMessageState) -> None:
        """
        Update state flags according to received state
        """

        # Reset State flags
        self.Active = False
        self.CommandAborted = False
        self.CommandInterrupted = False
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
                self.Active = True

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

        # Table 6-262: Received CMD payload (RC to PLC) of "MoveAxesAbsolute"  
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
        # Byte 04 : USINT   - InvocationCounter
        # Byte 05 : SINT    - Reserve
        # Byte 06 : INT     - OriginID LW HB
        # Byte 07 :         - OriginID LW LB
        # Byte 08 : UINT    - Progress LW HB
        # Byte 09 :         - Progress LW LB
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
            # Get Response.InvocationCounter
            self._response.InvocationCounter = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Reserve
            self._response.Reserve = ResponseData.GetSint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.OriginID
            self._response.OriginID = ResponseData.GetInt()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Progress
            self._response.Progress = ResponseData.GetUint()
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
            MessageText = 'Response.InvocationCounter = {1}',
            Para1       =  str(self._response.InvocationCounter)
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
            MessageText = 'Response.OriginID = {1}',
            Para1       =  str(self._response.OriginID)
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
            MessageText = 'Response.Progress = {1}',
            Para1       =  str(self._response.Progress)
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
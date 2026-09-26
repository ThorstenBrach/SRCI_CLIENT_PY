"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_ReturnToPrimaryFB
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
import copy
import math

from RobotLibrary.Enumerations.Mode.TrajectoryMode import TrajectoryMode
from RobotLibrary.Functions.ToString import VALID_REAL_TO_STRING
from RobotLibrary.IEC_Standard import SetTimeout, BYTE
from RobotLibrary.Constants import RUNNING, OK
from RobotLibrary.Functions.Convert import REAL_TO_PERCENT_UINT, PERCENT_UINT_TO_REAL

from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseEnableFB import RobotLibraryBaseEnableFB
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
from RobotLibrary.Enumerations.Mode.ReturnMode import ReturnMode

from .Structures.ReturnToPrimaryParCmd import ReturnToPrimaryParCmd
from .Structures.ReturnToPrimaryOutCmd import ReturnToPrimaryOutCmd
from .Structures.ReturnToPrimaryRecvData import ReturnToPrimaryRecvData
from .Structures.ReturnToPrimarySendData import ReturnToPrimarySendData
#endregion

class MC_ReturnToPrimaryFB( RobotLibraryBaseEnableFB):
    """Function block to return to primary position on the robot controller."""
    
    #VAR_INPUT
    ParCmd             : ReturnToPrimaryParCmd
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
    OutCmd             : ReturnToPrimaryOutCmd
    """command outputs"""

    #VAR
    _parCmd            : ReturnToPrimaryParCmd
    """ internal copy of command parameter """
    _command           : ReturnToPrimarySendData
    """ command data to send """
    _response          : ReturnToPrimaryRecvData
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
        self.ParCmd             = ReturnToPrimaryParCmd()
        
        # Initialize VAR_OUTPUT
        self.CommandBuffered    = False
        self.Active             = False
        self.CommandAborted     = False
        self.CommandInterrupted = False        
        self.OutCmd             = ReturnToPrimaryOutCmd()
        
        # Initialize VAR
        self._parCmd            = ReturnToPrimaryParCmd()
        self._command           = ReturnToPrimarySendData()
        self._response          = ReturnToPrimaryRecvData()



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
        CheckFunctionSupported : bool = AxesGroup.State.RobotData.RCSupportedFunctions.ReturnToPrimary.value

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

        # Check ParCmd.ReturnMode valid ? 
        if (( self.ParCmd.ReturnMode != ReturnMode.INTERRUPT_POSITION ) and
            ( self.ParCmd.ReturnMode != ReturnMode.END_POSITION       )) :
            
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
                MessageText = 'Invalid Parameter ParCmd.ReturnMode = {1}',
                Para1       = str(self.ParCmd.ReturnMode)
            )
            return CheckParameterValid


        # Check ParCmd.VelocityRate valid ? 
        if  (( math.isfinite(self.ParCmd.VelocityRate) == False )  or #noqa
            ((               self.ParCmd.VelocityRate   <     0 )  and
             (               self.ParCmd.VelocityRate  !=    -1 )) or
             (               self.ParCmd.VelocityRate   >   100 )) :
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
            ((               self.ParCmd.AccelerationRate   <     0 )  and
             (               self.ParCmd.AccelerationRate  !=    -1 )) or
             (               self.ParCmd.AccelerationRate   >   100 )) :

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
            ((               self.ParCmd.DecelerationRate   <     0 )  and
             (               self.ParCmd.DecelerationRate  !=    -1 )) or
             (               self.ParCmd.DecelerationRate   >   100 )) :
            
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
            ((               self.ParCmd.JerkRate   <     0 )  and
             (               self.ParCmd.JerkRate  !=    -1 )) or
             (               self.ParCmd.JerkRate   >   100 )) :

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
            ( self.ParCmd.ToolNo > AxesGroup.State.UnifiedToolIndex                   )):
        
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


        # Check ParCmd.FrameNo valid ? 
        if (( self.ParCmd.FrameNo <   0                                                 ) or  
            ( self.ParCmd.FrameNo > 254                                                 ) or
            ( self.ParCmd.FrameNo > AxesGroup.State.ConfigurationData.HighestFrameIndex ) or
            ( self.ParCmd.FrameNo > AxesGroup.State.UnifiedFrameIndex                   )) :

            # Parameter not valid
            CheckParameterValid = False
            
            # Check FrameNo available on RC ? 
            if ( self.ParCmd.FrameNo > AxesGroup.State.ConfigurationData.HighestFrameIndex ):
                
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_FRAMENO_UNAVAILABLE, Overwrite = True )
            else:
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_FRAMENO_RANGE, Overwrite = True )
            
            
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.FrameNo = {1}',
                Para1       = str(self.ParCmd.FrameNo)
            )
            return CheckParameterValid


        # Check ParCmd.DistanceLimit valid ? 
        if  ( math.isfinite(self.ParCmd.DistanceLimit) == False ): #noqa
            
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
                MessageText = 'Invalid Parameter ParCmd.DistanceLimit = {1}',
                Para1       = VALID_REAL_TO_STRING(self.ParCmd.DistanceLimit)
            )
            return CheckParameterValid


        # Check ParCmd.TrajectoryMode valid ? 
        if (( self.ParCmd.TrajectoryMode != TrajectoryMode.INVALID         ) and   
            ( self.ParCmd.TrajectoryMode != TrajectoryMode.LINEAR_MOVEMENT ) and
            ( self.ParCmd.TrajectoryMode != TrajectoryMode.PTP_MOVEMENT    )):

            # Parameter not valid
            CheckParameterValid = False
            # Set error
            self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_TRAJECTORYMODE_INVALID, Overwrite = True )
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MessageType.CMD,
                Severity    = Severity.ERROR,
                MessageCode = self.ErrorID,
                MessageText = 'Invalid Parameter ParCmd.TrajectoryMode = {1}',
                Para1       = str(self.ParCmd.TrajectoryMode)
            )
            return CheckParameterValid


        # Check ParCmd.MoveTime valid ? 
        if ( self.ParCmd.MoveTime < 0 ) :
            
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


        return CheckParameterValid

    #--------------------------------------------------------
    # CreateCommandPayload - create command payload
    #--------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup : AxesGroup) -> RobotLibraryCommandDataFB:
        
        # Parameter count
        _parameterCnt : int = 0

        #region Mapping table
        
       # Table 6-310: Sent CMD payload (PLC to RC) of "ReturnToPrimary"
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
       # Byte 04  : UINT  - VelocityRate LW HB
       # Byte 05  :       - VelocityRate LW LB
       # Byte 06  : UINT  - AccelerationRate LW HB
       # Byte 07  :       - AccelerationRate LW LB
       # Byte 08  : UINT  - DecelerationRate LW HB
       # Byte 09  :       - DecelerationRate LW LB
       # Byte 10  : UINT  - JerkRate LW HB
       # Byte 11  :       - JerkRate LW LB
       # Byte 12  : REAL  - DistanceLimit HW HB
       # Byte 13  :       - DistanceLimit HW LB
       # Byte 14  :       - DistanceLimit LW HB
       # Byte 15  :       - DistanceLimit LW LB
       # Byte 16  : USINT - ToolNo 
       # Byte 17  : USINT - FrameNo 
       # Byte 18  : UINT  - Move Time LW HB
       # Byte 19  : UINT  - Move Time LW LB
       # Byte 20  : BYTE  - BIT 00 : ReturnMode
       #                    BIT 01 : TrajectoryMode
       #                    BIT 02 : Enable
       #                    BIT 03 : AllowDifferences
       # Byte 21  : BYTE  - PaddingByte
       # --------------------------
       # endregion

        # set command parameter 
        self._command.CmdTyp               = CmdType.ReturnToPrimary
        self._command.ExecMode             = self. ExecMode
        self._command.ParSeq               = self._command.ParSeq
        self._command.Priority             = self. Priority
        self._command.ToolNo.value         = self._parCmd.ToolNo
        self._command.FrameNo.value        = self._parCmd.FrameNo
        self._command.VelocityRate         = REAL_TO_PERCENT_UINT(self._parCmd.VelocityRate     , IsOptional = False)
        self._command.AccelerationRate     = REAL_TO_PERCENT_UINT(self._parCmd.AccelerationRate , IsOptional = False)
        self._command.DecelerationRate     = REAL_TO_PERCENT_UINT(self._parCmd.DecelerationRate , IsOptional = True )
        self._command.JerkRate             = REAL_TO_PERCENT_UINT(self._parCmd.JerkRate         , IsOptional = True )
        self._command.DistanceLimit.value  = self._parCmd.DistanceLimit
        self._command.ReturnMode.value     = self._parCmd.ReturnMode == ReturnMode.END_POSITION
        self._command.TrajectoryMode.value = self._parCmd.TrajectoryMode == TrajectoryMode.PTP_MOVEMENT
        self._command.MoveTime.value       = self._parCmd.MoveTime
        self._command.Enable.value         = self.Enable
        
        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


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
        
            # add command.DistanceLimit
            self.CommandData.AddReal(self._command.DistanceLimit)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.FrameNo
            self.CommandData.AddUsint(self._command.FrameNo)
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
            
            tmpByte : BYTE = BYTE(0)
            tmpByte.Bit[0] = self._command.ReturnMode.value
            tmpByte.Bit[1] = self._command.TrajectoryMode.value
            tmpByte.Bit[2] = self._command.Enable.value
            tmpByte.Bit[3] = self._command.AllowDifferences.value

            # add command.MoveTime
            self.CommandData.AddByte(tmpByte)
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
            MessageText = 'Command.FrameNo = {1}',
            Para1       =  str(self._command.FrameNo)
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
            MessageText = 'Command.DistanceLimit = {1}',
            Para1       =  str(self._command.DistanceLimit)
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
            MessageText = 'Command.ReturnMode = {1}',
            Para1       =  str(self._command.ReturnMode)
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
            MessageText = 'Command.TrajectoryMode = {1}',
            Para1       =  str(self._command.TrajectoryMode)
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


    #--------------------------------------------------------
    # OnApplyOutCmd - apply output command data
    #--------------------------------------------------------
    def OnApplyOutCmd(self, State : CmdMessageState) -> None:
        """
        Apply output command data received from robot controller
        """

        if ( State == CmdMessageState.EMPTY ) :

            # Reset command outputs
            self.OutCmd = ReturnToPrimaryOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or
            ( State == CmdMessageState.DONE   )) :

            # Update results
            self.OutCmd.Progress          = PERCENT_UINT_TO_REAL( Value = self._response.Progress, IsOptional = True).value
            self.OutCmd.RemainingDistance = self._response.RemainingDistance.value
            self.OutCmd.PrimaryPosToolNo  = self._response.PrimaryPosToolNo.value
            self.OutCmd.PrimaryPosFrameNo = self._response.PrimaryPosFrameNo.value


    #--------------------------------------------------------
    # OnExecRun  - executed during execution
    #--------------------------------------------------------
    def OnExecRun(self, AxesGroup: AxesGroup) -> int:

        OnExecRun : int = RUNNING
        
        # call base implementation
        super().OnExecRun(AxesGroup = AxesGroup)

        match self._stepCmd :
        
            case 0: 
                
                if ( self._enable_R.Q ) and ( not self.Error) :
                
                    # reset the rising edge
                    self._enable_R()
                    # reset the falling edge
                    self._enable_F()

                    # Check function is supported and parameter are valid ?
                    if (( self.CheckFunctionSupported( AxesGroup = AxesGroup )) and
                        ( self.CheckParameterValid   ( AxesGroup = AxesGroup ))):

                        # set busy flag
                        self.Busy = True
                        # Reset command outputs
                        self.OutCmd = ReturnToPrimaryOutCmd()
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
                
                if ( not self.Enable ) :

                    self.Reset()
                    # reset step counter
                    self._stepCmd = 0
                    # finish OK
                    OnExecRun = OK


            case _:
                # invalid step
                self.SetError( ErrorID = RobotLibraryErrorIdEnum.ERR_INVALID_STEP, Overwrite = True )


        # Reset FB
        if (( self._enable_R.Q ) or
            ( self._enable_F.Q )) :

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

        # Table 6-311: Received CMD payload (RC to PLC) of "ReturnToPrimary"
        # --------------------------
        # Header
        # --------------------------
        # Byte 00 : USINT - ParSeq | State     
        # Byte 01 : SINT  - AlarmMessageSeverity    
        # Byte 02 : UINT  - AlarmMessageCode HB
        # Byte 03 :       - AlarmMessageCode LB
        # --------------------------
        # Datablock
        # --------------------------
        # Byte 04 : UINT  - Progress LW HB
        # Byte 05 :       - Progress LW LB
        # Byte 06 : REAL  - RemainingDistance HW HB
        # Byte 07 :       - RemainingDistance HW LB
        # Byte 08 :       - RemainingDistance LW HB
        # Byte 09 :       - RemainingDistance LW LB
        # Byte 10 : USINT - PrimaryPosToolNo 
        # Byte 11 : USINT - PrimaryPosToolNo 
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
            # Get Response.Progress
            self._response.Progress = ResponseData.GetUint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.RemainingDistance
            self._response.RemainingDistance = ResponseData.GetReal()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.PrimaryPosToolNo
            self._response.PrimaryPosToolNo = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.PrimaryPosFrameNo
            self._response.PrimaryPosFrameNo = ResponseData.GetUsint()
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
            MessageText = 'Response.Progress = {1}',
            Para1       =  str(self._response.Progress)
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
            MessageText = 'Response.RemainingDistance = {1}',
            Para1       =  str(self._response.RemainingDistance)
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
            MessageText = 'Response.PrimaryPosToolNo = {1}',
            Para1       =  str(self._response.PrimaryPosToolNo)
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
            MessageText = 'Response.PrimaryPosFrameNo = {1}',
            Para1       =  str(self._response.PrimaryPosFrameNo)
        )


    #--------------------------------------------------------
    # Reset - reset internal variables
    #--------------------------------------------------------
    def Reset(self) -> int:
        """ Reset internal variables """

        self.Done               = False
        self.Busy               = False
        self.Active             = False
        self.CommandBuffered    = False
        self.CommandAborted     = False
        self.CommandInterrupted = False
        
        return super().Reset()
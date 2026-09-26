"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      MC_ExchangeConfigurationFB
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

from RobotLibrary.IEC_Standard import SetTimeout, CheckTimeout
from RobotLibrary.Constants import RUNNING, OK, HAS_ERROR
from RobotLibrary.Enumerations.Level.PriorityLevel import PriorityLevel
from RobotLibrary.Enumerations.Mode.ExecutionMode import ExecutionMode
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity
from RobotLibrary.Enumerations.State import CmdMessageState
from RobotLibrary.Enumerations.Type.MessageType import MessageType
from RobotLibrary.Enumerations.Events.ErrorIdEnum import ErrorIdEnum as RobotLibraryErrorIdEnum

from RobotLibrary.Enumerations.Type.CmdType import CmdType
from RobotLibrary.Enumerations.Miscellaneous.SyncReaction import SyncReaction

from RobotLibrary.IEC_Types import USINT
from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseEnableFB import RobotLibraryBaseEnableFB
from RobotLibrary.POUs._internal.Send.RobotLibraryCommandDataFB import RobotLibraryCommandDataFB
from RobotLibrary.POUs._internal.Recv.RobotLibraryResponseDataFB import RobotLibraryResponseDataFB

from RobotLibrary.Structures.DatenAndTime.SystemTime import SystemTime
from RobotLibrary.Structures.AxesGroup.AxesGroup import AxesGroup

from .Structures.ExchangeConfigurationParCmd import ExchangeConfigurationParCmd
from .Structures.ExchangeConfigurationOutCmd import ExchangeConfigurationOutCmd
from .Structures.ExchangeConfigurationSendData import ExchangeConfigurationSendData
from .Structures.ExchangeConfigurationRecvData import ExchangeConfigurationRecvData

#endregion

class MC_ExchangeConfigurationFB( RobotLibraryBaseEnableFB):
    """Function block to exchange configuration data with the robot controller."""
    
    #region VAR_INPUT
    ParCmd : ExchangeConfigurationParCmd
    """command parameter"""
    #endregion
    
    #region VAR_OUTPUT
     
    CommandBuffered : bool
    """ Command is transferred and confirmed by the RC"""
    
    ParameterAccepted : bool
    """Receiving of input parameter values has been acknowledged by RC"""

    OutCmd : ExchangeConfigurationOutCmd
    """command outputs"""
    #endregion
    
    #region VAR
    _parCmd             : ExchangeConfigurationParCmd
    """internal copy of command parameter"""
    _command            : ExchangeConfigurationSendData
    """command data to send"""
    _response           : ExchangeConfigurationRecvData
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
        self.ParCmd = ExchangeConfigurationParCmd()

        # Initialize VAR_OUTPUT
        self.CommandBuffered = False
        self.ParameterAccepted = False
        self.OutCmd = ExchangeConfigurationOutCmd()

        # Initialize VAR
        self._parCmd   = ExchangeConfigurationParCmd()
        self._command  = ExchangeConfigurationSendData()
        self._response = ExchangeConfigurationRecvData()


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
        CheckFunctionSupported : bool = False

        CheckFunctionSupported = AxesGroup.State.RobotData.RCSupportedFunctions.ExchangeConfiguration.value

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

        # Check ParCmd.LogLevel valid ? 
        if (( self.ParCmd.LogLevel != Severity.DEACTIVATE  ) and  
            ( self.ParCmd.LogLevel != Severity.DEBUG       ) and
            ( self.ParCmd.LogLevel != Severity.INFO        ) and
            ( self.ParCmd.LogLevel != Severity.WARNING     ) and
            ( self.ParCmd.LogLevel != Severity.ERROR       ) and
            ( self.ParCmd.LogLevel != Severity.FATAL_ERROR )) :
            
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
                MessageText = 'Invalid Parameter ParCmd.LogLevel = {1}',
                Para1       =  str(self.ParCmd.LogLevel)
            )
            return CheckParameterValid

        # no plausibility check for boolean :
        # ParCmd.WaitAtBlendingZone
        # ParCmd.AllowSecSeqWhileSubprogram


        # Check ParCmd.DelayTime valid ? 
        if ( self.ParCmd.DelayTime < 0  ) :

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
                MessageText = 'Invalid Parameter ParCmd.DelayTime = {1} ms',
                Para1       =  str(self.ParCmd.DelayTime)
            )
            return CheckParameterValid


        # Check ParCmd.WaitForNrOfCmd valid ? 
        if ( self.ParCmd.WaitForNrOfCmd < 0  ) :

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
                MessageText = 'Invalid Parameter ParCmd.WaitForNrOfCmd = {1}',
                Para1       =  str(self.ParCmd.WaitForNrOfCmd)
            )
            return CheckParameterValid


        # Check ParCmd.LifeSignTimeOut valid ? 
        if ( self.ParCmd.LifeSignTimeOut < 10 ) :

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
                MessageText = 'Invalid Parameter ParCmd.LifeSignTimeOut = {1} ms',
                Para1       =  str(self.ParCmd.LifeSignTimeOut)
            )
            return CheckParameterValid


        # Check ParCmd.SyncDelay valid ? 
        if ( self.ParCmd.SyncDelay < 0  ) :

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
                MessageText = 'Invalid Parameter ParCmd.SyncDelay = {1}',
                Para1       =  str(self.ParCmd.SyncDelay)
            )
            return CheckParameterValid


        # Check ParCmd.SyncReaction valid ? 
        if (( self.ParCmd.SyncReaction != SyncReaction.NO_REACTION                      ) and  
            ( self.ParCmd.SyncReaction != SyncReaction.NO_AUTOMATIC_DISABLE             ) and
            ( self.ParCmd.SyncReaction != SyncReaction.INTERRUPT_WHEN_SEQUENCE_IS_EMPTY ) and
            ( self.ParCmd.SyncReaction != SyncReaction.IMMEDIATE_INTERRUPT              )):
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
                MessageText = 'Invalid Parameter ParCmd.SyncReaction = {1}',
                Para1       =  str(self.ParCmd.SyncReaction)
            )
            return CheckParameterValid


        # no plausibility check for boolean :

        # ParCmd.DataInSync.ToolsInSync
        # ParCmd.DataInSync.FramesInSync
        # ParCmd.DataInSync.LoadsInSync
        # ParCmd.DataInSync.WorkAreasInSync
        # ParCmd.DataInSync.SoftwareLimitsInSync
        # ParCmd.DataInSync.DefaultDynamicsInSync
        # ParCmd.DataInSync.ReferenceDynamicsInSync
        # ParCmd.DataEnableSync.EnableSyncTool
        # ParCmd.DataEnableSync.EnableSyncFrame
        # ParCmd.DataEnableSync.EnableSyncLoad
        # ParCmd.DataEnableSync.EnableSyncWorkArea
        # ParCmd.DataEnableSync.EnableSyncSWLimits
        # ParCmd.DataEnableSync.EnableSyncDefaultDynamics
        # ParCmd.DataEnableSync.EnableSyncReferenceDynamics
        # ParCmd.DataEnableSync.AllowDynamicBlending


        return CheckParameterValid


    #--------------------------------------------------------
    # CreateCommandPayload - create command payload
    #--------------------------------------------------------
    def CreateCommandPayload(self, AxesGroup : AxesGroup) -> RobotLibraryCommandDataFB:
        
        # Parameter count
        _parameterCnt : int = 0

        # region Mapping table
        
        # Table 6-86: Sent CMD payload (PLC to RC) of "ExchangeConfiguration"
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
        # Byte 4   : USINT      - LogLevel
        # Byte 5.0 : BOOL       - WaitAtBlendingZone
        # Byte 5.1 : BOOL       - Enable
        # Byte 5.2 : BOOL       - AllowSecSeqWhileSubprogram
        # Byte 5.3 : BOOL       - AllowDynamicBlending
        # Byte 6   : UINT       - DelayTime HB
        # Byte 7   :            - DelayTime LB
        # Byte 8   : UINT       - WaitForNrOfCmd HB
        # Byte 9   :            - WaitForNrOfCmd LB
        # Byte 10  : UINT       - LifeSignTimeOut HB
        # Byte 11  :            - LifeSignTimeOut LB
        # Byte 12  : UINT       - SyncDelay HB
        # Byte 13  :            - SyncDelay LB
        # Byte 14  : USINT      - SyncReaction
        # Byte 15  : DataInSync - DataInSync 
        # Byte 16  : BYTE       - Reserved
        # Byte 17  : BYTE       - DataEnableSync
        # Byte 18  : BYTE       - Reserved
        # --------------------------
        #endregion

        # set command parameter 
        self._command.CmdTyp                = CmdType.ReadMessages
        self._command.ExecMode              = self. ExecMode
        self._command.ParSeq                = self._command.ParSeq
        self._command.Priority              = self. Priority
        self._command.LogLevel              = self._parCmd.LogLevel
        self._command.CtrlByte.Bit[0]       = self._parCmd.WaitAtBlendingZone
        self._command.CtrlByte.Bit[1]       = self. Enable
        self._command.CtrlByte.Bit[2]       = self._parCmd.AllowSecSeqWhileSubprogram
        self._command.CtrlByte.Bit[3]       = self._parCmd.AllowDynamicBlending
        self._command.DelayTime.value       = self._parCmd.DelayTime
        self._command.WaitForNrOfCmd.value  = self._parCmd.WaitForNrOfCmd
        self._command.LifeSignTimeOut.value = self._parCmd.LifeSignTimeOut
        self._command.SyncDelay.value       = self._parCmd.SyncDelay
        self._command.SyncReaction          = self._parCmd.SyncReaction
        self._command.DataInSync            = self._parCmd.DataInSync
        self._command.Reserve1.value        = 0
        self._command.DataEnableSync        = self._parCmd.DataEnableSync
        self._command.Reserve2.value        = 0

        # copy command data to header
        self._cmdHeader = self._command
        # call base implementation to copy header to payload buffer
        super().CreateCommandPayload(AxesGroup)


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LogLevel
            self.CommandData.AddUsint(USINT(self._command.LogLevel.value))
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.CtrlByte
            self.CommandData.AddByte(self._command.CtrlByte)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.DelayTime
            self.CommandData.AddUint(self._command.DelayTime)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.WaitForNrOfCmd
            self.CommandData.AddUint(self._command.WaitForNrOfCmd)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.LifeSignTimeOut
            self.CommandData.AddUint(self._command.LifeSignTimeOut)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.SyncDelay
            self.CommandData.AddUint(self._command.SyncDelay)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.SyncReaction
            self.CommandData.AddUsint(self._command.SyncReaction.TypeValue)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.DataInSync
            self.CommandData.AddDataInSync(self._command.DataInSync)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.Reserve1
            self.CommandData.AddByte(self._command.Reserve1)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.DataEnableSync
            self.CommandData.AddDataEnableSync(self._command.DataEnableSync)
            # inc parameter counter
            _parameterCnt += 1


        # Check parameter must be added ? 
        if ( self.CheckAddParameter(self.CommandData.PayloadPtr.value)):
        
            # add command.Reserve2
            self.CommandData.AddByte(self._command.Reserve2)
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
            MessageText = 'Command.LogLevel = {1}',
            Para1       =  str(self._command.LogLevel)
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
            MessageText = 'Command.CtrlByte = {1}',
            Para1       =  str(self._command.CtrlByte)
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
            MessageText = 'Command.DelayTime = {1}',
            Para1       = str(self._command.DelayTime)
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
            MessageText = 'Command.WaitForNrOfCmd = {1}',
            Para1       = str(self._command.WaitForNrOfCmd)
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
            MessageText = 'Command.LifeSignTimeOut = {1}',
            Para1       = str(self._command.LifeSignTimeOut)
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
            MessageText = 'Command.SyncDelay = {1}',
            Para1       = str(self._command.SyncDelay)
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
            MessageText = 'Command.SyncReaction = {1}',
            Para1       = str(self._command.SyncReaction)
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
            MessageText = 'Command.DataInSync = {1}',
            Para1       = str(self._command.DataInSync) # Todo
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
            MessageText = 'Command.Reserve1 = {1}',
            Para1       = str(self._command.Reserve1)
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
            MessageText = 'Command.DataEnableSync = {1}',
            Para1       = str(self._command.DataEnableSync)
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
            MessageText = 'Command.Reserve2 = {1}',
            Para1       = str(self._command.Reserve2)
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
            self.OutCmd = ExchangeConfigurationOutCmd()


        if (( State == CmdMessageState.ACTIVE ) or (True)) :

            # Update results
            self.OutCmd.LengthACR                 = self._response.LengthACR.value
            self.OutCmd.HighestToolIndex          = self._response.HighestToolIndex.value
            self.OutCmd.HighestFrameIndex         = self._response.HighestFrameIndex.value
            self.OutCmd.HighestLoadIndex          = self._response.HighestLoadIndex.value
            self.OutCmd.HighestWorkAreaIndex      = self._response.HighestWorkAreaIndex.value
            self.OutCmd.DataInSync                = self._response.DataInSync
            self.OutCmd.ChangeIndexTool           = self._response.ChangeIndexTool.value
            self.OutCmd.ChangeIndexFrame          = self._response.ChangeIndexFrame.value
            self.OutCmd.ChangeIndexLoad           = self._response.ChangeIndexLoad.value
            self.OutCmd.ChangeIndexWorkArea       = self._response.ChangeIndexWorkArea.value
            self.OutCmd.RAWorkingHours            = self._response.RAWorkingHours.value
            self.OutCmd.BrakeTestRequired         = self._response.StatusByte.Bit[0]
            self.OutCmd.StepModeExactStopActive   = self._response.StatusByte.Bit[1]
            self.OutCmd.StepModeBlendingActive    = self._response.StatusByte.Bit[2]
            self.OutCmd.PathAccuracyMode          = self._response.StatusByte.Bit[3]
            self.OutCmd.AvoidSingularity          = self._response.StatusByte.Bit[4]
            self.OutCmd.CollisionDetectionEnabled = self._response.StatusByte.Bit[5]
            self.OutCmd.AcceleratingSupported     = self._response.StatusByte.Bit[6]
            self.OutCmd.DecceleratingSupported    = self._response.StatusByte.Bit[7]
            self.OutCmd.ConstantVelocitySupported = self._response.ConstantVelocitySupported.value
            self.OutCmd.RCWorkingHours            = self._response.RCWorkingHours.value


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
                        self.OutCmd = ExchangeConfigurationOutCmd()
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

                # do not abort directly, so that the ParSeq update can be send
                if ( self._enable_F.Q ) :
                
                    # Reset Enabled Flag
                    self.Enabled = False
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

        # Update Enabled flag
        self.Enabled = (self._response.Enabled.value or (State == CmdMessageState.ACTIVE)) # ToDo: Stäubli send Enabled = FALSE instead of true

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
                self.ParameterAccepted  = True

            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER : 
                self.CommandBuffered    = True
                self.ParameterAccepted  = True

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

        # Table 6-87: Received CMD payload (RC to PLC) of "ExchangeConfiguration"
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
        # Byte 04 : BOOL       - Enabled
        # Byte 05 : BYTE       - Reserve
        # Byte 05 : UINT       - LengthACR LW HB
        # Byte 06 :            - LengthACR LW LB
        # Byte 08 : USINT      - HighestToolIndex
        # Byte 09 : USINT      - HighestFrameIndex
        # Byte 10 : USINT      - HighestLoadIndex
        # Byte 11 : USINT      - HighestWorkAreaIndex
        # Byte 12 : DataInSync - DataInSync
        # Byte 13 : BYTE       - Reserve
        # Byte 14 : USINT      - ChangeIndexTool
        # Byte 15 : USINT      - ChangeIndexFrame
        # Byte 16 : USINT      - ChangeIndexLoad
        # Byte 17 : USINT      - ChangeIndexWorkArea
        # Byte 18 : UDINT      - RA WorkingHours HW HB
        # Byte 19 :            - RA WorkingHours HW LB
        # Byte 20 :            - RA WorkingHours LW HB
        # Byte 21 :            - RA WorkingHours LW LB
        # Byte 22 : BYTE       - StatusByte
        # Byte 23 : BOOL       - ConstantVelocitySupported
        # Byte 24 : UDINT      - RC WorkingHours HW HB
        # Byte 25 :            - RC WorkingHours HW LB
        # Byte 26 :            - RC WorkingHours LW HB
        # Byte 27 :            - RC WorkingHours LW LB
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
            # Get Response.Enabled
            self._response.Enabled = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Reserve1
            self._response.Reserve1 = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.LengthACR
            self._response.LengthACR = ResponseData.GetUint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.HighestToolIndex
            self._response.HighestToolIndex = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.HighestFrameIndex
            self._response.HighestFrameIndex = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.HighestLoadIndex
            self._response.HighestLoadIndex = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.HighestWorkAreaIndex
            self._response.HighestWorkAreaIndex = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.DataInSync
            self._response.DataInSync = ResponseData.GetDataInSync()
            # inc parameter counter
            _parameterCnt += 1
        
        
        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get Response.Reserve2
            self._response.Reserve2 = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt += 1

        
        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.ChangeIndexTool
            self._response.ChangeIndexTool  = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.ChangeIndexFrame
            self._response.ChangeIndexFrame  = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.ChangeIndexLoad
            self._response.ChangeIndexLoad  = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.ChangeIndexWorkArea
            self._response.ChangeIndexWorkArea  = ResponseData.GetUsint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.RAWorkingHours
            self._response.RAWorkingHours  = ResponseData.GetUdint()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.StatusByte
            self._response.StatusByte = ResponseData.GetByte()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.ConstantVelocitySupported
            self._response.ConstantVelocitySupported = ResponseData.GetBool()
            # inc parameter counter
            _parameterCnt += 1


        # Check payload remaining ? 
        if ( ResponseData.IsPayloadRemaining ) :
            # Get _response.RCWorkingHours
            self._response.RCWorkingHours = ResponseData.GetUdint()
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
            MessageText = 'Response.Reserve1 = {1}',
            Para1       =  str(self._response.Reserve1)
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
            MessageText = 'Response.LengthACR = {1}',
            Para1       =  str(self._response.LengthACR)
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
            MessageText = 'Response.HighestToolIndex = {1}',
            Para1       = str(self._response.HighestToolIndex)
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
            MessageText = 'Response.HighestFrameIndex = {1}',
            Para1       =  str(self._response.HighestFrameIndex)
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
            MessageText = 'Response.HighestLoadIndex = {1}',
            Para1       =  str(self._response.HighestLoadIndex)
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
            MessageText = 'Response.HighestWorkAreaIndex = {1}',
            Para1       = str(self._response.HighestWorkAreaIndex)
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
            MessageText = 'Response.DataInSync.ToolsInSync = {1}',
            Para1       =  str(self._response.DataInSync.ToolsInSync)
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
            MessageText = 'Response.DataInSync.FramesInSync = {1}',
            Para1       =  str(self._response.DataInSync.FramesInSync)
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
            MessageText = 'Response.DataInSync.LoadsInSync = {1}',
            Para1       =  str(self._response.DataInSync.LoadsInSync)
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
            MessageText = 'Response.DataInSync.WorkAreasInSync = {1}',
            Para1       =  str(self._response.DataInSync.WorkAreasInSync)
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
            MessageText = 'Response.DataInSync.SoftwareLimitsInSync = {1}',
            Para1       =  str(self._response.DataInSync.SoftwareLimitsInSync)
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
            MessageText = 'Response.DataInSync.DefaultDynamicsInSync = {1}',
            Para1       =  str(self._response.DataInSync.DefaultDynamicsInSync)
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
            MessageText = 'Response.DataInSync.ReferenceDynamicsInSync = {1}',
            Para1       =  str(self._response.DataInSync.ReferenceDynamicsInSync)
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
            MessageText = 'Response.Reserve2 = {1}',
            Para1       =  str(self._response.Reserve2)
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
            MessageText = 'Response.ChangeIndexTool = {1}',
            Para1       =  str(self._response.ChangeIndexTool)
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
            MessageText = 'Response.ChangeIndexFrame = {1}',
            Para1       =  str(self._response.ChangeIndexFrame)
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
            MessageText = 'Response.ChangeIndexLoad = {1}',
            Para1       =  str(self._response.ChangeIndexLoad)
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
            MessageText = 'Response.ChangeIndexWorkArea = {1}',
            Para1       =  str(self._response.ChangeIndexWorkArea)
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
            MessageText = 'Response.RAWorkingHours = {1}',
            Para1       =  str(self._response.RAWorkingHours)
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
            MessageText = 'Response.StatusByte = {1}',
            Para1       =  str(self._response.StatusByte)
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
            MessageText = 'Response.ConstantVelocitySupported = {1}',
            Para1       =  str(self._response.ConstantVelocitySupported)
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
            MessageText = 'Response.RCWorkingHours = {1}',
            Para1       =  str(self._response.RCWorkingHours)
        )


    #--------------------------------------------------------
    # Reset - reset internal variables
    #--------------------------------------------------------
    def Reset(self) -> int:
        """ Reset internal variables """

        self.Busy               = False
        self.CommandBuffered    = False
        self.ParameterAccepted  = False

        return super().Reset()    
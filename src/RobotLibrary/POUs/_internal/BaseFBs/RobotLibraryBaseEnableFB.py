"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotLibraryBaseEnableFB
Author:      Thorsten Brach
Date:        2026-01-02

Description:
  Base function block for robot library commands

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from RobotLibrary.Structures.AxesGroup.AxesGroup import AxesGroup


from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseFB import RobotLibraryBaseFB
from RobotLibrary.IEC_Standard import R_TRIG, F_TRIG, SetTimeout, CheckTimeout
from RobotLibrary.Constants import OK, RUNNING, HAS_ERROR
from RobotLibrary.Enumerations import CmdMessageState
from RobotLibrary.Enumerations.Events.ErrorIdEnum import ErrorIdEnum as RobotErrorIdEnum
from RobotLibrary.Enumerations.Miscellaneous.Severity import Severity as RobotSeverityEnum
from RobotLibrary.Enumerations.Type.MessageType import MessageType as MEssageTypeEnum

class RobotLibraryBaseEnableFB(RobotLibraryBaseFB):

    #region VAR_INPUT
    Enable : bool
    """Set TRUE to activate / Set False to deactivate"""
    #engion

    #region VAR_OUTPUT
    Busy : bool
    """FB is being processed"""
    Enabled : bool
    """ TRUE while function is active"""
    #endregion

    #region VAR 
    _enable_R : R_TRIG
    """Rising edge for enable"""
    _enable_F : F_TRIG
    """Falling edge for enable"""
    #endregion

    
    def __init__(self):
        
        self._enable_R = R_TRIG() # ToDo : should be initialized as new instance within the declaration?
        self._enable_F = F_TRIG() # ToDo : should be initialized as new instance within the declaration?
        
        # call base implementation
        super().__init__()

        # default input
        self.Enable = False

        # default outputs
        self.Busy    = False
        self.Enabled = False

    # --------------------------------------------------------------
    # OnCall - called on each cycle
    # ---------------------------------------------------------------
    def OnCall(self, AxesGroup: AxesGroup) -> None:
        
        # internal return value
        _retVal = int()
        
        # call base implementation
        super().OnCall(AxesGroup = AxesGroup)

        # building rising and falling edges
        self._enable_R( CLK = self.Enable)
        self._enable_F( CLK = self.Enable)
        

        # Check command execution is allowed ?
        if ((     self.Enable                                 ) and
            ( not AxesGroup.State.Initialized                 ) and
            ( not AxesGroup.State.Synchronized                ) and
            (     self.MyType != "MC_ExchangeConfigurationFB" ) and # is part of init sequence
            (     self.MyType != "MC_ReadMessagesFB"          ) and # is part of init sequence
            (     self.MyType != "MC_ReadRobotDataFB"         )):   # is part of init sequence

            self.SetError( ErrorID = RobotErrorIdEnum.ERR_COMMANDS_NOT_ENABLED, Overwrite = True )
            self.Error   = True
            self.Busy    = False


        # On execution started
        if ( self._enable_R.Q ):
            self.OnExecStart(AxesGroup = AxesGroup)


        # On execution cancel  
        if ( self.Busy ) and ( self._enable_F.Q ):
            # set cancel flag
            self._cancel = True


        if ( self._cancel ):
            # call OnExecCancel
            _retVal = self.OnExecCancel(AxesGroup = AxesGroup)
        
            # done or error ?
            if ( _retVal != RUNNING ):
            
                # reset cancel flag
                self._cancel = False
        

        # On execution error clear
        if ( self.Error ) and ( self._enable_F.Q ):
        
            # set ClearError flag
            self._clearError = True


        # clear error ?
        if ( self._clearError ):
            
             # call OnExecErrorClear
            _retVal = self.OnExecErrorClear(AxesGroup = AxesGroup) 

        # done or error ?
        if ( _retVal != RUNNING ):
        
            # reset ClearError flag
            self._clearError = False
            

    # --------------------------------------------------------------
    # OnExecCancel -called on cancel request
    # ---------------------------------------------------------------
    def OnExecCancel(self, AxesGroup: AxesGroup)-> int:
        
        # internal return value
        _retVal = int()
        
        # internal temporary return value
        _tmpRetVal = int()

         # call reset 
        _retVal = self.Reset()
        

        # Create log entry
        self.CreateLogMessage( 
            Timestamp   = AxesGroup.State.SystemTime,
            MessageType = MEssageTypeEnum.CMD,
            Severity    = RobotSeverityEnum.DEBUG,
            MessageCode = 0,
            MessageText = 'Execution of {1} cancelled',
            Para1       = self.MyType
        )

        # try to remove cmd
        _tmpRetVal = AxesGroup.Acyclic.ActiveCommandRegister.RemoveCmd(self._uniqueID)

        if (_tmpRetVal == OK):        
            # Create log entry
            self.CreateLogMessage(
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MEssageTypeEnum.CMD,
                Severity    = RobotSeverityEnum.DEBUG,
                MessageCode = 0,
                MessageText = '{1} successfully removed from ACR',
                Para1       = self.MyType
            )
        else:
            # Create log entry
            self.CreateLogMessage( 
                Timestamp   = AxesGroup.State.SystemTime,
                MessageType = MEssageTypeEnum.CMD,
                Severity    = RobotSeverityEnum.DEBUG,
                MessageCode = 0,
                MessageText = '{1} was not removed from ACR because execution was already in progress',
                Para1       = self.MyType
            )                 

        return _retVal

    # --------------------------------------------------------------
    # OnExecErrorClear -called on error clear
    # ---------------------------------------------------------------
    def OnExecErrorClear(self, AxesGroup: AxesGroup)-> int:
        
        # Return value
        _retVal : int = RUNNING

        match self._stepClearError :
        
            case  0:
                # Reset
                self.Reset()
                # trigger parameter update to disable FB
                self._parameterUpdateInternal = True
                # call Check Parameter changed method to trigger the parameter update
                self.CheckParameterChanged(AxesGroup)
                # set timeout
                SetTimeout(self._timeoutClearError, self._timerClearError)
                # increment step
                self._stepClearError += 1

            case  1:                
                # response received?                
                if (self._responseReceived):
                    # reset response received flag
                    self._responseReceived = False
                    # reset step counter
                    self._stepClearError = 0
                    # finished
                    _retVal = OK
                else:
                    # timeout exceeded?
                    if CheckTimeout(self._timerClearError) == OK:
                        _retVal = HAS_ERROR
            case _:
                # invalid step
                self.SetError(ErrorID = RobotErrorIdEnum.ERR_INVALID_STEP, Overwrite = True)

        # reset step counter if finished
        if _retVal != RUNNING:
            self._stepClearError = 0


        return _retVal

    # --------------------------------------------------------------
    # OnExecRun - called during execution
    # ---------------------------------------------------------------
    def OnExecRun(self, AxesGroup: AxesGroup)-> int :
        # call base implementation
        return super().OnExecRun(AxesGroup = AxesGroup)
        

    # --------------------------------------------------------------
    # OnExecStart - called on start of execution
    # ---------------------------------------------------------------
    def OnExecStart(self, AxesGroup: AxesGroup)-> int:
        
        return OK
    
    # --------------------------------------------------------------
    # OnUpdateStateFlags - called to update state flags
    # ---------------------------------------------------------------
    def OnUpdateStateFlags(self, State : CmdMessageState) -> None:

        match State.value:

            # No operation or process is active
            case CmdMessageState.EMPTY : 
                pass
            # Created but not yet started
            case CmdMessageState.CREATED: 
                pass
            # Buffered and awaiting execution
            case CmdMessageState.BUFFERED: 
                pass
            # Buffered in planner for future execution
            case CmdMessageState.BUFFERED_IN_PLANNER:
                pass 
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
            case CmdMessageState.DONE: 
                self.Busy = False
            # Aborted before completion
            case CmdMessageState.ABORTED:
                self.Busy = False
            # Encountered an error during execution
            case CmdMessageState.ERROR :
                self.Error = True
                self.Busy  = False
            


    # --------------------------------------------------------------
    # Reset - resets internal variables
    # ---------------------------------------------------------------
    def Reset(self)-> int:
        
        self.Busy = False
        self.Enabled = False
        
         # call base implementation
        return super().Reset()
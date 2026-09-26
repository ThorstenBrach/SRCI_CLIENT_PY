"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotTaskParCfgRob
Author:      Thorsten Brach
Date:        2026-01-06

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
from RobotLibrary.IEC_Types import IEC_Struct 
from RobotLibrary.Structures.AxesGroup.Parameter.Rob.AxesGroupParameterRob import AxesGroupParameterRobOptionalCyclic
from RobotLibrary.Enumerations.Miscellaneous.SyncReaction import SyncReaction
from RobotLibrary.Enumerations.Level.MessageLevel import MessageLevel as MessageLevelEnum


class RobotTaskParCfgRobParameter():
    
    WaitAtBlendingZone         : bool
    """
    Defines blending behavior for single move commands. One of the optional modes must be supported.\n
     • 0 (default): Move to end position\n
          Robot moves exactly the target position independently of the selected "BlendingMode"\n
     • 1: Wait at blending parameter \n
          Robot stops its movement when the specified blending parameter is reached \n
    """

    AllowSecSeqWhileSubprogram : bool
    """Allow a sequence switch from primary to secondary while a subprogram called via CallSubprogram (6.5.18) in the sequence is in progress"""

    AllowDynamicBlending       : bool
    """
    Allows blending when CallSubprogram is called in sequence and removed afterwards. For more information see chapter 6.5.21. \n
    • 0 (default): Dynamic blending is prevented \n
    • 1: Dynamic blending is allowed \n
    """

    DelayTime                  : int
    """Defines waiting time of RC between receiving a first move command when motion queue is empty and starting the first movement. See also chapter 5.6.8."""

    WaitForNrOfCmd             : int
    """Define number of points required to calculate the blending. See also chapter 5.6.8."""

    SyncDelay                  : int
    """
    Defines a delay time between detecting an inconsistency of configuration data between server and client and executing the defined SyncReaction. \n
    Always positive. Default: 0 ms
    """

    SyncReaction               : SyncReaction
    """Specifies system reaction in case inconsistency of synchronization data is detected according to Table 6-81. For more information refer to chapter 5.6.7.2"""

    MessageLevel               : MessageLevelEnum = MessageLevelEnum.WARNING
    """Defines up to which level of severity messages will be transmitted to the PLC's message buffer"""

    def __init__(self):
        self.WaitAtBlendingZone = False
        self.AllowSecSeqWhileSubprogram = False
        self.AllowDynamicBlending = False
        self.DelayTime = 0
        self.WaitForNrOfCmd = 0
        self.SyncDelay = 0
        self.SyncReaction = SyncReaction.NO_REACTION
        self.MessageLevel = MessageLevelEnum.WARNING


class RobotTaskParCfgRob(IEC_Struct):

    Parameter      : RobotTaskParCfgRobParameter
    """Robot parameter"""
    OptionalCyclic : AxesGroupParameterRobOptionalCyclic
    """Configuration of optional cyclic data received from the Robot"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, 'Parameter', None) is None or not isinstance(self.Parameter, RobotTaskParCfgRobParameter):
            self.Parameter = RobotTaskParCfgRobParameter()
        if getattr(self, 'OptionalCyclic', None) is None or not isinstance(self.OptionalCyclic, AxesGroupParameterRobOptionalCyclic):
            self.OptionalCyclic = AxesGroupParameterRobOptionalCyclic()
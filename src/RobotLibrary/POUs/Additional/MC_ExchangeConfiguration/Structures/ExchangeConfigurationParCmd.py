"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      ExchangeConfigurationParCmd
Author:      Thorsten Brach
Date:        2025-12-23

Description:

Copyright:
    (C) 2025 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""

from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.Enumerations.Level.LogLevel import LogLevel
from RobotLibrary.Enumerations.Miscellaneous.SyncReaction import SyncReaction
from RobotLibrary.Structures.Miscellaneous.DataInSync import DataInSync
from RobotLibrary.Structures.Miscellaneous.DataEnableSync import DataEnableSync

class ExchangeConfigurationParCmd(IEC_Struct):
    """
    Configuration parameters for exchange configuration command.
    """
    
    LogLevel: LogLevel
    """Defines up to which level of severity messages will be logged in the RC's server log"""
    
    WaitAtBlendingZone: bool
    """
    Defines blending behavior for single move commands. One of the optional modes must be supported.
    • 0 (default): Move to end position - Robot moves exactly the target position independently of the selected "BlendingMode"
    • 1: Wait at blending parameter - Robot stops its movement when the specified blending parameter is reached
    """
    
    AllowSecSeqWhileSubprogram: bool
    """Allow a sequence switch from primary to secondary while a subprogram called via CallSubprogram (6.5.18) in the sequence is in progress"""
    
    AllowDynamicBlending: bool
    """
    Allows blending when CallSubprogram is called in sequence and removed afterwards. For more information see chapter 6.5.21.
    • 0 (default): Dynamic blending is prevented
    • 1: Dynamic blending is allowed
    """
    
    DelayTime: int
    """Defines waiting time of RC between receiving a first move command when motion queue is empty and starting the first movement. See also chapter 5.6.8."""
    
    WaitForNrOfCmd: int
    """Define number of points required to calculate the blending. See also chapter 5.6.8."""
    
    LifeSignTimeOut: int
    """
    Maximum allowed time between incrementation of LifeSign before communication error.
    • <10 ms: Invalid
    • 50 ms: default
    See also chapter 5.6.6.2.
    """
    
    SyncDelay: int
    """Defines a delay time between detecting an inconsistency of configuration data between server and client and executing the defined SyncReaction. Always positive. Default: 0 ms"""
    
    SyncReaction: SyncReaction
    """Specifies system reaction in case inconsistency of synchronization data is detected according to Table 6-81. For more information refer to chapter 5.6.7.2"""
    
    DataInSync: DataInSync    
    """Datas which are synchronized"""
    
    DataEnableSync: DataEnableSync
    """Enable datas to synchronize"""
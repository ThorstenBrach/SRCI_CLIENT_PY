"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupStateSyncState
Author:      Thorsten Brach
Date:        2025-12-20

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

class AxesGroupStateSyncState(IEC_Struct):
    
    Tool: bool
    """Bit 00: Tool"""

    Frame: bool
    """Bit 01: Frame"""

    Load: bool
    """Bit 02: Load"""

    WorkArea: bool
    """Bit 03: WorkArea"""

    SwLimits: bool
    """Bit 04: SwLimits"""

    DefaultDynamics: bool
    """Bit 05: DefaultDynamics"""

    ReferenceDynamics: bool
    """Bit 06: ReferenceDynamics"""

    Bit07: bool
    """Bit 07"""

    Bit08: bool
    """Bit 08"""

    Bit09: bool
    """Bit 09"""

    Bit10: bool
    """Bit 10"""

    Bit11: bool
    """Bit 11"""

    Bit12: bool
    """Bit 12"""

    Bit13: bool
    """Bit 13"""

    Bit14: bool
    """Bit 14"""

    Bit15: bool
    """Bit 15"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Default all sync flags to False
        for name in (
            'Tool','Frame','Load','WorkArea','SwLimits',
            'DefaultDynamics','ReferenceDynamics',
            'Bit07','Bit08','Bit09','Bit10','Bit11','Bit12','Bit13','Bit14','Bit15'
        ):
            if getattr(self, name, None) is None:
                setattr(self, name, False)
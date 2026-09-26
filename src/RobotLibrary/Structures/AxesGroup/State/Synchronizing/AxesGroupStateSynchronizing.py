"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupStateSynchronizing
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

class AxesGroupStateSynchronizing(IEC_Struct):
    
    Tool: bool
    """Indicates that the tool data are synchronized"""

    Frame: bool
    """Indicates that the frame data are synchronized"""

    Load: bool
    """Indicates that the load data are synchronized"""

    WorkAreas: bool
    """Indicates that the work areas are synchronized"""

    ReferenceDynamics: bool
    """Indicates that the reference dynamics are synchronized"""

    DefaultDynamics: bool
    """Indicates that the default dynamics are synchronized"""

    SwLimits: bool
    """Indicates that the software limits are synchronized"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(self, 'Tool', None) is None:
            self.Tool = False
        if getattr(self, 'Frame', None) is None:
            self.Frame = False
        if getattr(self, 'Load', None) is None:
            self.Load = False
        if getattr(self, 'WorkAreas', None) is None:
            self.WorkAreas = False
        if getattr(self, 'ReferenceDynamics', None) is None:
            self.ReferenceDynamics = False
        if getattr(self, 'DefaultDynamics', None) is None:
            self.DefaultDynamics = False
        if getattr(self, 'SwLimits', None) is None:
            self.SwLimits = False
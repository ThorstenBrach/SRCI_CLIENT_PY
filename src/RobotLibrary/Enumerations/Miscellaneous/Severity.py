"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      Severity
Author:      Thorsten Brach
Date:        2025-12-13

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

from RobotLibrary.IEC_Types import SINT, SINTEnum

class Severity(SINTEnum):
    """Enum für Severity-Level mit Beschreibungen."""

    DEACTIVATE  = 0,  
    """
    Informative message\n
    • No user action required
    """
    
    DEBUG = 4, 
    """
    Debug message\n
    • No user action required
    """
    
    INFO = 5,  
    """
    Informative message\n
    • No user action required
    """
    
    WARNING = 20,
    """
    Warning message\n
    • User action will be required at some point
    """
    
    ERROR = 28, 
    """
    Error message\n
    • User action required immediately
    """
    
    FATAL_ERROR = 29, 
    """
    Fatal error message\n
    • User action required immediately\n
    • Reinitialization of RI required\n
    """
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)
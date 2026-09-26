
"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SequenceFlag
Author:      Thorsten Brach
Date:        2025-12-14

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

from RobotLibrary.IEC_Types import USINT, USINTEnum

class SequenceFlag(USINTEnum):

    NO_SEQUENCE = 0
    """
    Refers to ProcessingModes 2 to 5 and 9 (2 = Parallel, 3 = Continuous, 4 = not available, 5 = Trigger Multiple, 9 = Deactivate)\n
    Command is not handled by any sequence\n
    For more information on ProcessingModes
    """

    PRIMARY_SEQUENCE = 1
    """
    Command will be handled by primary sequence
    """

    SECONDARY_SEQUENCE = 2
    """
    Command will be handled by secondary sequence
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    
    
# Alias
SequenceFlagEnum = SequenceFlag 
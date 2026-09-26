"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      LoadMeasurementSteps
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

from RobotLibrary.IEC_Types import USINT, USINTEnum

class LoadMeasurementSteps(USINTEnum):

    RESET = 0
    """
    0: Reset (default)\n
    Delete all positions saved on the RC
    """

    FIRST_POSITION = 1
    """
    1: First position\n
    Save the first position for the load estimation with the required data
    """

    SECOND_POSITION = 2
    """
    2: Second position\n
    Save the second position for the load estimation with the required data
    """

    THIRD_POSITION = 3
    """
    3: Third position\n
    Save the third position for the load estimation with the required data
    """

    FOURTH_POSITION = 4
    """
    4: Fourth position\n
    Save the fourth position for the load estimation with the required data
    """

    LOAD_CALCULATION = 99
    """
    99: Load calculation\n
    Start the load calculation with the data saved in the four positions
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)
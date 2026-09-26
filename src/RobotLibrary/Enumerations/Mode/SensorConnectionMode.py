"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SensorConnectionMode
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

class SensorConnectionMode(USINTEnum):
    RC_SENSOR_ALGORITHM = 0
    """
    RC sensor and algorithm\n
    Force-Torque-Sensor connected to RC\n
    Control algorithm in RC
    """

    PLC_SENSOR_RC_ALGORITHM = 1
    """
    PLC sensor and RC algorithm\n
    Force-Torque-Sensor connected to PLC\n
    Control algorithm in RC
    """

    PLC_SENSOR_ALGORITHM = 2
    """
    PLC sensor and algorithm\n
    Force-Torque-Sensor connected to PLC\n
    Control algorithm in PLC
    """
    
    # Set enum size for ctypes evaluation
    setattr(USINTEnum, 'ctypes_type', USINT)    
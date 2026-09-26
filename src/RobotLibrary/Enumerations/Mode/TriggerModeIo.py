"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

TriggerModeIoAuthor:      Thorsten Brach
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

from RobotLibrary.IEC_Types import SINT, SINTEnum

class TriggerModeIo(SINTEnum):
    INVALID = 0
    """Invalid (default)"""

    DIGITAL_INPUT_RISING_EDGE = 10
    """
    Digital Input Rising Edge
    """

    DIGITAL_INPUT_FALLING_EDGE = 11
    """
    Digital Input Falling Edge
    """

    DIGITAL_INPUT_RISING_OR_FALLING_EDGE = 12
    """
    Digital Input Rising or Falling Edge
    """

    DIGITAL_INPUT_RISING_OR_FALLING_EDGE_INVERTED = 13
    """
    Digital Input Rising or Falling Edge (Inverted)
    """

    DIGITAL_OUTPUT_RISING_EDGE = 20
    """
    Digital Output Rising Edge
    """

    DIGITAL_OUTPUT_FALLING_EDGE = 21
    """
    Digital Output Falling Edge
    """

    DIGITAL_OUTPUT_RISING_OR_FALLING_EDGE = 22
    """
    Digital Output Rising or Falling Edge
    """

    DIGITAL_OUTPUT_RISING_OR_FALLING_EDGE_INVERTED = 23
    """
    Digital Output Rising or Falling Edge (Inverted)
    """

    ANALOG_INPUT_EXCEEDING_DEFINED_THRESHOLD = 30
    """
    Analog Input Exceeding Defined Threshold
    """

    ANALOG_INPUT_FALLING_BELOW_DEFINED_THRESHOLD = 31
    """
    Analog Input Falling Below Defined Threshold
    """

    ANALOG_INPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD = 32
    """
    Analog Input Exceeding or Falling Below Defined Threshold
    """

    ANALOG_INPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED = 33
    """
    Analog Input Exceeding or Falling Below Defined Threshold (Inverted)
    """

    ANALOG_INPUT_ENTERING_DEFINED_RANGE = 34
    """
    Analog Input Entering Defined Range
    """

    ANALOG_INPUT_LEAVING_DEFINED_RANGE = 35
    """
    Analog Input Leaving Defined Range
    """

    ANALOG_INPUT_ENTERING_OR_LEAVING_DEFINED_RANGE = 36
    """
    Analog Input Entering or Leaving Defined Range
    """

    ANALOG_INPUT_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED = 37
    """
    Analog Input Entering or Leaving Defined Range (Inverted)
    """

    ANALOG_OUTPUT_EXCEEDING_DEFINED_THRESHOLD = 40
    """
    Analog Output Exceeding Defined Threshold
    """

    ANALOG_OUTPUT_FALLING_BELOW_DEFINED_THRESHOLD = 41
    """
    Analog Output Falling Below Defined Threshold
    """

    ANALOG_OUTPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD = 42
    """
    Analog Output Exceeding or Falling Below Defined Threshold
    """

    ANALOG_OUTPUT_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED = 43
    """
    Analog Output Exceeding or Falling Below Defined Threshold (Inverted)
    """

    ANALOG_OUTPUT_ENTERING_DEFINED_RANGE = 44
    """
    Analog Output Entering Defined Range
    """

    ANALOG_OUTPUT_LEAVING_DEFINED_RANGE = 45
    """
    Analog Output Leaving Defined Range
    """

    ANALOG_OUTPUT_ENTERING_OR_LEAVING_DEFINED_RANGE = 46
    """
    Analog Output Entering or Leaving Defined Range
    """

    ANALOG_OUTPUT_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED = 47
    """
    Analog Output Entering or Leaving Defined Range (Inverted)
    """

    INTEGER_REGISTER_EXCEEDING_DEFINED_THRESHOLD = 50
    """
    Integer Register Exceeding Defined Threshold
    """

    INTEGER_REGISTER_FALLING_BELOW_DEFINED_THRESHOLD = 51
    """
    Integer Register Falling Below Defined Threshold
    """

    INTEGER_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD = 52
    """
    Integer Register Exceeding or Falling Below Defined Threshold
    """

    INTEGER_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_VALUE_INVERTED = 53
    """
    Integer Register Exceeding or Falling Below Defined Value (Inverted)
    """

    INTEGER_REGISTER_ENTERING_DEFINED_RANGE = 54
    """
    Integer Register Entering Defined Range
    """

    INTEGER_REGISTER_LEAVING_DEFINED_RANGE = 55
    """
    Integer Register Leaving Defined Range
    """

    INTEGER_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE = 56
    """
    Integer Register Entering or Leaving Defined Range
    """

    INTEGER_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED = 57
    """
    Integer Register Entering or Leaving Defined Range (Inverted)
    """

    REAL_REGISTER_EXCEEDING_DEFINED_THRESHOLD = 60
    """
    Real Register Exceeding Defined Threshold
    """

    REAL_REGISTER_FALLING_BELOW_DEFINED_THRESHOLD = 61
    """
    Real Register Falling Below Defined Threshold
    """

    REAL_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD = 62
    """
    Real Register Exceeding or Falling Below Defined Threshold
    """

    REAL_REGISTER_EXCEEDING_OR_FALLING_BELOW_DEFINED_THRESHOLD_INVERTED = 63
    """
    Real Register Exceeding or Falling Below Defined Threshold (Inverted)
    """

    REAL_REGISTER_ENTERING_DEFINED_RANGE = 64
    """
    Real Register Entering Defined Range
    """

    REAL_REGISTER_LEAVING_DEFINED_RANGE = 65
    """
    Real Register Leaving Defined Range
    """

    REAL_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE = 66
    """
    Real Register Entering or Leaving Defined Range
    """

    REAL_REGISTER_ENTERING_OR_LEAVING_DEFINED_RANGE_INVERTED = 67
    """
    Real Register Entering or Leaving Defined Range (Inverted)
    """
    # Set enum size for ctypes evaluation
    setattr(SINTEnum, 'ctypes_type', SINT)    
"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      CyclicStateData:
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

from ...IEC_Types import ( UINT,IEC_Struct )
from ..Miscellaneous.RaStatusWord import RaStatusWord

class CyclicStateData(IEC_Struct):
    StatusWord: RaStatusWord
    """Combination of various RA related states."""

    Override: UINT
    """
    Actual override in percentage multiplied by 100
    (see chapter 5.6.2 for more information about the percentage encoding)
    """
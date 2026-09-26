"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      FragmentAction
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

from RobotLibrary.IEC_Types import BOOL, IEC_Struct

class FragmentAction(IEC_Struct):
    Complete: BOOL
    """Bit 00 : Command Message is completely received - Flag to trigger processing of the payload"""

    Reset: BOOL
    """
    Bit 01 :
    (only client->server) The first message fragment of a new CMD resets
    (set all ACR values of this CMD ID to 0) the ACR entry
    """

    Clear: BOOL
    """Bit 02 : Clears the receiving buffer by setting all of its Bytes to 0"""

    BIT03: BOOL
    """Bit 03"""

    BIT04: BOOL
    """Bit 04"""

    BIT05: BOOL
    """Bit 05"""

    BIT06: BOOL
    """Bit 06"""

    BIT07: BOOL
    """Bit 07"""
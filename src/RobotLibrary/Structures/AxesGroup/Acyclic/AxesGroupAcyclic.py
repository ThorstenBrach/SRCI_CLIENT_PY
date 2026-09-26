"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupAcyclic
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
from __future__ import annotations

from RobotLibrary.IEC_Types import IEC_Struct
from RobotLibrary.POUs._internal.ActiveCommandRegisterFB import ActiveCommandRegisterFB


class AxesGroupAcyclic(IEC_Struct):

    ActiveCommandRegister: ActiveCommandRegisterFB
    """Active command register """
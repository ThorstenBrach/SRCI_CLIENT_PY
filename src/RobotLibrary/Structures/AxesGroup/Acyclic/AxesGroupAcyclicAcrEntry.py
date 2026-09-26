"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      AxesGroupAcyclicAcrEntry
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

from RobotLibrary.IEC_Types import UINT, IEC_Struct, ARRAY
from RobotLibrary.POUs._internal.BaseFBs.RobotLibraryBaseFB import RobotLibraryBaseFB
from RobotLibrary.Enumerations.State.ActiveCommandRegisterState import ActiveCommandRegisterState
from RobotLibrary.Structures.AxesGroup.Acyclic.AxesGroupAcyclicAcrEntryCmdBuffer import AxesGroupAcyclicAcrEntryCmdBuffer
from RobotLibrary.Structures.AxesGroup.Acyclic.AxesGroupAcyclicAcrEntryRspBuffer import AxesGroupAcyclicAcrEntryRspBuffer

class AxesGroupAcyclicAcrEntry(IEC_Struct):
    
    UniqueID: UINT
    """Unique identifier"""

    State: ActiveCommandRegisterState
    """State of the command entry"""

    Command : ARRAY[AxesGroupAcyclicAcrEntryCmdBuffer] = ARRAY(1, 2, AxesGroupAcyclicAcrEntryCmdBuffer) 
    """
    Command data
    1 = DataToSend
    2 = DataInBuffer
    """

    Response : ARRAY[AxesGroupAcyclicAcrEntryRspBuffer] = ARRAY(1, 2, AxesGroupAcyclicAcrEntryRspBuffer)
    """
    Response data
    1 = DataRecv
    2 = DataInRecvBuffer
    """

    pCommandFB: RobotLibraryBaseFB
    """Pointer to the corresponding command-FB to enable a callback mechanism"""
    
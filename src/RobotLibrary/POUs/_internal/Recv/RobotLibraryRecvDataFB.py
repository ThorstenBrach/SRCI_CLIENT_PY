"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotLibraryRecvDataFB
Author:      Thorsten Brach
Date:        2026-01-01

Description:

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""
from typing import Any
from RobotLibrary.POUs._internal.Recv.RobotLibraryRecvDataBaseFB import RobotLibraryRecvDataBaseFB
from RobotLibrary.IEC_Types import UDINT,BYTE

class RobotLibraryRecvDataFB(RobotLibraryRecvDataBaseFB):
    
    #VAR_INPUT
    Payload = bytearray()
    """External payload buffer provided by the user"""
    
    PayloadSize : UDINT
    """Size of the external payload buffer"""
    
    #END_VAR_INPUT

    # --------------------------------------------------------
    # __call__ - to enable direct calls of the FB like a function
    #   -----------------------------------------------------
    def __call__(self, Payload : bytearray, PayloadSize : UDINT) -> Any:

        """Call the FB like a function with input parameters."""

        # set input parameters
        self.Payload = Payload
        self.PayloadSize = PayloadSize


    # --------------------------------------------------------
    # UpdatePointer - override in derived classes to set a custom buffer
    # --------------------------------------------------------
    def UpdatePointer(self) -> None:
        """Update the internal payload pointer to the external buffer."""

        if self.Payload is not None:
            # set the internal payload to the external one
            self._payload = self.Payload

   
    # --------------------------------------------------------
    # Reset - override to reset internal state if needed
    # --------------------------------------------------------
    def Reset(self) -> None:
        """Reset the internal state of the FB and clear the payload buffer."""
        
        # clear content of existing payload buffer 
        if self.Payload is not None:
            for i in range(len(self.Payload)):
                self.Payload[i] = 0

        # Call base implementation to clear payload and reset pointers
        super().Reset()

        
    # --------------------------------------------------------
    # ReseSetLifeSignFootert
    # --------------------------------------------------------
    def GetLifeSignFooter(self) -> BYTE:
        result = BYTE(0)        
        # check payload pointer is valid? 
        if self._payload is not None:
            # calculate pointer to last byte
            LifeSignPtr = len(self._payload) - 1
            # get LifeSign byte
            result = BYTE(self._payload[LifeSignPtr])
        else:
            raise Exception("Payload pointer is not valid in GetLifeSignFooter")
        
        return result
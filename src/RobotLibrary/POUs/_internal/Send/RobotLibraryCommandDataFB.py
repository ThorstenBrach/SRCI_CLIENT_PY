"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotLibraryCommandDataFB
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
from RobotLibrary.POUs._internal.Send.RobotLibrarySendDataBaseFB import RobotLibrarySendDataBaseFB
from RobotLibrary.Parameter import PARAMETER_PAYLOAD_MAX

class RobotLibraryCommandDataFB(RobotLibrarySendDataBaseFB):
    
    # VAR_INPUT
    Payload = bytearray(PARAMETER_PAYLOAD_MAX)
    """Payload buffer"""
    # END_VAR
    

    def __init__(self) -> None:
        self.Payload = bytearray(PARAMETER_PAYLOAD_MAX)
        
    
    # --------------------------------------------------------
    # UpdatePointer - override in derived classes to set a custom buffer
    # --------------------------------------------------------
    def UpdatePointer(self) -> None:
        """Update the internal payload pointer to the external buffer."""
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


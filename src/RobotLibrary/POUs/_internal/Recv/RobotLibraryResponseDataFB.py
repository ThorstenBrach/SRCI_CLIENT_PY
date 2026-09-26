"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotLibraryResponseDataFB
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
from RobotLibrary.Parameter import RESPONSE_PAYLOAD_MAX
from RobotLibrary.POUs._internal.Recv.RobotLibraryRecvDataBaseFB import RobotLibraryRecvDataBaseFB
from RobotLibrary.IEC_Types import UDINT, BOOL

class RobotLibraryResponseDataFB(RobotLibraryRecvDataBaseFB):

    #VAR_INPUT
    Payload : bytearray = bytearray(RESPONSE_PAYLOAD_MAX)
    #END_VAR

    # --------------------------------------------------------
    # Derived classes should link external buffers here
    # --------------------------------------------------------
    @property
    def IsPayloadRemaining(self) -> BOOL:
        """Check if there is remaining data in the payload buffer."""
        return BOOL(self.PayloadPtr.value < self.PayloadLen.value)


    # --------------------------------------------------------
    # UpdatePointer - link external buffers here
    # --------------------------------------------------------
    def UpdatePointer(self) -> None:
        """Update the internal payload pointer to the derived buffer."""
    
        if self.Payload is not None:
            # set the internal payload to the external one
            self._payload = self.Payload
            self.PayloadLen = UDINT(len(self.Payload))
        
    # --------------------------------------------------------
    # Reset internal variables
    # --------------------------------------------------------
    def Reset(self) -> None:
        
        if self.Payload is not None:
            # reset buffer content
            for i in range(len(self.Payload)):
                self.Payload[i] = 0
            
        super().Reset()
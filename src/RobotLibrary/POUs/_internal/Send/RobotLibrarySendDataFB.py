"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotLibrarySendDataFB
Author:      Thorsten Brach
Date:        2026-01-06

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
from RobotLibrary.IEC_Types import BYTE, UDINT
from RobotLibrary.POUs._internal.Send.RobotLibrarySendDataBaseFB import RobotLibrarySendDataBaseFB
from RobotLibrary.Parameter import RESPONSE_PAYLOAD_MAX

class RobotLibrarySendDataFB(RobotLibrarySendDataBaseFB):
    
    #region VAR_INPUT
    Payload    : bytearray = bytearray(RESPONSE_PAYLOAD_MAX)
    """ Payload"""

    PayLoadSize : UDINT
    """Size of the Payload array"""
    #endregion
    
    #--------------------------------------------------------
    # __call__ - cylcic call
    #--------------------------------------------------------    
    def __call__(self, Payload : bytearray, PayLoadSize : UDINT ) :

        self.Payload = Payload
        self.PayLoadSize = PayLoadSize  


    # --------------------------------------------------------
    # UpdatePointer -link external buffers here
    # --------------------------------------------------------
    def UpdatePointer(self) -> None:
        """Update the internal payload pointer to the derived buffer."""

    
        if self.Payload is not None:
            # set the internal payload to the external one
            self._payload = self.Payload
            self.PayloadLen = UDINT(len(self.Payload))


    def SetLifeSignFooter (self, LifeSign : BYTE) -> None:
        """Set the life sign footer at the end of the payload."""
        
        # check payload pointer is valid? 
        if self._payload is not None:
            # calculate pointer to last byte
            LifeSignPtr = len(self._payload) - 1
            # set LifeSign byte
            self._payload[LifeSignPtr] = LifeSign.value
        else:
            raise Exception("Payload pointer is not valid in SetLifeSignFooter")


    # --------------------------------------------------------
    # Reset internal variables
    # --------------------------------------------------------
    def Reset(self) -> None:
        
        # call base implementation
        super().Reset()
    
        if self.Payload is not None:
            # reset buffer content
            for i in range(len(self.Payload)):
                self.Payload[i] = 0
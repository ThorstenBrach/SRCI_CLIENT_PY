"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      SystemTime
Author:      Thorsten Brach
Date:        2025-12-18

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

from RobotLibrary.IEC_Types import DATE,TOD, IEC_Struct

class SystemTime(IEC_Struct):
            
    """
    IEC_TIMESTAMP structure representing date and time.
    """

    SystemDate : DATE
    """
    Date part of the system time.
    """

    SystemTime: TOD
    """
    Time part of the system time.
    """

    def __init__(self, **kwargs):
        from RobotLibrary.IEC_Types import DATE, TOD
        import datetime
        now = datetime.datetime.now()
        # IEC DATE: Tage seit 1970-01-01
        epoch = datetime.date(1970, 1, 1)
        days = (now.date() - epoch).days
        # IEC TOD: ms seit Mitternacht
        ms_since_midnight = (now.hour * 3600 + now.minute * 60 + now.second) * 1000 + now.microsecond // 1000
        # Standardwerte setzen, falls nicht explizit übergeben
        if 'SystemDate' not in kwargs:
            kwargs['SystemDate'] = DATE(days)
        if 'SystemTime' not in kwargs:
            kwargs['SystemTime'] = TOD(ms_since_midnight)
        super().__init__(**kwargs)

    
    def __str__(self) -> str:
        # Greife auf das value-Attribut (_FieldProxy) zu und wandle in DATE/TOD um
        from RobotLibrary.IEC_Types import DATE, TOD
        return f"{DATE(self.SystemDate.value).to_string()} {TOD(self.SystemTime.value).to_string()}" #type: ignore
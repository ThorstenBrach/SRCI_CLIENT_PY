"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      RobotCartesianFoce
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

from RobotLibrary.IEC_Types import REAL, IEC_Struct

    
class RobotCartesianForceShort(IEC_Struct):
  
    X: REAL
    """
    Force on the X-Axis
    """
    
    Y: REAL
    """ 
    Force on the Y-Axis
    """
    
    Z: REAL
    """
    Force on the Z-Axis
    """
    
    Rx: REAL
    """
    Force around the X-Axis (RX)
    """
    
    Ry: REAL
    """
    Force around the Y-Axis (RY)
    """
    
    Rz: REAL
    """
    Force around the Z-Axis (RZ)
    """


class RobotCartesianForceExt(RobotCartesianForceShort):
  E1 : REAL
  """ 
  Force on the first external axis
  """
  
  E2 : REAL
  """
  Force of second external axis
  """
  
  E3 : REAL
  """
  Force of third external axis  
  """

  E4 : REAL
  """ 
  Force of fourth external axis
  """

  E5 : REAL
  """
  Force of fifth external axis
  """

  E6 : REAL
  """
  Force of sixth external axis
  """
    
class RobotCartesianForce(IEC_Struct):
    X: REAL
    """
    Force on the X-Axis
    """
    
    Y: REAL
    """ 
    Force on the Y-Axis
    """
    
    Z: REAL
    """
    Force on the Z-Axis
    """
    
    Rx: REAL
    """
    Force around the X-Axis (RX)
    """
    
    Ry: REAL
    """
    Force around the Y-Axis (RY)
    """
    
    Rz: REAL
    """
    Force around the Z-Axis (RZ)
    """
    
    E1 : REAL
    """ 
    Force on the first external axis
    """
    
    E2 : REAL
    """
    Force of second external axis
    """
    
    E3 : REAL
    """
    Force of third external axis  
    """

    E4 : REAL
    """ 
    Force of fourth external axis
    """

    E5 : REAL
    """
    Force of fifth external axis
    """

    E6 : REAL
    """
    Force of sixth external axis
    """
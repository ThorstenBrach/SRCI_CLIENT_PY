"""
-------------------------------------------------------------------------
SRCI Robot Library
-------------------------------------------------------------------------

Object:      Check
Author:      Thorsten Brach
Date:        2026-01-11

Description:
  Converts various data types to their string representations

Copyright:
    (C) 2026 Thorsten Brach. All rights reserved
    Licensed under the LGPL-3.0 license.

Disclaimer:
    This project is provided without any guarantee and can be used for
    private and commercial purposes. Any use is at the user's
    own risk and responsibility.
-------------------------------------------------------------------------
"""
import copy
from RobotLibrary.Structures.Data.Frame.FrameData import FrameData
from RobotLibrary.Structures.Data.Load.LoadData import LoadData
from RobotLibrary.Structures.Data.Tool.ToolData import ToolData
from RobotLibrary.Structures.Data.WorkArea.RobotWorkAreaData import RobotWorkAreaData
from RobotLibrary.Structures.Dynamics.DefaultDynamics import DefaultDynamics
from RobotLibrary.Structures.Dynamics.ReferenceDynamics import ReferenceDynamics
from RobotLibrary.Structures.Miscellaneous.SWLimits import SWLimits

#---------------------------------------------------------
# IsFrameDataEqual - Compares two frame data sets for equality
#---------------------------------------------------------
def IsFrameDataEqual(Data1 : FrameData, Data2 : FrameData, IgnoreTimestamp : bool) -> bool:
    """
    Compares two frame data sets for equality.
    
    Args:
        Data1: The first frame data set.
        Data2: The second frame data set.
        IgnoreTimestamp: If True, timestamps will be ignored during comparison.
        
    Returns:
        bool: True if both frame data sets are equal, False otherwise.
    """
    # make a copy to not modify the original data
    _tmpData1  : FrameData = copy.deepcopy(Data1)
    _tmpData2  : FrameData = copy.deepcopy(Data2)

    # check if timestamps should be ignored ?
    if IgnoreTimestamp:

        _tmpData1.Timestamp = _tmpData2.Timestamp

    # compare the data
    if _tmpData1 == _tmpData2:
        return True
    else:
        return False


#---------------------------------------------------------
# IsLoadDataEqual - Compares two load data sets for equality
#---------------------------------------------------------
def IsLoadDataEqual(Data1 : LoadData, Data2 : LoadData, IgnoreTimestamp : bool) -> bool:
    """
    Compares two load data sets for equality.
    
    Args:
        Data1: The first load data set.
        Data2: The second load data set.
        IgnoreTimestamp: If True, timestamps will be ignored during comparison.
        
    Returns:
        bool: True if both load data sets are equal, False otherwise.
    """
    # make a copy to not modify the original data
    _tmpData1  : LoadData = copy.deepcopy(Data1)
    _tmpData2  : LoadData = copy.deepcopy(Data2)

    # check if timestamps should be ignored ?
    if IgnoreTimestamp:

        _tmpData1.Timestamp = _tmpData2.Timestamp

    # compare the data
    if _tmpData1 == _tmpData2:
        return True
    else:
        return False


#---------------------------------------------------------
# IsToolDataEqual - Compares two tool data sets for equality
#---------------------------------------------------------
def IsToolDataEqual(Data1 : ToolData, Data2 : ToolData, IgnoreTimestamp : bool) -> bool:
    """
    Compares two tool data sets for equality.
    
    Args:
        Data1: The first tool data set.
        Data2: The second tool data set.
        IgnoreTimestamp: If True, timestamps will be ignored during comparison.
        
    Returns:
        bool: True if both tool data sets are equal, False otherwise.
    """
    # make a copy to not modify the original data
    _tmpData1  : ToolData = copy.deepcopy(Data1)
    _tmpData2  : ToolData = copy.deepcopy(Data2)
    
    # check if timestamps should be ignored ?
    if IgnoreTimestamp:

        _tmpData1.Timestamp = _tmpData2.Timestamp

    # compare the data
    if _tmpData1 == _tmpData2:
        return True
    else:
        return False
    


#---------------------------------------------------------
# IsWorkAreaEqual - Compares two work area data sets for equality
#---------------------------------------------------------
def IsWorkAreaEqual(Data1 : RobotWorkAreaData, Data2 : RobotWorkAreaData, IgnoreTimestamp : bool) -> bool:
    """
    Compares two work area data sets for equality.
    
    Args:
        Data1: The first work area data set.
        Data2: The second work area data set.
        IgnoreTimestamp: If True, timestamps will be ignored during comparison.
        
    Returns:
        bool: True if both work area data sets are equal, False otherwise.
    """
    # make a copy to not modify the original data
    _tmpData1  : RobotWorkAreaData = copy.deepcopy(Data1)
    _tmpData2  : RobotWorkAreaData = copy.deepcopy(Data2)
    
    # check if timestamps should be ignored ?
    if IgnoreTimestamp:

        _tmpData1.Timestamp = _tmpData2.Timestamp

    # compare the data
    if _tmpData1 == _tmpData2:
        return True
    else:
        return False    
    
#---------------------------------------------------------
# IsDefaultDynamicsEqual - Compares two default dynamics sets for equality
#---------------------------------------------------------
def IsDefaultDynamicsEqual(Data1 : DefaultDynamics, Data2 : DefaultDynamics, IgnoreTimestamp : bool) -> bool:
    """
    Compares two default dynamics sets for equality.
    
    Args:
        Data1: The first default dynamics data set.
        Data2: The second default dynamics data set.
        IgnoreTimestamp: If True, timestamps will be ignored during comparison.
        
    Returns:
        bool: True if both default dynamics data sets are equal, False otherwise.
    """
    # make a copy to not modify the original data
    _tmpData1  : DefaultDynamics = copy.deepcopy(Data1)
    _tmpData2  : DefaultDynamics = copy.deepcopy(Data2)
    
    # check if timestamps should be ignored ?
    if IgnoreTimestamp:

        _tmpData1.Timestamp = _tmpData2.Timestamp

    # compare the data
    if _tmpData1 == _tmpData2:
        return True
    else:
        return False    


#---------------------------------------------------------
# IsReferenceDynamicsEqual - Compares two reference dynamics sets for equality
#---------------------------------------------------------
def IsReferenceDynamicsEqual(Data1 : ReferenceDynamics, Data2 : ReferenceDynamics, IgnoreTimestamp : bool) -> bool:
    """
    Compares two reference dynamics sets for equality.
    
    Args:
        Data1: The first reference dynamics data set.
        Data2: The second reference dynamics data set.
        IgnoreTimestamp: If True, timestamps will be ignored during comparison.
        
    Returns:
        bool: True if both reference dynamics data sets are equal, False otherwise.
    """
    # make a copy to not modify the original data
    _tmpData1  : ReferenceDynamics = copy.deepcopy(Data1)
    _tmpData2  : ReferenceDynamics = copy.deepcopy(Data2)
    
    # check if timestamps should be ignored ?
    if IgnoreTimestamp:

        _tmpData1.Timestamp = _tmpData2.Timestamp

    # compare the data
    if _tmpData1 == _tmpData2:
        return True
    else:
        return False    

#---------------------------------------------------------
# IsSwLimitsEqual - Compares two software limits sets for equality
#---------------------------------------------------------

def IsSwLimitsEqual(Data1 : SWLimits, Data2 : SWLimits, IgnoreTimestamp : bool) -> bool:
    """
    Compares two software limits sets for equality.
    
    Args:
        Data1: The first software limits data set.
        Data2: The second software limits data set.
        IgnoreTimestamp: If True, timestamps will be ignored during comparison.
        
    Returns:
        bool: True if both software limits data sets are equal, False otherwise.
    """
    # make a copy to not modify the original data
    _tmpData1  : SWLimits = copy.deepcopy(Data1)
    _tmpData2  : SWLimits = copy.deepcopy(Data2)
    
    # check if timestamps should be ignored ?
    if IgnoreTimestamp:

        _tmpData1.Timestamp = _tmpData2.Timestamp

    # compare the data
    if _tmpData1 == _tmpData2:
        return True
    else:
        return False    
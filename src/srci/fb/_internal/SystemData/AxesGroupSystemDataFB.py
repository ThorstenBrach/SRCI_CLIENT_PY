"""AxesGroupSystemDataFB

ST-Source: POUs/_internal/SystemData/AxesGroupSystemDataFB.st
Generated from the PLC library by ``python -m tools.st2py`` - DO NOT EDIT.
"""

# ruff: noqa
# fmt: off
# mypy: disable-error-code="no-any-return,assignment,arg-type,attr-defined,union-attr,operator,index,misc,override,call-arg,comparison-overlap,return-value,has-type,name-defined,no-untyped-def,var-annotated,valid-type,call-overload,unreachable,truthy-function"
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from srci.types import iec as _iec
import srci.types as _T
from srci.iec.conv import DINT_TO_UDINT, USINT_TO_STRING
from srci.iec.fb import FunctionBlock
from srci.iec.rt import copy_into
from srci.types import DefaultDynamics, Frame, FrameData, Load, LoadData, MessageType, ReferenceDynamics, RobotLibraryConstants, RobotLibraryWarningIdEnum, RobotWorkArea, RobotWorkAreaData, SWLimits, Severity, SystemTime, ToolData

if TYPE_CHECKING:
    from srci.fb._internal.BaseFBs.RobotLibraryBaseFB import RobotLibraryBaseFB
    from srci.iec.rt import Ptr

__all__ = ['AxesGroupSystemDataFB']


class AxesGroupSystemDataFB(FunctionBlock):

    def _init_vars_(self) -> None:
        # VAR_INPUT
        # Pointer to ToolData array
        self.ToolDataPtr: Ptr | None = None
        # Lower dimension of ToolData array
        self.ToolDataMin: int = 0
        # Lower dimension of ToolData array
        self.ToolDataMax: int = 0
        # Amount of ToolData elements in array
        self.ToolDataCount: int = 0
        # Pointer to LoadData array
        self.LoadDataPtr: Ptr | None = None
        # Lower dimension of LoadData array
        self.LoadDataMin: int = 0
        # Lower dimension of LoadData array
        self.LoadDataMax: int = 0
        # Amount of Load elements in array
        self.LoadDataCount: int = 0
        # Pointer to FrameData array
        self.FrameDataPtr: Ptr | None = None
        # Lower dimension of FrameData array
        self.FrameDataMin: int = 0
        # Lower dimension of FrameData array
        self.FrameDataMax: int = 0
        # Amount of FrameData elements in array
        self.FrameDataCount: int = 0
        # Pointer to WorkAreas array
        self.WorkAreasPtr: Ptr | None = None
        # Lower dimension of WorkAreas array
        self.WorkAreasMin: int = 0
        # Lower dimension of WorkAreas array
        self.WorkAreasMax: int = 0
        # Amount of WorkAreas elements in array
        self.WorkAreasCount: int = 0
        # Software limits stored on PLC
        self.SWLimits: SWLimits | None = None
        # Default dynamics stored on PLC. For more information refer to 5.5.7
        self.DefaultDynamics: DefaultDynamics | None = None
        # Reference dynamics stored on PLC. For more information refer to 5.5.7
        self.ReferenceDynamics: ReferenceDynamics | None = None

    def __call__(self, *, ToolDataPtr: Ptr | None | None = None, ToolDataMin: int | None = None, ToolDataMax: int | None = None, ToolDataCount: int | None = None, LoadDataPtr: Ptr | None | None = None, LoadDataMin: int | None = None, LoadDataMax: int | None = None, LoadDataCount: int | None = None, FrameDataPtr: Ptr | None | None = None, FrameDataMin: int | None = None, FrameDataMax: int | None = None, FrameDataCount: int | None = None, WorkAreasPtr: Ptr | None | None = None, WorkAreasMin: int | None = None, WorkAreasMax: int | None = None, WorkAreasCount: int | None = None, SWLimits: SWLimits | None | None = None, DefaultDynamics: DefaultDynamics | None | None = None, ReferenceDynamics: ReferenceDynamics | None | None = None) -> None:
        if ToolDataPtr is not None:
            self.ToolDataPtr = ToolDataPtr
        if ToolDataMin is not None:
            self.ToolDataMin = ToolDataMin
        if ToolDataMax is not None:
            self.ToolDataMax = ToolDataMax
        if ToolDataCount is not None:
            self.ToolDataCount = ToolDataCount
        if LoadDataPtr is not None:
            self.LoadDataPtr = LoadDataPtr
        if LoadDataMin is not None:
            self.LoadDataMin = LoadDataMin
        if LoadDataMax is not None:
            self.LoadDataMax = LoadDataMax
        if LoadDataCount is not None:
            self.LoadDataCount = LoadDataCount
        if FrameDataPtr is not None:
            self.FrameDataPtr = FrameDataPtr
        if FrameDataMin is not None:
            self.FrameDataMin = FrameDataMin
        if FrameDataMax is not None:
            self.FrameDataMax = FrameDataMax
        if FrameDataCount is not None:
            self.FrameDataCount = FrameDataCount
        if WorkAreasPtr is not None:
            self.WorkAreasPtr = WorkAreasPtr
        if WorkAreasMin is not None:
            self.WorkAreasMin = WorkAreasMin
        if WorkAreasMax is not None:
            self.WorkAreasMax = WorkAreasMax
        if WorkAreasCount is not None:
            self.WorkAreasCount = WorkAreasCount
        if SWLimits is not None:
            self.SWLimits = SWLimits
        if DefaultDynamics is not None:
            self.DefaultDynamics = DefaultDynamics
        if ReferenceDynamics is not None:
            self.ReferenceDynamics = ReferenceDynamics
        self.__body()

    def __body(self) -> None:
        pass

    def UpdateDefaultDynamics(self, *, DynamicValues: DefaultDynamics | None = None) -> int:
        if DynamicValues is None:
            DynamicValues = DefaultDynamics()
        UpdateDefaultDynamics: int = 0

        # Check pointer is vaild ?
        if not self.DefaultDynamics is not None:
            return UpdateDefaultDynamics

        # Applay new values
        copy_into(self.DefaultDynamics, DynamicValues)
        return UpdateDefaultDynamics

    def UpdateFrameData(self, *, Caller: RobotLibraryBaseFB | None = None, SystemTime: _T.SystemTime | None = None, FrameNo: int = 0, FrameData: _T.FrameData | None = None) -> int:
        if SystemTime is None:
            SystemTime = _T.SystemTime()
        if FrameData is None:
            FrameData = _T.FrameData()
        UpdateFrameData: int = 0
        # pointer to frame data
        pFrameData: Ptr | None = None

        # Check pointer is vaild ?
        if self.FrameDataPtr is None:
            return UpdateFrameData

        # Check Frame number is in range ?
        if FrameNo < self.FrameDataMin or FrameNo > self.FrameDataMax:
            if Caller is not None:
                # set warning
                Caller.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SAVE_FRAME_FAILED, Overwrite=False)

                # Create log entry
                Caller.CreateLogMessagePara1(Timestamp=SystemTime, MessageType=MessageType.CMD, Severity=Severity.WARNING, MessageCode=Caller.WarningID, MessageText='Save FrameData failed. Index {1} not available in user defined system data', Para1=USINT_TO_STRING(FrameNo))

            return UpdateFrameData

        # Calculate pointer address for the index of the FrameData Array
        pFrameData = self.FrameDataPtr + (FrameNo - DINT_TO_UDINT(self.FrameDataMin)) * 32
        # copy frame data to Array index
        pFrameData.deref(_iec.StructType(Frame)).Available = True
        copy_into(pFrameData.deref(_iec.StructType(Frame)).Data, FrameData)
        return UpdateFrameData

    def UpdateLoadData(self, *, Caller: RobotLibraryBaseFB | None = None, SystemTime: _T.SystemTime | None = None, LoadNo: int = 0, LoadData: _T.LoadData | None = None) -> int:
        if SystemTime is None:
            SystemTime = _T.SystemTime()
        if LoadData is None:
            LoadData = _T.LoadData()
        UpdateLoadData: int = 0
        # pointer to load data
        pLoadData: Ptr | None = None

        # Check pointer is vaild ?
        if self.LoadDataPtr is None:
            return UpdateLoadData

        # Check Load number is in range ?
        if LoadNo < self.LoadDataMin or LoadNo > self.LoadDataMax:
            if Caller is not None:
                # set warning
                Caller.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SAVE_LOAD_FAILED, Overwrite=False)

                # Create log entry
                Caller.CreateLogMessagePara1(Timestamp=SystemTime, MessageType=MessageType.CMD, Severity=Severity.WARNING, MessageCode=Caller.WarningID, MessageText='Save LoadData failed. Index {1} not available in user defined system data', Para1=USINT_TO_STRING(LoadNo))

            return UpdateLoadData

        # Calculate pointer address for the index of the LoadData Array
        pLoadData = self.LoadDataPtr + (LoadNo - DINT_TO_UDINT(self.LoadDataMin)) * 47
        # copy load data to Array index
        pLoadData.deref(_iec.StructType(Load)).Available = True
        copy_into(pLoadData.deref(_iec.StructType(Load)).Data, LoadData)
        return UpdateLoadData

    def UpdateReferenceDynamics(self, *, DynamicValues: ReferenceDynamics | None = None) -> int:
        if DynamicValues is None:
            DynamicValues = ReferenceDynamics()
        UpdateReferenceDynamics: int = 0

        # Check pointer is vaild ?
        if not self.ReferenceDynamics is not None:
            return UpdateReferenceDynamics

        # Applay new values
        copy_into(self.ReferenceDynamics, DynamicValues)
        return UpdateReferenceDynamics

    def UpdateSWLimits(self, *, LimitValues: SWLimits | None = None) -> int:
        if LimitValues is None:
            LimitValues = SWLimits()
        UpdateSWLimits: int = 0

        # Check pointer is vaild ?
        if not self.SWLimits is not None:
            return UpdateSWLimits

        # Applay new values
        copy_into(self.SWLimits, LimitValues)
        return UpdateSWLimits

    def UpdateToolData(self, *, Caller: RobotLibraryBaseFB | None = None, SystemTime: _T.SystemTime | None = None, ToolNo: int = 0, ToolData: _T.ToolData | None = None) -> int:
        if SystemTime is None:
            SystemTime = _T.SystemTime()
        if ToolData is None:
            ToolData = _T.ToolData()
        UpdateToolData: int = 0
        # pointer to tool data
        pToolData: Ptr | None = None

        # Check pointer is vaild ?
        if self.ToolDataPtr is None:
            return UpdateToolData

        # Check Tool number is in range ?
        if ToolNo < self.ToolDataMin or ToolNo > self.ToolDataMax:
            if Caller is not None:
                # set warning
                Caller.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SAVE_TOOL_FAILED, Overwrite=False)

                # Create log entry
                Caller.CreateLogMessagePara1(Timestamp=SystemTime, MessageType=MessageType.CMD, Severity=Severity.WARNING, MessageCode=Caller.WarningID, MessageText='Save ToolData failed. Index {1} not available in user defined system data', Para1=USINT_TO_STRING(ToolNo))

            return UpdateToolData
        # {warning 'ToDo: Compiler Fehler'}
        # // Calculate pointer address for the index of the ToolData Array
        # pToolData := ToolDataPtr + (( ToolNo - DINT_TO_UDINT(ToolDataMin)) * SIZEOF(Tool));
        # // copy tool data to Array index
        # pToolData^.Available := TRUE;
        # pToolData^.Data := ToolData;
        return UpdateToolData

    def UpdateWorAreas(self, *, Caller: RobotLibraryBaseFB | None = None, SystemTime: _T.SystemTime | None = None, WorkAreaNo: int = 0, WorkAreaData: RobotWorkAreaData | None = None) -> int:
        if SystemTime is None:
            SystemTime = _T.SystemTime()
        if WorkAreaData is None:
            WorkAreaData = RobotWorkAreaData()
        UpdateWorAreas: int = 0
        # pointer to WorkArea
        pWorkAreaData: Ptr | None = None

        # Check pointer is vaild ?
        if self.WorkAreasPtr is None:
            return UpdateWorAreas

        # Check WorkArea number is in range ?
        if WorkAreaNo < self.WorkAreasMin or WorkAreaNo > self.WorkAreasMax:
            if Caller is not None:
                # set warning
                Caller.SetWarning(WarningID=RobotLibraryWarningIdEnum.WARN_SAVE_WORKAREA_FAILED, Overwrite=False)

                # Create log entry
                Caller.CreateLogMessagePara1(Timestamp=SystemTime, MessageType=MessageType.CMD, Severity=Severity.WARNING, MessageCode=Caller.WarningID, MessageText='Save WorkArea failed. Index {1} not available in user defined system data', Para1=USINT_TO_STRING(WorkAreaNo))

            return UpdateWorAreas

        # Calculate pointer address for the index of the WorkArea Array
        pWorkAreaData = self.WorkAreasPtr + (WorkAreaNo - DINT_TO_UDINT(self.WorkAreasMin)) * 149
        # copy WorkArea to Array index
        pWorkAreaData.deref(_iec.StructType(RobotWorkArea)).Available = True
        copy_into(pWorkAreaData.deref(_iec.StructType(RobotWorkArea)).Data, WorkAreaData)
        return UpdateWorAreas

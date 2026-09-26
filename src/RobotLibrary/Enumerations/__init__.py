"""Enumerations module for robot library."""

# ArmConfig
from .ArmConfig.ArmConfigElbow import ArmConfigElbow
from .ArmConfig.ArmConfigShoulder import ArmConfigShoulder
from .ArmConfig.ArmConfigWrist import ArmConfigWrist

# Events
from .Events.ErrorIdEnum import ErrorIdEnum
from .Events.InfoIdEnum import InfoIdEnum
from .Events.WarningIdEnum import WarningIdEnum

# Flag
from .Flag.SequenceFlag import SequenceFlag

# Level
from .Level.LogLevel import LogLevel
from .Level.MessageLevel import MessageLevel
from .Level.PriorityLevel import PriorityLevel

# Miscellaneous
from .Miscellaneous.AxisUnit import AxisUnit
from .Miscellaneous.CircPlane import CircPlane
from .Miscellaneous.ComDirection import ComDirection
from .Miscellaneous.ControlHalfByte import ControlHalfByte
from .Miscellaneous.ErrorReaction import ErrorReaction
from .Miscellaneous.LoadMeasurementSteps import LoadMeasurementSteps
from .Miscellaneous.PathChoice import PathChoice
from .Miscellaneous.ReferenceElement import ReferenceElement
from .Miscellaneous.Severity import Severity
from .Miscellaneous.SyncDirection import SyncDirection
from .Miscellaneous.SyncReaction import SyncReaction
from .Miscellaneous.SyncTime import SyncTime
from .Miscellaneous.TriggerCondition import TriggerCondition
from .Miscellaneous.UnitLimitAxis import UnitLimitAxis

# Mode
from .Mode.AbortingMode import AbortingMode
from .Mode.BlendingMode import BlendingMode
from .Mode.CircMode import CircMode
from .Mode.CollisionReactionMode import CollisionReactionMode
from .Mode.ConnectionMode import ConnectionMode
from .Mode.DefinitionMode import DefinitionMode
from .Mode.DetectionMode import DetectionMode
from .Mode.ErrorTriggerMode import ErrorTriggerMode
from .Mode.ExecutionMode import ExecutionMode
from .Mode.FrameCalculationMode import FrameCalculationMode
from .Mode.FunctionMode import FunctionMode
from .Mode.InterpolationMode import InterpolationMode
from .Mode.JogMode import JogMode
from .Mode.LimitMode import LimitMode
from .Mode.LoadMeasurementMode import LoadMeasurementMode
from .Mode.LogonMode import LogonMode
from .Mode.MeasuringIoMode import MeasuringIoMode
from .Mode.MeasuringUnitMode import MeasuringUnitMode
from .Mode.OperationMode import OperationMode
from .Mode.OrientationMode import OrientationMode
from .Mode.OriMode import OriMode
from .Mode.ProcessingMode import ProcessingMode
from .Mode.ResistanceForceMode import ResistanceForceMode
from .Mode.ReturnMode import ReturnMode
from .Mode.SensorConnectionMode import SensorConnectionMode
from .Mode.SingularityAvoidanceMode import SingularityAvoidanceMode
from .Mode.SplineMode import SplineMode
from .Mode.StepMode import StepMode
from .Mode.StopMode import StopMode
from .Mode.SyncInMode import SyncInMode
from .Mode.SyncMode import SyncMode
from .Mode.ThresholdMode import ThresholdMode
from .Mode.ToolCalculationMode import ToolCalculationMode
from .Mode.TrajectoryMode import TrajectoryMode
from .Mode.TransformMode import TransformMode
from .Mode.TriggerModeIo import TriggerModeIo
from .Mode.TriggerModeLimit import TriggerModeLimit
from .Mode.TriggerModeMeasurement import TriggerModeMeasurement
from .Mode.TriggerReactionMode import TriggerReactionMode
from .Mode.TurnMode import TurnMode
from .Mode.WorkAreaReactionMode import WorkAreaReactionMode

# State
from .State.ActiveCommandRegisterState import ActiveCommandRegisterState
from .State.BufferStateCmd import BufferStateCmd
from .State.BufferStateRsp import BufferStateRsp
from .State.CmdMessageState import CmdMessageState
from .State.InitializationState import InitializationState
from .State.RaPowerState import RaPowerState
from .State.RaSequenceState import RaSequenceState
from .State.RiState import RiState
from .State.TelegramState import TelegramState

# Type
from .Type.AreaType import AreaType
from .Type.AxesGroupParameterCmdEntries import AxesGroupParameterCmdEntries
from .Type.CmdType import CmdType
from .Type.ConveyorType import ConveyorType
from .Type.DataType import DataType
from .Type.MessageType import MessageType
from .Type.ReferenceType import ReferenceType
from .Type.UnitType import UnitType

__all__ = [
    # ArmConfig
    "ArmConfigElbow",
    "ArmConfigShoulder",
    "ArmConfigWrist",
    # Events
    "ErrorIdEnum",
    "InfoIdEnum",
    "WarningIdEnum",
    # Flag
    "SequenceFlag",
    # Level
    "LogLevel",
    "MessageLevel",
    "PriorityLevel",
    # Miscellaneous
    "AxisUnit",
    "CircPlane",
    "ComDirection",
    "ControlHalfByte",
    "ErrorReaction",
    "LoadMeasurementSteps",
    "PathChoice",
    "ReferenceElement",
    "Severity",
    "SyncDirection",
    "SyncReaction",
    "SyncTime",
    "TriggerCondition",
    "UnitLimitAxis",
    # Mode
    "AbortingMode",
    "BlendingMode",
    "CircMode",
    "CollisionReactionMode",
    "ConnectionMode",
    "DefinitionMode",
    "DetectionMode",
    "ErrorTriggerMode",
    "ExecutionMode",
    "FrameCalculationMode",
    "FunctionMode",
    "InterpolationMode",
    "JogMode",
    "LimitMode",
    "LoadMeasurementMode",
    "LogonMode",
    "MeasuringIoMode",
    "MeasuringUnitMode",
    "OperationMode",
    "OrientationMode",
    "OriMode",
    "ProcessingMode",
    "ResistanceForceMode",
    "ReturnMode",
    "SensorConnectionMode",
    "SingularityAvoidanceMode",
    "SplineMode",
    "StepMode",
    "StopMode",
    "SyncInMode",
    "SyncMode",
    "ThresholdMode",
    "ToolCalculationMode",
    "TrajectoryMode",
    "TransformMode",
    "TriggerModeIo",
    "TriggerModeLimit",
    "TriggerModeMeasurement",
    "TriggerReactionMode",
    "TurnMode",
    "WorkAreaReactionMode",
    # State
    "ActiveCommandRegisterState",
    "BufferStateCmd",
    "BufferStateRsp",
    "CmdMessageState",
    "InitializationState",
    "RaPowerState",
    "RaSequenceState",
    "RiState",
    "TelegramState",
    # Type
    "AreaType",
    "AxesGroupParameterCmdEntries",
    "CmdType",
    "ConveyorType",
    "DataType",
    "MessageType",
    "ReferenceType",
    "UnitType",
]
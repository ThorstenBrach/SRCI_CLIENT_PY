"""MC_RobotTaskFB.HandleSync: output Synchronized (spec 5.6.7.1), without the SDK."""

from __future__ import annotations

import pytest

from srci.fb.General.MC_RobotTask.MC_RobotTaskFB import MC_RobotTaskFB
from srci.types import (
    AxesGroup,
    DefaultDynamics,
    Frame,
    Load,
    ReferenceDynamics,
    RobotWorkArea,
    SWLimits,
    Tool,
)

FUNCTIONS = {
    "SwLimits": ("ReadRobotSWLimits", "WriteRobotSWLimits"),
    "WorkArea": ("ReadWorkArea", "WriteWorkArea"),
}


def handle_sync(ag: AxesGroup) -> MC_RobotTaskFB:
    rt = MC_RobotTaskFB()
    rt.HandleSync(
        AxesGroup=ag,
        ToolData=[Tool()],
        FrameData=[Frame()],
        LoadData=[Load()],
        WorkAreas=[RobotWorkArea()],
        SWLimits=SWLimits(),
        DefaultDynamics=DefaultDynamics(),
        ReferenceDynamics=ReferenceDynamics(),
    )
    return rt


def axes_group(*, work_area_supported: bool, initialized: bool = True) -> AxesGroup:
    """SW limits and work areas enabled for the synchronisation; only the SW limits are in sync."""
    ag = AxesGroup()
    ag.State.Initialized = initialized
    ag.State.DataEnableSync.EnableSyncSWLimits = True
    ag.State.DataEnableSync.EnableSyncWorkArea = True
    ag.State.SyncStatePlc.InSync.SwLimits = ag.State.SyncStateRc.InSync.SwLimits = True
    functions = ag.State.RobotData.RCSupportedFunctions
    for name in FUNCTIONS["SwLimits"]:
        setattr(functions, name, True)
    for name in FUNCTIONS["WorkArea"]:
        setattr(functions, name, work_area_supported)
    return ag


def test_supported_data_set_out_of_sync_blocks_synchronized() -> None:
    assert not handle_sync(axes_group(work_area_supported=True)).Synchronized


def test_unsupported_data_set_does_not_block_synchronized() -> None:
    """F24 (spec 5.6.7.1): '… or not supported by the RC does not impact the RI state Synchronized'."""
    assert handle_sync(axes_group(work_area_supported=False)).Synchronized


@pytest.mark.parametrize("work_area_supported", [False, True])
def test_not_synchronized_before_initialized(work_area_supported: bool) -> None:
    """The RC functions are unknown before the initialisation."""
    ag = axes_group(work_area_supported=work_area_supported, initialized=False)
    ag.State.SyncStatePlc.InSync.SwLimits = ag.State.SyncStateRc.InSync.SwLimits = False
    assert not handle_sync(ag).Synchronized

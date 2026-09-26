"""Telegram level tests against the real SRCI SDK (robot controller side).

The client side is the ported telegram code (MC_RobotTaskFB_Telegram); the RI handshake
is done by hand here - the complete RobotTask follows in M6.
"""

from __future__ import annotations

import pytest

from srci.functions.Convert.Misc import DwordToRaStatusWord, PlcOptionalCyclicToUint, RobOptionalCyclicToUint
from srci.sim.gateway import PlcGatewaySimulator
from srci.sim.sdk import SdkSimulator, sdk_transport
from srci.transport import TcpTransport, Transport
from srci.types import AxesGroup, OperationMode, TelegramRobToPlc, TelegramState
from tests.helpers import Host, new_axes_group

SIZE = 128
CONTROL_INITIALIZE, CONTROL_RESET = 1, 3


class Client:
    """Minimal client: header fields + LifeSign handling, telegrams via the ported codec."""

    def __init__(self, transport: Transport, rob_cartesian: bool = False) -> None:
        self.transport = transport
        self.host, (self.ag, self.acr) = Host(), new_axes_group()
        self.host._parCfg.Com.TelegramLengthPlcToRob = SIZE
        self.host._parCfg.Com.TelegramLengthRobToPlc = SIZE
        self.ag.Parameter.Rob.OptionalCyclic.UseCartesianPosition = rob_cartesian
        self.ag.CyclicOptional.RobToPlc.CartesianPosition.Active = rob_cartesian
        h = self.host.Telegram.PlcToRob.Header
        h.SRCIVersion = 0x25
        h.TelegramLengthPlcToRob = SIZE
        h.TelegramLengthRobToPlc = SIZE
        h.TelegramNumberPlcToRob = PlcOptionalCyclicToUint(self.ag.Parameter.Plc.OptionalCyclic)
        h.TelegramNumberRobToPlc = RobOptionalCyclicToUint(self.ag.Parameter.Rob.OptionalCyclic)
        h.ClientDate = 13_000
        h.ClientTime = 12 * 3_600_000
        self.lifesign = 0
        self.out = bytearray(SIZE)

    def cycle(self, control: int = CONTROL_INITIALIZE, seq: int | None = None) -> AxesGroup:
        self.lifesign = self.lifesign % 15 + 1
        h = self.host.Telegram.PlcToRob.Header
        h.FastStop_LifeSign = self.lifesign  # FastStop in the high nibble = 0
        h.AxesGroupID_Control = control  # AxesGroupID 0 (high nibble), control (low nibble)
        self.ag.Cyclic.PlcToRob.LifeSign = self.lifesign
        if seq is not None:
            self.host.Telegram.PlcToRob.Sequence[0].Header.SEQ_ACK = seq
        self.host.CreateSendPayload(self.ag, self.out)
        self.host.ParseRecvPayload(self.ag, self.transport.exchange(self.out))
        return self.ag

    def initialize(self) -> None:
        for control in (CONTROL_RESET, CONTROL_RESET, CONTROL_INITIALIZE, CONTROL_INITIALIZE):
            self.cycle(control)

    @property
    def rob(self) -> TelegramRobToPlc:
        return self.host.Telegram.RobToPlc


def test_sdk_library(sdk: SdkSimulator) -> None:
    assert sdk.sdk_version.startswith("1.5")
    with pytest.raises(ValueError):
        sdk.exchange(bytes(600), SIZE)


def test_ri_handshake(sdk: SdkSimulator) -> None:
    c = Client(sdk_transport(sdk, SIZE, SIZE))
    c.cycle(CONTROL_RESET)
    assert c.rob.Header.TelegramState == TelegramState.READY_FOR_INITIALIZATION
    c.cycle(CONTROL_INITIALIZE)
    assert c.rob.Header.TelegramState == TelegramState.INITIALIZED
    assert sdk.states.ri_state == 71  # RL_SERVER_STATE_RI_INITIALIZED
    h = c.rob.Header
    assert (h.SRCIVersion.MajorVersion, h.SRCIVersion.MinorVersion) == (1, 5)
    assert h.LifeSign == c.lifesign  # RC mirrors the LifeSign (high nibble)
    assert c.rob.Footer.LifeSign == c.lifesign  # and repeats it in the footer
    assert not any(log.severity >= 28 for log in sdk.logs), sdk.logs


def test_status_word_from_the_sdk(sdk: SdkSimulator) -> None:
    """ST-FIX F6/F7: little endian bit field, operation mode in bits 10..12."""
    c = Client(sdk_transport(sdk, SIZE, SIZE))
    c.initialize()
    status = DwordToRaStatusWord(c.rob.Header.StatusRobotArm)
    assert status.OperationMode == OperationMode(sdk.states.operation_mode) == OperationMode.AUTO_EXT
    assert not status.Enabled and not status.IsMoving


def test_wrong_major_version_is_rejected(sdk: SdkSimulator) -> None:
    c = Client(sdk_transport(sdk, SIZE, SIZE))
    c.host.Telegram.PlcToRob.Header.SRCIVersion = 0x45  # 2.5
    c.cycle(CONTROL_RESET)
    c.cycle(CONTROL_INITIALIZE)
    assert c.rob.Header.TelegramState == TelegramState.ERROR_164_SRCI_MAJOR_VERSION_INCOMPATIBLE


def test_telegram_length_too_small_is_rejected(sdk: SdkSimulator) -> None:
    c = Client(sdk_transport(sdk, SIZE, SIZE))
    c.host.Telegram.PlcToRob.Header.TelegramLengthRobToPlc = 20
    c.cycle(CONTROL_RESET)
    c.cycle(CONTROL_INITIALIZE)
    assert c.rob.Header.TelegramState == TelegramState.ERROR_163_TELEGRAM_LENGTH_MISMATCH


@pytest.mark.parametrize("rob_cartesian", [False, True])
def test_sequence_position_matches_the_sdk(sdk: SdkSimulator, rob_cartesian: bool) -> None:
    """ST-FIX F2 verified: the RC acknowledges the sequence number only at the right position."""
    c = Client(sdk_transport(sdk, SIZE, SIZE), rob_cartesian=rob_cartesian)
    c.initialize()
    for seq in (1, 2, 3):
        c.cycle(seq=seq)
        assert c.rob.Sequence[0].Header.SEQ_ACK == seq
    assert c.ag.State.LastACK[0] == 3


def test_cartesian_position_rc_to_plc(sdk: SdkSimulator) -> None:
    sdk.joints = [100.0, 200.0, 300.0, 10.0, 20.0, 30.0, 5.0] + [0.0] * 5
    c = Client(sdk_transport(sdk, SIZE, SIZE), rob_cartesian=True)
    c.initialize()
    c.cycle()
    pos = c.rob.CyclicOptional.CartesianPosition
    assert (pos.X, pos.Y, pos.Z, pos.Rx, pos.Ry, pos.Rz) == (100.0, 200.0, 300.0, 10.0, 20.0, 30.0)


def test_lifesign_is_mirrored_every_cycle(sdk: SdkSimulator) -> None:
    c = Client(sdk_transport(sdk, SIZE, SIZE))
    c.initialize()
    for _ in range(40):
        c.cycle()
        assert c.rob.Header.LifeSign == c.rob.Footer.LifeSign == c.lifesign
        assert c.rob.Header.TelegramState == TelegramState.INITIALIZED


@pytest.mark.tcp
def test_same_handshake_over_tcp(sdk: SdkSimulator) -> None:
    """SDK behind the PLC gateway simulator: identical results via TcpTransport."""
    with PlcGatewaySimulator(lambda telegram: sdk.exchange(telegram, SIZE), SIZE, SIZE) as gateway:
        transport = TcpTransport("127.0.0.1", gateway.port, SIZE, SIZE, response_timeout=0.5)
        with transport:
            c = Client(transport, rob_cartesian=True)
            c.initialize()
            assert c.rob.Header.TelegramState == TelegramState.INITIALIZED
            for seq in (1, 2):
                c.cycle(seq=seq)
                assert c.rob.Sequence[0].Header.SEQ_ACK == seq
    assert gateway.errors == []

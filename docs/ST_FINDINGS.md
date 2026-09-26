# Findings in the PLC library (ST)

Found while porting. Reference: SRCI profile V1.5.9 (2024-12-04) and the SRCI SDK.
The Python code marks every deviation with `ST-FIX <id>`; tests in `tests/unit` cover them.
Status "fixed in Python" means: still to be fixed in the PLC library.

| ID | Where (ST) | Problem | Spec / SDK | Python |
|---|---|---|---|---|
| F1 | `MC_RobotTaskFB.CreateSendPayloadCyclicOptional` | Cartesian position PLC→RC: `Config` is sent as **1 byte**, but `SIZEOF(...CartesianPosition)` = 34 counts 2 bytes → all following bytes are shifted by one compared to the calculated layout | Table 5-97: Config = bytes 24–25 | fixed: 2 bytes (`config`, `0`) |
| F2 | `MC_RobotTaskFB.CreateSendPayloadCyclic`, `CalculateCyclicDataLength` | `ToolNo`/`FrameNo` are **always** sent after the header | Table 5-88 bit 1 / 5-90 and SDK (`AutoTransmitCartesianPos`): only when "Cartesian Position" RC→PLC is configured; otherwise the RC expects the sequence at byte 18 | fixed: only with `RobToPlc.CartesianPosition.Active` (to be confirmed against the SDK in M5) |
| F3 | `RobotLibrarySendDataBaseFB.AddTurnNumber`, `RobotLibraryRecvDataBaseFB.GetTurnNumbers` | turn numbers encoded as two's complement nibble (`SINT_TO_BYTE`, -1 → `2#1111` = -7 for the RC); decoding ignores the sign bit (`-1` = `2#1001` → 9) | 5.5.4.4, tables 5-24…5-26: sign + magnitude, bits 0..2 value, bit 3 sign (E1: bits 0..6, bit 7) | fixed |
| F4 | `MC_RobotTaskFB.ParseRecvPayload` | "delete old telegram data" compares the ACK of the *previous* telegram with `LastACK[0]` – both are always equal, the branch is dead code | – | kept as in ST (documented) |
| F5 | `MC_RobotTaskFB.ParseRecvPayloadSequence` | `_fragIdx` and `_seqPayloadPtr` are not reset for the second sequence – with two sequences the second one is parsed with a wrong fragment index/length | – | fixed: reset per sequence |
| F6 | `DwordToRaStatusWord` | inserts `CollisionDetectedEnabled` at bit 13 → `CollisionDetected`, `RestartRequested`, `Accelerating`, `Decelerating`, `ConstantVelocity` are read one bit too high | Table 5-105 and SDK: 13 CollisionDetected, 14 RestartRequested, 15 Accelerating, 16 Decelerating, 17 ConstantVelocity | fixed; `CollisionDetectedEnabled` stays FALSE |
| F7 | `RobotLibraryRecvDataBaseFB.GetDword` | no byte swap (all other getters swap; `AddDword` swaps) | SDK sends the status word as little-endian bit field, so reading it without swap is *correct* for `StatusRobotArm`; unclear for `MC_ReadMessages` (`ErrorCode`) | kept as in ST, to be checked in M7 |
| F8 | `MC_RobotTaskFB.CalculateTelegramLengthPlcToRob` | uses `SIZEOF(Footer)` = 2, the footer is 1 byte (`FOOTER_SIZE`) | Tables 5-84/5-85 | kept as in ST (conservative by one byte) |
| F9 | `ByteToAxisJointUnit` | bit 1 and bit 2 both assigned to `J2`, `J1` never set | – | fixed: J1..J6 = bits 1..6 like `ByteToAxisJointUsed` |
| F10 | `PERCENT_INT_TO_REAL` | compares an `INT` with `16#FFFF_FFFF`/`16#0000_FFFF`; depending on the implicit conversion `-1` (16#FFFF) is not recognised as "not supported" | 5.6.2 percentage encoding | intended meaning implemented: all 16 bits set → -1.0 |
| F11 | `TurnNumber` (SINT per axis) | cannot represent "-0" | 5.5.4.4 uses -0 and +0 (e.g. table 5-26) | as in ST (known limitation); raw bytes are available in the telegram |

## Notes on the specification

- 5.6.6.2 states "The actual SRCI version is V1.3" (also in draft 1.5.9) while the SDK uses 1.5.
  Only the major version is checked (SDK `04_Network.cpp`). Python uses 1.5.0 (generator override).
- Tables 5-87 (ClientServer, "bytes required": Cartesian 40, Joint 30) and 5-97/5-99 (34/28 bytes)
  contradict each other. The PLC library and Python follow the detailed tables (34/28). The SDK
  does not decode optional cyclic data PLC→RC yet.

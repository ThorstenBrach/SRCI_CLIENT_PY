These fixes are implemented in hand written Python (telegram coding of `MC_RobotTaskFB`,
send/receive base FBs, conversion functions), so there is no generated diff. The ST code
below is the proposed fix; the referenced Python code is the tested reference.

### F1

`MC_RobotTaskFB.CreateSendPayloadCyclicOptional` – Cartesian position PLC→RC: `Config` is 2 bytes
(spec table 5-97), the ST code sends 1 byte. Reference: `MC_RobotTaskFB_Telegram.CreateSendPayloadCyclicOptional`.

```diff
  _tmpByte   := 0;
  _tmpByte.0 := Telegram.PlcToRob.CyclicOptional.CartesianPosition.Config.0;
  _tmpByte.1 := Telegram.PlcToRob.CyclicOptional.CartesianPosition.Config.1;
  _tmpByte.2 := Telegram.PlcToRob.CyclicOptional.CartesianPosition.Config.2;

  SendData.AddByte(_tmpByte);
+ SendData.AddByte(0); // ST-FIX F1: Config is 2 bytes (spec table 5-97)
```

### F2

`MC_RobotTaskFB.CreateSendPayloadCyclic` and `CalculateCyclicDataLength` – `ToolNo`/`FrameNo`
(table 5-90) are only part of the telegram PLC→RC when "Cartesian Position" is configured in the
direction RC→PLC (table 5-88 bit 1, SDK `AutoTransmitCartesianPos`). Reference:
`MC_RobotTaskFB_Telegram.CreateSendPayloadCyclic`, `.CalculateCyclicDataLength`.

```diff
 // CreateSendPayloadCyclic
-SendData.AddByte(Telegram.PlcToRob.Cyclic.ToolNo);
-SendData.AddByte(Telegram.PlcToRob.Cyclic.FrameNo);
+// ST-FIX F2: only with Cartesian Position RC -> PLC (spec table 5-88 bit 1)
+IF ( AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active )
+THEN
+  SendData.AddByte(Telegram.PlcToRob.Cyclic.ToolNo);
+  SendData.AddByte(Telegram.PlcToRob.Cyclic.FrameNo);
+END_IF
```

```diff
 // CalculateCyclicDataLength, direction PLC_TO_ROB
-  // Add Cyclic size
-  CalculateCyclicDataLength := CalculateCyclicDataLength + SIZEOF(Telegram.PlcToRob.Cyclic);
+  // Add Cyclic size (ST-FIX F2: only with Cartesian Position RC -> PLC)
+  IF ( AxesGroup.CyclicOptional.RobToPlc.CartesianPosition.Active )
+  THEN
+    CalculateCyclicDataLength := CalculateCyclicDataLength + SIZEOF(Telegram.PlcToRob.Cyclic);
+  END_IF
```

### F3

`RobotLibrarySendDataBaseFB.AddTurnNumber`, `RobotLibraryRecvDataBaseFB.GetTurnNumbers` – turn
numbers are sign + magnitude (spec 5.5.4.4, tables 5-24…5-26): J1..J6 bits 0..2 = value, bit 3 =
sign (1 = negative); E1 bits 0..6 = value, bit 7 = sign. The ST code uses two's complement
(`SINT_TO_BYTE`) and ignores the sign when reading. Reference: `turn_to_half_byte`,
`half_byte_to_turn` in `src/srci/fb/_internal/Send|Recv/…BaseFB.py`.

Add two functions (e.g. to `Functions/Convert/Misc`):

```iecst
FUNCTION TURN_TO_SIGN_MAGNITUDE : BYTE // ST-FIX F3
VAR_INPUT
  Turns : SINT;
  Bits  : USINT; // 3 for J1..J6, 7 for E1
END_VAR
VAR
  _mag : BYTE;
END_VAR
_mag := SINT_TO_BYTE(ABS(Turns)) AND (SHL(BYTE#1, Bits) - 1);
IF Turns < 0 THEN
  _mag := _mag OR SHL(BYTE#1, Bits);
END_IF
TURN_TO_SIGN_MAGNITUDE := _mag;
END_FUNCTION

FUNCTION SIGN_MAGNITUDE_TO_TURN : SINT // ST-FIX F3
VAR_INPUT
  Value : BYTE;
  Bits  : USINT;
END_VAR
SIGN_MAGNITUDE_TO_TURN := BYTE_TO_SINT(Value AND (SHL(BYTE#1, Bits) - 1));
IF (Value AND SHL(BYTE#1, Bits)) <> 0 THEN
  SIGN_MAGNITUDE_TO_TURN := -SIGN_MAGNITUDE_TO_TURN;
END_IF
END_FUNCTION
```

```diff
 // AddTurnNumber
-AddHalfBytes( HalfByteHi := SINT_TO_BYTE(Value.J2Turns) , HalfByteLo := SINT_TO_BYTE(Value.J1Turns));
-AddHalfBytes( HalfByteHi := SINT_TO_BYTE(Value.J4Turns) , HalfByteLo := SINT_TO_BYTE(Value.J3Turns));
-AddHalfBytes( HalfByteHi := SINT_TO_BYTE(Value.J6Turns) , HalfByteLo := SINT_TO_BYTE(Value.J5Turns));
-AddByte(SINT_TO_BYTE(Value.E1Turns));
+AddHalfBytes( HalfByteHi := TURN_TO_SIGN_MAGNITUDE(Value.J2Turns, 3), HalfByteLo := TURN_TO_SIGN_MAGNITUDE(Value.J1Turns, 3));
+AddHalfBytes( HalfByteHi := TURN_TO_SIGN_MAGNITUDE(Value.J4Turns, 3), HalfByteLo := TURN_TO_SIGN_MAGNITUDE(Value.J3Turns, 3));
+AddHalfBytes( HalfByteHi := TURN_TO_SIGN_MAGNITUDE(Value.J6Turns, 3), HalfByteLo := TURN_TO_SIGN_MAGNITUDE(Value.J5Turns, 3));
+AddByte(TURN_TO_SIGN_MAGNITUDE(Value.E1Turns, 7));
```

```diff
 // GetTurnNumbers
-GetTurnNumbers.J1Turns := BYTE_TO_SINT(GetHalfeByte1(FALSE));
-GetTurnNumbers.J2Turns := BYTE_TO_SINT(GetHalfeByte2(TRUE));
+GetTurnNumbers.J1Turns := SIGN_MAGNITUDE_TO_TURN(GetHalfeByte1(FALSE), 3);
+GetTurnNumbers.J2Turns := SIGN_MAGNITUDE_TO_TURN(GetHalfeByte2(TRUE), 3);
 // same for J3..J6
-GetTurnNumbers.E1Turns := BYTE_TO_SINT(GetByte());
+GetTurnNumbers.E1Turns := SIGN_MAGNITUDE_TO_TURN(GetByte(), 7);
```

Values out of range (|J| > 7, |E1| > 127) are rejected in Python (`ValueRangeError`); in ST check
them in `CheckParameterValid` of the blocks with turn numbers or clamp them.

### F5

`MC_RobotTaskFB.ParseRecvPayloadSequence` – `_fragIdx` and `_seqPayloadPtr` are not reset for the
second sequence. Reference: `MC_RobotTaskFB_Telegram.ParseRecvPayloadSequence`.

```diff
 FOR _seqIdx := 0 TO _seqCount
 DO
+  // ST-FIX F5: every sequence starts with fragment 0
+  _fragIdx       := 0;
+  _seqPayloadPtr := 0;
   // Check 2nd sequence ? -> goto 2nd sequence payload address
```

### F6

`DwordToRaStatusWord` – bits 13..17 are shifted by one (spec table 5-105 and SDK: 13
CollisionDetected, 14 RestartRequested, 15 Accelerating, 16 Decelerating, 17 ConstantVelocity).
`CollisionDetectedEnabled` is not part of the status word. Reference: `DwordToRaStatusWord` in
`src/srci/functions/Convert/Misc.py`.

```diff
-DwordToRaStatusWord.CollisionDetectedEnabled := Value.13;
-DwordToRaStatusWord.CollisionDetected        := Value.14;
-DwordToRaStatusWord.RestartRequested         := Value.15;
-DwordToRaStatusWord.Accelerating             := Value.16;
-DwordToRaStatusWord.Decelerating             := Value.17;
-DwordToRaStatusWord.ConstantVelocity         := Value.18;
+DwordToRaStatusWord.CollisionDetectedEnabled := FALSE; // ST-FIX F6: not in the status word (table 5-105)
+DwordToRaStatusWord.CollisionDetected        := Value.13;
+DwordToRaStatusWord.RestartRequested         := Value.14;
+DwordToRaStatusWord.Accelerating             := Value.15;
+DwordToRaStatusWord.Decelerating             := Value.16;
+DwordToRaStatusWord.ConstantVelocity         := Value.17; // bit 18 reserved
```

### F9

`ByteToAxisJointUnit` – bit 1 and bit 2 are both assigned to `J2`, `J1` is never set. Bits 1..6 =
J1..J6 like `ByteToAxisJointUsed`. Reference: `ByteToAxisJointUnit` in `Misc.py`.

```diff
-ByteToAxisJointUnit.J2.0 := AxisJointUnit.1;
-ByteToAxisJointUnit.J2.0 := AxisJointUnit.2;
+ByteToAxisJointUnit.J1.0 := AxisJointUnit.1; // ST-FIX F9
+ByteToAxisJointUnit.J2.0 := AxisJointUnit.2;
```

### F10

`PERCENT_INT_TO_REAL` – compares an `INT` with `16#FFFF_FFFF` / `16#0000_FFFF`; the intended
meaning is "all 16 bits set" (INT −1). Reference: `PERCENT_INT_TO_REAL` in `Misc.py`.

```diff
-IF (( Value = 16#FFFF_FFFF ) AND (IsOptional)) OR // 16#FFFF_FFFF for not supported values
-   (( Value = 16#0000_FFFF ) AND (IsOptional))    // 16#0000_FFFF for not supported values
+IF ( INT_TO_WORD(Value) = 16#FFFF ) AND ( IsOptional ) // ST-FIX F10: 16#FFFF for not supported values
 THEN
```

### F22

`RobotLibraryRecvDataBaseFB.GetDataBlock` – copies `Size` bytes even when the payload buffer ends
earlier (`MC_ReadMessagesFB` reads the 255 byte text at offset 20 of a 256 byte buffer) → reads
memory behind the buffer. Missing bytes must be 0. Reference: `GetDataBlock` in
`src/srci/fb/_internal/Recv/RobotLibraryRecvDataBaseFB.py`.

- `RobotLibraryRecvDataBaseFB`: new variable `_payloadSize : UDINT;` set in `UpdatePointer` of the
  derived blocks: `RobotLibraryRecvDataFB`: `_payloadSize := PayLoadSize;`,
  `RobotLibraryResponseDataFB`: `_payloadSize := SIZEOF(Payload);`
- `GetDataBlock`:

```diff
   // copy data
-  SysDepMemCpy(pDest := pData, pSrc := pPayload + DINT_TO_DWORD(PayloadPtr), DataLen := Size);
+  // ST-FIX F22: only the bytes that are in the buffer, the rest is 0
+  SysDepMemSet(pDest := pData, Value := 0, DataLen := Size);
+  IF ( DINT_TO_UDINT(PayloadPtr) < _payloadSize )
+  THEN
+    SysDepMemCpy(pDest := pData, pSrc := pPayload + DINT_TO_DWORD(PayloadPtr),
+                 DataLen := MIN(Size, _payloadSize - DINT_TO_UDINT(PayloadPtr)));
+  END_IF
```

(Use the memory functions the library already wraps; `SysDepMemSet` stands for the set function
of the target, e.g. `MEMSET` in TwinCAT, `SysMemSet` in Codesys.)

### F41

`REAL_TO_PERCENT_INT`, `REAL_TO_PERCENT_UINT` – besides the new defaults −1.0 (section *Data
types*), −1.0 ("<0 %: use the default") must be sent as 16#FFFF **for every parameter**, not only
for optional ones (the ST code sends −100 otherwise). Reference: `Misc.py`.

```diff
 // REAL_TO_PERCENT_INT (same in REAL_TO_PERCENT_UINT)
-IF ( Value = -1.0)  AND (IsOptional)// 16#FFFF for not supported values
+IF ( Value = -1.0 ) // ST-FIX F41: -1.0 = use the default (also for not optional parameters)
 THEN
```

### F47

`MC_ExchangeConfigurationFB`, `MC_ReadMessagesFB`, `MC_ReadRobotDataFB` stay Busy without a running
RobotTask. No own change: fixed by the command timeout of F53 (the blocks end with
`ERR_TIMEOUT_CMD`).

### F52

`MC_RobotTaskFB.ParseRecvPayloadSequence` – besides `FRAGMENT_MAX := 31` (section *Data types*)
the message when the limit is still reached must be an error, because the responses are lost:

```diff
         IF ( _fragIdx > RobotLibraryParameter.FRAGMENT_MAX )
         THEN
           // Create log entry
           CreateLogMessagePara1 ( Timestamp   := SystemTime,
                                   MessageType := MessageType.CMD,
-                                  Severity    := Severity.DEBUG,
+                                  Severity    := Severity.ERROR, // ST-FIX F52: responses are lost
```

### Not to fix

- F4 (dead code), F7 (`GetDword` without byte swap is correct for the status word), F8 (footer
  size, conservative), F11 (`TurnNumber` cannot represent "-0"): documented only.
- F39: parameters without a telegram field in the spec – specification topic, no change.
- Open questions (see ST_FINDINGS / Fixliste): only unsupported data set enabled → `Synchronized`
  TRUE (F24); start-up `SERVER_TO_CLIENT` without after-start-up sync does not write back (F20);
  write error during the start-up sync ends only with the timeout. Not changed in Python either.

These fixes are implemented in hand written Python (telegram coding of `MC_RobotTaskFB`,
send/receive base FBs, conversion functions), so there is no generated diff. The ST code
below is the proposed fix; the referenced Python code is the tested reference.

All fixes that the Python port implements in hand written code (F1, F2, F3, F5, F6, F9, F10, F22,
F41, F47, F52, F60, F63, F96) are in the PLC library since the export of 2026-10-17 (their
descriptions are in the git history of this file).

### Not to fix

- F4 (dead code), F7 (`GetDword` without byte swap is correct for the status word), F8 (footer
  size, conservative), F11 (`TurnNumber` cannot represent "-0"): documented only.
- F39: parameters without a telegram field in the spec – specification topic, no change.
- Open questions (see ST_FINDINGS / Fixliste): only unsupported data set enabled → `Synchronized`
  TRUE (F24); start-up `SERVER_TO_CLIENT` without after-start-up sync does not write back (F20);
  write error during the start-up sync ends only with the timeout. Not changed in Python either.

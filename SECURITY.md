# Security policy

## Reporting a vulnerability

Please report security problems privately through
[GitHub private vulnerability reporting](https://github.com/ThorstenBrach/SRCI_CLIENT_PY/security/advisories/new),
not as a public issue or discussion.

This includes any behaviour that can make a robot move unexpectedly, for example a command that is
sent although it should have been rejected, or a stop that is not passed on.

Please include the affected version, the robot controller and firmware, and the steps that
reproduce the problem. We confirm the report, keep you informed in the advisory and publish
the advisory together with the fixed release.

## Supported versions

Security fixes go into the newest release only.

## Scope

srci-client (SRCI_CLIENT_PY) sends commands to a robot controller. It is not a safety function: personal safety
must always be ensured by the safety functions of the robot controller and of the safety PLC
(emergency stop, enabling device, safe speed monitoring), as required by ISO 10218.

# Contributing

Thank you for your interest in the SRCI Python client.

## How this repository is maintained

Almost all of the code in `src/srci` (function blocks, data types, functions) is **generated** from
the open SRCI PLC library ([SRCI_CLIENT_PLC](https://github.com/ThorstenBrach/SRCI_CLIENT_PLC)), so
that the Python client and the PLC library stay identical: same function blocks, same inputs and
outputs, same error IDs. The generator and the tests (against the specification and a simulated
robot controller) live in a separate development repository; this repository receives the result
of every release.

This means a change made directly in `src/srci` would be overwritten by the next release. Changes
are therefore always made in the PLC library or the generator first and come back here with the
next release.

## Reporting bugs and ideas

Please open an [issue](https://github.com/ThorstenBrach/SRCI_CLIENT_PY/issues) with

- the version (`python -c "import srci; print(srci.__version__)"`),
- the robot controller (manufacturer, firmware, SRCI version and profile) and the transport
  (TCP gateway, OPC UA),
- what you did, what you expected and what happened - ideally with the log
  (`client.program.system_log`, logger `srci.plc`) or the telegram trace (logger `srci.telegram`).

## Pull requests

Pull requests are welcome - also for the examples and the documentation. They are not merged
directly: the change is carried over into the development repository (with tests and, for the
function blocks, into the PLC library as well) and published with the next release. The pull request
is then closed with a reference to that release, and you are named as co-author of the change.

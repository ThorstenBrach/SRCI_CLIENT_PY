# Support

This page explains where to get help with srci-client (SRCI_CLIENT_PY), the SRCI client for the
Standard Robot Command Interface.

## Where to ask

| You want to ... | Use |
|---|---|
| ask a question about setup, use or a specific robot controller | [GitHub Discussions](https://github.com/ThorstenBrach/SRCI_CLIENT_PY/discussions) |
| report a bug or a deviation from the SRCI specification | [an issue](https://github.com/ThorstenBrach/SRCI_CLIENT_PY/issues/new/choose), using the bug report form |
| report how the client works with your robot controller | [an issue](https://github.com/ThorstenBrach/SRCI_CLIENT_PY/issues/new/choose), using the robot controller report form |
| read the documentation | the [SRCI wiki](https://github.com/ThorstenBrach/SRCI/wiki) |
| report a security problem | [a private security advisory](https://github.com/ThorstenBrach/SRCI_CLIENT_PY/security/advisories/new), not a public issue (see [SECURITY.md](SECURITY.md)) |

Support for users runs only through GitHub. Please do not send support requests by e-mail.

## What to include

- package version (`pip show srci-client`), Python version and operating system
- robot controller, manufacturer and firmware version
- the function block involved, ErrorID or WarningID
- an excerpt of the message log
- the steps that reproduce the problem

Please remove anything confidential before you post, such as IP addresses of production systems
or customer names.

## What happens next

1. We check whether the cause is in the client, in the robot controller, in the SRCI
   specification or in the application.
2. A bug in the client is reproduced in the automated tests, fixed and released.
   Until then we point out a workaround when there is one.
3. If the cause is in the robot controller, we pass the case on to the SRCI experts of
   that robot manufacturer and tell you in the issue who is working on it.
4. A question about the specification goes to the SRCI working group of PROFIBUS & PROFINET
   International (PI).

## Supported versions

Fixes go into the newest release. Please check the
[releases](https://github.com/ThorstenBrach/SRCI_CLIENT_PY/releases) and update before you report a problem.

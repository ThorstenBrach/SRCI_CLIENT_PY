# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added
 - Python client of the SRCI interface (specification V1.5.9): all function blocks, data types and
   functions of the SRCI PLC library, generated from the PLC library and kept identical to it
 - `srci.api.RobotProgram` (RobotTask + user data + function blocks) and `srci.api.SrciClient`
   (sequential scripts; the program runs cyclically in a background thread like a PLC task,
   `background=False` for deterministic tests), `srci.runtime.Runner` (fixed cycle in a thread)
 - Transports: TCP/IP to a PLC gateway (lockstep, reconnect), loopback, fault injection
 - Example `examples/core_profile`: every function of the Core profile
 - Two telegram sequences, RI error handling (lifesign, sequence timeout, invalid frames)
 - Tests on Linux and Windows, Python 3.12 – 3.14, including a simulated robot controller;
   test case catalog and test report

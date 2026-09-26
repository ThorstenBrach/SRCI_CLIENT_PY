# Robot Library Py

A Python implementation of the IEC 61131 Robot Library.

## Overview

This project converts the original IEC 61131 Structured Text robot library to Python, maintaining modularity and state-of-the-art practices.

## Installation

### Using pip (from source)
```bash
pip install -e .
```

### Development Setup
```bash
pip install -e ".[dev]"
```

## Project Structure

- `src/robot_library_py/`: Main package
  - `constants/`: Global constants
  - `structures/`: Data structures
  - `enumerations/`: Enums
  - `functions/`: Utility functions
  - `pous/`: Programmable Organization Units (Function Blocks)
- `tests/`: Unit tests
- `docs/`: Documentation

## Usage

```python
from robot_library_py import ...
```

## Development

- Format code: `black src tests`
- Lint: `flake8 src tests`
- Type check: `mypy src`
- Run tests: `pytest`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests
4. Ensure all checks pass
5. Submit a pull request

## License

LGPL-3.0
# Lanelet2 Python API for Autoware

A standalone Python API for Lanelet2 and Autoware Lanelet2 Extension, managed with UV for easy installation and dependency management.

## Features

- 🚀 **Easy Installation**: Use UV for streamlined dependency management
- 📦 **Standalone Package**: No ROS dependencies required
- 🔧 **Automated Build**: Single command builds all C++ libraries
- 🐍 **Pure Python API**: Import and use like any Python package
- 📊 **NumPy Integration**: Uses numpy.array instead of geometry messages

## System Requirements

- **OS**: Ubuntu 20.04/22.04 or compatible Linux distribution
- **Python**: 3.9+
- **UV**: Latest version recommended
- **System Dependencies**:
  - git, gcc, cmake
  - libboost-dev, libeigen3-dev, libpugixml-dev, libgeographic-dev
  - libboost-python-dev, libboost-serialization-dev, librange-v3-dev
  - libboost-filesystem-dev, libboost-program-options-dev

## Quick Start

### 1. Install System Dependencies
```bash
# Ubuntu/Debian
sudo apt install git gcc cmake python3 python3-pip \
  libboost-dev libeigen3-dev libpugixml-dev libgeographic-dev \
  libboost-python-dev libboost-serialization-dev librange-v3-dev \
  libboost-filesystem-dev libboost-program-options-dev

# Or use the provided script (requires sudo)
bash pre-install.sh
```

### 2. Install with UV

#### Option A: One-Command Install (Recommended)
```bash
# Install UV if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# One command to install and build everything
uv run lanelet2-install
```

#### Option B: Step-by-Step Install
```bash
# Install the package in development mode (auto-builds libraries)
uv pip install -e .

# Or manually build libraries if needed
uv run lanelet2-build
```

### 3. Use the Library
```python
import lanelet2
from lanelet2 import core, io, projection, routing, traffic_rules

# Your Lanelet2 code here...
print("Lanelet2 modules available:", dir(lanelet2))
```

## Alternative Setup (Legacy)

If you prefer the original setup method:

```bash
# Install system dependencies
bash pre-install.sh 

# Build libraries manually
bash build.sh

# Set environment variables
source setup.bash
```

## Available Modules

- **lanelet2.core**: Core Lanelet2 primitives and data structures
- **lanelet2.io**: Reading and writing Lanelet2 maps
- **lanelet2.projection**: Coordinate system projections
- **lanelet2.routing**: Routing and path planning
- **lanelet2.traffic_rules**: Traffic rule definitions
- **lanelet2.matching**: Map matching utilities

## Development

```bash
# Install development dependencies
uv sync --dev

# Run tests
uv run pytest

# Build documentation
uv run python -m docs
```

## Project Structure

```
├── lanelet2_python_api/          # Python package
│   ├── __init__.py              # Package initialization
│   └── build.py                 # Build script
├── Rosless-Lanelet2/            # Core Lanelet2 libraries
├── autoware_lanelet2_extension/ # Autoware-specific extensions
├── pyproject.toml               # UV configuration
└── install/                     # Built libraries (created by build)
```

## API Changes from Original

- ✅ Use `numpy.array` instead of geometry pose messages
- ✅ Improved Python function documentation
- ✅ Simplified import structure
- ✅ No ROS dependencies required

## Acknowledgments

Thanks to [Rosless-Lanelet2](https://github.com/embedded-software-laboratory/Rosless-Lanelet2) for their developments that made this standalone version possible.

## License

This project follows the same license terms as the original Lanelet2 project. 
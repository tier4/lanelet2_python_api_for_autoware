# Lanelet2 Python API for Autoware

A standalone Python API for Lanelet2 and Autoware Lanelet2 Extension, managed with UV for easy installation and dependency management.

## Features

- ⚡ **One-Command Setup**: `uv run lanelet2-install` does everything automatically
- 🚀 **Easy Installation**: UV-powered dependency management with auto-build
- 📦 **Standalone Package**: No ROS dependencies required
- 🔧 **Smart Building**: Automatic C++ library building on install
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

## ⚡ Ultra-Quick Start (30 seconds)

```bash
# 1. Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install system dependencies (Ubuntu/Debian)
sudo apt install git gcc cmake python3 python3-pip \
  libboost-dev libeigen3-dev libpugixml-dev libgeographic-dev \
  libboost-python-dev libboost-serialization-dev librange-v3-dev \
  libboost-filesystem-dev libboost-program-options-dev

# 3. One command to rule them all! 🎯
uv run lanelet2-install
```

That's it! The system will:
- ✅ Install the Python package
- ✅ Build all C++ libraries automatically  
- ✅ Configure import paths
- ✅ Verify everything works
- ✅ Show you how to use it

### Alternative Installation Methods

#### Option A: Auto-Build on Install
```bash
# Package installs AND builds automatically
uv pip install -e .
```

#### Option B: Manual Build Control
```bash
# Install first, build later
uv pip install -e . --no-build-isolation
uv run lanelet2-build
```

#### Option C: Legacy Method (Still Works!)
```bash
bash pre-install.sh    # System dependencies
bash build.sh          # Build libraries
source setup.bash      # Set environment
```

## Usage

```python
import lanelet2
from lanelet2 import core, io, projection, routing, traffic_rules

# All modules ready to use!
print("Available modules:", dir(lanelet2))
```


## Available Modules

### Core Lanelet2 Modules
- **lanelet2.core**: Core Lanelet2 primitives and data structures
- **lanelet2.io**: Reading and writing Lanelet2 maps
- **lanelet2.projection**: Coordinate system projections
- **lanelet2.routing**: Routing and path planning
- **lanelet2.traffic_rules**: Traffic rule definitions
- **lanelet2.matching**: Map matching utilities

### Autoware Extension Modules
- **autoware_lanelet2_extension_python.projection**: MGRS and Transverse Mercator projectors
- **autoware_lanelet2_extension_python.regulatory_elements**: Autoware-specific traffic elements
- **autoware_lanelet2_extension_python.utility**: Query and utility functions for Autoware

### Usage Examples
```python
# Core Lanelet2
from lanelet2 import core, io, routing
map = io.load("map.osm")

# Autoware Extensions  
from autoware_lanelet2_extension_python.projection import MGRSProjector
from autoware_lanelet2_extension_python.regulatory_elements import AutowareTrafficLight
from autoware_lanelet2_extension_python.utility import query

projector = MGRSProjector()
traffic_lights = query.autowareTrafficLights(map)
```

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
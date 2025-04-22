# Standable Autoware Lanelet2 Extension

This repository provides a standalone implementation of the Lanelet2 library and Autoware's Lanelet2 extension, allowing for map processing and route planning without ROS dependencies.

## Setup

This repository will build and install the Lanelet2 library and the autoware_lanelet2_extension (first in the local directory).

```bash
# Install common packages (required for bare Ubuntu container)
sudo apt install git gcc cmake python3 python3-pip

# Install additional necessary packages
bash pre-install.sh 

# Build the repositories (creates an 'install' folder locally)
bash build.sh

# Add environmental variables to the current terminal
source setup.bash
```

After installation, `lanelet2` and `autoware_lanelet2_extension_python` can be used as standard Python packages anywhere in your environment.

> Note: This installation has been tested and verified on Ubuntu 22.04 containers.

## Tutorials

This repository includes three Jupyter notebooks that serve as tutorials:

### [Basic Operation](./basic_lanelet2_extraction.ipynb)
- Setting up environments
- Loading maps
- Getting local map
- Visualizing lanelets
- Computing routes and connecting lanelets

### [Regulation Elements](./RegulationElements.ipynb)
- Extracting traffic light information
- Extracting road types and polygons

### [JSON Schema](./interaction_with_cache_json.ipynb)
- Indexing into keyframes
- Visualizing current keyframe
  - Visualizing routes
  - Visualizing history and future
  - Visualizing traffic lights
- Visualizing in local coordinate system

## API Changes

- Replaced geometry pose messages with NumPy arrays
- Improved Python function documentation

## Acknowledgments

Thanks to [Rosless-Lanelet2](https://github.com/embedded-software-laboratory/Rosless-Lanelet2) for their development work that contributed to this project.
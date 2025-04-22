#!/bin/bash

# Get the current directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Python path setup
export PYTHONPATH=$INSTALL_DIR/install/lib/python3/dist-packages:$INSTALL_DIR/install/lib/python3/dist-packages:$PYTHONPATH

# C++ library path setup
export LD_LIBRARY_PATH=$INSTALL_DIR/install/lib:$LD_LIBRARY_PATH
export CPATH=$INSTALL_DIR/install/include:$CPATH

# Add binary path to PATH
export PATH=$INSTALL_DIR/install/lib:$PATH

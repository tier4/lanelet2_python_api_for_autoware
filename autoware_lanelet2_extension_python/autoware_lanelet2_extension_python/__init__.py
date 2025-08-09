import os
import sys
import ctypes
from pathlib import Path

# Pre-load required shared libraries before importing any C++ modules
_package_dir = Path(__file__).parent

# List of required libraries in dependency order
_required_libs = [
    "liblanelet2_core.so.1.1.1",
    "liblanelet2_io.so", 
    "liblanelet2_projection.so",
    "liblanelet2_routing.so",
    "liblanelet2_traffic_rules.so",
    "liblanelet2_validation.so", 
    "liblanelet2_matching.so",
    "liblanelet2_extension_lib.so"
]

# Pre-load libraries using ctypes.CDLL
for lib_name in _required_libs:
    lib_path = _package_dir / lib_name
    if lib_path.exists():
        try:
            ctypes.CDLL(str(lib_path), ctypes.RTLD_GLOBAL)
        except OSError:
            pass  # Skip if library can't be loaded

import lanelet2

# Import submodules to make them available
from . import projection
from . import regulatory_elements
from . import utility
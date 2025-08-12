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
    # Try multiple locations
    lib_paths = [
        _package_dir / lib_name,  # Direct in package dir
        _package_dir / "lib" / lib_name,  # In lib subdir
        _package_dir / "autoware_lanelet2_extension_python" / lib_name,  # In nested package dir
        _package_dir / "autoware_lanelet2_extension_python" / "lib" / lib_name  # In nested lib dir
    ]
    
    loaded = False
    for lib_path in lib_paths:
        if lib_path.exists():
            try:
                ctypes.CDLL(str(lib_path), ctypes.RTLD_GLOBAL)
                # print(f"Successfully loaded {lib_path}")
                loaded = True
                break
            except OSError as e:
                # print(f"Failed to load {lib_path}: {e}")
                pass
    
    if not loaded:
        # Print warning instead of failing
        import warnings
        warnings.warn(f"Could not load {lib_name}, some functionality may not work", ImportWarning)

import lanelet2

# Import submodules to make them available
from . import projection
from . import regulatory_elements
from . import utility
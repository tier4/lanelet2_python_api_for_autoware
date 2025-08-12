"""
Python API for lanelet2_extension for Autoware
"""

import os
import sys
import ctypes
from pathlib import Path

def _check_compiled_extensions():
    """Check if compiled extensions are available."""
    current_dir = Path(__file__).parent
    required_extensions = [
        "_lanelet2_extension_python_boost_python_projection.so",
        "_lanelet2_extension_python_boost_python_regulatory_elements.so", 
        "_lanelet2_extension_python_boost_python_utility.so"
    ]
    
    missing_extensions = []
    for ext in required_extensions:
        if not (current_dir / ext).exists():
            missing_extensions.append(ext)
    
    if missing_extensions:
        error_msg = f"""
Missing compiled extensions: {missing_extensions}

This package requires prebuilt Lanelet2 libraries and compiled C++ extensions.

For development, please:
1. Use 'poetry install' in the development environment, OR
2. Build the package using 'poetry build' and install the resulting wheel

For pip install from git, the package must be built with all dependencies.
Current directory: {current_dir}
Available files: {list(current_dir.glob('*'))}
"""
        raise ImportError(error_msg)

# Check for compiled extensions first
_check_compiled_extensions()

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

# Try to import lanelet2 if available (for development environments)
try:
    import lanelet2
except ImportError:
    # lanelet2 not available, continue without it
    pass

# Import submodules to make them available
try:
    from . import projection
    from . import regulatory_elements
    from . import utility
except ImportError as e:
    # Expected when .so files are not available
    import warnings
    warnings.warn(
        f"Failed to import C++ extensions: {e}. "
        "This package is a stub version. For full functionality, "
        "use 'poetry install' in development or install prebuilt wheels.",
        UserWarning
    )
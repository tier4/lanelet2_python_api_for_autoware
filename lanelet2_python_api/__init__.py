"""
Lanelet2 Python API for Autoware
Standalone Python bindings for Lanelet2 and Autoware Lanelet2 Extension
"""

import sys
import os

# Add the install directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
install_lib_path = os.path.join(current_dir, 'install', 'lib', 'python3', 'dist-packages')

if os.path.exists(install_lib_path) and install_lib_path not in sys.path:
    sys.path.insert(0, install_lib_path)

try:
    # Import lanelet2 core modules
    import lanelet2
    from lanelet2 import core, io, matching, projection, routing, traffic_rules
    
    # Import autoware extension modules
    import autoware_lanelet2_extension_python
    from autoware_lanelet2_extension_python import projection as autoware_projection
    from autoware_lanelet2_extension_python import regulatory_elements as autoware_regulatory
    from autoware_lanelet2_extension_python import utility as autoware_utility
    
    __all__ = [
        'core', 'io', 'matching', 'projection', 'routing', 'traffic_rules',
        'autoware_projection', 'autoware_regulatory', 'autoware_utility'
    ]
    
except ImportError as e:
    print(f"Warning: Could not import lanelet2 modules. Make sure to build the project first: {e}")
    __all__ = []

__version__ = "0.1.0"
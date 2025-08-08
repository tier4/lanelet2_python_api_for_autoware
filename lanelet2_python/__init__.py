"""
Python bindings for Lanelet2 with Autoware extension
"""

try:
    from ._lanelet2_python_api import *
except ImportError as e:
    print(f"Failed to import C++ extension: {e}")
    print("Make sure the C++ extension is built correctly.")

__version__ = "0.1.0"
# Import shared libraries first to set up library paths
import os
import sys
from pathlib import Path

# Add library path for shared objects
module_dir = Path(__file__).parent
lib_dir = module_dir.parent / "lanelet2" / "lib"

if lib_dir.exists():
    # Add to LD_LIBRARY_PATH for Linux
    if "LD_LIBRARY_PATH" in os.environ:
        os.environ["LD_LIBRARY_PATH"] = f"{lib_dir}:{os.environ['LD_LIBRARY_PATH']}"
    else:
        os.environ["LD_LIBRARY_PATH"] = str(lib_dir)
    
    # For immediate effect, use ctypes to add library path
    try:
        import ctypes
        import ctypes.util
        # This only works on Linux
        if sys.platform.startswith("linux"):
            # Load libraries in dependency order
            for lib_name in ["liblanelet2_core.so.1.1.1", "liblanelet2_io.so", 
                            "liblanelet2_traffic_rules.so", "liblanelet2_routing.so",
                            "liblanelet2_projection.so", "liblanelet2_extension_lib.so"]:
                lib_path = lib_dir / lib_name
                if lib_path.exists():
                    ctypes.CDLL(str(lib_path), ctypes.RTLD_GLOBAL)
    except Exception as e:
        print(f"Warning: Could not preload libraries: {e}", file=sys.stderr)

import lanelet2
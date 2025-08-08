#!/usr/bin/env python3
"""
Comprehensive library loader for Lanelet2 Python API
Handles shared library loading for both development and production environments
"""

import os
import sys
import ctypes
import site
from pathlib import Path
from typing import List, Optional


def find_library_paths() -> List[Path]:
    """Find all possible locations where Lanelet2 libraries might be installed"""
    search_paths = []
    
    # 1. Virtual environment lib directory
    if hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
        venv_root = Path(sys.prefix)
        search_paths.append(venv_root / "lib")
    
    # 2. Site-packages lib directory (for pip installed packages)
    try:
        for site_pkg in site.getsitepackages():
            site_lib = Path(site_pkg) / "lib"
            if site_lib.exists():
                search_paths.append(site_lib)
    except AttributeError:
        # site.getsitepackages() might not exist in some environments
        pass
    
    # 3. User site-packages (pip install --user)
    try:
        user_site = Path(site.getusersitepackages()) / "lib"
        if user_site.exists():
            search_paths.append(user_site)
    except AttributeError:
        pass
    
    # 4. Package installation directories
    try:
        import lanelet2_python_api
        pkg_path = Path(lanelet2_python_api.__file__).parent
        search_paths.extend([
            pkg_path / "install" / "lib",
            pkg_path.parent / "install" / "lib",
            pkg_path / "lib",
            pkg_path.parent / "lib"
        ])
    except ImportError:
        pass
    
    # 5. System-wide installation paths
    system_paths = [
        Path("/usr/local/lib"),
        Path("/usr/lib"),
        Path("/opt/ros/humble/lib/x86_64-linux-gnu"),
    ]
    search_paths.extend(system_paths)
    
    # 6. Current working directory install/lib (development mode)
    search_paths.append(Path.cwd() / "install" / "lib")
    
    # 7. Environment variable paths
    ld_library_path = os.environ.get('LD_LIBRARY_PATH', '')
    if ld_library_path:
        for path_str in ld_library_path.split(':'):
            if path_str.strip():
                search_paths.append(Path(path_str.strip()))
    
    # Remove duplicates and return only existing paths
    unique_paths = []
    seen = set()
    for path in search_paths:
        path = path.resolve()
        if path not in seen and path.exists():
            unique_paths.append(path)
            seen.add(path)
    
    return unique_paths


def get_required_libraries() -> List[str]:
    """Get list of required Lanelet2 libraries in dependency order"""
    return [
        "liblanelet2_core.so.1.1.1",
        "liblanelet2_core.so",
        "liblanelet2_io.so",
        "liblanelet2_projection.so", 
        "liblanelet2_traffic_rules.so",
        "liblanelet2_routing.so",
        "liblanelet2_matching.so",
        "liblanelet2_validation.so",
        "liblanelet2_extension_lib.so"
    ]


def preload_libraries(verbose: bool = False) -> tuple[int, int]:
    """
    Preload required libraries using ctypes
    
    Returns:
        (loaded_count, total_count) tuple
    """
    lib_names = get_required_libraries()
    search_paths = find_library_paths()
    
    if verbose:
        print(f"Looking for {len(lib_names)} libraries in {len(search_paths)} locations")
        for i, path in enumerate(search_paths[:5]):  # Show first 5 paths
            print(f"  {i+1}. {path}")
        if len(search_paths) > 5:
            print(f"  ... and {len(search_paths) - 5} more paths")
    
    loaded_libs = set()
    
    # Try to preload each library from found locations
    for search_path in search_paths:
        if not search_path.exists():
            continue
            
        for lib_name in lib_names:
            if lib_name in loaded_libs:
                continue
                
            lib_path = search_path / lib_name
            if lib_path.exists():
                try:
                    ctypes.CDLL(str(lib_path), mode=ctypes.RTLD_GLOBAL)
                    loaded_libs.add(lib_name)
                    if verbose:
                        print(f"✅ Loaded: {lib_name} from {search_path}")
                except OSError as e:
                    if verbose:
                        print(f"⚠️ Failed to load {lib_name}: {e}")
                    continue
        
        # Update LD_LIBRARY_PATH for this location if it has our libraries
        if search_path.exists() and any((search_path / lib).exists() for lib in lib_names):
            current_path = os.environ.get('LD_LIBRARY_PATH', '')
            search_path_str = str(search_path)
            
            if search_path_str not in current_path:
                if current_path:
                    os.environ['LD_LIBRARY_PATH'] = f"{search_path_str}:{current_path}"
                else:
                    os.environ['LD_LIBRARY_PATH'] = search_path_str
    
    return len(loaded_libs), len(lib_names)


def setup_library_environment(verbose: bool = False) -> bool:
    """
    Setup library environment for Lanelet2
    
    Returns:
        True if setup was successful, False otherwise
    """
    if verbose:
        print("🔧 Setting up Lanelet2 library environment...")
    
    try:
        loaded_count, total_count = preload_libraries(verbose=verbose)
        
        if verbose:
            print(f"📚 Loaded {loaded_count}/{total_count} libraries")
            if loaded_count < total_count:
                print("⚠️ Some libraries could not be loaded - imports might fail")
        
        return loaded_count > 0
        
    except Exception as e:
        if verbose:
            print(f"❌ Failed to setup library environment: {e}")
        return False


if __name__ == "__main__":
    # Test the library loader
    success = setup_library_environment(verbose=True)
    print(f"Library setup {'successful' if success else 'failed'}")
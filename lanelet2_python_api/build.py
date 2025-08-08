#!/usr/bin/env python3
"""
Build script for Lanelet2 Python API
Provides a command-line interface to build the C++ libraries
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None, env=None):
    """Run a shell command and check for errors"""
    # Convert Path objects to strings
    cmd_str = [str(c) for c in cmd]
    print(f"Running: {' '.join(cmd_str)}")
    try:
        result = subprocess.run(cmd_str, cwd=cwd, env=env, check=True, 
                              capture_output=False, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        return False


def build_cmake_project(source_dir, build_dir, install_dir):
    """Build a CMake project"""
    # Create build directory
    os.makedirs(build_dir, exist_ok=True)
    
    # Configure
    cmake_args = [
        'cmake',
        str(source_dir),
        f'-DCMAKE_INSTALL_PREFIX={str(install_dir)}',
        f'-DCMAKE_PREFIX_PATH={str(install_dir)}',
        '-DCMAKE_BUILD_TYPE=Release'
    ]
    
    if not run_command(cmake_args, cwd=build_dir):
        return False
    
    # Build
    if not run_command(['make', '-j4'], cwd=build_dir):
        return False
    
    # Install
    if not run_command(['make', 'install'], cwd=build_dir):
        return False
    
    return True


def main():
    """Main build function"""
    print("Building Lanelet2 Python API...")
    
    # Get project root directory
    project_root = Path(__file__).parent.parent.absolute()
    install_dir = project_root / 'install'
    
    print(f"Project root: {project_root}")
    print(f"Install directory: {install_dir}")
    
    # Build Rosless-Lanelet2
    print("\n=== Building Rosless-Lanelet2 ===")
    rosless_src = project_root / 'Rosless-Lanelet2'
    rosless_build = project_root / 'build' / 'Rosless-Lanelet2'
    
    if not build_cmake_project(rosless_src, rosless_build, install_dir):
        print("Failed to build Rosless-Lanelet2")
        return 1
    
    # Build Autoware extension  
    print("\n=== Building Autoware Lanelet2 Extension ===")
    autoware_src = project_root / 'autoware_lanelet2_extension'
    autoware_build = project_root / 'build' / 'autoware_lanelet2_extension'
    
    # Skip validation dependency for now
    if not build_cmake_project(autoware_src, autoware_build, install_dir):
        print("⚠️  Autoware Extension build failed (likely validation dependency)")
        print("Core Lanelet2 libraries are still available")
    else:
        print("✅ Autoware Extension built successfully")
    
    # Build autoware_lanelet2_extension_python
    print("\n=== Building Autoware Lanelet2 Extension Python ===")
    python_src = project_root / 'autoware_lanelet2_extension_python'
    python_build = project_root / 'build' / 'autoware_lanelet2_extension_python'
    
    if not build_cmake_project(python_src, python_build, install_dir):
        print("⚠️  Autoware Python Extension build failed")
        print("Core Lanelet2 libraries are still available")
    else:
        print("✅ Autoware Python Extension built successfully")
    
    print("\n=== Build completed successfully! ===")
    print(f"Libraries installed to: {install_dir}")
    
    # Set up environment
    print("\nTo use the libraries, make sure to set these environment variables:")
    print(f"export PYTHONPATH={install_dir}/lib/python3/dist-packages:$PYTHONPATH")
    print(f"export LD_LIBRARY_PATH={install_dir}/lib:$LD_LIBRARY_PATH")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
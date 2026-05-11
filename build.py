#!/usr/bin/env python3
"""
Build script for Poetry to compile C++ extensions before packaging.
This is called by Poetry during the build process.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a shell command and check for errors."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return result.stdout


def build():
    """Build all C++ extensions using CMake."""
    root_dir = Path(__file__).parent.absolute()
    
    # Use a different build directory to avoid conflicts
    for project in ["Rosless-Lanelet2", "autoware_lanelet2_extension", "autoware_lanelet2_extension_python"]:
        project_path = root_dir / project
        if project_path.exists():
            project_build = root_dir / "build_poetry" / project
            project_build.mkdir(parents=True, exist_ok=True)
            
            print(f"Building {project}...")
            run_command([
                "cmake",
                str(project_path),
                f"-DCMAKE_INSTALL_PREFIX={root_dir / 'install'}",
                "-DCMAKE_BUILD_TYPE=Release"
            ], cwd=project_build)
            
            run_command(["make", "-j"], cwd=project_build)
            run_command(["make", "install"], cwd=project_build)
    
    print("C++ extensions built successfully!")
    
    # Copy extensions to source directory for Poetry
    copy_extensions()


def copy_extensions():
    """Copy built C++ extensions to source directory."""
    root_dir = Path(__file__).parent.absolute()
    install_dir = root_dir / "install"
    src_dir = root_dir / "autoware_lanelet2_extension_python" / "autoware_lanelet2_extension_python"
    
    # Copy autoware extension .so files
    autoware_install = install_dir / "lib" / "python3" / "dist-packages" / "autoware_lanelet2_extension_python"
    if autoware_install.exists():
        for so_file in autoware_install.glob("*.so"):
            dst = src_dir / so_file.name
            print(f"Copying {so_file} -> {dst}")
            import shutil
            shutil.copy2(so_file, dst)
    
    # Copy lanelet2 module
    lanelet2_install = install_dir / "lib" / "python3" / "dist-packages" / "lanelet2"
    lanelet2_dst = root_dir / "lanelet2"
    if lanelet2_install.exists():
        import shutil
        if lanelet2_dst.exists():
            shutil.rmtree(lanelet2_dst)
        print(f"Copying {lanelet2_install} -> {lanelet2_dst}")
        shutil.copytree(lanelet2_install, lanelet2_dst)
        
        # Copy shared libraries
        lib_src = install_dir / "lib"
        lib_dst = lanelet2_dst / "lib"
        lib_dst.mkdir(exist_ok=True)
        for so_file in lib_src.glob("*.so*"):
            if so_file.is_file():
                print(f"Copying {so_file} -> {lib_dst / so_file.name}")
                shutil.copy2(so_file, lib_dst)


if __name__ == "__main__":
    build()
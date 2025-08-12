import shutil
from distutils import log as distutils_log
from pathlib import Path
from typing import Any, Dict

import skbuild
import skbuild.constants
import subprocess
import sysconfig
import os

__all__ = ("build",)


def get_poetry_venv_path() -> Path:
    """Get the path to the Poetry virtual environment."""
    try:
        result = subprocess.run(
            ["poetry", "env", "info", "--path"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        venv_path = result.stdout.strip()
        return Path(venv_path)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Failed to get Poetry virtual environment: {e.stderr}"
        ) from e


def remove_files(target_dir: Path, pattern: str) -> None:
    """Delete files matched with a glob pattern in a directory tree."""
    for path in target_dir.glob(pattern):
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        distutils_log.info(f"removed {path}")


def copy_files(src_dir: Path, dest_dir: Path, pattern: str) -> None:
    """Copy files matched with a glob pattern in a directory tree to another."""
    for src in src_dir.glob(pattern):
        dest = dest_dir / src.relative_to(src_dir)
        if src.is_dir():
            # NOTE: inefficient if subdirectories also match to the pattern.
            copy_files(src, dest, "*")
        else:
            try:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
                distutils_log.info(f"copied {src} to {dest}")
            except (FileNotFoundError, PermissionError) as e:
                distutils_log.warn(f"failed to copy {src} to {dest}: {e}")


def build(setup_kwargs: Dict[str, Any]) -> None:
    venv_path = get_poetry_venv_path()
    """Build C-extensions."""
    pybind11_path = (
        venv_path
        / "lib"
        / f"python{sysconfig.get_python_version()}"
        / "site-packages"
        / "pybind11"
        / "share"
        / "cmake"
        / "pybind11"
    )
    skbuild.setup(
        **setup_kwargs,
        script_args=["build_ext"],
        cmake_args=["-Dpybind11_DIR=" + str(pybind11_path)],
    )

    src_dir = Path(skbuild.constants.CMAKE_INSTALL_DIR())

    # Get the installation directory for the Poetry virtual environment
    dest_dir = (
        venv_path / "lib" / f"python{sysconfig.get_python_version()}" / "site-packages"
    )

    print(f"Copy from {src_dir} to {dest_dir}")
    print(f"Source directory exists: {src_dir.exists()}")
    if src_dir.exists():
        for file in src_dir.glob("**/*.so"):
            print(f"Found .so file: {file}")

    # Delete C-extensions copied in previous runs, just in case.
    remove_files(dest_dir, "**/_lanelet2_extension_python_boost_python_*.so")
    remove_files(dest_dir, "**/_lanelet2_python_api.*.so")

    # Copy built C-extensions back to the Poetry virtual environment.
    if src_dir.exists():
        copy_files(src_dir, dest_dir, "**/*.pyd")
        copy_files(src_dir, dest_dir, "**/*.so")
        
        # Fix Python extension modules - move from nested structure to correct location
        nested_python_dir = dest_dir / "lib" / "python3" / "dist-packages" / "autoware_lanelet2_extension_python"
        correct_python_dir = dest_dir / "autoware_lanelet2_extension_python"
        if nested_python_dir.exists():
            print(f"Moving Python extensions from {nested_python_dir} to {correct_python_dir}")
            # Ensure the correct directory exists
            correct_python_dir.mkdir(parents=True, exist_ok=True)
            for so_file in nested_python_dir.glob("*.so"):
                target = correct_python_dir / so_file.name
                if target.exists():
                    target.unlink()  # Remove existing file
                shutil.copy2(so_file, target)  # Use copy instead of rename
                print(f"copied {so_file} to {target}")
            # Clean up nested directory structure
            try:
                shutil.rmtree(dest_dir / "lib")
            except OSError:
                pass  # Directory not empty or doesn't exist
                
        # Copy all required shared libraries to lib subdirectory within package
        # This ensures $ORIGIN/lib RPATH can find them
        print("Copying required libraries to package lib directory...")
        lib_dir = correct_python_dir / "lib"
        lib_dir.mkdir(exist_ok=True)
        
        required_libs = [
            "liblanelet2_core.so",
            "liblanelet2_core.so.1.1.1", 
            "liblanelet2_io.so",
            "liblanelet2_projection.so",
            "liblanelet2_routing.so", 
            "liblanelet2_traffic_rules.so",
            "liblanelet2_validation.so",
            "liblanelet2_matching.so",
            "liblanelet2_extension_lib.so"
        ]
        
        for lib_name in required_libs:
            # Try to find the library in various locations
            found = False
            search_dirs = [
                src_dir / "lib",
                Path("install/lib"),
                Path("Rosless-Lanelet2/build/lanelet2_core"),
                Path("Rosless-Lanelet2/build/lanelet2_io"),
                Path("Rosless-Lanelet2/build/lanelet2_projection"),
                Path("Rosless-Lanelet2/build/lanelet2_routing"),
                Path("Rosless-Lanelet2/build/lanelet2_traffic_rules"),
                Path("Rosless-Lanelet2/build/lanelet2_validation"),
                Path("Rosless-Lanelet2/build/lanelet2_matching"),
                Path("autoware_lanelet2_extension/build")
            ]
            
            for search_dir in search_dirs:
                lib_path = search_dir / lib_name
                if lib_path.exists():
                    try:
                        target_path = lib_dir / lib_name
                        if target_path.exists():
                            target_path.unlink()
                        shutil.copy2(lib_path, target_path)
                        print(f"copied {lib_path} to {target_path}")
                        found = True
                        break
                    except (FileNotFoundError, PermissionError) as e:
                        print(f"Failed to copy {lib_path}: {e}")
                        continue
                    
            if not found:
                print(f"Warning: Could not find {lib_name}")
                
        # Create all necessary symlinks and copies for versioned libraries in lib dir
        
        # Handle liblanelet2_core.so versioning
        core_versioned = lib_dir / "liblanelet2_core.so.1.1.1"
        if core_versioned.exists():
            # Create symlink for version 1
            core_v1 = lib_dir / "liblanelet2_core.so.1"
            if core_v1.exists():
                core_v1.unlink()
            core_v1.symlink_to("liblanelet2_core.so.1.1.1")
            print(f"created symlink {core_v1} -> liblanelet2_core.so.1.1.1")
                
            # Create unversioned symlink
            core_unversioned = lib_dir / "liblanelet2_core.so"
            if core_unversioned.exists():
                core_unversioned.unlink()
            core_unversioned.symlink_to("liblanelet2_core.so.1.1.1")
            print(f"created symlink {core_unversioned} -> liblanelet2_core.so.1.1.1")
            
        print("Copied extensions and shared libraries to Poetry venv")
    else:
        print(f"Warning: Source directory {src_dir} does not exist")
    
    # Always ensure extensions are in the right place for wheel building
    ensure_extensions_for_wheel()


def ensure_extensions_for_wheel():
    """Ensure C extensions are copied to package directories for wheel building."""
    print("Ensuring extensions are in correct locations for wheel building...")
    
    # Copy autoware_lanelet2_extension_python extensions
    extension_build_dir = Path("_skbuild/linux-x86_64-3.10/cmake-build/autoware_lanelet2_extension_python")
    package_dir = Path("autoware_lanelet2_extension_python/autoware_lanelet2_extension_python")
    
    if extension_build_dir.exists():
        for so_file in extension_build_dir.glob("*.so"):
            if so_file.exists() and so_file.is_file():
                try:
                    target = package_dir / so_file.name
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(so_file, target)
                    print(f"Copied {so_file} to {target}")
                except (FileNotFoundError, PermissionError) as e:
                    print(f"Failed to copy {so_file}: {e}")
    
    # Copy lanelet2_python extensions
    lanelet2_package_dir = Path("lanelet2_python")
    
    # Look for built lanelet2_python extensions
    for build_path in [
        Path("_skbuild/linux-x86_64-3.10/cmake-install/lanelet2_python"),
        Path("_skbuild/linux-x86_64-3.10/cmake-build/lanelet2_python"),
        Path("build/lanelet2_python"),
        Path("Rosless-Lanelet2/build/lanelet2_python"),
    ]:
        if build_path.exists():
            for so_file in build_path.glob("*.so"):
                if so_file.exists() and so_file.is_file():
                    try:
                        target = lanelet2_package_dir / so_file.name
                        target.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(so_file, target)
                        print(f"Copied {so_file} to {target}")
                    except (FileNotFoundError, PermissionError) as e:
                        print(f"Failed to copy {so_file}: {e}")
    
    # Ensure shared libraries are also copied to package lib directories for wheel building
    print("Copying shared libraries to package directories for wheel...")
    
    # For autoware_lanelet2_extension_python
    package_lib_dir = package_dir / "lib"
    package_lib_dir.mkdir(exist_ok=True)
    
    required_libs = [
        "liblanelet2_core.so",
        "liblanelet2_core.so.1.1.1", 
        "liblanelet2_io.so",
        "liblanelet2_projection.so",
        "liblanelet2_routing.so", 
        "liblanelet2_traffic_rules.so",
        "liblanelet2_validation.so",
        "liblanelet2_matching.so",
        "liblanelet2_extension_lib.so"
    ]
    
    for lib_name in required_libs:
        search_dirs = [
            Path("install/lib"),
            Path("Rosless-Lanelet2/build/lanelet2_core"),
            Path("Rosless-Lanelet2/build/lanelet2_io"),
            Path("Rosless-Lanelet2/build/lanelet2_projection"),
            Path("Rosless-Lanelet2/build/lanelet2_routing"),
            Path("Rosless-Lanelet2/build/lanelet2_traffic_rules"),
            Path("Rosless-Lanelet2/build/lanelet2_validation"),
            Path("Rosless-Lanelet2/build/lanelet2_matching"),
            Path("autoware_lanelet2_extension/build")
        ]
        
        for search_dir in search_dirs:
            lib_path = search_dir / lib_name
            if lib_path.exists():
                try:
                    target_path = package_lib_dir / lib_name
                    if target_path.exists():
                        target_path.unlink()
                    shutil.copy2(lib_path, target_path)
                    print(f"Copied {lib_path} to {target_path}")
                    break
                except (FileNotFoundError, PermissionError) as e:
                    print(f"Failed to copy {lib_path}: {e}")
                    continue
    
    # Create symlinks for liblanelet2_core.so versioning in package lib dir
    core_versioned = package_lib_dir / "liblanelet2_core.so.1.1.1"
    if core_versioned.exists():
        core_v1 = package_lib_dir / "liblanelet2_core.so.1"
        if core_v1.exists():
            core_v1.unlink()
        core_v1.symlink_to("liblanelet2_core.so.1.1.1")
        
        core_unversioned = package_lib_dir / "liblanelet2_core.so"
        if core_unversioned.exists():
            core_unversioned.unlink()
        core_unversioned.symlink_to("liblanelet2_core.so.1.1.1")
        
        print(f"Created symlinks for liblanelet2_core.so in {package_lib_dir}")
    
    # For lanelet2_python package
    lanelet2_lib_dir = lanelet2_package_dir / "lib"
    lanelet2_lib_dir.mkdir(exist_ok=True)
    
    for lib_name in required_libs:
        search_dirs = [
            Path("install/lib"),
            Path("Rosless-Lanelet2/build/lanelet2_core"),
            Path("Rosless-Lanelet2/build/lanelet2_io"),
            Path("Rosless-Lanelet2/build/lanelet2_projection"),
            Path("Rosless-Lanelet2/build/lanelet2_routing"),
            Path("Rosless-Lanelet2/build/lanelet2_traffic_rules"),
            Path("Rosless-Lanelet2/build/lanelet2_validation"),
            Path("Rosless-Lanelet2/build/lanelet2_matching"),
            Path("autoware_lanelet2_extension/build")
        ]
        
        for search_dir in search_dirs:
            lib_path = search_dir / lib_name
            if lib_path.exists():
                try:
                    target_path = lanelet2_lib_dir / lib_name
                    if target_path.exists():
                        target_path.unlink()
                    shutil.copy2(lib_path, target_path)
                    print(f"Copied {lib_path} to {target_path}")
                    break
                except (FileNotFoundError, PermissionError) as e:
                    print(f"Failed to copy {lib_path}: {e}")
                    continue
    
    # Create symlinks for liblanelet2_core.so versioning in lanelet2_python lib dir
    core_versioned = lanelet2_lib_dir / "liblanelet2_core.so.1.1.1"
    if core_versioned.exists():
        core_v1 = lanelet2_lib_dir / "liblanelet2_core.so.1"
        if core_v1.exists():
            core_v1.unlink()
        core_v1.symlink_to("liblanelet2_core.so.1.1.1")
        
        core_unversioned = lanelet2_lib_dir / "liblanelet2_core.so"
        if core_unversioned.exists():
            core_unversioned.unlink()
        core_unversioned.symlink_to("liblanelet2_core.so.1.1.1")
        
        print(f"Created symlinks for liblanelet2_core.so in {lanelet2_lib_dir}")


if __name__ == "__main__":
    build({})
"""Setup script for lanelet2-python-api-for-autoware with C++ extension building."""

import os
import subprocess
import sys
from pathlib import Path
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.install import install


def run_command(cmd, cwd=None):
    """Run a shell command and check for errors."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")
    return result.stdout


def init_submodules():
    """Initialize git submodules if not already done.

    When this package is installed via pip/uv from a git URL, the tool clones
    the repository but does NOT initialise submodules automatically.  We run
    ``git submodule update --init --recursive`` here so that the
    ``autoware_lanelet2_extension`` directory is populated before setuptools
    tries to resolve ``package_dir``.
    """
    root_dir = Path(__file__).parent.absolute()
    marker = root_dir / "autoware_lanelet2_extension" / "CMakeLists.txt"
    if not marker.exists():
        print("Initializing git submodules ...")
        subprocess.run(
            ["git", "submodule", "update", "--init", "--recursive"],
            cwd=root_dir,
            check=True,
        )


def apply_autoware_patch():
    """Apply the autoware_lanelet2_extension patch after submodule init.

    The submodule contains the upstream autoware_lanelet2_extension which
    depends on ROS/autoware_cmake.  The patch removes those dependencies
    so the project can be built standalone.
    """
    root_dir = Path(__file__).parent.absolute()
    submodule = root_dir / "autoware_lanelet2_extension"
    patch = root_dir / "patches" / "autoware_lanelet2_extension_full.patch"
    if not patch.is_file():
        return
    if not submodule.is_dir():
        return

    # Check if the patch is already applied (reverse-apply check succeeds).
    result = subprocess.run(
        ["git", "apply", "--reverse", "--check", str(patch)],
        cwd=submodule,
        capture_output=True,
    )
    if result.returncode == 0:
        # Patch is already applied.
        return

    print("Applying autoware_lanelet2_extension patch ...")
    subprocess.run(
        ["git", "apply", str(patch)],
        cwd=submodule,
        check=True,
    )


# Initialise submodules and apply patches early – before setuptools
# inspects package_dir.
init_submodules()
apply_autoware_patch()

# Path prefix for sources that live inside the submodule.
_EXT_SUB = "autoware_lanelet2_extension"


def build_cpp_extensions():
    """Build all C++ extensions using CMake."""
    root_dir = Path(__file__).parent.absolute()
    install_dir = root_dir / "install"
    
    # Check for system dependencies first
    try:
        run_command(["cmake", "--version"])
        run_command(["make", "--version"])
    except (FileNotFoundError, RuntimeError):
        print("Error: Required build tools (cmake, make) not found.", file=sys.stderr)
        print("Please install build dependencies first.", file=sys.stderr)
        raise RuntimeError("Missing build dependencies")
    
    # Build projects in dependency order with proper CMAKE_PREFIX_PATH
    # After submodule init the C++ and Python extension sources live under
    # autoware_lanelet2_extension/<name> (one level deeper than before).
    projects = [
        ("Rosless-Lanelet2", []),
        (f"{_EXT_SUB}/autoware_lanelet2_extension", [str(install_dir)]),
        (f"{_EXT_SUB}/autoware_lanelet2_extension_python", [str(install_dir)])
    ]
    
    for project_name, cmake_prefix_paths in projects:
        project_path = root_dir / project_name
        if project_path.exists():
            project_build = root_dir / "build_cpp" / project_name
            project_build.mkdir(parents=True, exist_ok=True)
            
            print(f"Building {project_name}...")
            
            cmake_cmd = [
                "cmake",
                str(project_path),
                f"-DCMAKE_INSTALL_PREFIX={install_dir}",
                f"-DPython3_EXECUTABLE={sys.executable}",
                "-DCMAKE_BUILD_TYPE=Release",
                "-Wno-dev"  # Suppress developer warnings
            ]
            
            # Add CMAKE_PREFIX_PATH for dependency projects
            if cmake_prefix_paths:
                cmake_cmd.append(f"-DCMAKE_PREFIX_PATH={';'.join(cmake_prefix_paths)}")
            
            run_command(cmake_cmd, cwd=project_build)
            # Use parallel build with available cores
            import multiprocessing
            nproc = multiprocessing.cpu_count()
            run_command(["make", f"-j{nproc}"], cwd=project_build)
            run_command(["make", "install"], cwd=project_build)


class BuildPyCommand(build_py):
    """Custom build command that builds C++ extensions first."""
    
    def run(self):
        # First build C++ extensions
        build_cpp_extensions()
        
        # Then run the parent class's run method to set up directories
        super().run()
        
        # Copy built extensions to package directory
        root_dir = Path(__file__).parent.absolute()
        install_dir = root_dir / "install"
        
        # Copy lanelet2 modules
        lanelet2_src = install_dir / "lib" / "python3" / "dist-packages" / "lanelet2"
        if lanelet2_src.exists():
            import shutil
            lanelet2_dst = Path(self.build_lib) / "lanelet2"
            if lanelet2_dst.exists():
                shutil.rmtree(lanelet2_dst)
            shutil.copytree(lanelet2_src, lanelet2_dst)
        
        # Copy autoware extension modules next to the Python package (nested layout)
        autoware_src = install_dir / "lib" / "python3" / "dist-packages" / "autoware_lanelet2_extension_python"
        if autoware_src.exists():
            import shutil
            autoware_dst = Path(self.build_lib) / "autoware_lanelet2_extension_python"
            for so_file in autoware_src.glob("*.so"):
                shutil.copy2(so_file, autoware_dst)
        
        # Copy shared libraries
        lib_src = install_dir / "lib"
        if lib_src.exists():
            lib_dst = Path(self.build_lib) / "lanelet2" / "lib"
            lib_dst.mkdir(parents=True, exist_ok=True)
            for so_file in lib_src.glob("*.so*"):
                if so_file.is_file():
                    import shutil
                    shutil.copy2(so_file, lib_dst)


class DevelopCommand(develop):
    """Custom develop command that builds C++ extensions first."""
    
    def run(self):
        build_cpp_extensions()
        super().run()


class InstallCommand(install):
    """Custom install command that builds C++ extensions first."""
    
    def run(self):
        build_cpp_extensions()
        super().run()


# Determine packages and package directories
def get_packages_and_dirs():
    """Get packages and package directories based on what exists."""
    packages = [
        "autoware_lanelet2_extension_python",
        "autoware_lanelet2_extension_python.impl",
        "autoware_lanelet2_extension_python.projection",
        "autoware_lanelet2_extension_python.regulatory_elements",
        "autoware_lanelet2_extension_python.utility",
    ]
    
    package_dir = {
        "autoware_lanelet2_extension_python": f"{_EXT_SUB}/autoware_lanelet2_extension_python/autoware_lanelet2_extension_python",
    }
    
    package_data = {
        "autoware_lanelet2_extension_python": ["*.so"],
    }
    
    # Check if lanelet2 package exists (after build)
    lanelet2_path = Path("install/lib/python3/dist-packages/lanelet2")
    if lanelet2_path.exists() or Path("lanelet2").exists():
        packages.append("lanelet2")
        # Use local copy if it exists, otherwise use install path
        if Path("lanelet2").exists():
            package_dir["lanelet2"] = "lanelet2"
        else:
            package_dir["lanelet2"] = str(lanelet2_path)
        package_data["lanelet2"] = ["*.so", "lib/*.so*"]
    
    return packages, package_dir, package_data


packages, package_dir, package_data = get_packages_and_dirs()

# Setup configuration
setup(
    cmdclass={
        'build_py': BuildPyCommand,
        'develop': DevelopCommand,
        'install': InstallCommand,
    },
    packages=packages,
    package_dir=package_dir,
    package_data=package_data,
    include_package_data=True,
)
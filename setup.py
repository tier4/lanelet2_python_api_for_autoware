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


def build_cpp_extensions():
    """Build all C++ extensions using existing build script."""
    root_dir = Path(__file__).parent.absolute()
    
    # Use a different build directory to avoid conflicts
    for project in ["Rosless-Lanelet2", "autoware_lanelet2_extension", "autoware_lanelet2_extension_python"]:
        project_path = root_dir / project
        if project_path.exists():
            project_build = root_dir / "build_cpp" / project
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


class BuildPyCommand(build_py):
    """Custom build command that builds C++ extensions first."""
    
    def run(self):
        # First run the parent class's run method to set up directories
        super().run()
        
        # Then build C++ extensions
        build_cpp_extensions()
        
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
        
        # Copy autoware extension modules
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


# Setup configuration
setup(
    cmdclass={
        'build_py': BuildPyCommand,
        'develop': DevelopCommand,
        'install': InstallCommand,
    },
    packages=[
        "autoware_lanelet2_extension_python",
        "autoware_lanelet2_extension_python.impl",
        "autoware_lanelet2_extension_python.projection",
        "autoware_lanelet2_extension_python.regulatory_elements",
        "autoware_lanelet2_extension_python.utility",
        "lanelet2",
    ],
    package_dir={
        "autoware_lanelet2_extension_python": "autoware_lanelet2_extension_python/autoware_lanelet2_extension_python",
        "lanelet2": "install/lib/python3/dist-packages/lanelet2",
    },
    package_data={
        "autoware_lanelet2_extension_python": ["*.so"],
        "lanelet2": ["*.so", "lib/*.so*"],
    },
    include_package_data=True,
)
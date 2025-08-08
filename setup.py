import os
import subprocess
from pathlib import Path
from skbuild import setup

def build_dependencies():
    """Build C++ dependencies using the existing build.sh script"""
    current_dir = Path(__file__).parent
    build_script = current_dir / "build.sh"
    
    if build_script.exists():
        print("Building C++ dependencies...")
        subprocess.run(["bash", str(build_script)], check=True, cwd=current_dir)
    else:
        print("Warning: build.sh not found, skipping dependency build")

# Build dependencies before setting up the Python package
build_dependencies()

setup(
    name="autoware_lanelet2_extension_python",
    version="0.1.0", 
    description="Python bindings for Lanelet2 with Autoware extension",
    author="Masaya Kataoka",
    author_email="ms.kataoka@gmail.com",
    license="MIT",
    packages=["lanelet2_python"],
    install_requires=[
        "numpy",
    ],
    cmake_args=[
        "-DCMAKE_BUILD_TYPE=Release",
    ],
)
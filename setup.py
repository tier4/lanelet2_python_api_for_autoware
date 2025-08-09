import os
import subprocess
from pathlib import Path
from skbuild import setup

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
"""Setup script for autoware-lanelet2-extension-python."""

import os
import subprocess
import sys
from pathlib import Path

from setuptools import setup, find_packages


# Note: The actual build is handled by Poetry's build.py script when using poetry build
# This setup.py is primarily for compatibility with pip install from git repositories


setup(
    name="autoware-lanelet2-extension-python",
    version="0.1.0",
    description="Python bindings for Lanelet2 with Autoware extension",
    author="Masaya Kataoka",
    author_email="ms.kataoka@gmail.com",
    packages=find_packages(include=['autoware_lanelet2_extension_python*', 'lanelet2_python*']),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.21.0",
    ],
    include_package_data=True,
    package_data={
        'autoware_lanelet2_extension_python': ['*.so', '*.pyd'],
        'lanelet2_python': ['*.so', '*.pyd'],
    },
    zip_safe=False,
)
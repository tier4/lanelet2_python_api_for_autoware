"""
Simple setup.py for pip install compatibility.
This package requires prebuilt Lanelet2 libraries.
"""

import sys
import warnings
from pathlib import Path
from setuptools import setup, find_packages

def check_prebuilt_extensions():
    """Check if prebuilt extensions exist."""
    current_dir = Path(__file__).parent
    required_extensions = [
        current_dir / "autoware_lanelet2_extension_python" / "_lanelet2_extension_python_boost_python_projection.so",
        current_dir / "autoware_lanelet2_extension_python" / "_lanelet2_extension_python_boost_python_regulatory_elements.so",
        current_dir / "autoware_lanelet2_extension_python" / "_lanelet2_extension_python_boost_python_utility.so"
    ]
    
    missing = [ext.name for ext in required_extensions if not ext.exists()]
    
    if missing:
        print(f"""
WARNING: Missing prebuilt extensions: {missing}

This is a stub package for pip install compatibility.
For full functionality, please:

1. For development: Use 'poetry install' in a cloned repository
2. For production: Install from prebuilt wheels from GitHub Releases
3. With existing libraries: Use this package in an environment where 
   Lanelet2 libraries are already available

The package will install but may not function without the required libraries.
""", file=sys.stderr)

# Check for prebuilt extensions
check_prebuilt_extensions()

setup(
    name="autoware-lanelet2-extension-python",
    version="0.1.0",
    description="Python bindings for Lanelet2 with Autoware extension",
    long_description="""
Python bindings for Lanelet2 with Autoware extension.

Note: This package requires prebuilt Lanelet2 libraries. 
For development, use 'poetry install' in the cloned repository.
For production, install from prebuilt wheels.
""",
    long_description_content_type="text/plain",
    author="Masaya Kataoka",
    author_email="ms.kataoka@gmail.com",
    url="https://github.com/tier4/lanelet2_python_api_for_autoware",
    packages=find_packages(include=['autoware_lanelet2_extension_python*', 'lanelet2_python*']),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.21.0",
    ],
    include_package_data=True,
    package_data={
        'autoware_lanelet2_extension_python': ['*.so', '*.pyd', '**/*.so', '**/*.pyd', '**/*.py'],
        'lanelet2_python': ['*.so', '*.pyd', '**/*.so', '**/*.pyd', '**/*.py'],
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
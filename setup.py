"""
Simple setup.py for pip install compatibility.
This package requires prebuilt Lanelet2 libraries and is intended for development use.
For production, use poetry build or pre-built wheels.
"""

import warnings
from setuptools import setup, find_packages

# Warn users about limitations
warnings.warn(
    "This package requires prebuilt Lanelet2 libraries. "
    "For full functionality, use 'poetry install' in the development environment "
    "or install from pre-built wheels.",
    UserWarning
)

setup(
    name="autoware-lanelet2-extension-python",
    version="0.1.0",
    description="Python bindings for Lanelet2 with Autoware extension (development version)",
    long_description="This is a development version that requires prebuilt libraries. Use poetry for full build.",
    author="Masaya Kataoka",
    author_email="ms.kataoka@gmail.com",
    packages=find_packages(include=['autoware_lanelet2_extension_python*', 'lanelet2_python*']),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.21.0",
    ],
    include_package_data=True,
    package_data={
        'autoware_lanelet2_extension_python': ['*.so', '*.pyd', '**/*.so', '**/*.pyd'],
        'lanelet2_python': ['*.so', '*.pyd', '**/*.so', '**/*.pyd'],
    },
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
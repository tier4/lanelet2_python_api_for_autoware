#!/usr/bin/env python3
import os
import subprocess
import sys
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def _run_build():
    """Run the lanelet2-build command after installation."""
    try:
        print("🚀 Auto-building Lanelet2 libraries...")
        from lanelet2_python_api.build import main
        result = main()
        if result == 0:
            print("✅ Lanelet2 build completed successfully!")
        else:
            print("❌ Lanelet2 build failed. You can retry with: uv run lanelet2-build")
    except Exception as e:
        print(f"⚠️  Auto-build failed: {e}")
        print("You can manually build with: uv run lanelet2-build")


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        _run_build()


class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        _run_build()


# Use the custom commands
setup(
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)
#!/usr/bin/env python3
import os
import subprocess
import sys
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install


def _add_lanelet2_path():
    """Add Lanelet2 paths to virtual environment"""
    try:
        import site
        project_root = os.path.dirname(os.path.abspath(__file__))
        install_python_path = os.path.join(project_root, 'install', 'lib', 'python3', 'dist-packages')
        install_lib_path = os.path.join(project_root, 'install', 'lib')
        install_include_path = os.path.join(project_root, 'install', 'include')
        
        # Find site-packages directory
        site_packages = None
        venv_bin = None
        
        # Check if we're in a virtual environment
        if hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix:
            # We're in a virtual environment
            venv_root = sys.prefix
            venv_bin = os.path.join(venv_root, 'bin')
            site_packages = os.path.join(venv_root, 'lib', f'python{sys.version_info.major}.{sys.version_info.minor}', 'site-packages')
        
        # Fallback search
        if not site_packages:
            for path in sys.path:
                if 'site-packages' in path and os.path.exists(path):
                    site_packages = path
                    break
        
        success = False
        
        # Add .pth file for Python path
        if site_packages and os.path.exists(install_python_path):
            pth_file = os.path.join(site_packages, 'lanelet2_autoware.pth')
            with open(pth_file, 'w') as f:
                f.write(install_python_path + '\n')
            print(f"✅ Added Python path to {pth_file}")
            success = True
        
        # Add environment setup script for virtual environment
        if venv_bin and os.path.exists(venv_bin):
            setup_script = os.path.join(venv_bin, 'lanelet2_setup.sh')
            with open(setup_script, 'w') as f:
                f.write(f'''#!/bin/bash
# Lanelet2 Environment Setup for UV Virtual Environment
export LD_LIBRARY_PATH="{install_lib_path}:$LD_LIBRARY_PATH"
export CPATH="{install_include_path}:$CPATH"
''')
            os.chmod(setup_script, 0o755)
            
            # Add to activate script
            activate_script = os.path.join(venv_bin, 'activate')
            if os.path.exists(activate_script):
                with open(activate_script, 'r') as f:
                    content = f.read()
                if 'lanelet2_setup.sh' not in content:
                    with open(activate_script, 'a') as f:
                        f.write(f'\n# Lanelet2 setup\nsource "{setup_script}"\n')
            
            print(f"✅ Added environment setup to {setup_script}")
            success = True
        
        if not success:
            print("⚠️  Could not set up automatic path configuration")
            print("   Manual setup required: export LD_LIBRARY_PATH=...")
            
    except Exception as e:
        print(f"⚠️  Failed to add Lanelet2 paths: {e}")


def _run_build():
    """Run the lanelet2-build command after installation."""
    try:
        print("🚀 Auto-building Lanelet2 libraries...")
        from lanelet2_python_api.build import main
        result = main()
        if result == 0:
            print("✅ Lanelet2 build completed successfully!")
            # Add path after successful build
            _add_lanelet2_path()
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
    # Include shared libraries in the package
    data_files=[
        ('lib', [
            'install/lib/liblanelet2_core.so.1.1.1',
            'install/lib/liblanelet2_core.so',
            'install/lib/liblanelet2_extension_lib.so',
            'install/lib/liblanelet2_io.so',
            'install/lib/liblanelet2_matching.so',
            'install/lib/liblanelet2_projection.so',
            'install/lib/liblanelet2_routing.so',
            'install/lib/liblanelet2_traffic_rules.so',
            'install/lib/liblanelet2_validation.so',
        ] if os.path.exists('install/lib') else []),
    ] if os.path.exists('install/lib') else [],
    include_package_data=True,
    package_data={
        'lanelet2_python_api': ['install/**/*'],
        '': ['install/**/*'],
    },
)
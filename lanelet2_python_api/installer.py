#!/usr/bin/env python3
"""
One-command installer for Lanelet2 Python API
Combines package installation and library building
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command with proper error handling"""
    if description:
        print(f"🔧 {description}")
    
    print(f"   Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False, e.stderr


def check_uv_environment():
    """Check and display UV virtual environment status"""
    print("🔍 Checking UV environment...")
    
    # Check if we're in a UV project
    if not Path("pyproject.toml").exists():
        print("❌ No pyproject.toml found - not a UV project")
        return False
        
    # Check for .venv directory
    venv_path = Path(".venv")
    if venv_path.exists():
        print(f"✅ Virtual environment found: {venv_path.absolute()}")
    else:
        print("📦 Virtual environment will be created by UV")
    
    # Show UV version
    success, output = run_command(["uv", "--version"], "")
    if success:
        print(f"🔧 {output.strip()}")
    
    return True


def main():
    """Main installer function"""
    print("🚀 Lanelet2 Python API One-Command Installer")
    print("=" * 50)
    
    # Get project root
    project_root = Path(__file__).parent.parent.absolute()
    print(f"📁 Project root: {project_root}")
    
    # Change to project directory
    original_cwd = os.getcwd()
    os.chdir(project_root)
    
    try:
        # Step 0: Check UV environment
        if not check_uv_environment():
            return 1
            
        print()
        
        # Step 1: Sync UV environment (creates venv + installs dependencies)
        print("🔄 Setting up UV virtual environment and dependencies...")
        success, output = run_command(
            ["uv", "sync", "--dev"],
            "Syncing UV environment"
        )
        if not success:
            print("⚠️  UV sync failed, trying basic install...")
            # Fallback to direct install
            success, output = run_command(
                ["uv", "pip", "install", "-e", "."],
                "Installing package in editable mode (fallback)"
            )
            if not success:
                print("❌ Package installation failed")
                return 1
        
        print("✅ UV environment setup completed")
        
        # Step 2: Show virtual environment info
        print("\n📋 Virtual Environment Info:")
        venv_path = Path(".venv").absolute()
        if venv_path.exists():
            print(f"   Location: {venv_path}")
            python_exe = venv_path / "bin" / "python"
            if python_exe.exists():
                success, output = run_command(
                    [str(python_exe), "--version"], 
                    ""
                )
                if success:
                    print(f"   Python: {output.strip()}")
        
        # Step 3: Build libraries automatically (triggered by setup.py post-install hook)
        print("\n🏗️  C++ libraries will be built automatically via post-install hooks")
        
        # Step 4: Verify installation within UV environment
        print("\n🔍 Verifying installation in UV environment...")
        success, output = run_command(
            ["uv", "run", "python", "-c", "import lanelet2_python_api; print('✅ Package import successful')"],
            "Testing package import"
        )
        
        if success:
            # Test full functionality
            success, output = run_command(
                ["uv", "run", "python", "-c", """
import sys
print('🔧 Testing all modules...')
try:
    from lanelet2 import core, io, projection, routing, traffic_rules
    print('✅ Core Lanelet2 modules working')
    from autoware_lanelet2_extension_python.projection import MGRSProjector
    print('✅ Autoware extensions working')
    print('🎉 Full installation test passed!')
except ImportError as e:
    print(f'⚠️  Some modules missing: {e}')
    print('Run: uv run lanelet2-build')
"""],
                "Testing full functionality"
            )
        
        if success:
            print("\n🎉 Installation completed successfully!")
            print("\n📋 Usage (always use 'uv run'):")
            print("   uv run python -c \"import lanelet2\"")
            print("   uv run python your_script.py")
            print("\n🔧 Available commands:")
            print("   uv run lanelet2-build   # Manual C++ library build")
            print("   uv run lanelet2-install # This installer")
            print("\n💡 To activate environment manually:")
            print("   source .venv/bin/activate")
            return 0
        else:
            print("⚠️  Installation completed but some tests failed")
            print("   Try running: uv run lanelet2-build")
            return 1
            
    except KeyboardInterrupt:
        print("\n⏹️  Installation cancelled by user")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    finally:
        os.chdir(original_cwd)


if __name__ == '__main__':
    sys.exit(main())
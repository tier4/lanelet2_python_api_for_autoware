#!/usr/bin/env python3
"""
One-command installer for Lanelet2 Python API
Combines package installation and library building
"""

import os
import subprocess
import sys
import shutil
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


def copy_shared_libraries():
    """Copy shared libraries (.so files) to UV virtual environment and create wrapper"""
    print("📚 Copying shared libraries to virtual environment...")
    
    # Get paths
    project_root = Path.cwd()
    install_lib_path = project_root / "install" / "lib"
    venv_lib_path = project_root / ".venv" / "lib"
    venv_bin_path = project_root / ".venv" / "bin"
    
    if not install_lib_path.exists():
        print(f"⚠️  Install library path not found: {install_lib_path}")
        print("   Run 'uv run lanelet2-build' first to build libraries")
        return False
    
    if not venv_lib_path.exists():
        print(f"⚠️  Virtual environment lib path not found: {venv_lib_path}")
        return False
    
    # Find all .so files
    so_files = list(install_lib_path.glob("*.so*"))
    
    if not so_files:
        print("⚠️  No shared libraries found to copy")
        return False
    
    # Copy each .so file
    copied_count = 0
    for so_file in so_files:
        dest_path = venv_lib_path / so_file.name
        try:
            shutil.copy2(so_file, dest_path)
            print(f"   ✅ Copied: {so_file.name}")
            copied_count += 1
        except Exception as e:
            print(f"   ❌ Failed to copy {so_file.name}: {e}")
    
    # Create UV wrapper script with library path
    if venv_bin_path.exists() and copied_count > 0:
        wrapper_script = venv_bin_path / "uv-run-with-libs"
        wrapper_content = f"""#!/bin/bash
# UV run wrapper that sets up library path automatically

# Get the directory of this script (venv/bin)
SCRIPT_DIR="$(cd "$(dirname "${{BASH_SOURCE[0]}}")" && pwd)"
VENV_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_LIB="$VENV_ROOT/lib"

# Add venv lib to LD_LIBRARY_PATH if libraries exist
if [ -f "$VENV_LIB/liblanelet2_core.so.1.1.1" ]; then
    export LD_LIBRARY_PATH="$VENV_LIB:$LD_LIBRARY_PATH"
fi

# Execute the command with uv run
exec uv run "$@"
"""
        try:
            wrapper_script.write_text(wrapper_content)
            wrapper_script.chmod(0o755)
            print(f"   ✅ Created wrapper script: {wrapper_script}")
        except Exception as e:
            print(f"   ⚠️  Failed to create wrapper script: {e}")
    
    if copied_count > 0:
        print(f"✅ Successfully copied {copied_count} shared libraries to virtual environment")
        print("💡 Libraries are automatically preloaded - normal 'uv run' commands will work!")
        return True
    else:
        print("❌ No libraries were copied successfully")
        return False


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
        
        # Step 3.5: Copy shared libraries to virtual environment
        print()
        copy_shared_libraries()
        
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
        
        # Test the readme example
        if success:
            success, output = run_command(
                ["uv", "run", "python", "-c", "import lanelet2; print('Success!')"],
                "Testing readme example"
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
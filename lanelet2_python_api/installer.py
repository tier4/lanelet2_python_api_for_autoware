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
        # Step 1: Install package in editable mode
        success, output = run_command(
            ["uv", "pip", "install", "-e", "."],
            "Installing package in editable mode"
        )
        if not success:
            print("❌ Package installation failed")
            return 1
        
        print("✅ Package installed successfully")
        
        # Step 2: Build libraries automatically (this will be triggered by setup.py)
        print("🏗️  Libraries will be built automatically via post-install hook")
        
        # Step 3: Verify installation
        print("\n🔍 Verifying installation...")
        success, output = run_command(
            ["python", "-c", "import lanelet2; print('✅ Import successful')"],
            "Testing import"
        )
        
        if success:
            print("🎉 Installation completed successfully!")
            print("\n📋 Usage:")
            print("   import lanelet2")
            print("   from lanelet2 import core, io, projection, routing, traffic_rules")
            print("\n🔧 Manual build (if needed):")
            print("   uv run lanelet2-build")
            return 0
        else:
            print("⚠️  Installation completed but import test failed")
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
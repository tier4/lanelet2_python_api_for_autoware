#!/usr/bin/env python3
"""
Debug script for pip install issues with autoware-lanelet2-extension-python
"""

def debug_installation():
    print("🔍 Debugging autoware-lanelet2-extension-python installation")
    print("=" * 60)
    
    # Check Python version
    import sys
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Check if package is installed
    try:
        import autoware_lanelet2_extension_python
        print(f"✅ Package found at: {autoware_lanelet2_extension_python.__file__}")
        print(f"✅ Package version: {autoware_lanelet2_extension_python.__version__}")
    except ImportError as e:
        print(f"❌ Package not found: {e}")
        print("\n🔧 Solution: Run the following command:")
        print("pip install git+https://github.com/tier4/lanelet2_python_api_for_autoware.git@feature/poetry")
        return
    
    # Test specific imports
    test_imports = [
        ("projection.MGRSProjector", "from autoware_lanelet2_extension_python.projection import MGRSProjector"),
        ("projection.TransverseMercatorProjector", "from autoware_lanelet2_extension_python.projection import TransverseMercatorProjector"),
        ("regulatory_elements.AutowareTrafficLight", "from autoware_lanelet2_extension_python.regulatory_elements import AutowareTrafficLight"),
        ("utility.calculate_distance", "from autoware_lanelet2_extension_python.utility import calculate_distance"),
        ("lanelet2_python.Point3d", "from lanelet2_python import Point3d"),
    ]
    
    print("\n🧪 Testing imports:")
    for name, import_statement in test_imports:
        try:
            exec(import_statement)
            print(f"✅ {name}")
        except Exception as e:
            print(f"❌ {name}: {e}")
    
    # Test basic functionality
    print("\n🚀 Testing functionality:")
    try:
        from autoware_lanelet2_extension_python.projection import MGRSProjector
        mgrs = MGRSProjector('54SUE')
        result = mgrs.forward(35.6762, 139.6503)
        print(f"✅ MGRSProjector.forward(): {result}")
    except Exception as e:
        print(f"❌ MGRSProjector test failed: {e}")
    
    try:
        from autoware_lanelet2_extension_python.regulatory_elements import AutowareTrafficLight
        traffic_light = AutowareTrafficLight(id=1, type='test_light')
        print(f"✅ AutowareTrafficLight creation: {traffic_light.type}")
    except Exception as e:
        print(f"❌ AutowareTrafficLight test failed: {e}")
    
    try:
        from autoware_lanelet2_extension_python.utility import calculate_distance
        dist = calculate_distance((0, 0), (3, 4))
        print(f"✅ calculate_distance(): {dist}")
    except Exception as e:
        print(f"❌ calculate_distance test failed: {e}")
    
    try:
        import lanelet2_python
        point1 = lanelet2_python.Point3d(1.0, 2.0, 3.0, 123)
        point2 = lanelet2_python.Point3d(4.0, 5.0, 6.0, 456)
        dist = point1.distance(point2)
        print(f"✅ lanelet2_python.Point3d.distance(): {dist:.2f}")
    except Exception as e:
        print(f"❌ lanelet2_python test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Debug completed! If all tests pass, the package is working correctly.")
    print("\nIf you see any ❌ errors, please:")
    print("1. Uninstall: pip uninstall autoware-lanelet2-extension-python")
    print("2. Reinstall: pip install git+https://github.com/tier4/lanelet2_python_api_for_autoware.git@feature/poetry")
    print("3. Run this script again")

if __name__ == "__main__":
    debug_installation()
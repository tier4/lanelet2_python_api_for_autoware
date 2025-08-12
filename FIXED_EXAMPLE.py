#!/usr/bin/env python3
"""
Fixed example showing how to use lanelet2.io.load correctly
"""

import lanelet2
from pathlib import Path

def read_lanelet_v1(path: Path):
    """Solution 1: Use Origin directly (simplest)"""
    return lanelet2.io.load(str(path), lanelet2.io.Origin(0.0, 0.0))

def read_lanelet_v2(path: Path):
    """Solution 2: Use standard UTM Projector"""
    origin = lanelet2.io.Origin(0.0, 0.0)
    projector = lanelet2.projection.UtmProjector(origin)
    return lanelet2.io.load(str(path), projector)

def read_lanelet_v3(path: Path):
    """Solution 3: Use default Mercator Projector"""
    return lanelet2.io.load(str(path))  # Uses default MercatorProjector

def read_lanelet_v4(path: Path):
    """Solution 4: Use Mercator Projector explicitly"""
    origin = lanelet2.io.Origin(0.0, 0.0)
    projector = lanelet2.projection.MercatorProjector(origin)
    return lanelet2.io.load(str(path), projector)

# Your original code that fails:
def read_lanelet_original(path: Path):
    """This fails because MGRSProjector is not a C++ lanelet::Projector"""
    from autoware_lanelet2_extension_python.projection import MGRSProjector
    return lanelet2.io.load(str(path), MGRSProjector(lanelet2.io.Origin(0.0, 0.0)))

if __name__ == "__main__":
    # Test the working solutions
    print("Testing working solutions:")
    
    try:
        result1 = read_lanelet_v1("lanelet2_map.osm")
        print("✅ Solution 1 (Origin): Success")
    except Exception as e:
        print(f"❌ Solution 1: {e}")
    
    try:
        result2 = read_lanelet_v2("lanelet2_map.osm")
        print("✅ Solution 2 (UTM): Success")
    except Exception as e:
        print(f"❌ Solution 2: {e}")
    
    try:
        result3 = read_lanelet_v3("lanelet2_map.osm")
        print("✅ Solution 3 (Default): Success")
    except Exception as e:
        print(f"❌ Solution 3: {e}")
    
    try:
        result4 = read_lanelet_v4("lanelet2_map.osm")
        print("✅ Solution 4 (Mercator): Success")
    except Exception as e:
        print(f"❌ Solution 4: {e}")
    
    # Test the failing original code
    try:
        result_orig = read_lanelet_original("lanelet2_map.osm")
        print("❌ Original should have failed but didn't")
    except Exception as e:
        print(f"✅ Original fails as expected: {type(e).__name__}")
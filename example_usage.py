#!/usr/bin/env python3
"""Example usage of Lanelet2 Python API with Autoware extensions."""

import lanelet2
from autoware_lanelet2_extension_python.projection import MGRSProjector, TransverseMercatorProjector

def main():
    print("=== Lanelet2 Python API with Autoware Extensions Example ===\n")
    
    # Create an origin point (Tokyo area)
    lat, lon, alt = 35.681298, 139.766247, 0.0
    origin = lanelet2.io.Origin(lat, lon, alt)
    print(f"Created origin point at lat={lat}, lon={lon}, alt={alt}")
    
    # Create MGRS projector
    mgrs_projector = MGRSProjector(origin)
    print("\n✓ MGRS Projector created successfully")
    
    # Create Transverse Mercator projector
    tm_projector = TransverseMercatorProjector(origin)
    print("✓ Transverse Mercator Projector created successfully")
    
    # Create a simple point
    point = lanelet2.core.Point3d(1, 0.0, 1.0, 0.0)
    print(f"\nCreated 3D point: id={point.id}, x={point.x}, y={point.y}, z={point.z}")
    
    # Create a LineString
    points = [
        lanelet2.core.Point3d(1, 0.0, 0.0, 0.0),
        lanelet2.core.Point3d(2, 1.0, 0.0, 0.0),
        lanelet2.core.Point3d(3, 2.0, 0.0, 0.0)
    ]
    linestring = lanelet2.core.LineString3d(100, points)
    print(f"Created LineString with {len(linestring)} points")
    
    # Create a simple Lanelet
    left_bound = lanelet2.core.LineString3d(101, [
        lanelet2.core.Point3d(11, 0.0, 0.0, 0.0),
        lanelet2.core.Point3d(12, 10.0, 0.0, 0.0)
    ])
    
    right_bound = lanelet2.core.LineString3d(102, [
        lanelet2.core.Point3d(21, 0.0, 2.0, 0.0),
        lanelet2.core.Point3d(22, 10.0, 2.0, 0.0)
    ])
    
    lanelet = lanelet2.core.Lanelet(200, left_bound, right_bound)
    print(f"\nCreated Lanelet: id={lanelet.id}")
    print(f"  Left bound has {len(lanelet.leftBound)} points")
    print(f"  Right bound has {len(lanelet.rightBound)} points")
    
    # Create a LaneletMap
    lanelet_map = lanelet2.core.LaneletMap()
    lanelet_map.add(lanelet)
    print(f"\nCreated LaneletMap with {len(list(lanelet_map.laneletLayer))} lanelets")
    
    print("\n✅ All operations completed successfully!")

if __name__ == "__main__":
    main()
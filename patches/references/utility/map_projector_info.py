"""
From tier4_autoware_msgs: https://github.com/tier4/tier4_autoware_msgs/blob/tier4/universe/tier4_map_msgs/msg/MapProjectorInfo.msg

# Projector type
# Also refer to https://github.com/autowarefoundation/autoware.universe/tree/main/map/autoware_map_projection_loader/README.md
string LOCAL = "local"
string LOCAL_CARTESIAN_UTM = "LocalCartesianUTM"
string MGRS = "MGRS"
string TRANSVERSE_MERCATOR = "TransverseMercator"
string projector_type

# Vertical datum
# Also refer to https://github.com/autowarefoundation/autoware.universe/tree/main/map/autoware_map_projection_loader/README.md
string WGS84 = "WGS84"
string EGM2008 = "EGM2008"
string vertical_datum

# Used for MGRS map
string mgrs_grid

# Used for some map projection types
# altitude may not be in ellipsoid height
geographic_msgs/GeoPoint map_origin

-----
https://docs.ros.org/en/melodic/api/geographic_msgs/html/msg/GeoPoint.html
# Geographic point, using the WGS 84 reference ellipsoid.

# Latitude [degrees]. Positive is north of equator; negative is south
# (-90 <= latitude <= +90).
float64 latitude

# Longitude [degrees]. Positive is east of prime meridian; negative is
# west (-180 <= longitude <= +180). At the poles, latitude is -90 or
# +90, and longitude is irrelevant, but must be in range.
float64 longitude

# Altitude [m]. Positive is above the WGS 84 ellipsoid (NaN if unspecified).
float64 altitude
"""
import yaml

class GeoPoint:
    """
    # Geographic point, using the WGS 84 reference ellipsoid.
    # Latitude [degrees]. Positive is north of equator; negative is south
    # (-90 <= latitude <= +90).
    float64 latitude
    # Longitude [degrees]. Positive is east of prime meridian; negative is
    # west (-180 <= longitude <= +180). At the poles, latitude is -90 or
    # +90, and longitude is irrelevant, but must be in range.
    float64 longitude
    # Altitude [m]. Positive is above the WGS 84 ellipsoid (NaN if unspecified).
    float64 altitude
    """
    def __init__(self, latitude:float, longitude:float, altitude:float):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude


class MapProjectorInfo:
    """
    # Projector type
    # Also refer to https://github.com/autowarefoundation/autoware.universe/tree/main/map/autoware_map_projection_loader/README.md
    string LOCAL = "local"
    string LOCAL_CARTESIAN_UTM = "LocalCartesianUTM"
    string MGRS = "MGRS"
    string TRANSVERSE_MERCATOR = "TransverseMercator"
    string projector_type
    # Vertical datum
    # Also refer to https://github.com/autowarefoundation/autoware.universe/tree/main/map/autoware_map_projection_loader/README.md
    string WGS84 = "WGS84"
    string EGM2008 = "EGM2008"
    string vertical_datum
    # Used for MGRS map
    string mgrs_grid
    # Used for some map projection types
    # altitude may not be in ellipsoid height
    geographic_msgs/GeoPoint map_origin
    """
    def __init__(self, projector_type:str, vertical_datum:str, mgrs_grid:str, map_origin:GeoPoint=GeoPoint(0, 0, 0)):
        assert projector_type in ["LOCAL", "LOCAL_CARTESIAN_UTM", "MGRS", "TransverseMercator"]
        self.projector_type = projector_type
        self.vertical_datum = vertical_datum
        self.mgrs_grid = mgrs_grid
        self.map_origin = map_origin

def load_info_from_yaml(yaml_path:str):
    with open(yaml_path, "r") as f:
        yaml_dict = yaml.safe_load(f)
    
    assert "projector_type" in yaml_dict
    vertical_datum = yaml_dict.get("vertical_datum", "WGS84")
    mgrs_grid = yaml_dict.get("mgrs_grid", "")
    map_origin = yaml_dict.get("map_origin", None)
    if map_origin is not None:
        map_origin = GeoPoint(map_origin["latitude"], map_origin["longitude"], map_origin["altitude"])
    else:
        map_origin = GeoPoint(0, 0, 0)
    return MapProjectorInfo(yaml_dict["projector_type"], vertical_datum, mgrs_grid, map_origin)
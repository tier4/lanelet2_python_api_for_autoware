"""Utility functions for lanelet2 operations.

This module provides various utility functions for working with lanelets,
including operations for centerline generation, lanelet expansion, and
geometric calculations.
"""

import autoware_lanelet2_extension_python._lanelet2_extension_python_boost_python_utility as _utility_cpp
import lanelet2
import numpy as np

# Direct imports from C++ module
combineLaneletsShape = _utility_cpp.combineLaneletsShape
"""Combines multiple lanelets into a single shape.

Args:
    lanelets (list): List of lanelets to combine.

Returns:
    lanelet2.core.CompoundPolygon3d: Combined shape of the lanelets.
"""

generateFineCenterline = _utility_cpp.generateFineCenterline
"""Generates a fine centerline for a lanelet.

Args:
    lanelet (lanelet2.core.Lanelet): The lanelet to generate centerline for.
    resolution (float, optional): Resolution of the centerline. Default is determined by implementation.

Returns:
    lanelet2.core.LineString3d: Generated centerline.
"""

getCenterlineWithOffset = _utility_cpp.getCenterlineWithOffset
"""Gets the centerline of a lanelet with a lateral offset.

Args:
    lanelet (lanelet2.core.Lanelet): The lanelet.
    offset (float): Lateral offset from the centerline.
    resolution (float, optional): Resolution of the centerline. Default is determined by implementation.

Returns:
    lanelet2.core.LineString3d: Centerline with offset.
"""

getRightBoundWithOffset = _utility_cpp.getRightBoundWithOffset
"""Gets the right boundary of a lanelet with a lateral offset.

Args:
    lanelet (lanelet2.core.Lanelet): The lanelet.
    offset (float): Lateral offset from the right boundary.
    resolution (float, optional): Resolution of the boundary. Default is determined by implementation.

Returns:
    lanelet2.core.LineString3d: Right boundary with offset.
"""

getLeftBoundWithOffset = _utility_cpp.getLeftBoundWithOffset
"""Gets the left boundary of a lanelet with a lateral offset.

Args:
    lanelet (lanelet2.core.Lanelet): The lanelet.
    offset (float): Lateral offset from the left boundary.
    resolution (float, optional): Resolution of the boundary. Default is determined by implementation.

Returns:
    lanelet2.core.LineString3d: Left boundary with offset.
"""

getExpandedLanelet = _utility_cpp.getExpandedLanelet
"""Expands a lanelet by a specified width.

Args:
    lanelet (lanelet2.core.Lanelet): The lanelet to expand.
    left_offset (float): Offset to expand the left boundary.
    right_offset (float): Offset to expand the right boundary.

Returns:
    lanelet2.core.Lanelet: Expanded lanelet.
"""

getExpandedLanelets = _utility_cpp.getExpandedLanelets
"""Expands multiple lanelets by a specified width.

Args:
    lanelets (list): List of lanelets to expand.
    left_offset (float): Offset to expand the left boundary.
    right_offset (float): Offset to expand the right boundary.

Returns:
    list: List of expanded lanelets.
"""

overwriteLaneletsCenterline = _utility_cpp.overwriteLaneletsCenterline
"""Overwrites the centerline of lanelets.

Args:
    lanelets (list): List of lanelets to overwrite centerlines.
    resolution (float, optional): Resolution of the centerline. Default is determined by implementation.
    force_overwrite (bool, optional): Whether to force overwrite existing centerlines. Default is false.

Returns:
    None
"""

getConflictingLanelets = _utility_cpp.getConflictingLanelets
"""Gets conflicting lanelets for a lanelet.

Args:
    lanelet (lanelet2.core.Lanelet): The lanelet to check conflicts for.
    lanelets (list): List of lanelets to check against.

Returns:
    list: List of conflicting lanelets.
"""

lineStringWithWidthToPolygon = _utility_cpp.lineStringWithWidthToPolygon
"""Converts a linestring with width attribute to a polygon.

Args:
    linestring (lanelet2.core.LineString3d): The linestring to convert.

Returns:
    Optional[lanelet2.core.Polygon3d]: Resulting polygon, or None if conversion failed.
"""

lineStringToPolygon = _utility_cpp.lineStringToPolygon
"""Converts a linestring to a polygon.

Args:
    linestring (lanelet2.core.LineString3d): The linestring to convert.

Returns:
    Optional[lanelet2.core.Polygon3d]: Resulting polygon, or None if conversion failed.
"""


def getLaneletLength2d(*args):
    """Gets the 2D length of a lanelet or sequence of lanelets.

    Args:
        args: Either a single lanelet or a list of lanelets.

    Returns:
        float: 2D length of the lanelet(s).

    Raises:
        TypeError: If arguments don't match expected types.
    """
    if len(args) == 1 and isinstance(args[0], lanelet2.core.Lanelet):
        return _utility_cpp.getLaneletLength2d(args[0])
    if len(args) == 1 and isinstance(args[0], list):
        return _utility_cpp.getLaneletLength2d(args[0])
    raise TypeError(
        "argument number does not match or 1st argument is not Lanelet or [Lanelet] type"
    )


def getLaneletLength3d(*args):
    """Gets the 3D length of a lanelet or sequence of lanelets.

    Args:
        args: Either a single lanelet or a list of lanelets.

    Returns:
        float: 3D length of the lanelet(s).

    Raises:
        TypeError: If arguments don't match expected types.
    """
    if len(args) == 1 and isinstance(args[0], lanelet2.core.Lanelet):
        return _utility_cpp.getLaneletLength3d(args[0])
    if len(args) == 1 and isinstance(args[0], list):
        return _utility_cpp.getLaneletLength3d(args[0])
    raise TypeError(
        "argument number does not match or 1st argument is not Lanelet or [Lanelet] type"
    )


def getArcCoordinates(lanelet_sequence, pose: np.ndarray):
    """Gets arc coordinates for a pose within a lanelet sequence.

    Args:
        lanelet_sequence: Sequence of lanelets
        pose: numpy array [x, y, z, yaw] representing position and orientation

    Returns:
        lanelet2.core.ArcCoordinates: Arc coordinates of the pose.
    """
    return _utility_cpp.getArcCoordinates(lanelet_sequence, np.array(pose, dtype=np.double).tobytes())


getClosestSegment = _utility_cpp.getClosestSegment
"""Gets the closest segment in a linestring to a point.

Args:
    linestring (lanelet2.core.LineString3d): The linestring to search in.
    point (lanelet2.core.BasicPoint2d): The point to find closest segment to.

Returns:
    tuple: Tuple containing (segment_idx, segment_ratio).
"""

getPolygonFromArcLength = _utility_cpp.getPolygonFromArcLength
"""Gets a polygon from a lanelet at a specific arc length.

Args:
    lanelet (lanelet2.core.Lanelet): The lanelet.
    s_start (float): Start arc length.
    s_end (float): End arc length.

Returns:
    lanelet2.core.CompoundPolygon3d: Polygon representing the lanelet section.
"""


def getLaneletAngle(lanelet, point: np.ndarray):
    """Gets the angle of a lanelet at a specific point.

    Args:
        lanelet: Lanelet object
        point: numpy array [x, y, z] representing 3D point

    Returns:
        float: Angle of the lanelet at the point (radians).
    """
    return _utility_cpp.getLaneletAngle(lanelet, np.array(point, dtype=np.double).tobytes())


def isInLanelet(pose, lanelet, radius=0.0):
    """Checks if a pose is within a lanelet.

    Args:
        pose: numpy array [x, y, z, yaw] representing position and orientation
        lanelet: Lanelet object
        radius: float, optional radius to expand the lanelet check

    Returns:
        bool: True if the pose is in the lanelet, False otherwise.
    """
    return _utility_cpp.isInLanelet(np.array(pose, dtype=np.double).tobytes(), lanelet, radius)


def getClosestCenterPose(lanelet, point: np.ndarray):
    """Gets the closest pose on the centerline of a lanelet to a point.

    Args:
        lanelet: Lanelet object
        point: numpy array [x, y, z] representing 3D point

    Returns:
        numpy array [x, y, z, yaw] representing position and orientation
    """
    pose_array = _utility_cpp.getClosestCenterPose(lanelet, np.array(point, dtype=np.double).tobytes())
    return np.array(pose_array)  # Returns [x, y, z, yaw]


def getLateralDistanceToCenterline(lanelet, pose):
    """Gets the lateral distance from a pose to the centerline of a lanelet.

    Args:
        lanelet: Lanelet object
        pose: numpy array [x, y, z, yaw] representing position and orientation

    Returns:
        float: Lateral distance to the centerline.
    """
    return _utility_cpp.getLateralDistanceToCenterline(lanelet, np.array(pose, dtype=np.double).tobytes())


def getLateralDistanceToClosestLanelet(lanelet_sequence, pose):
    """Gets the lateral distance from a pose to the closest lanelet in a sequence.

    Args:
        lanelet_sequence: Sequence of lanelets
        pose: numpy array [x, y, z, yaw] representing position and orientation

    Returns:
        float: Lateral distance to the closest lanelet.
    """
    return _utility_cpp.getLateralDistanceToClosestLanelet(lanelet_sequence, np.array(pose, dtype=np.double).tobytes())
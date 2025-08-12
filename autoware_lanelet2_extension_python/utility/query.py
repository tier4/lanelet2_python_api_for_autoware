import autoware_lanelet2_extension_python._lanelet2_extension_python_boost_python_utility as _utility_cpp
import lanelet2.core
import numpy as np

# from rclpy.serialization import deserialize_message

laneletLayer = _utility_cpp.laneletLayer
subtypeLanelets = _utility_cpp.subtypeLanelets
crosswalkLanelets = _utility_cpp.crosswalkLanelets
walkwayLanelets = _utility_cpp.walkwayLanelets
roadLanelets = _utility_cpp.roadLanelets
shoulderLanelets = _utility_cpp.shoulderLanelets
trafficLights = _utility_cpp.trafficLights
autowareTrafficLights = _utility_cpp.autowareTrafficLights
detectionAreas = _utility_cpp.detectionAreas
noStoppingAreas = _utility_cpp.noStoppingAreas
noParkingAreas = _utility_cpp.noParkingAreas
speedBumps = _utility_cpp.speedBumps
crosswalks = _utility_cpp.crosswalks
curbstones = _utility_cpp.curbstones
getAllPolygonsByType = _utility_cpp.getAllPolygonsByType
getAllObstaclePolygons = _utility_cpp.getAllObstaclePolygons
getAllParkingLots = _utility_cpp.getAllParkingLots
getAllPartitions = _utility_cpp.getAllPartitions
getAllFences = _utility_cpp.getAllFences
getAllPedestrianPolygonMarkings = _utility_cpp.getAllPedestrianPolygonMarkings
getAllPedestrianLineMarkings = _utility_cpp.getAllPedestrianLineMarkings
getAllParkingSpaces = _utility_cpp.getAllParkingSpaces
getLinkedParkingSpaces = _utility_cpp.getLinkedParkingSpaces
getLinkedLanelet = _utility_cpp.getLinkedLanelet
getLinkedLanelets = _utility_cpp.getLinkedLanelets
getLinkedParkingLot = _utility_cpp.getLinkedParkingLot
stopLinesLanelets = _utility_cpp.stopLinesLanelets
stopLinesLanelet = _utility_cpp.stopLinesLanelet
stopSignStopLines = _utility_cpp.stopSignStopLines


def getLaneletsWithinRange(lanelets, point, rng):
    """Get lanelets within range of a point.

    Args:
        lanelets: List of lanelets to search
        point: Either lanelet2.core.BasicPoint2d or numpy array [x,y,z]
        rng: Search radius
    """
    rng = float(rng)
    if isinstance(point, np.ndarray):
        return _utility_cpp.getLaneletsWithinRange_point(lanelets, np.array(point, dtype=np.double).tobytes(), rng)
    if isinstance(point, lanelet2.core.BasicPoint2d):
        return _utility_cpp.getLaneletsWithinRange(lanelets, point, rng)
    raise TypeError("argument point must be numpy array or BasicPoint2d")


def getLaneChangeableNeighbors(*args):
    """Get lane-changeable neighbor lanelets.

    Args:
        graph: Routing graph
        lanelet: Target lanelet
        point: (Optional) numpy array [x,y,z] to search from
    """
    if len(args) == 2 and isinstance(args[1], lanelet2.core.Lanelet):
        return _utility_cpp.getLaneChangeableNeighbors(args[0], args[1])
    if len(args) == 3 and isinstance(args[2], np.ndarray):
        return _utility_cpp.getLaneChangeableNeighbors_point(args[0], args[1], np.array(args[2], dtype=np.double).tobytes())
    raise TypeError("Invalid arguments")


def getAllNeighbors(*args):
    """Get all neighbor lanelets.

    Args:
        graph: Routing graph
        lanelet: Target lanelet
        point: (Optional) numpy array [x,y,z] to search from
    """
    if len(args) == 2 and isinstance(args[1], lanelet2.core.Lanelet):
        return _utility_cpp.getAllNeighbors(args[0], args[1])
    if len(args) == 3 and isinstance(args[2], np.ndarray):
        return _utility_cpp.getAllNeighbors_point(args[0], args[1], np.array(args[2], dtype=np.double).tobytes())
    raise TypeError("Invalid arguments")


getAllNeighborsLeft = _utility_cpp.getAllNeighborsLeft
getAllNeighborsRight = _utility_cpp.getAllNeighborsRight


def getClosestLanelet(lanelets, pose):
    """Get closest lanelet to pose.

    Args:
        lanelets: List of lanelets to search
        pose: numpy array [x,y,z,yaw]
    """
    return _utility_cpp.getClosestLanelet(lanelets, np.array(pose, dtype=np.double).tobytes())


def getClosestLaneletWithConstrains(lanelets, pose, closest_lanelet, dist_threshold, yaw_threshold):
    """Get closest lanelet with distance and yaw constraints.

    Args:
        lanelets: List of lanelets to search
        pose: numpy array [x,y,z,yaw]
        closest_lanelet: Reference lanelet
        dist_threshold: Maximum allowed distance
        yaw_threshold: Maximum allowed yaw difference
    """
    return _utility_cpp.getClosestLaneletWithConstrains_point(
        lanelets, np.array(pose, dtype=np.double).tobytes(), closest_lanelet, dist_threshold, yaw_threshold
    )


def getCurrentLanelets(lanelets, point_or_pose):
    """Get current lanelets containing point/pose.

    Args:
        lanelets: List of lanelets to search
        point_or_pose: numpy array [x,y,z] or [x,y,z,yaw]
    """
    if len(point_or_pose) == 3:
        return _utility_cpp.getCurrentLanelets_point(lanelets, np.array(point_or_pose, dtype=np.double).tobytes())
    if len(point_or_pose) == 4:
        return _utility_cpp.getCurrentLanelets_pose(lanelets, np.array(point_or_pose, dtype=np.double).tobytes())
    raise TypeError("point_or_pose must be [x,y] or [x,y,z,yaw] numpy array")


getSucceedingLaneletSequences = _utility_cpp.getSucceedingLaneletSequences
getPrecedingLaneletSequences = _utility_cpp.getPrecedingLaneletSequences

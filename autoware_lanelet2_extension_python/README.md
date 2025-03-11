# Autoware Lanelet2 Extension Python

Python bindings for the Autoware Lanelet2 extension library, providing enhanced functionality for handling HD maps in autonomous driving applications.

## Features

The library provides Python bindings in three main categories:

### 1. Regulatory Elements

Provides access to various regulatory elements used in Autoware's HD maps:

```python
from autoware_lanelet2_extension_python.regulatory_elements import (
    AutowareTrafficLight,
    Crosswalk,
    DetectionArea,
    NoParkingArea,
    NoStoppingArea,
    RoadMarking,
    SpeedBump,
    VirtualTrafficLight
)
```

### 2. Projection

Provides specialized map projections:

```python
from autoware_lanelet2_extension_python.projection import MGRSProjector
```

### 3. Utility Functions

#### Map Element Queries
```python
from autoware_lanelet2_extension_python.utility.query import (
    # Layer access
    laneletLayer,
    
    # Lanelet type queries
    subtypeLanelets,
    crosswalkLanelets,
    walkwayLanelets,
    roadLanelets,
    shoulderLanelets,
    
    # Regulatory element queries
    trafficLights,
    autowareTrafficLights,
    detectionAreas,
    noStoppingAreas,
    noParkingAreas,
    speedBumps,
    crosswalks,
    
    # Map element queries
    curbstones,
    getAllPolygonsByType,
    getAllObstaclePolygons,
    getAllParkingLots,
    getAllPartitions,
    getAllFences,
    getAllPedestrianPolygonMarkings,
    getAllPedestrianLineMarkings,
    getAllParkingSpaces
)
```

#### Spatial Queries

```python
# Get lanelets within range of a point
getLaneletsWithinRange(lanelets, point, range)
    """
    Args:
        lanelets: List of lanelets to search
        point: Either lanelet2.core.BasicPoint2d or numpy array [x,y,z]
        range: Search radius
    """

# Get closest lanelet
getClosestLanelet(lanelets, pose)
    """
    Args:
        lanelets: List of lanelets to search
        pose: numpy array [x,y,z,yaw]
    """

# Get current lanelets containing a point/pose
getCurrentLanelets(lanelets, point_or_pose)
    """
    Args:
        lanelets: List of lanelets to search
        point_or_pose: numpy array [x,y,z] or [x,y,z,yaw]
    """
```

#### Routing and Neighbor Queries

```python
# Get lane-changeable neighbors
getLaneChangeableNeighbors(graph, lanelet, [point])
    """
    Args:
        graph: Routing graph
        lanelet: Target lanelet
        point: (Optional) numpy array [x,y,z] to search from
    """

# Get all neighbors
getAllNeighbors(graph, lanelet, [point])
getAllNeighborsLeft(graph, lanelet)
getAllNeighborsRight(graph, lanelet)

# Get lanelet sequences
getSucceedingLaneletSequences(graph, lanelet, max_length=10, routing_cost_id=0)
    """
    Retrieves sequences of lanelets that follow the given lanelet in the routing graph.
    
    Args:
        graph: Routing graph
        lanelet: Starting lanelet
        max_length: Maximum number of lanelets in each sequence
        routing_cost_id: ID of the routing cost to use
    
    Returns:
        List of lanelet sequences (each sequence is a list of lanelets)
    """

getPrecedingLaneletSequences(graph, lanelet, max_length=10, routing_cost_id=0)
    """
    Retrieves sequences of lanelets that precede the given lanelet in the routing graph.
    
    Args:
        graph: Routing graph
        lanelet: Target lanelet
        max_length: Maximum number of lanelets in each sequence
        routing_cost_id: ID of the routing cost to use
    
    Returns:
        List of lanelet sequences (each sequence is a list of lanelets)
    """
```

#### Linking Queries

```python
getLinkedParkingSpaces(lanelet, lanelet_map_ptr)
    """
    Gets all parking spaces linked to the given lanelet.
    
    Args:
        lanelet: Target lanelet
        lanelet_map_ptr: Lanelet map pointer
    
    Returns:
        List of LineString3d representing parking spaces
    """

getLinkedLanelet(parking_space, lanelet_map_ptr)
    """
    Gets the lanelet linked to the given parking space.
    
    Args:
        parking_space: LineString3d representing a parking space
        lanelet_map_ptr: Lanelet map pointer
    
    Returns:
        The linked lanelet if found, None otherwise
    """

getLinkedLanelets(parking_space, lanelet_map_ptr)
    """
    Gets all lanelets linked to the given parking space.
    
    Args:
        parking_space: LineString3d representing a parking space
        lanelet_map_ptr: Lanelet map pointer
    
    Returns:
        List of lanelets linked to the parking space
    """

getLinkedParkingLot(parking_space, lanelet_map_ptr)
    """
    Gets the parking lot containing the given parking space.
    
    Args:
        parking_space: LineString3d representing a parking space
        lanelet_map_ptr: Lanelet map pointer
    
    Returns:
        The linked parking lot if found, None otherwise
    """
```

#### Stop Line Queries

```python
stopLinesLanelets(lanelet_map_ptr)
    """
    Gets all stop lines in the map with their associated lanelets.
    
    Args:
        lanelet_map_ptr: Lanelet map pointer
    
    Returns:
        Dictionary mapping stop lines (LineString3d) to lists of lanelets
    """

stopLinesLanelet(lanelet, lanelet_map_ptr)
    """
    Gets all stop lines associated with the given lanelet.
    
    Args:
        lanelet: Target lanelet
        lanelet_map_ptr: Lanelet map pointer
    
    Returns:
        List of stop lines (LineString3d) for the lanelet
    """

stopSignStopLines(lanelet_map_ptr)
    """
    Gets all stop lines associated with stop signs.
    
    Args:
        lanelet_map_ptr: Lanelet map pointer
    
    Returns:
        List of stop lines (LineString3d) for stop signs
    """
```

## Installation

The package can be installed through your ROS workspace:

```bash
cd <your_workspace>
colcon build --packages-select autoware_lanelet2_extension_python
```

## Dependencies

As listed in package.xml:
- lanelet2_core
- lanelet2_extension
- lanelet2_io
- lanelet2_projection
- lanelet2_python
- lanelet2_routing
- lanelet2_traffic_rules
- lanelet2_validation
- libboost-python-dev

## License

Apache License 2.0

## Maintainers

- Mamoru Sobue (<mamoru.sobue@tier4.jp>)
- Yutaka Kondo (<yutaka.kondo@tier4.jp>)
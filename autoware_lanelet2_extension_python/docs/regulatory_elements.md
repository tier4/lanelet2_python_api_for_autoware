# Autoware Lanelet2 Extension Python - Regulatory Elements

This document provides documentation for the regulatory elements available in the Autoware Lanelet2 Extension Python module.

## AutowareTrafficLight

A specialized traffic light regulatory element that includes light bulbs information.

### Constructor

```python
AutowareTrafficLight(Id, attributes, trafficLights, stopline=None, lightBulbs=[])
```

**Parameters:**
- `Id`: Unique identifier for the regulatory element
- `attributes`: Dictionary of attributes for the regulatory element
- `trafficLights`: List of traffic light linestrings
- `stopline`: Optional linestring representing the stop line
- `lightBulbs`: Optional linestring representing the light bulbs

### Methods

- `lightBulbs()`: Returns the light bulbs linestring
- `addLightBulbs(light_bulbs)`: Add light bulbs to the traffic light
- `removeLightBulbs()`: Remove light bulbs from the traffic light

## Crosswalk

A regulatory element representing a crosswalk.

### Constructor

```python
Crosswalk(Id, attributes, crosswalk_lanelet, crosswalk_area, stop_line)
```

**Parameters:**
- `Id`: Unique identifier for the regulatory element
- `attributes`: Dictionary of attributes for the regulatory element
- `crosswalk_lanelet`: Lanelet representing the crosswalk
- `crosswalk_area`: Area representing the crosswalk
- `stop_line`: Linestring representing the stop line

### Methods

- `crosswalkAreas()`: Returns the crosswalk areas
- `stopLines()`: Returns the stop lines
- `crosswalkLanelet()`: Returns the crosswalk lanelet
- `addCrosswalkArea(area)`: Add a crosswalk area
- `removeCrosswalkArea(area)`: Remove a crosswalk area

## DetectionArea

A regulatory element representing a detection area.

### Constructor

```python
DetectionArea(Id, attributes, detectionAreas, stopLine)
```

**Parameters:**
- `Id`: Unique identifier for the regulatory element
- `attributes`: Dictionary of attributes for the regulatory element
- `detectionAreas`: List of areas representing detection areas
- `stopLine`: Linestring representing the stop line

### Methods

- `detectionAreas()`: Returns the detection areas
- `addDetectionArea(area)`: Add a detection area
- `removeDetectionArea(area)`: Remove a detection area
- `stopLine()`: Returns the stop line
- `setStopLine(line)`: Set the stop line
- `removeStopLine()`: Remove the stop line

## NoParkingArea

A regulatory element representing an area where parking is prohibited.

### Constructor

```python
NoParkingArea(Id, attributes, no_parking_areas)
```

**Parameters:**
- `Id`: Unique identifier for the regulatory element
- `attributes`: Dictionary of attributes for the regulatory element
- `no_parking_areas`: List of areas where parking is prohibited

### Methods

- `noParkingAreas()`: Returns the no parking areas
- `addNoParkingArea(area)`: Add a no parking area
- `removeNoParkingArea(area)`: Remove a no parking area

## NoStoppingArea

A regulatory element representing an area where stopping is prohibited.

### Constructor

```python
NoStoppingArea(Id, attributes, no_stopping_areas, stopLine=None)
```

**Parameters:**
- `Id`: Unique identifier for the regulatory element
- `attributes`: Dictionary of attributes for the regulatory element
- `no_stopping_areas`: List of areas where stopping is prohibited
- `stopLine`: Optional linestring representing the stop line

### Methods

- `noStoppingAreas()`: Returns the no stopping areas
- `addNoStoppingArea(area)`: Add a no stopping area
- `removeNoStoppingArea(area)`: Remove a no stopping area
- `stopLine()`: Returns the stop line
- `setStopLine(line)`: Set the stop line
- `removeStopLine()`: Remove the stop line

## RoadMarking

A regulatory element representing a road marking.

### Constructor

```python
RoadMarking(Id, attributes, road_marking)
```

**Parameters:**
- `Id`: Unique identifier for the regulatory element
- `attributes`: Dictionary of attributes for the regulatory element
- `road_marking`: Linestring representing the road marking

### Methods

- `roadMarking()`: Returns the road marking
- `setRoadMarking(marking)`: Set the road marking
- `removeRoadMarking()`: Remove the road marking

## SpeedBump

A regulatory element representing a speed bump.

### Constructor

```python
SpeedBump(Id, attributes, speed_bump)
```

**Parameters:**
- `Id`: Unique identifier for the regulatory element
- `attributes`: Dictionary of attributes for the regulatory element
- `speed_bump`: Linestring representing the speed bump

### Methods

- `speedBump()`: Returns the speed bump
- `addSpeedBump(bump)`: Add a speed bump
- `removeSpeedBump(bump)`: Remove a speed bump

## VirtualTrafficLight

A regulatory element representing a virtual traffic light.

### Constructor

```python
VirtualTrafficLight(Id, attributes, virtual_traffic_light)
```

**Parameters:**
- `Id`: Unique identifier for the regulatory element
- `attributes`: Dictionary of attributes for the regulatory element
- `virtual_traffic_light`: Linestring representing the virtual traffic light

### Methods

- `getVirtualTrafficLight()`: Returns the virtual traffic light
- `getStopLine()`: Returns the stop line
- `getStartLine()`: Returns the start line
- `getEndLines()`: Returns the end lines

## Usage Example

```python
import lanelet2
from lanelet2.core import AttributeMap, LineString3d, Point3d
from lanelet2_extension_python import AutowareTrafficLight, Crosswalk

# Create a traffic light
attrs = AttributeMap({"type": "traffic_light"})
points = [Point3d(0, 0, 0), Point3d(1, 0, 0), Point3d(2, 0, 0)]
traffic_light_ls = LineString3d(1, points)
light_bulbs = LineString3d(2, [Point3d(0.5, 0, 0), Point3d(1.5, 0, 0)])

traffic_light = AutowareTrafficLight(
    100,                   # Id
    AttributeMap(),        # attributes
    [traffic_light_ls],    # trafficLights
    None,                  # stopline
    light_bulbs            # lightBulbs
)

# Access light bulbs
bulbs = traffic_light.lightBulbs()
```

## Notes

- All regulatory elements are derived from the base `RegulatoryElement` class in lanelet2
- These classes provide Python bindings to the C++ implementation in the lanelet2_extension library
- All regulatory elements can be implicitly converted to `RegulatoryElementPtr`
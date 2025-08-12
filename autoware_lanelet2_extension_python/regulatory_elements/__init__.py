"""
Regulatory elements for Autoware's lanelet2 extension.

This module provides Python bindings for Autoware's custom regulatory elements
that extend the lanelet2 map representation capabilities.
"""

import autoware_lanelet2_extension_python._lanelet2_extension_python_boost_python_regulatory_elements as _regulatory_elements_cpp

AutowareTrafficLight = _regulatory_elements_cpp.AutowareTrafficLight
"""Autoware traffic light regulatory element.
    
This class represents a traffic light in Autoware with additional
capabilities for light bulb information.

Methods:
    lightBulbs(): Get the light bulbs LineString3d
    addLightBulbs(light_bulbs: LineString3d): Add light bulbs
    removeLightBulbs(light_bulbs: LineString3d): Remove light bulbs
"""
Crosswalk = _regulatory_elements_cpp.Crosswalk
"""Autoware crosswalk regulatory element.

This class represents a crosswalk area in Autoware.

Methods:
    crosswalkAreas(): Get the crosswalk areas (list of Polygon3d)
    stopLines(): Get the stop lines (list of LineString3d)
    crosswalkLanelet(): Get the crosswalk lanelet (Lanelet)
    addCrosswalkArea(area: Polygon3d): Add a crosswalk area
    removeCrosswalkArea(area: Polygon3d): Remove a crosswalk area
"""
DetectionArea = _regulatory_elements_cpp.DetectionArea
"""Detection area regulatory element.

This class represents an area where detection of objects is important.

Methods:
    detectionAreas(): Get the detection areas (list of Polygon3d)
    addDetectionArea(area: Polygon3d): Add a detection area
    removeDetectionArea(area: Polygon3d): Remove a detection area
    stopLine(): Get the stop line (Optional[LineString3d])
    setStopLine(line: LineString3d): Set the stop line
    removeStopLine(): Remove the stop line
"""
NoParkingArea = _regulatory_elements_cpp.NoParkingArea
"""No parking area regulatory element.

This class represents an area where parking is prohibited.

Methods:
    noParkingAreas(): Get the no parking areas (list of Polygon3d)
    addNoParkingArea(area: Polygon3d): Add a no parking area
    removeNoParkingArea(area: Polygon3d): Remove a no parking area
"""

NoStoppingArea = _regulatory_elements_cpp.NoStoppingArea
"""No stopping area regulatory element.

This class represents an area where stopping is prohibited.

Methods:
    noStoppingAreas(): Get the no stopping areas (list of Polygon3d)
    addNoStoppingArea(area: Polygon3d): Add a no stopping area
    removeNoStoppingArea(area: Polygon3d): Remove a no stopping area
    stopLine(): Get the stop line (Optional[LineString3d])
    setStopLine(line: LineString3d): Set the stop line
    removeStopLine(): Remove the stop line
"""




RoadMarking = _regulatory_elements_cpp.RoadMarking
"""Road marking regulatory element.

This class represents a road marking in Autoware.

Methods:
    roadMarking(): Get the road marking (LineString3d)
    setRoadMarking(marking: LineString3d): Set the road marking
    removeRoadMarking(): Remove the road marking
"""

SpeedBump = _regulatory_elements_cpp.SpeedBump
"""Speed bump regulatory element.

This class represents a speed bump in Autoware.

Methods:
    speedBump(): Get the speed bump (LineString3d)
    addSpeedBump(bump: LineString3d): Add a speed bump
    removeSpeedBump(bump: LineString3d): Remove a speed bump
"""

VirtualTrafficLight = _regulatory_elements_cpp.VirtualTrafficLight
"""Virtual traffic light regulatory element.

This class represents a virtual traffic light in Autoware.

Methods:
    getVirtualTrafficLight(): Get the virtual traffic light (Point3d)
    getStopLine(): Get the stop line (LineString3d)
    getStartLine(): Get the start line (LineString3d)
    getEndLines(): Get the end lines (list of LineString3d)
"""
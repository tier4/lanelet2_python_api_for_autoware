"""
Regulatory elements for Lanelet2 with Autoware extension
Pure Python implementation
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AutowareTrafficLight:
    """
    Autoware traffic light regulatory element.
    """
    id: int = 0
    type: str = "traffic_light"
    subtype: str = "autoware"
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

@dataclass
class BusStopArea:
    """
    Bus stop area regulatory element.
    """
    id: int = 0
    type: str = "bus_stop"
    name: str = ""
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

@dataclass 
class Crosswalk:
    """
    Crosswalk regulatory element.
    """
    id: int = 0
    type: str = "crosswalk"
    subtype: str = "zebra"
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

@dataclass
class DetectionArea:
    """
    Detection area regulatory element.
    """
    id: int = 0
    type: str = "detection_area"
    subtype: str = ""
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

@dataclass
class NoParkingArea:
    """
    No parking area regulatory element.
    """
    id: int = 0
    type: str = "no_parking"
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

@dataclass
class NoStoppingArea:
    """
    No stopping area regulatory element.
    """
    id: int = 0
    type: str = "no_stopping"
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

@dataclass
class RoadMarking:
    """
    Road marking regulatory element.
    """
    id: int = 0
    type: str = "road_marking"
    subtype: str = ""
    color: str = "white"
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

@dataclass
class SpeedBump:
    """
    Speed bump regulatory element.
    """
    id: int = 0
    type: str = "speed_bump"
    height: float = 0.1
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

@dataclass
class VirtualTrafficLight:
    """
    Virtual traffic light regulatory element.
    """
    id: int = 0
    type: str = "virtual_traffic_light"
    attributes: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}

__all__ = [
    "AutowareTrafficLight",
    "BusStopArea", 
    "Crosswalk",
    "DetectionArea",
    "NoParkingArea",
    "NoStoppingArea",
    "RoadMarking",
    "SpeedBump",
    "VirtualTrafficLight"
]
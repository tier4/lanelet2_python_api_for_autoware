"""
Python API for lanelet2_extension for Autoware
Pure Python implementation for pip install compatibility
"""

__version__ = "0.1.0"

# Import submodules
from . import projection
from . import regulatory_elements
from . import utility

# Make key classes available at package level
from .projection import MGRSProjector, TransverseMercatorProjector
from .regulatory_elements import (
    AutowareTrafficLight,
    BusStopArea, 
    Crosswalk,
    DetectionArea,
    NoParkingArea,
    NoStoppingArea,
    RoadMarking,
    SpeedBump,
    VirtualTrafficLight
)

__all__ = [
    "projection", 
    "regulatory_elements",
    "utility",
    "MGRSProjector",
    "TransverseMercatorProjector",
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
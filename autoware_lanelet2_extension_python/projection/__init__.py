"""
Projection utilities for Lanelet2 with Autoware extension
Pure Python implementation
"""

import numpy as np
from typing import Tuple, Optional
import math

class MGRSProjector:
    """
    Military Grid Reference System (MGRS) projector.
    Pure Python implementation for basic functionality.
    """
    
    def __init__(self, mgrs_grid: str):
        """
        Initialize MGRS projector with grid specification.
        
        Args:
            mgrs_grid: MGRS grid string (e.g., "54SUE")
        """
        self.mgrs_grid = mgrs_grid
        # Parse MGRS grid for basic info
        self.zone = int(mgrs_grid[:2])
        self.band = mgrs_grid[2]
        self.square = mgrs_grid[3:5] if len(mgrs_grid) >= 5 else ""
        
    def forward(self, lat: float, lon: float) -> Tuple[float, float]:
        """
        Convert from latitude/longitude to projected coordinates.
        
        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees
            
        Returns:
            Tuple of (x, y) projected coordinates
        """
        # Simple UTM-like projection for demonstration
        # This is a simplified implementation
        x = (lon + 180) * 111320 * math.cos(math.radians(lat))
        y = lat * 110540
        return (x, y)
        
    def reverse(self, x: float, y: float) -> Tuple[float, float]:
        """
        Convert from projected coordinates to latitude/longitude.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Tuple of (lat, lon) in degrees
        """
        # Simple reverse projection
        lat = y / 110540
        lon = x / (111320 * math.cos(math.radians(lat))) - 180
        return (lat, lon)

class TransverseMercatorProjector:
    """
    Transverse Mercator projector.
    Pure Python implementation for basic functionality.
    """
    
    def __init__(self, origin_lat: float, origin_lon: float):
        """
        Initialize Transverse Mercator projector.
        
        Args:
            origin_lat: Origin latitude in degrees
            origin_lon: Origin longitude in degrees
        """
        self.origin_lat = math.radians(origin_lat)
        self.origin_lon = math.radians(origin_lon)
        
    def forward(self, lat: float, lon: float) -> Tuple[float, float]:
        """
        Convert from latitude/longitude to projected coordinates.
        
        Args:
            lat: Latitude in degrees
            lon: Longitude in degrees
            
        Returns:
            Tuple of (x, y) projected coordinates
        """
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        
        # Simplified Transverse Mercator projection
        dlon = lon_rad - self.origin_lon
        
        x = 6378137.0 * dlon * math.cos(self.origin_lat)
        y = 6378137.0 * (lat_rad - self.origin_lat)
        
        return (x, y)
        
    def reverse(self, x: float, y: float) -> Tuple[float, float]:
        """
        Convert from projected coordinates to latitude/longitude.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            Tuple of (lat, lon) in degrees
        """
        lat_rad = self.origin_lat + y / 6378137.0
        lon_rad = self.origin_lon + x / (6378137.0 * math.cos(self.origin_lat))
        
        return (math.degrees(lat_rad), math.degrees(lon_rad))

__all__ = [
    "MGRSProjector",
    "TransverseMercatorProjector"
]

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
    
    def __init__(self, origin_or_grid):
        """
        Initialize MGRS projector with origin or grid specification.
        
        Args:
            origin_or_grid: Either a lanelet2.io.Origin object or MGRS grid string (e.g., "54SUE")
        """
        # Handle both Origin objects and string inputs for compatibility
        if hasattr(origin_or_grid, 'lat') and hasattr(origin_or_grid, 'lon'):
            # This is an Origin object - convert to MGRS grid
            lat = origin_or_grid.lat
            lon = origin_or_grid.lon
            self.origin_lat = lat
            self.origin_lon = lon
            # Convert lat/lon to MGRS grid (simplified)
            zone = int((lon + 180) / 6) + 1
            if zone > 60:
                zone = 60
            self.mgrs_grid = f"{zone:02d}SUE"  # Simplified MGRS grid
        else:
            # This is a string grid specification
            self.mgrs_grid = str(origin_or_grid)
            # Default origin for string-based initialization
            self.origin_lat = 0.0
            self.origin_lon = 0.0
            
        # Parse MGRS grid for basic info
        if len(self.mgrs_grid) >= 2 and self.mgrs_grid[:2].isdigit():
            self.zone = int(self.mgrs_grid[:2])
            self.band = self.mgrs_grid[2] if len(self.mgrs_grid) > 2 else 'S'
            self.square = self.mgrs_grid[3:5] if len(self.mgrs_grid) >= 5 else "UE"
        else:
            # Fallback for invalid grid strings
            self.zone = 1
            self.band = 'S'
            self.square = "UE"
        
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
    
    def __init__(self, origin_or_lat, origin_lon=None):
        """
        Initialize Transverse Mercator projector.
        
        Args:
            origin_or_lat: Either a lanelet2.io.Origin object or latitude in degrees
            origin_lon: Longitude in degrees (if first arg is latitude)
        """
        # Handle both Origin objects and separate lat/lon arguments
        if hasattr(origin_or_lat, 'lat') and hasattr(origin_or_lat, 'lon'):
            # This is an Origin object
            self.origin_lat = math.radians(origin_or_lat.lat)
            self.origin_lon = math.radians(origin_or_lat.lon)
        else:
            # These are separate lat/lon arguments
            self.origin_lat = math.radians(float(origin_or_lat))
            self.origin_lon = math.radians(float(origin_lon))
        
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

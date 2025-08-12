"""
Utility functions for Lanelet2 with Autoware extension
Pure Python implementation
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points.
    
    Args:
        point1: First point as (x, y) tuple
        point2: Second point as (x, y) tuple
        
    Returns:
        Distance between the points
    """
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return np.sqrt(dx*dx + dy*dy)

def calculate_bearing(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate bearing from point1 to point2.
    
    Args:
        point1: Starting point as (x, y) tuple
        point2: End point as (x, y) tuple
        
    Returns:
        Bearing in radians
    """
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return np.arctan2(dy, dx)

def interpolate_points(point1: Tuple[float, float], point2: Tuple[float, float], ratio: float) -> Tuple[float, float]:
    """
    Interpolate between two points.
    
    Args:
        point1: First point as (x, y) tuple
        point2: Second point as (x, y) tuple
        ratio: Interpolation ratio (0.0 = point1, 1.0 = point2)
        
    Returns:
        Interpolated point as (x, y) tuple
    """
    x = point1[0] + ratio * (point2[0] - point1[0])
    y = point1[1] + ratio * (point2[1] - point1[1])
    return (x, y)

class LaneletUtility:
    """
    Utility class for Lanelet operations.
    """
    
    @staticmethod
    def calculate_lanelet_length(points: List[Tuple[float, float]]) -> float:
        """
        Calculate the length of a lanelet from its centerline points.
        
        Args:
            points: List of (x, y) points representing the centerline
            
        Returns:
            Total length of the lanelet
        """
        if len(points) < 2:
            return 0.0
            
        total_length = 0.0
        for i in range(1, len(points)):
            total_length += calculate_distance(points[i-1], points[i])
        
        return total_length
    
    @staticmethod
    def calculate_lanelet_width(left_points: List[Tuple[float, float]], 
                               right_points: List[Tuple[float, float]]) -> float:
        """
        Calculate average width of a lanelet.
        
        Args:
            left_points: Left boundary points
            right_points: Right boundary points
            
        Returns:
            Average width of the lanelet
        """
        if len(left_points) != len(right_points) or len(left_points) == 0:
            return 0.0
            
        total_width = 0.0
        for left, right in zip(left_points, right_points):
            total_width += calculate_distance(left, right)
            
        return total_width / len(left_points)

__all__ = [
    "calculate_distance",
    "calculate_bearing", 
    "interpolate_points",
    "LaneletUtility"
]
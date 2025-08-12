# Usage Guide: C++ API Compatibility

## Problem
The original C++ code using `MGRSProjector` fails because:
1. `MGRSProjector` is not available in the standard lanelet2 C++ bindings
2. `lanelet2.io.load()` expects either an `Origin` or a standard `Projector`

## Error
```python
# This fails:
return lanelet2.io.load(str(path), MGRSProjector(lanelet2.io.Origin(0.0, 0.0)))
# Error: MGRSProjector is not a valid lanelet::Projector
```

## Solutions

### Option 1: Use Origin directly (Recommended)
```python
import lanelet2_python as lanelet2

def read_lanelet(path):
    return lanelet2.io.load(str(path), lanelet2.io.Origin(0.0, 0.0))
```

### Option 2: Use standard UTM Projector
```python
import lanelet2_python as lanelet2

def read_lanelet(path):
    origin = lanelet2.io.Origin(0.0, 0.0)
    projector = lanelet2.projection.UtmProjector(origin)
    return lanelet2.io.load(str(path), projector)
```

### Option 3: Use default Mercator Projector
```python
import lanelet2_python as lanelet2

def read_lanelet(path):
    return lanelet2.io.load(str(path))  # Uses default MercatorProjector
```

### Option 4: Use our pure Python MGRSProjector (if you need MGRS specifically)
```python
# This works with our pip-installed package
from autoware_lanelet2_extension_python.projection import MGRSProjector
import lanelet2_python as lanelet2

def read_lanelet(path):
    # For our pure Python implementation
    mgrs = MGRSProjector(lanelet2.io.Origin(0.0, 0.0))
    # But you'll need to handle the projection manually
    # since lanelet2.io.load() doesn't accept our Python MGRSProjector
    
    # Use Origin instead:
    return lanelet2.io.load(str(path), lanelet2.io.Origin(0.0, 0.0))
```

## Available C++ Projectors
The following projectors are available in the C++ lanelet2 library:
- `lanelet2.projection.MercatorProjector(origin)`
- `lanelet2.projection.UtmProjector(origin)`
- `lanelet2.projection.GeocentricProjector(origin)`
- `lanelet2.projection.LocalCartesianProjector(origin)`

## Recommended Fix
Replace your original code:
```python
# Before (fails)
def read_lanelet(path):
    return lanelet2.io.load(str(path), MGRSProjector(lanelet2.io.Origin(0.0, 0.0)))

# After (works)
def read_lanelet(path):
    return lanelet2.io.load(str(path), lanelet2.io.Origin(0.0, 0.0))
```
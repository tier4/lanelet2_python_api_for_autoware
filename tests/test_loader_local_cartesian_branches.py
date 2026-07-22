"""Tests for the LOCAL_CARTESIAN_UTM / LOCAL_CARTESIAN branches of
loader.get_lanelet2_projector().

Requires the built C++ extension; skipped automatically when unavailable.
"""
import pytest

lanelet2 = pytest.importorskip("lanelet2")

from map_projector_info import GeoPoint  # noqa: E402
import loader  # noqa: E402


class Info:
    pass


def make_info(projector_type):
    info = Info()
    info.projector_type = projector_type
    info.map_origin = GeoPoint(35.0, 139.0, 0.0)
    info.scale_factor = 0.9996
    return info


def test_local_cartesian_utm_returns_utm_projector():
    projector = loader.get_lanelet2_projector(make_info("LOCAL_CARTESIAN_UTM"))
    assert isinstance(projector, lanelet2.projection.UtmProjector)


def test_local_cartesian_returns_local_cartesian_projector():
    projector = loader.get_lanelet2_projector(make_info("LOCAL_CARTESIAN"))
    assert isinstance(projector, lanelet2.projection.LocalCartesianProjector)


def test_local_cartesian_forward_reverse_round_trip():
    origin = lanelet2.io.Origin(lanelet2.core.GPSPoint(35.0, 139.0, 0.0))
    projector = lanelet2.projection.LocalCartesianProjector(origin)
    gps = lanelet2.core.GPSPoint(35.001, 139.001, 10.0)
    local = projector.forward(gps)
    back = projector.reverse(local)
    assert back.lat == pytest.approx(gps.lat, abs=1e-9)
    assert back.lon == pytest.approx(gps.lon, abs=1e-9)
    # NOTE: boost.python binds C++ GPSPoint::ele to the Python attribute name
    # "alt" (see lanelet2_python/python_api/core.cpp), not "ele".
    # alt is in meters, not degrees like lat/lon, so it gets a looser
    # (but still sub-micrometer) tolerance rather than reusing 1e-9 (1 nm),
    # which is unrealistically tight for a double-precision ellipsoidal
    # round-trip and risks flaky CI failures across platforms/libm versions.
    assert back.alt == pytest.approx(gps.alt, abs=1e-6)


def test_local_cartesian_forward_of_origin_is_zero():
    origin = lanelet2.io.Origin(lanelet2.core.GPSPoint(35.0, 139.0, 0.0))
    projector = lanelet2.projection.LocalCartesianProjector(origin)
    local = projector.forward(lanelet2.core.GPSPoint(35.0, 139.0, 0.0))
    assert local.x == pytest.approx(0.0, abs=1e-6)
    assert local.y == pytest.approx(0.0, abs=1e-6)
    assert local.z == pytest.approx(0.0, abs=1e-6)


def test_local_cartesian_differs_from_utm():
    origin = lanelet2.io.Origin(lanelet2.core.GPSPoint(35.0, 139.0, 0.0))
    local_cartesian_projector = lanelet2.projection.LocalCartesianProjector(origin)
    utm_projector = lanelet2.projection.UtmProjector(origin)
    gps = lanelet2.core.GPSPoint(35.001, 139.001, 10.0)
    local_cartesian = local_cartesian_projector.forward(gps)
    utm = utm_projector.forward(gps)
    # A tangent-plane local-cartesian projection and a UTM projection use
    # fundamentally different coordinate systems, so their outputs for the
    # same off-origin point must diverge well beyond floating-point noise.
    # This guards against the boost.python binding accidentally being wired
    # to some other already-invertible projector.
    assert abs(local_cartesian.x - utm.x) > 1.0 or abs(local_cartesian.y - utm.y) > 1.0


# ---------------------------------------------------------------------------
# End-to-end via loader.load_map()
# ---------------------------------------------------------------------------

MINIMAL_OSM = (
    '<?xml version="1.0"?>\n<osm version="0.6">\n'
    '  <node id="-1" lat="35.0001" lon="139.0001" visible="true" version="1"/>\n'
    "</osm>\n"
)


@pytest.fixture
def osm_path(tmp_path):
    path = tmp_path / "minimal.osm"
    path.write_text(MINIMAL_OSM)
    return str(path)


def test_load_map_accepts_local_cartesian_utm(osm_path):
    map_obj = loader.load_map(osm_path, make_info("LOCAL_CARTESIAN_UTM"))
    assert len(list(map_obj.pointLayer)) == 1


def test_load_map_accepts_local_cartesian(osm_path):
    map_obj = loader.load_map(osm_path, make_info("LOCAL_CARTESIAN"))
    assert len(list(map_obj.pointLayer)) == 1

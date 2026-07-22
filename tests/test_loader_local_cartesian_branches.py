"""Tests for the LOCAL_CARTESIAN_UTM / LOCAL_CARTESIAN branches of
loader.get_lanelet2_projector().

Requires the built C++ extension; skipped automatically when unavailable.

lanelet2.projection.LocalCartesianProjector is not implemented anywhere in
this repo's vendored lanelet2 / autoware_lanelet2_extension (#10), so the
LOCAL_CARTESIAN branch is expected to fail with AttributeError.
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


def test_local_cartesian_raises_attribute_error_for_unimplemented_projector():
    """lanelet2.projection.LocalCartesianProjector is not implemented (#10)."""
    with pytest.raises(AttributeError):
        loader.get_lanelet2_projector(make_info("LOCAL_CARTESIAN"))


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


def test_load_map_local_cartesian_raises_attribute_error(osm_path):
    """load_map's LOCAL_CARTESIAN path fails for the same reason (#10)."""
    with pytest.raises(AttributeError):
        loader.load_map(osm_path, make_info("LOCAL_CARTESIAN"))

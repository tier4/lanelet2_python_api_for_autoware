"""TransverseMercatorProjector の scale_factor 対応のテスト。

このファイルのテストはビルド済みの C++ 拡張が必要（未ビルド環境では skip される）。
純 Python のテストは test_map_projector_info.py にある。
"""
import pytest

lanelet2 = pytest.importorskip("lanelet2")
projection = pytest.importorskip("autoware_lanelet2_extension_python.projection")

UTM_K = 0.9996
JPRCS_K = 0.9999  # 日本の平面直角座標系


@pytest.fixture
def origin():
    return lanelet2.io.Origin(lanelet2.core.GPSPoint(35.0, 139.0, 0.0))


@pytest.fixture
def gps_5km_north():
    return lanelet2.core.GPSPoint(35.045, 139.0, 0.0)


def test_ctor_backward_compatible(origin):
    projection.TransverseMercatorProjector(origin)


def test_ctor_accepts_scale_factor_kwarg(origin):
    projection.TransverseMercatorProjector(origin, scale_factor=JPRCS_K)


def test_default_scale_factor_is_utm(origin, gps_5km_north):
    p_default = projection.TransverseMercatorProjector(origin)
    p_utm = projection.TransverseMercatorProjector(origin, scale_factor=UTM_K)
    assert p_default.forward(gps_5km_north).y == pytest.approx(
        p_utm.forward(gps_5km_north).y, abs=1e-9
    )


def test_scale_factor_scales_projection(origin, gps_5km_north):
    y_jprcs = projection.TransverseMercatorProjector(
        origin, scale_factor=JPRCS_K).forward(gps_5km_north).y
    y_utm = projection.TransverseMercatorProjector(
        origin, scale_factor=UTM_K).forward(gps_5km_north).y
    # k=0.9999 と k=0.9996 では原点から 5km で約 1.5m ずれる
    assert abs(y_jprcs - y_utm) > 1.0
    assert y_jprcs / y_utm == pytest.approx(JPRCS_K / UTM_K, abs=1e-12)


def test_round_trip(origin, gps_5km_north):
    p = projection.TransverseMercatorProjector(origin, scale_factor=JPRCS_K)
    back = p.reverse(p.forward(gps_5km_north))
    assert back.lat == pytest.approx(gps_5km_north.lat, abs=1e-9)
    assert back.lon == pytest.approx(gps_5km_north.lon, abs=1e-9)


# ---------------------------------------------------------------------------
# loader 経由のエンドツーエンド
# ---------------------------------------------------------------------------

MINIMAL_OSM = (
    '<?xml version="1.0"?>\n<osm version="0.6">\n'
    '  <node id="-1" lat="35.0449" lon="139.0001" visible="true" version="1"/>\n'
    "</osm>\n"
)


@pytest.fixture
def osm_path(tmp_path):
    path = tmp_path / "minimal.osm"
    path.write_text(MINIMAL_OSM)
    return str(path)


@pytest.mark.parametrize("projector_type", ["TransverseMercator", "TRANSVERSE_MERCATOR"])
def test_loader_accepts_both_spellings(osm_path, projector_type):
    from map_projector_info import GeoPoint
    import loader

    class Info:
        pass

    info = Info()
    info.projector_type = projector_type
    info.map_origin = GeoPoint(35.0, 139.0, 0.0)
    info.scale_factor = JPRCS_K
    map_obj = loader.load_map(osm_path, info)
    assert len(list(map_obj.pointLayer)) == 1


def test_loader_passes_scale_factor_through(osm_path, tmp_path):
    pytest.importorskip("yaml")
    from map_projector_info import load_info_from_yaml
    import loader

    def load_y(scale_factor):
        yaml_path = tmp_path / f"info_{scale_factor}.yaml"
        yaml_path.write_text(
            "projector_type: TransverseMercator\n"
            f"scale_factor: {scale_factor}\n"
            "map_origin:\n  latitude: 35.0\n  longitude: 139.0\n  altitude: 0.0\n"
        )
        info = load_info_from_yaml(str(yaml_path))
        return list(loader.load_map(osm_path, info).pointLayer)[0].y

    # scale_factor が C++ プロジェクタまで届いていれば、ロード後の座標が約 1.5m ずれる
    assert abs(load_y(JPRCS_K) - load_y(UTM_K)) > 1.0


def test_loader_defaults_without_scale_factor_attribute(osm_path):
    from map_projector_info import GeoPoint
    import loader

    class LegacyInfo:  # scale_factor 属性を持たない旧来のオブジェクト
        projector_type = "TransverseMercator"
        map_origin = GeoPoint(35.0, 139.0, 0.0)

    map_obj = loader.load_map(osm_path, LegacyInfo())
    assert len(list(map_obj.pointLayer)) == 1

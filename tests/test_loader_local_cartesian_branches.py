"""loader.get_lanelet2_projector() の LOCAL_CARTESIAN_UTM / LOCAL_CARTESIAN 分岐のテスト。

これまで一度もテストで実行されたことがなく、実際に呼ばれると
`lanelet2.GPSPoint` / `lanelet2.ioOrigin` という誤ったシンボル参照により
AttributeError で落ちていた（Issue #9）。

このファイルのテストはビルド済みの C++ 拡張が必要（未ビルド環境では skip される）。

既知の制限（Issue #9 のスコープ外、Issue #10 で追跡）:
LOCAL_CARTESIAN 分岐が呼び出す `lanelet2.projection.LocalCartesianProjector` は
このリポジトリ（vendored lanelet2 / autoware_lanelet2_extension のいずれにも）
実装されていない。Issue #9 の symbol-path 修正（`lanelet2.io.Origin` へのタイポ修正）
だけではこの分岐は解決しないため、このファイルでは「LOCAL_CARTESIAN_UTM は成功する」
「LOCAL_CARTESIAN は LocalCartesianProjector 未実装により AttributeError で失敗する
（既知の制限）」ことをそれぞれ明示的に検証する。
https://github.com/tier4/lanelet2_python_api_for_autoware/issues/10
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
    """LOCAL_CARTESIAN は LocalCartesianProjector 未実装のため AttributeError で落ちる（issue #10）。"""
    with pytest.raises(AttributeError):
        loader.get_lanelet2_projector(make_info("LOCAL_CARTESIAN"))


# ---------------------------------------------------------------------------
# loader.load_map() 経由のエンドツーエンド
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
    """LOCAL_CARTESIAN 経由の load_map も LocalCartesianProjector 未実装により失敗する（issue #10）。"""
    with pytest.raises(AttributeError):
        loader.load_map(osm_path, make_info("LOCAL_CARTESIAN"))

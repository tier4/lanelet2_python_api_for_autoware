"""MapProjectorInfo の scale_factor 対応のテスト（ビルド不要・純 Python）。"""
import pytest

UTM_K = 0.9996
JPRCS_K = 0.9999  # 日本の平面直角座標系


def test_default_scale_factor():
    from map_projector_info import MapProjectorInfo

    info = MapProjectorInfo("MGRS", "WGS84", "54SUE")
    assert info.scale_factor == UTM_K


def test_explicit_scale_factor():
    from map_projector_info import MapProjectorInfo

    info = MapProjectorInfo("TransverseMercator", "WGS84", "", scale_factor=JPRCS_K)
    assert info.scale_factor == JPRCS_K


def test_load_info_from_yaml_scale_factor(tmp_path):
    pytest.importorskip("yaml")
    from map_projector_info import load_info_from_yaml

    yaml_path = tmp_path / "projector_info.yaml"
    yaml_path.write_text(
        "projector_type: TransverseMercator\n"
        "scale_factor: 0.9999\n"
        "map_origin:\n  latitude: 35.0\n  longitude: 139.0\n  altitude: 0.0\n"
    )
    info = load_info_from_yaml(str(yaml_path))
    assert info.scale_factor == JPRCS_K


def test_load_info_from_yaml_scale_factor_defaults(tmp_path):
    pytest.importorskip("yaml")
    from map_projector_info import load_info_from_yaml

    yaml_path = tmp_path / "projector_info.yaml"
    yaml_path.write_text(
        "projector_type: TransverseMercator\n"
        "map_origin:\n  latitude: 35.0\n  longitude: 139.0\n  altitude: 0.0\n"
    )
    info = load_info_from_yaml(str(yaml_path))
    assert info.scale_factor == UTM_K


def test_load_info_from_yaml_scale_factor_null_defaults(tmp_path):
    """`scale_factor:`（値なし=null）の場合もデフォルト値にフォールバックすること。"""
    pytest.importorskip("yaml")
    from map_projector_info import load_info_from_yaml

    yaml_path = tmp_path / "projector_info.yaml"
    yaml_path.write_text(
        "projector_type: TransverseMercator\n"
        "scale_factor:\n"
        "map_origin:\n  latitude: 35.0\n  longitude: 139.0\n  altitude: 0.0\n"
    )
    info = load_info_from_yaml(str(yaml_path))
    assert info.scale_factor == UTM_K


def test_load_info_from_yaml_scale_factor_zero_is_preserved(tmp_path):
    """`scale_factor: 0.0` は有効な値としてそのまま保持されること（None ガードで潰さない）。"""
    pytest.importorskip("yaml")
    from map_projector_info import load_info_from_yaml

    yaml_path = tmp_path / "projector_info.yaml"
    yaml_path.write_text(
        "projector_type: TransverseMercator\n"
        "scale_factor: 0.0\n"
        "map_origin:\n  latitude: 35.0\n  longitude: 139.0\n  altitude: 0.0\n"
    )
    info = load_info_from_yaml(str(yaml_path))
    assert info.scale_factor == 0.0

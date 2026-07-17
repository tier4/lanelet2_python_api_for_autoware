import sys
from pathlib import Path

# loader.py / map_projector_info.py はリポジトリ直下のモジュールなので、その場所を import path に追加する
ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "autoware_lanelet2_extension" / "autoware_lanelet2_extension_python"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

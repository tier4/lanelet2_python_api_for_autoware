import sys
from pathlib import Path

# loader.py / map_projector_info.py はリポジトリ直下のモジュールなので、その場所を import path に追加する
# append(), not insert(0, ...): the second path is the submodule's source-tree
# package copy, which has no built boost.python .so files. Appending keeps it
# as a fallback instead of shadowing the built package provided via PYTHONPATH.
ROOT = Path(__file__).resolve().parent.parent
for p in (ROOT, ROOT / "autoware_lanelet2_extension" / "autoware_lanelet2_extension_python"):
    if str(p) not in sys.path:
        sys.path.append(str(p))

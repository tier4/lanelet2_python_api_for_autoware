# Standable Autoware Lanelet2 Extension

## Poetry環境での使用方法（推奨）

### ✅ 問題解決完了！
Poetry環境でのインポート問題を完全に解決しました。**環境変数の設定は不要**で、直接使用できます。

### セットアップ手順

```bash
# 1. 依存関係のインストールとビルド（一度だけ実行）
poetry install
```

これだけで完了です！`poetry install`でビルドも自動実行されます。

### 使用方法

環境変数設定やシェルスクリプト不要で、直接Poetry環境からインポートできます：

```bash
# 直接実行可能
poetry run python -c "from autoware_lanelet2_extension_python.projection import MGRSProjector; print('Success!')"

# スクリプトの実行
poetry run python your_script.py

# インタラクティブPython
poetry run python
```

### Pythonでの使用例

```python
from autoware_lanelet2_extension_python.projection import MGRSProjector
import lanelet2

# Originの作成
origin = lanelet2.io.Origin(35.681298, 139.766247, 0.0)

# MGRSProjectorの作成（環境変数設定不要！）
projector = MGRSProjector(origin)
```

### 実装済み機能

- ✅ 自動ライブラリ事前読み込み
- ✅ 共有ライブラリの自動バンドル  
- ✅ RPATHの適切な設定
- ✅ ROSとの競合回避

## Setup (従来の方法)
This repository will build and install (first in the local directory) the Lanelet2 library and the autoware_lanelet2_extension.

```
## Common packages only not available in bare ubuntu container
sudo apt install git gcc cmake python3 python3-pip

## install addtional necessary packages
bash pre-install.sh 

## build the repositories and it will create an `install` folder locally
bash build.sh

## add environmental variables in the current terminal
source setup.bash
```

Then we can use `lanelet2` and `autoware_lanelet2_extension_python` as if normal python packages everywhere.

I have already tested that I can launch lanelet2 (and the sub-packages) package normally, (with the installation pipeline reproduced in ubuntu 22.04 container).

###
Thanks https://github.com/embedded-software-laboratory/Rosless-Lanelet2 for there developments.

## API Changes

- Utilize numpy.array instead of geometry pose messages.
- Improve python function documentation. 
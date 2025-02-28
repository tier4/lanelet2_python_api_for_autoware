import lanelet2

class LocalProjector(lanelet2.Projector):
    def __init__(self):
        # C++ の: LocalProjector() : Projector(lanelet::Origin(lanelet::GPSPoint{})) {}
        super().__init__(lanelet2.Origin(lanelet2.GPSPoint()))
    
    def forward(self, gps):
        # C++ の: return lanelet::BasicPoint3d{0.0, 0.0, gps.ele};
        return lanelet2.BasicPoint3d(0.0, 0.0, gps.ele)
    
    def reverse(self, point):
        # C++ の: return lanelet::GPSPoint{0.0, 0.0, point.z()};
        return lanelet2.GPSPoint(0.0, 0.0, point.z())

def load_map(lanelet2_filename, projector_info):
    """
    指定されたファイル名とプロジェクタ情報に基づいて、Lanelet2形式の地図を読み込みます。
    
    引数:
      lanelet2_filename (str): 地図ファイルのパス
      projector_info: プロジェクタ情報を保持するオブジェクト。属性 'projector_type' を持ち、値が "local" でなければグローバル系、
                        "local" の場合はローカル系として処理します。
    
    戻り値:
      読み込んだ地図オブジェクト（成功時）または None（エラー発生時）
    """
    errors = []  # エラーメッセージを格納するリスト

    # グローバル系の場合（"local" 以外）
    if projector_info.projector_type != "local":
        projector = get_lanelet2_projector(projector_info) # TODO: get_lanelet2_projector の実装
        map_obj = lanelet2.io.load(lanelet2_filename, projector, errors)
        if not errors:
            return map_obj
    else:
        # ローカルプロジェクタを使用
        projector = LocalProjector()
        map_obj = lanelet2.io.load(lanelet2_filename, projector, errors)

        if errors:
            for error in errors:
                print("Map load error:", error)

        # 各点の local_x, local_y 属性があれば、その値で座標を上書き
        for point in map_obj.pointLayer:
            if "local_x" in point.attributes:
                try:
                    point.x = float(point.attributes["local_x"])
                except ValueError:
                    print("Invalid local_x for point:", point)
            if "local_y" in point.attributes:
                try:
                    point.y = float(point.attributes["local_y"])
                except ValueError:
                    print("Invalid local_y for point:", point)

        # 更新された点情報を基に、レーンレットの左右境界線を再整列
        for lanelet in map_obj.laneletLayer:
            left = lanelet.leftBound()
            right = lanelet.rightBound()
            new_left, new_right = lanelet2.geometry.align(left, right)
            lanelet.setLeftBound(new_left)
            lanelet.setRightBound(new_right)
        return map_obj

    # グローバル系でエラーがあった場合、エラーメッセージを出力
    for error in errors:
        print("Map load error:", error)
    return None

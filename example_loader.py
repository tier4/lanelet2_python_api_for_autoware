from map_projector_info import load_info_from_yaml
from loader import load_map
import autoware_lanelet2_extension_python.utility.query as query
import matplotlib.pyplot as plt
import numpy as np


def plot_ll2_id(ll2, ax, text):
    xs, ys = np.array([pt.x for pt in ll2.centerline]), np.array([pt.y for pt in ll2.centerline])
    x, y = np.average(xs), np.average(ys)
    ax.text(x, y, text)


def plot_linestring(linestring, ax:plt.Axes, color, linestyle, **kwargs):
    xs = [pt.x for pt in linestring]
    ys = [pt.y for pt in linestring]
    ax.plot(xs, ys, color=color, linestyle=linestyle, **kwargs)


def visualize_map(map_obj):
    all_lanelets = query.laneletLayer(map_obj)
    road_lanelets = query.roadLanelets(all_lanelets)

    fig, ax = plt.subplots()
    for lanelet in road_lanelets:
        plot_ll2_id(lanelet, ax, str(lanelet.id))
        # plot_linestring(lanelet.centerline, ax, "blue", "-", "centerline")
        plot_linestring(lanelet.leftBound, ax, "red", "-", label=f"leftBound_{lanelet.id}")
        plot_linestring(lanelet.rightBound, ax, "green", "-", label=f"rightBound_{lanelet.id}")

    ax.set_aspect('equal')
    # ax.legend()
    plt.show()




def main(lanelet2_path, yaml_path):
    info = load_info_from_yaml(yaml_path)
    map_obj = load_map(lanelet2_path, info)
    visualize_map(map_obj)
    return map_obj

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print('Usage: python main.py <lanelet2_path> <yaml_path>')
        sys.exit(1)
    lanelet2_path = sys.argv[1]
    yaml_path = sys.argv[2]
    map_obj = main(lanelet2_path, yaml_path)
    print(map_obj)

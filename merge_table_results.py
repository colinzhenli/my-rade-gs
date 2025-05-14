import glob
import json
import os

import open3d as o3d
import pandas as pd

from gs_planes.full_eval import (
    blender_scenes,
    hypersim_scenes,
    mipnerf360_indoor_scenes,
    mipnerf360_outdoor_scenes,
    scannetpp_scenes,
)

scannetv2_scenes = [
    # "scene0084_00",
    "scene0164_03",
    "scene0217_00",
    "scene0316_00",
    "scene0356_00",
    # "scene0427_00",
    "scene0488_01",
    # "scene0568_00",
]


def merge_results(root: str, scenes: list, scenes_name: str):
    merged_results_30000 = {}
    merged_results_7000 = {}

    for scene in sorted(scenes):
        try:
            path = f"{root}/{scene}/results.json"

            with open(path) as f:
                data = json.load(f)

        except FileNotFoundError:
            print(f"Scene not found: {scene}")
            continue

        try:
            merged_results_30000[scene] = data["ours_30000"]
            # merged_results_7000[scene] = data["ours_7000"]
        except KeyError:
            print(f"Scene not found: {scene}")

        pointcloud_dir = f"{root}/{scene}/point_cloud/iteration_30000/"
        pointcloud_files = os.listdir(pointcloud_dir)

        if "planes.json" in pointcloud_files:
            with open(f"{pointcloud_dir}/planes.json") as f:
                planes_data = json.load(f)
                plane_ids = planes_data["plane_ids"]

                total_gaussians = len(plane_ids)
                total_planar = len([p for p in plane_ids if p != -1])

                merged_results_30000[scene]["total_gaussians"] = total_gaussians
                merged_results_30000[scene]["total_planar"] = total_planar

        else:
            pcd = o3d.io.read_point_cloud(f"{pointcloud_dir}/point_cloud.ply")
            total_gaussians = len(pcd.points)

            merged_results_30000[scene]["total_gaussians"] = total_gaussians

    df_results_30000 = pd.DataFrame(merged_results_30000)
    df_results_30000["mean"] = df_results_30000.mean(axis=1)

    # df_results_7000 = pd.DataFrame(merged_results_7000)
    # df_results_7000["mean"] = df_results_7000.mean(axis=1)

    print(f"Processsing {scenes_name}")
    print()
    print("Results 30000")
    print(df_results_30000)
    # print()
    # print("Results 7000")
    # print(df_results_7000)
    # print()

    pd.DataFrame.to_csv(df_results_30000, f"{root}/results_30000_{scenes_name}.csv")
    # pd.DataFrame.to_csv(df_results_7000, f"{root}/results_7000_{scenes_name}.csv")


for root in glob.glob("*/eval_dist10"):
    print("Processing root:", root)

    # merge_results(root, blender_scenes, "blender")
    # merge_results(
    #     root, mipnerf360_outdoor_scenes + mipnerf360_indoor_scenes, "mipnerf360"
    # )
    merge_results(root, scannetpp_scenes, "scannetpp")
    merge_results(root, scannetv2_scenes, "scannetv2")
    # merge_results(root, hypersim_scenes, "hypersim")

import subprocess
from tqdm import tqdm

scannetpp_scenes = [
    # "0a7cc12c0e",
    # "0cf2e9402d",
    # "0e75f3c4d9",
    # "1ae9e5d2a6",
    # "1b75758486",
    # "1c4b893630",
    # "2e74812d00",
    "4c5c60fa76",
    # "4ea827f5a1",
    # "5748ce6f01",
    # "7079b59642",
]

source_root = "/localhome/zla247/theia2_data_shared/scannetpp/data"
output_root = "/localhome/zla247/theia2_data_shared/scannetpp/data/output/rade_gs_iphone"

for scene_id in tqdm(scannetpp_scenes, desc="Training scenes"):
    source_path = f"{source_root}/{scene_id}/iphone"
    output_path = f"{output_root}/{scene_id}"

    print(f"\n▶ Starting training for scene {scene_id}...")

    cmd = [
        "python", "train.py",
        "-s", source_path,
        "-m", output_path,
        "--resolution", "2",
        "--use_decoupled_appearance",
        "--eval"
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Finished training for scene {scene_id}")
    except subprocess.CalledProcessError:
        print(f"❌ Failed training for scene {scene_id}")

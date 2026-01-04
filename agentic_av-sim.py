import numpy as np
from datasets import load_dataset
from time import sleep
from claudette import Chat, tool

def matches_edge_case_tight(pose, target_speed=20, target_yaw=0.05, max_yaw=0.1, tolerance=0.2):
    speeds = np.array(pose)[:, 0]
    yaws = np.abs(np.array(pose)[:, 5])
    if np.nanmax(yaws) >= max_yaw: return False
    high_speed = speeds > target_speed * (1 - tolerance)
    in_yaw_range = (yaws > target_yaw * (1 - tolerance)) & (yaws < max_yaw)
    return np.any(high_speed & in_yaw_range)

@tool
def find_edge_cases(n: int = 10):
    "Stream through control data and find edge cases where openpilot was in control."
    ds = load_dataset("commaai/commaSteeringControl", streaming=True)
    samples = []
    for i, s in enumerate(ds['train']):
        if i % 1000 != 0: continue
        gap = abs(s['latAccelDesired'] - s['latAccelLocalizer'])
        if gap > 1.0 and s['vEgo'] > 15 and s['latActive'] and not s['steeringPressed']:
            samples.append(s)
            print(f"Found {len(samples)} at row {i}")
            if len(samples) >= n: break
    return samples

@tool
def match_video(speed: float, latAccel: float, n: int = 3, retries: int = 3):
    "Find commavq segments matching speed and latAccel signature."
    yaw_rate = abs(latAccel / speed)
    for attempt in range(retries):
        try:
            ds_vq = load_dataset("commaai/commavq", streaming=True)
            keys = []
            for sample in ds_vq['train']:
                if matches_edge_case_tight(sample['pose.npy'], target_speed=speed, target_yaw=yaw_rate):
                    keys.append(sample['__key__'])
                    if len(keys) >= n: break
            return keys
        except Exception as e:
            if attempt < retries - 1:
                sleep(2 ** attempt)
                continue
            raise e

def create_agent():
    sp = "You are an AV simulation assistant. Find edge cases where openpilot struggled and match them to video segments."
    return Chat(model="claude-sonnet-4-20250514", sp=sp, tools=[find_edge_cases, match_video])

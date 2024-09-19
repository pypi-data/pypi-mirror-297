"""Compute stats for all continuous systems, useful for downstream modeling"""

import json

from dysts.systems import compute_trajectory_statistics, get_attractor_list

if __name__ == "__main__":
    num_points = 4096
    num_periods = 10
    subset = get_attractor_list()

    stats = compute_trajectory_statistics(
        num_points,
        subset=subset,
        use_multiprocessing=True,
        use_tqdm=True,
        pts_per_period=num_points // num_periods,
    )

    with open("dysts/data/chaotic_attractors.json") as f:
        data = json.load(f)

    for system in subset:
        data[system].update({k: v.tolist() for k, v in stats[system].items()})

    with open("dysts/data/chaotic_attractors.json", "w") as f:
        json.dump(data, f, indent=2)

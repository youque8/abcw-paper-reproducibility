#!/usr/bin/env python3
"""Recompute and verify the complete numerical evidence chain for the paper."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal


ROOT = Path(__file__).resolve().parents[1]
EXACT = ROOT / "experiments" / "03_exact_partition" / "results"
FEATURES = ROOT / "experiments" / "02_natural_features" / "results"


def run(relative_path: str) -> None:
    print(f"\n== RUN {relative_path} ==", flush=True)
    subprocess.run(
        [sys.executable, str(ROOT / relative_path)],
        cwd=ROOT,
        check=True,
    )


def verify_upper_bound() -> None:
    data = np.load(EXACT / "conflict_data_recomputed.npz")
    conflict = data["conflict"]
    response = data["T"]
    coloring = pd.read_csv(EXACT / "min_partition_upper692.csv").sort_values("field_id")

    n = conflict.shape[0]
    assert conflict.shape == (2562, 2562)
    assert response.shape[0] == 2562
    assert len(coloring) == n
    assert coloring["field_id"].is_unique
    assert np.array_equal(coloring["field_id"].to_numpy(), np.arange(n))

    colors = coloring["color_class"].to_numpy()
    assert len(np.unique(colors)) == 692
    monochromatic_edges = int(
        np.triu(conflict & (colors[:, None] == colors[None, :]), 1).sum()
    )
    assert monochromatic_edges == 0

    # Directly verify that each observed (action, color) has one future field.
    for action_index in range(response.shape[1]):
        observed = np.flatnonzero(response[:, action_index] >= 0)
        pairs: dict[tuple[int, int], int] = {}
        for field_index in observed:
            key = (action_index, int(colors[field_index]))
            future = int(response[field_index, action_index])
            previous = pairs.setdefault(key, future)
            assert previous == future

    edges = int(np.triu(conflict, 1).sum())
    print(
        "PASS upper bound: 2,562 fields, "
        f"{edges:,} conflict edges, 692 colors, 0 monochromatic edges"
    )


def verify_lower_bound() -> None:
    archived = pd.read_csv(EXACT / "anchor_group_chromatic.csv")
    recomputed = pd.read_csv(EXACT / "anchor_group_chromatic_recomputed.csv")
    columns = ["future_id", "n", "edges", "chi", "lb", "ub"]
    archived = archived[columns].sort_values("future_id").reset_index(drop=True)
    recomputed = recomputed[columns].sort_values("future_id").reset_index(drop=True)
    assert_frame_equal(archived, recomputed, check_dtype=False)

    assert len(recomputed) == 625
    assert recomputed["chi"].notna().all()
    assert (recomputed["chi"] == recomputed["lb"]).all()
    assert (recomputed["chi"] == recomputed["ub"]).all()
    assert int(recomputed["chi"].sum()) == 692
    counts = recomputed["chi"].astype(int).value_counts().to_dict()
    assert counts == {1: 575, 2: 39, 3: 8, 4: 2, 7: 1}
    print("PASS lower bound: 625 anchor groups re-solved; chromatic sum = 692")


def verify_natural_features() -> None:
    archived = pd.read_csv(FEATURES / "true_compression_all_511.csv")
    recomputed = pd.read_csv(FEATURES / "true_compression_all_511_recomputed.csv")
    columns = [
        "mask",
        "features",
        "n_features",
        "unique_groups",
        "deterministic_groups",
        "D_state",
        "A_freq",
        "B_unique_DeltaW",
        "DeltaW_compression_rate",
    ]
    archived = archived[columns].sort_values("mask").reset_index(drop=True)
    recomputed = recomputed[columns].sort_values("mask").reset_index(drop=True)
    assert_frame_equal(
        archived,
        recomputed,
        check_dtype=False,
        check_exact=False,
        rtol=1e-13,
        atol=1e-15,
    )
    assert len(recomputed) == 511
    compressive = recomputed["B_unique_DeltaW"] < 2562
    assert int(compressive.sum()) == 261
    assert int((compressive & (recomputed["D_state"] == 1.0)).sum()) == 0
    print("PASS natural features: all 511 rows match the archived reference table")


def main() -> None:
    print("ABCW full reproducibility verification")
    print(f"Python: {sys.version.split()[0]}")
    print(f"NumPy: {np.__version__}; pandas: {pd.__version__}")

    run("experiments/01_dataset/generate_transitions.py")
    run("experiments/03_exact_partition/build_conflict_data.py")
    verify_upper_bound()

    run("experiments/03_exact_partition/exact_anchor_refinement.py")
    verify_lower_bound()

    run("experiments/02_natural_features/run_511_features.py")
    verify_natural_features()

    print("\nPASS FULL VERIFICATION")
    print("Regenerated dataset -> rebuilt conflict graph -> verified 692-color upper bound")
    print("-> re-solved 625 anchor groups -> recomputed all 511 natural-feature candidates.")


if __name__ == "__main__":
    main()

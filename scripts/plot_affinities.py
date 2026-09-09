#!/usr/bin/env python3
"""Bar plot of best docking affinity per ligand from a score CSV."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scores", type=Path, default=Path("data/fake_pose_scores.csv"))
    parser.add_argument("--out", type=Path, default=Path("results/best_affinities.png"))
    args = parser.parse_args()

    df = pd.read_csv(args.scores)
    best = (
        df.sort_values("affinity_kcal_mol")
        .groupby("ligand_id", as_index=False)
        .first()
        .sort_values("affinity_kcal_mol")
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.barh(best["ligand_id"], best["affinity_kcal_mol"], color="#2a6f97")
    ax.set_xlabel("Affinity (kcal/mol)")
    ax.set_title("Best pose affinity per ligand")
    ax.axvline(0, color="gray", linewidth=0.8)
    fig.tight_layout()
    fig.savefig(args.out, dpi=150)
    plt.close(fig)
    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

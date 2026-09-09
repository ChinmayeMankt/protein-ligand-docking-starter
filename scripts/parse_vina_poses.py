#!/usr/bin/env python3
"""Parse a Vina-style pose score table and summarize top poses per ligand."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_scores(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    required = {"ligand_id", "mode", "affinity_kcal_mol"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    return df


def summarize(df: pd.DataFrame, top_n: int = 3) -> pd.DataFrame:
    ranked = df.sort_values(["ligand_id", "affinity_kcal_mol", "mode"])
    return ranked.groupby("ligand_id", as_index=False).head(top_n)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scores",
        type=Path,
        default=Path("data/fake_pose_scores.csv"),
        help="CSV with ligand_id, mode, affinity_kcal_mol[, rmsd_lb, rmsd_ub]",
    )
    parser.add_argument("--top-n", type=int, default=3)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/top_poses_summary.csv"),
    )
    args = parser.parse_args()

    df = parse_scores(args.scores)
    summary = summarize(df, top_n=args.top_n)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(args.out, index=False)

    best = (
        df.sort_values("affinity_kcal_mol")
        .groupby("ligand_id", as_index=False)
        .first()[["ligand_id", "mode", "affinity_kcal_mol"]]
    )
    print("Best pose per ligand (kcal/mol):")
    print(best.to_string(index=False))
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()

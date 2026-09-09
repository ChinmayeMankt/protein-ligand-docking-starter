#!/usr/bin/env python3
"""Distance-based ligand-receptor contact map from toy coordinate CSVs."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def load_coords(path: Path, label: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ("x", "y", "z"):
        if col not in df.columns:
            raise ValueError(f"{label} file missing column '{col}'")
    return df


def pairwise_contacts(
    receptor: pd.DataFrame,
    ligand: pd.DataFrame,
    cutoff: float,
) -> pd.DataFrame:
    r = receptor[["x", "y", "z"]].to_numpy(dtype=float)
    l = ligand[["x", "y", "z"]].to_numpy(dtype=float)
    # (n_lig, n_rec) distances
    d = np.linalg.norm(l[:, None, :] - r[None, :, :], axis=-1)

    rows = []
    lig_ids = ligand["atom_id"].tolist()
    rec_ids = receptor["atom_id"].tolist()
    resnames = receptor.get("resname", pd.Series(["?"] * len(receptor))).tolist()
    resids = receptor.get("resid", pd.Series([0] * len(receptor))).tolist()
    elements = ligand.get("element", pd.Series(["X"] * len(ligand))).tolist()

    for i in range(d.shape[0]):
        for j in range(d.shape[1]):
            dist = float(d[i, j])
            if dist <= cutoff:
                rows.append(
                    {
                        "ligand_atom": lig_ids[i],
                        "ligand_element": elements[i],
                        "receptor_atom": rec_ids[j],
                        "resname": resnames[j],
                        "resid": resids[j],
                        "distance_A": round(dist, 3),
                    }
                )
    return pd.DataFrame(rows).sort_values("distance_A")


def residue_summary(contacts: pd.DataFrame) -> pd.DataFrame:
    if contacts.empty:
        return pd.DataFrame(columns=["resname", "resid", "n_contacts", "min_distance_A"])
    g = (
        contacts.groupby(["resname", "resid"], as_index=False)
        .agg(n_contacts=("distance_A", "size"), min_distance_A=("distance_A", "min"))
        .sort_values(["n_contacts", "min_distance_A"], ascending=[False, True])
    )
    return g


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receptor", type=Path, default=Path("data/toy_receptor_pocket.csv"))
    parser.add_argument("--ligand", type=Path, default=Path("data/toy_ligand_pose.csv"))
    parser.add_argument("--cutoff", type=float, default=4.5, help="Contact cutoff in Angstroms")
    parser.add_argument("--out-contacts", type=Path, default=Path("results/contacts.csv"))
    parser.add_argument("--out-residues", type=Path, default=Path("results/contact_residues.csv"))
    args = parser.parse_args()

    receptor = load_coords(args.receptor, "receptor")
    ligand = load_coords(args.ligand, "ligand")
    contacts = pairwise_contacts(receptor, ligand, args.cutoff)
    residues = residue_summary(contacts)

    args.out_contacts.parent.mkdir(parents=True, exist_ok=True)
    contacts.to_csv(args.out_contacts, index=False)
    residues.to_csv(args.out_residues, index=False)

    print(f"Contacts within {args.cutoff} A: {len(contacts)}")
    print(residues.to_string(index=False) if not residues.empty else "(none)")
    print(f"\nWrote {args.out_contacts}")
    print(f"Wrote {args.out_residues}")


if __name__ == "__main__":
    main()

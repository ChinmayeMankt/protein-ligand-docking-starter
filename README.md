# Protein-Ligand Docking Starter

Python helpers and templates for an AutoDock Vina-style docking workflow: pose score parsing, distance-based interaction/contact mapping, and receptor/ligand prep notes. Sample SMILES and toy coordinate tables are included so the scripts run without a local PDB or Vina install.

## Features

- Parse Vina-like pose score CSVs and summarize top modes per ligand
- Map ligand-receptor contacts from coordinate tables (configurable Angstrom cutoff)
- Plot best affinities across a small ligand set
- Shell templates for common `vina` command lines
- Prep notes covering PDBQT conversion and search-box setup (optional RDKit path)

## Repository layout

```
data/           sample SMILES, pose scores, toy receptor/ligand coords
docs/           receptor & ligand preparation notes
scripts/        parse_vina_poses.py, map_contacts.py, plot_affinities.py
templates/      vina_commands.sh
results/        example outputs from the sample data
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Core scripts use NumPy / pandas / matplotlib. RDKit is optional for SMILES to 3D prep (see `docs/prep_notes.md`).

## How to run

From the repository root:

```bash
# Summarize top docking poses
python scripts/parse_vina_poses.py --scores data/fake_pose_scores.csv --out results/top_poses_summary.csv

# Distance-based contacts (toy pocket + pose)
python scripts/map_contacts.py --receptor data/toy_receptor_pocket.csv \
  --ligand data/toy_ligand_pose.csv --cutoff 4.5

# Affinity bar chart
python scripts/plot_affinities.py --out results/best_affinities.png
```

To run real docking, prepare PDBQT files and adapt `templates/vina_commands.sh` (requires AutoDock Vina on your PATH).

## Example output

Best poses from the bundled score table:

| ligand_id | mode | affinity_kcal_mol |
|-----------|------|-------------------|
| ibuprofen | 1 | -7.1 |
| aspirin | 1 | -6.8 |
| caffeine | 1 | -5.7 |

Contact mapping writes `results/contacts.csv` and a per-residue summary in `results/contact_residues.csv`.

## License

MIT

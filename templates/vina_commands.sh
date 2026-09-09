#!/usr/bin/env bash
# AutoDock Vina-style command templates (edit paths / box for your system).
# Requires: vina (or vina_1.2+), receptor/ligand PDBQT files.

set -euo pipefail

RECEPTOR="data/receptor.pdbqt"
LIGAND="data/ligand.pdbqt"
OUT="results/ligand_out.pdbqt"
LOG="results/ligand_vina.log"

# Search box centered on the binding site (Angstroms)
CENTER_X=12.5
CENTER_Y=9.5
CENTER_Z=6.0
SIZE_X=20
SIZE_Y=20
SIZE_Z=20

mkdir -p results

# Basic docking run
vina \
  --receptor "${RECEPTOR}" \
  --ligand "${LIGAND}" \
  --center_x "${CENTER_X}" \
  --center_y "${CENTER_Y}" \
  --center_z "${CENTER_Z}" \
  --size_x "${SIZE_X}" \
  --size_y "${SIZE_Y}" \
  --size_z "${SIZE_Z}" \
  --exhaustiveness 8 \
  --num_modes 9 \
  --out "${OUT}" \
  --log "${LOG}"

# Batch example (loop over ligands in a directory)
# for lig in ligands/*.pdbqt; do
#   base=$(basename "${lig}" .pdbqt)
#   vina --receptor "${RECEPTOR}" --ligand "${lig}" \
#     --center_x "${CENTER_X}" --center_y "${CENTER_Y}" --center_z "${CENTER_Z}" \
#     --size_x "${SIZE_X}" --size_y "${SIZE_Y}" --size_z "${SIZE_Z}" \
#     --out "results/${base}_out.pdbqt" --log "results/${base}_vina.log"
# done

echo "Done. Inspect ${OUT} and ${LOG}."

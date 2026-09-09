# Receptor and ligand preparation notes

## Receptor (protein)

1. Start from a cleaned PDB (remove waters/ions unless needed; keep catalytic waters if relevant).
2. Add hydrogens and assign charges suitable for docking (e.g. Gasteiger for classic AutoDock tools).
3. Convert to PDBQT (`prepare_receptor4.py` from AutoDockTools, or Meeko / Open Babel depending on your stack).
4. Define the search box from known ligand coordinates, known site residues, or pocket detection.

## Ligand

1. From SMILES or 3D SDF: generate a reasonable 3D conformer (RDKit, Open Babel).
2. Add hydrogens, assign rotatable bonds and charges, write PDBQT.
3. Optional RDKit sketch (if installed):

```python
from rdkit import Chem
from rdkit.Chem import AllChem
mol = Chem.MolFromSmiles("CC(=O)Oc1ccccc1C(=O)O")
mol = Chem.AddHs(mol)
AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
AllChem.MMFFOptimizeMolecule(mol)
Chem.MolToMolFile(mol, "aspirin.sdf")
```

## Docking box tips

- Center on the geometric center of the binding-site residues or a co-crystallized ligand.
- Start with ~20 A cubes; enlarge if poses clip the box edges.
- Re-dock a known binder as a sanity check when a crystal pose is available.

These notes complement `templates/vina_commands.sh` and the Python parsing / contact scripts in `scripts/`.

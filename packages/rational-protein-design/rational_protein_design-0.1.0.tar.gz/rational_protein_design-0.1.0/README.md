# Rational Protein Design

This package is designed for rational protein binder design using Biopython data structures. It allows for efficient identification and extraction of protein sequences based on proximity to target residues in a protein structure.

## Features

- Parse PDB files and extract chains
- Identify neighboring residues based on distance thresholds
- Extract protein sequences and generate rational binders
- Support for randomization and multiple design attempts

## Installation

You can install the package from PyPI:

```bash
pip install rational_protein_design
```

## Usage

```python
from rational_protein_design import BinderDesigner

designer = BinderDesigner(
    pdb_file="path/to/pdb/file.pdb",
    chain_id="A",
    target_residues_range=(100, 120),
    neighbor_chain_id="B",
    N=50,
    num_seq=10
)
designer.design_binder("output_fasta_file.fasta")
```

## License

This project is licensed under the MIT License.


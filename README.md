# k-path-graphs-toolkit

K-Path Graphs Toolkit: generator and analyzer for unlabeled k-path graphs.

This repository contains code to generate pairwise non-isomorphic unlabeled k-path graphs, convert them to Graph6 format, and analyze their algebraic connectivity. The implementation is organized as a reproducible scientific pipeline focused on large-scale generation with stream-based processing.

## What This Project Does

1. Generates canonical colored sequences for fixed `(k, n)`.
2. Converts sequences to graph instances and exports `.g6` files.
3. Computes algebraic connectivity (`lambda_2`) and summary tables.

## Mathematical Basis

The counting functions are based on the following recurrences:

```text
M(n,k) = k*M(n-2,k) + M(n-3,k-1) + M(n-4,k-2)
N(n,k) = k^2*N(n-2,k) + (2k-1)*N(n-3,k-1) + N(n-4,k-2)
         + (k(k-1)/2)*M(n-2,k) + (k-1)*M(n-3,k-1)
T(n,k) = T(n-1,k-1) + M(n,k) + N(n,k)
```

`T(n,k)` is used as an internal consistency target during generation and conversion.

## Tracked Repository Structure

The current Git-tracked source files are:

```text
.gitignore
README.md
pyproject.toml
requirements.txt
run_special_sequence_generation.py
setup.py
notebooks/generate_and_analyze_k_path_graphs.ipynb
src/__init__.py
src/generators.py
src/converters.py
src/analyzers.py
src/paths.py
```

Runtime data outputs are written under `data/` when you execute the notebook or scripts.

## Installation

```bash
git clone <repository-url>
cd k-path-graphs-toolkit

python3 -m venv venv_grafos
source venv_grafos/bin/activate

pip install -e .

# Optional: install pinned runtime dependencies directly
pip install -r requirements.txt
```

## Main Workflow

The main reproducible workflow is provided in:

`notebooks/generate_and_analyze_k_path_graphs.ipynb`

The notebook is iterative and uses skip logic, so partially completed runs can be resumed safely.

## Special Batch Script

This repository also includes a dedicated batch script for sequence generation with fixed limits:

- `k=2`: `n=6..26`
- `k=3`: `n=8..20`
- `k=4`: `n=10..18`

Script:

`run_special_sequence_generation.py`

Usage:

```bash
python run_special_sequence_generation.py --dry-run
python run_special_sequence_generation.py
python run_special_sequence_generation.py --force
```

The script skips existing files by default and performs an internal assertion (`expected == observed`) for each generated case.

## Programmatic Example

```python
from src.generators import T_n_k, gerarSequenciaN_stream
from src.converters import generateOneG6_stream
from src.analyzers import verify_algebraic_connectivity_one_stream

k = 2
n = 10

expected = int(T_n_k(n, k))
print(f"Expected objects for (n={n}, k={k}): {expected}")

# 1) Sequence generation
gerarSequenciaN_stream(n, k, "data/sequences/2_caminhos")

# 2) Graph6 conversion
generateOneG6_stream(n, k, "data/sequences", "data/g6")

# 3) Algebraic connectivity
verify_algebraic_connectivity_one_stream(n, k, "data/g6", "data/algebraic_connectivity")
```

## Output Files

- Sequences: `data/sequences/{k}_caminhos/{k}_caminhos_n_{n}_T_{T}.txt`
- Graph6: `data/g6/{k}_caminhos_g6/{k}_caminhos_n_{n}_T_{T}.g6`
- Algebraic connectivity: `data/algebraic_connectivity/CA_{k}_path_graph/{k}_CAs_n_{n}.txt`
- Consolidated lists: `data/algebraic_connectivity/{k}_CA_lista.txt`

## Available Link

- Graph6 format reference: http://users.cecs.anu.edu.au/~bdm/data/formats.html

## License

License definition is pending.

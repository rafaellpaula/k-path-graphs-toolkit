# k-path-graphs-toolkit

K-Path Graphs Toolkit: Generator and Analyzer.

This repository contains an implementation for generating pairwise non-isomorphic unlabeled k-path graphs, exporting them in Graph6 format, and computing algebraic connectivity for each generated graph.

The project is organized as a reproducible pipeline:

1. Generate canonical colored sequences for fixed `(k, n)`.
2. Convert sequences to graphs and export to `.g6`.
3. Compute algebraic connectivity (`lambda_2`) for each graph.

## Mathematical Background

The counting functions are based on recursive relations used for unlabeled k-path graph enumeration:

```text
M(n,k) = k*M(n-2,k) + M(n-3,k-1) + M(n-4,k-2)
N(n,k) = k^2*N(n-2,k) + (2k-1)*N(n-3,k-1) + N(n-4,k-2)
				 + (k(k-1)/2)*M(n-2,k) + (k-1)*M(n-3,k-1)
T(n,k) = T(n-1,k-1) + M(n,k) + N(n,k)
```

`T(n,k)` is used as a validation target during generation and conversion.

## Repository Layout

```text
src/
	generators.py          sequence generation (list and stream modes)
	converters.py          TXT -> Graph6 conversion
	analyzers.py           algebraic connectivity computation
	paths.py               default output paths

src_fase2/
	compatibility layer that reexports src/ modules for legacy imports

notebooks/
	generate_and_analyze_k_path_graphs.ipynb

data/
	sequences/
	g6/
	algebraic_connectivity/
```

## Installation

```bash
git clone <your-repository-url>
cd k-path-graphs-toolkit

python3 -m venv venv_grafos
source venv_grafos/bin/activate

pip install -r requirements.txt
```

## Usage

Main reproducible workflow is available in:

`notebooks/generate_and_analyze_k_path_graphs.ipynb`

The notebook is configured for iterative execution (with skip logic), so it can resume partially completed runs.

## Programmatic Example

```python
from src.generators import T_n_k, gerarSequenciaN_stream
from src.converters import generateOneG6_stream
from src.analyzers import verify_algebraic_connectivity_one_stream

k = 2
n = 10

expected = int(T_n_k(n, k))
print(f"Expected objects for (n={n}, k={k}): {expected}")

# 1) sequence generation
gerarSequenciaN_stream(n, k, "data/sequences/2_caminhos")

# 2) Graph6 conversion
generateOneG6_stream(n, k, "data/sequences", "data/g6")

# 3) algebraic connectivity
verify_algebraic_connectivity_one_stream(n, k, "data/g6", "data/algebraic_connectivity")
```

## Output Files

- Sequences: `data/sequences/{k}_caminhos/{k}_caminhos_n_{n}_T_{T}.txt`
- Graph6: `data/g6/{k}_caminhos_g6/{k}_caminhos_n_{n}_T_{T}.g6`
- Algebraic connectivity: `data/algebraic_connectivity/CA_{k}_path_graph/ca_n_{n}.txt`
- Consolidated lists: `data/algebraic_connectivity/{k}_CA_lista.txt`

## Notes on Performance

- Stream-based functions are recommended for large values of `n`.
- Runtime and storage grow quickly with `n`, especially for `k=2` at higher orders.
- The notebook workflow is designed to avoid recomputation of existing outputs.

## References and Useful Links

- Graph6 format reference: http://users.cecs.anu.edu.au/~bdm/data/formats.html

If you plan to cite the theoretical basis of this implementation, add your preferred paper references here.

## License

License definition is pending.

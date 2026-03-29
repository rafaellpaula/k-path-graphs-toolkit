# K-Path Graph Generator

**Optimized generation and analysis of unlabeled k-path graphs with algebraic connectivity computation**

## Overview

This project provides an efficient implementation for generating all non-isomorphic unlabeled k-path graphs and computing their algebraic connectivity (second smallest Laplacian eigenvalue). The work is based on the recursive formula for unlabeled k-path graphs and includes several performance optimizations for large-scale graph generation and analysis.

## Mathematical Foundation

### Definitions

- **k-path graph**: An unlabeled graph that can be recognized as a path or a union of disjoint paths, parameterized by a coloring of vertices using colors {1, 2, ..., k}.
- **T(n,k)**: Total count of non-isomorphic unlabeled k-path graphs with n vertices.

### Recurrence Relations

The number of such graphs follows:

```
M(n,k) = k⋅M(n-2,k) + M(n-3,k-1) + M(n-4,k-2)   n ≥ 2k+2
N(n,k) = k²⋅N(n-2,k) + (2k-1)⋅N(n-3,k-1) + N(n-4,k-2) + (k(k-1)/2)⋅M(n-2,k) + (k-1)⋅M(n-3,k-1)

T(n,k) = T(n-1,k-1) + M(n,k) + N(n,k)
```

**Algebraic Connectivity**: The second-smallest eigenvalue of the Laplacian matrix, reflecting graph connectivity properties.

## Project Structure

```
.
├── src/                          # Main Python modules
│   ├── generators.py             # Sequence generation for k-path graphs
│   ├── converters.py             # Format conversion (TXT → adjacency → G6)
│   ├── analyzers.py              # Algebraic connectivity analysis
│   ├── paths.py                  # Path utilities
│   └── __init__.py               # Package initialization
│
├── notebooks/                    # Jupyter notebooks for analysis and examples
│   └── construct_2_3_4_path_graphs_copia_17-03-26.ipynb
│
├── data/                         # Dataset storage (organized by type)
│   ├── sequences/                # Text files with colored sequence data
│   │   ├── 2_caminhos/
│   │   ├── 3_caminhos/
│   │   └── 4_caminhos/
│   ├── g6/                       # Graph6 format files
│   │   ├── 2_caminhos_g6/
│   │   ├── 3_caminhos_g6/
│   │   └── 4_caminhos_g6/
│   └── algebraic_connectivity/  # Computed CA values
│       ├── CA_2_path_graph/
│       ├── CA_3_path_graph/
│       └── CA_4_path_graph/
│
├── docs/                         # Documentation (future)
│
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
├── pyproject.toml               # Modern Python packaging (PEP 517/518)
├── .gitignore                   # Version control rules
└── README.md                    # This file
```

## Installation

### From source (development mode)

```bash
# Clone the repository
git clone <repository-url>
cd k-path-graph-generator

# Create virtual environment
python3 -m venv venv_grafos
source venv_grafos/bin/activate  # On Windows: venv_grafos\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in editable mode
pip install -e .

# For Jupyter support
pip install -e ".[jupyter]"
```

## Usage

### As a Python package

```python
import sys
sys.path.insert(0, '.')

from src.generators import generating_all_unlabeled_k_path_graph, T_n_k
from src.converters import coloredToAdjacence, generateG6Archives
from src.analyzers import verify_algebraic_connectivity_all

# Generate sequences for k=2, n=10
sequences = generating_all_unlabeled_k_path_graph(k=2, n=10)
expected = int(T_n_k(10, 2))
print(f"Generated {len(sequences)} sequences (expected {expected})")
```

### In Jupyter notebooks

See `notebooks/construct_2_3_4_path_graphs_copia_17-03-26.ipynb` for complete examples including:
- Baseline benchmarks (Phase 1)
- Modular integration (Phase 2)
- Core optimizations validation (Phase 3)
- Large-scale testing with time limits (Phase 4+)

### Command-line Usage

```bash
# Activate environment
source venv_grafos/bin/activate

# Run notebook analysis
jupyter notebook notebooks/
```

## Optimizations

The implementation includes several key performance improvements:

1. **Memoization**: `@lru_cache` on recursive formulas M(n,k), N(n,k), T(n,k)
2. **Efficient deduplication**: O(1) set-based lookup replacing O(n) list searching
3. **Stream I/O**: Line-by-line writing for large sequences without in-memory buffering
4. **Incremental tracking**: Removed redundant slicing and repeated max computations

**Performance**: ~2.5x speedup observed on core generation (baseline → optimized).

## Data Availability

All datasets are version-controlled and included in the repository:

- **Sequences**: Colored integer sequences for k=2,3,4 with various n values
- **Graph6 format**: Binary graph representation for efficient storage
- **Algebraic Connectivity**: Pre-computed CA values for all generated graphs

For reproducing results from scratch, run the Jupyter notebook with appropriate parameters.

## Contributors & Collaboration

To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Install development dependencies: `pip install -e ".[dev]"`
4. Run tests and validation
5. Submit a pull request

**Important**: Ensure any new code passes the validation tests in `notebooks/` to prevent regressions.

## Computational Limitations

- **Memory**: Stream processing recommended for n > 28 (k=2)
- **Time**: Expect ~16s per n for k=2 at maximum tested values
- **Storage**: Databases grow exponentially; Git LFS recommended for future scaling

## References

The mathematical foundations follow work in:
- Pereira's algorithm for k-path graph enumeration
- Laplacian spectral analysis of graph connectivity

## License

**⚠️ Pending decision** — Choose between MIT, GPL, or academic-specific license. To be defined before public release.

## Acknowledgments

Built as part of PhD research in graph optimization and spectral analysis.

---

**Last Updated**: March 19, 2026  
**Status**: Active Development (Phase 5 - Refactoring)

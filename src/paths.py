from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Phase2Paths:
    base: Path
    sequences: Path
    g6: Path
    ca: Path


def get_default_paths(base_dir: str | Path = "data") -> Phase2Paths:
    base = Path(base_dir)
    sequences = base / "sequences"
    g6 = base / "g6"
    ca = base / "algebraic_connectivity"

    sequences.mkdir(parents=True, exist_ok=True)
    g6.mkdir(parents=True, exist_ok=True)
    ca.mkdir(parents=True, exist_ok=True)

    return Phase2Paths(base=base, sequences=sequences, g6=g6, ca=ca)

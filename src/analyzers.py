from __future__ import annotations

from pathlib import Path

import networkx as nx
import numpy as np

from .generators import T_n_k
from .paths import get_default_paths


def RecordAlgebraics(vector, name: str, k: int, pasta_destino: str | Path | None = None):
    paths = get_default_paths()
    destino = Path(pasta_destino) if pasta_destino else paths.ca / f"CA_{k}_path_graph"
    destino.mkdir(parents=True, exist_ok=True)

    arr = np.reshape(vector, (len(vector), 1))
    out_path = destino / f"{name}.txt"
    with open(out_path, "w", encoding="utf-8") as f:
        np.savetxt(f, arr, fmt="%1.20f")
    return out_path


def import_graph_g6(path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        G = nx.read_graph6(f.name)
    return G


def verify_algebraic_connectivity_all(
    k: int,
    Nf: int,
    g6_base: str | Path | None = None,
    ca_base: str | Path | None = None,
    list_output_path: str | Path | None = None,
):
    paths = get_default_paths()
    g6_dir = Path(g6_base) if g6_base else paths.g6 / f"{k}_caminhos_g6"
    ca_dir = Path(ca_base) if ca_base else paths.ca / f"CA_{k}_path_graph"
    ca_dir.mkdir(parents=True, exist_ok=True)

    str_CA = ""

    for i in range(k * 2 + 2, Nf + 1):
        valueTNK = int(T_n_k(i, k))
        graph_path = g6_dir / f"{k}_caminhos_n_{i}_T_{valueTNK}.g6"
        G = import_graph_g6(graph_path)
        CA = [nx.algebraic_connectivity(element) for element in G]

        RecordAlgebraics(CA, f"{k}_CAs_n_{i}", k, pasta_destino=ca_dir)

        max_CA = max(CA)
        min_CA = min(CA)
        pos_min = CA.index(min_CA)
        pos_max = CA.index(max_CA)

        str_CA += (
            f"N({i}) 3_max_CA({max_CA}) pos_elemento_max_CA({pos_max}) | "
            f"min_CA({min_CA}) pos_elemento_min_CA({pos_min})  \n"
        )

    if list_output_path:
        list_path = Path(list_output_path)
    else:
        list_path = paths.ca / f"{k}_CA_lista.txt"

    with open(list_path, "w", encoding="utf-8") as f:
        f.writelines(str_CA)

    return list_path


def MaxAlgebraicConnectivity(N: int, k: int, ca_base: str | Path | None = None):
    paths = get_default_paths()
    base = Path(ca_base) if ca_base else paths.ca / f"CA_{k}_path_graph"
    tabela_CA = np.loadtxt(base / f"{k}_CAs_n_{N}.txt")
    max_CA = max(tabela_CA)
    return N, max_CA


def TableMaxCA(Nf: int, k: int, ca_base: str | Path | None = None):
    paths = get_default_paths()
    base = Path(ca_base) if ca_base else paths.ca / f"CA_{k}_path_graph"
    base.mkdir(parents=True, exist_ok=True)

    str_CA = ""
    for i in range(k * 2 + 2, Nf + 1):
        n, max_CA = MaxAlgebraicConnectivity(i, k, ca_base=base)
        str_CA += f"{n} {max_CA:,.4f}\n"

    nome_arquivo = base / f"{k}_CAs_Max_{k * 2 + 2}_a_{Nf}.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.writelines(str_CA)

    return nome_arquivo


def indexCA(NF: int, k: int, ca_base: str | Path | None = None):
    paths = get_default_paths()
    base = Path(ca_base) if ca_base else paths.ca / f"CA_{k}_path_graph"
    pasta_destino = base / f"CA_{k}_indexadas"
    pasta_destino.mkdir(parents=True, exist_ok=True)

    outputs = []
    for n in range(k * 2 + 2, NF + 1):
        listaCA = np.loadtxt(base / f"{k}_CAs_n_{n}.txt")
        matriz_ordenada = np.sort(listaCA)
        x = len(listaCA)
        y = 1

        listaDeIndices = np.array([np.where(v == matriz_ordenada)[0][0] for v in listaCA])
        novoArray1 = np.reshape(listaCA, (x, y))
        novoArray2 = np.array(np.reshape(listaDeIndices, (x, y)), dtype=np.uint64)
        novoArray = np.concatenate((novoArray1, novoArray2), axis=1)

        out = pasta_destino / f"{k}_CA_indexadas_{n}.txt"
        np.savetxt(out, novoArray, fmt="%.20f %d")
        outputs.append(out)

    return outputs


def verify_algebraic_connectivity_one_stream(
    n: int,
    k: int,
    g6_base: str | Path | None = None,
    ca_base: str | Path | None = None,
):
    paths = get_default_paths()
    g6_dir = Path(g6_base) if g6_base else paths.g6 / f"{k}_caminhos_g6"
    ca_dir = Path(ca_base) if ca_base else paths.ca / f"CA_{k}_path_graph"
    ca_dir.mkdir(parents=True, exist_ok=True)

    expected = int(T_n_k(n, k))
    g6_path = g6_dir / f"{k}_caminhos_n_{n}_T_{expected}.g6"
    ca_file = ca_dir / f"{k}_CAs_n_{n}.txt"

    values = []
    with open(g6_path, "r", encoding="utf-8") as infile, open(ca_file, "w", encoding="utf-8") as outfile:
        for raw_line in infile:
            line = raw_line.strip()
            if not line:
                continue
            graph = nx.from_graph6_bytes(line.encode("utf-8"))
            ca_val = float(nx.algebraic_connectivity(graph))
            values.append(ca_val)
            outfile.write(f"{ca_val:.20f}\n")

    if not values:
        raise RuntimeError(f"Arquivo .g6 vazio ou inválido: {g6_path}")

    max_ca = max(values)
    min_ca = min(values)
    pos_max = values.index(max_ca)
    pos_min = values.index(min_ca)

    return {
        "n": n,
        "path": ca_file,
        "expected": expected,
        "observed": len(values),
        "match": len(values) == expected,
        "max_ca": max_ca,
        "min_ca": min_ca,
        "pos_max": pos_max,
        "pos_min": pos_min,
    }


def verify_algebraic_connectivity_all_stream(
    k: int,
    Nf: int,
    g6_base: str | Path | None = None,
    ca_base: str | Path | None = None,
    list_output_path: str | Path | None = None,
):
    paths = get_default_paths()
    ca_root = Path(ca_base) if ca_base else paths.ca / f"CA_{k}_path_graph"
    ca_root.mkdir(parents=True, exist_ok=True)

    lines = []
    details = []
    for i in range(k * 2 + 2, Nf + 1):
        info = verify_algebraic_connectivity_one_stream(i, k, g6_base=g6_base, ca_base=ca_root)
        details.append(info)
        lines.append(
            f"N({i}) 3_max_CA({info['max_ca']}) pos_elemento_max_CA({info['pos_max']}) | "
            f"min_CA({info['min_ca']}) pos_elemento_min_CA({info['pos_min']})  \n"
        )

    if list_output_path:
        list_path = Path(list_output_path)
    else:
        list_path = paths.ca / f"{k}_CA_lista.txt"

    with open(list_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return {"list_path": list_path, "details": details}

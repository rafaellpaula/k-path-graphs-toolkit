from __future__ import annotations

from pathlib import Path

import networkx as nx
import numpy as np

from .generators import T_n_k
from .paths import get_default_paths


def toAdjacenceMatrix(L, k: int):
    B = [int(i) for i in range(1, k + 2)]
    juncao = np.concatenate((B, L))
    n = len(L) + len(B)
    matrix = np.zeros((n, n))
    for element in range(len(juncao) - 1, -1, -1):
        conjuntoPath = B.copy()
        conjuntoAux = [juncao[element]]
        for j in range(element - 1, -1, -1):
            if set(conjuntoAux) != set(conjuntoPath):
                if juncao[j] not in conjuntoAux:
                    conjuntoAux.append(juncao[j])
                    matrix[element][j] = 1
                    matrix[j][element] = 1
    return matrix


def coloredToAdjacence(pasta_origem: str | Path, nameArchive: str, k: int, pasta_destino: str | Path | None = None):
    paths = get_default_paths()
    origem = Path(pasta_origem)
    destino = Path(pasta_destino) if pasta_destino else paths.g6 / f"{k}_caminhos_g6"
    destino.mkdir(parents=True, exist_ok=True)

    listColor = np.loadtxt(origem / f"{k}_{nameArchive}.txt")
    conjuntoG = []

    for l in listColor:
        G = toAdjacenceMatrix(l, k)
        grafo = nx.Graph(G)
        g6Format = nx.to_graph6_bytes(grafo).decode("utf-8")
        conjuntoG.append(g6Format)

    caminho_completo = destino / f"{k}_{nameArchive}.g6"
    with open(caminho_completo, "w", encoding="utf-8") as arquivo:
        for item in conjuntoG:
            arquivo.write(item + "\n")

    return caminho_completo


def generateOneG6(N: int, k: int, pasta_origem: str | Path | None = None, pasta_destino: str | Path | None = None):
    paths = get_default_paths()
    origem = Path(pasta_origem) if pasta_origem else paths.sequences / f"{k}_caminhos"

    valueTNK = int(T_n_k(N, k))
    nome_arquivo = f"caminhos_n_{N}_T_{valueTNK}"
    return coloredToAdjacence(origem, nome_arquivo, k, pasta_destino=pasta_destino)


def generateG6Archives(N: int, k: int, pasta_origem: str | Path | None = None, pasta_destino: str | Path | None = None):
    paths = get_default_paths()
    origem = Path(pasta_origem) if pasta_origem else paths.sequences / f"{k}_caminhos"
    destino = Path(pasta_destino) if pasta_destino else paths.g6 / f"{k}_caminhos_g6"
    destino.mkdir(parents=True, exist_ok=True)

    outputs = []
    for i in range(k * 2 + 2, N + 1):
        valueTNK = int(T_n_k(i, k))
        outputs.append(
            coloredToAdjacence(origem, f"caminhos_n_{i}_T_{valueTNK}", k, pasta_destino=destino)
        )
    return outputs


def remover_linhas_em_branco_g6(pasta: str | Path, recursivo: bool = False):
    arquivos_processados = 0
    pasta = Path(pasta)

    for raiz, _, arquivos in __import__("os").walk(pasta):
        for nome in arquivos:
            if nome.endswith(".g6"):
                caminho = Path(raiz) / nome

                with open(caminho, "r", encoding="utf-8") as f:
                    linhas = f.readlines()

                linhas_limpas = [linha.strip() for linha in linhas if linha.strip()]

                with open(caminho, "w", encoding="utf-8") as f:
                    for linha in linhas_limpas:
                        f.write(linha + "\n")

                arquivos_processados += 1

        if not recursivo:
            break

    return arquivos_processados


def coloredToAdjacence_stream(
    pasta_origem: str | Path,
    nameArchive: str,
    k: int,
    pasta_destino: str | Path | None = None,
):
    paths = get_default_paths()
    origem = Path(pasta_origem)
    destino = Path(pasta_destino) if pasta_destino else paths.g6 / f"{k}_caminhos_g6"
    destino.mkdir(parents=True, exist_ok=True)

    in_path = origem / f"{k}_{nameArchive}.txt"
    out_path = destino / f"{k}_{nameArchive}.g6"

    total = 0
    with open(in_path, "r", encoding="utf-8") as infile, open(out_path, "w", encoding="utf-8") as outfile:
        for raw_line in infile:
            line = raw_line.strip()
            if not line:
                continue

            l = np.fromstring(line, dtype=int, sep=" ")
            G = toAdjacenceMatrix(l, k)
            grafo = nx.Graph(G)
            g6Format = nx.to_graph6_bytes(grafo).decode("utf-8").strip()
            outfile.write(g6Format + "\n")
            total += 1

    return out_path, total


def generateOneG6_stream(
    N: int,
    k: int,
    pasta_origem: str | Path | None = None,
    pasta_destino: str | Path | None = None,
):
    paths = get_default_paths()
    origem = Path(pasta_origem) if pasta_origem else paths.sequences / f"{k}_caminhos"

    valueTNK = int(T_n_k(N, k))
    nome_arquivo = f"caminhos_n_{N}_T_{valueTNK}"
    out_path, total = coloredToAdjacence_stream(origem, nome_arquivo, k, pasta_destino=pasta_destino)
    return {"path": out_path, "observed": total, "expected": valueTNK, "match": total == valueTNK}


def generateG6Archives_stream(
    N: int,
    k: int,
    pasta_origem: str | Path | None = None,
    pasta_destino: str | Path | None = None,
):
    paths = get_default_paths()
    origem = Path(pasta_origem) if pasta_origem else paths.sequences / f"{k}_caminhos"
    destino = Path(pasta_destino) if pasta_destino else paths.g6 / f"{k}_caminhos_g6"
    destino.mkdir(parents=True, exist_ok=True)

    outputs = []
    for i in range(k * 2 + 2, N + 1):
        valueTNK = int(T_n_k(i, k))
        nome = f"caminhos_n_{i}_T_{valueTNK}"
        out_path, total = coloredToAdjacence_stream(origem, nome, k, pasta_destino=destino)
        outputs.append(
            {
                "n": i,
                "path": out_path,
                "expected": valueTNK,
                "observed": total,
                "match": total == valueTNK,
            }
        )
    return outputs

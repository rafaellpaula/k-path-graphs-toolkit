from __future__ import annotations

import time
from functools import lru_cache
from pathlib import Path
import numpy as np

from .paths import get_default_paths


def maxI(sequencia: list[int], k: int):
    maiorI = valor = -1
    if not sequencia:
        return False, False

    max_prefix = sequencia[0]
    x = 1
    for i in sequencia[1:]:
        prev = sequencia[x - 1]
        a = i + 2 if prev == (i + 1) else i + 1
        b = min(max_prefix + 1, k + 1)

        if a <= b:
            maiorI = x
            valor = a

        if i > max_prefix:
            max_prefix = i

        x = x + 1
    if maiorI == -1 and valor == -1:
        return False, False
    return valor, maiorI


def step2_A(sequencia: list[int], valor: int, posicao: int):
    sequencia[posicao] = valor
    if len(sequencia[posicao:]) > 0:
        acrescimo = [2 if i % 2 else 1 for i in range(len(sequencia[posicao + 1 :]))]
        sequencia[posicao + 1 :] = acrescimo


def step2_B(sequencia: list[int]):
    copia = list(reversed(sequencia))
    retrita_e_normalizada, sequencia_normalizada = normaliza_reversa_e_verifica_restrita(copia)

    if retrita_e_normalizada is False:
        return []

    return sequencia_normalizada


def step2_C(sequenciaA: list[int], sequenciaB: list[int]):
    if sequenciaA <= sequenciaB or sequenciaB == []:
        return True
    return False


def nomalizado(sequencia: list[int]):
    if sequencia[0] == 1:
        for i in range(1, len(sequencia)):
            if sequencia[i] <= 1 + max(sequencia[:i]):
                pass
            else:
                return False
        return True
    else:
        return False


def restrito(sequencia: list[int]):
    for i in range(1, len(sequencia) - 1):
        if sequencia[i - 1] != sequencia[i]:
            pass
        else:
            return False
    return True


def normaliza_reversa_e_verifica_restrita(sequencia: list[int]):
    sequencia = sequencia.copy()
    troca: dict[int, int] = {}
    maximo_da_sequencia = 1
    if nomalizado(sequencia) and restrito(sequencia):
        return True, sequencia

    if sequencia[0] == 1:
        troca[1] = 1
    else:
        troca[sequencia[0]] = 1
        sequencia[0] = 1

    for i in range(1, len(sequencia[1:]) + 1):
        if sequencia[i] in troca:
            sequencia[i] = troca[sequencia[i]]
        else:
            maximo_da_sequencia += 1
            troca[sequencia[i]] = maximo_da_sequencia
            sequencia[i] = maximo_da_sequencia

        if sequencia[i] == sequencia[i - 1]:
            return False, sequencia

    sequencia_normalizada_e_restrita = restrito(sequencia)
    return sequencia_normalizada_e_restrita, sequencia


def generating_all_unlabeled_k_path_graph(k: int, n: int):
    sequencia = [2 if i % 2 else 1 for i in range(n - k - 1)]
    T_list = [sequencia.copy()]
    T_set = {tuple(sequencia)}

    while True:
        valor, posicao = maxI(sequencia, k)

        if not (valor and posicao):
            return T_list
        step2_A(sequencia, valor, posicao)
        sequenciaReversa = step2_B(sequencia)
        if step2_C(sequencia, sequenciaReversa):
            novo = tuple(sequencia)

            if novo in T_set:
                return T_list
            else:
                T_list.append(sequencia.copy())
                T_set.add(novo)


def iter_unlabeled_k_path_graph_sequences(k: int, n: int):
    sequencia = [2 if i % 2 else 1 for i in range(n - k - 1)]
    total_expected = int(T_n_k(n, k))

    if total_expected <= 0:
        return

    yielded = 0
    seen = {tuple(sequencia)}
    yield sequencia.copy()
    yielded += 1

    while yielded < total_expected:
        valor, posicao = maxI(sequencia, k)
        if not (valor and posicao):
            break

        step2_A(sequencia, valor, posicao)
        sequenciaReversa = step2_B(sequencia)

        if step2_C(sequencia, sequenciaReversa):
            novo = tuple(sequencia)
            if novo in seen:
                break

            seen.add(novo)
            yield sequencia.copy()
            yielded += 1

    if yielded != total_expected:
        raise RuntimeError(
            f"Stream interrompido antes do esperado para (k={k}, n={n}). "
            f"Gerado={yielded}, esperado={total_expected}."
        )


def _cacheable_M(n: int, k: int):
    if n == 2 * k + 2:
        return 1
    if n < 2 * k + 2 or k < 1:
        return 0
    return k * _cacheable_M(n - 2, k) + _cacheable_M(n - 3, k - 1) + _cacheable_M(n - 4, k - 2)


def _cacheable_N(n: int, k: int):
    if n < 2 * k + 2 or k < 1:
        return 0
    if k == 1:
        return 0
    parte1 = k**2 * _cacheable_N(n - 2, k)
    parte2 = (2 * k - 1) * _cacheable_N(n - 3, k - 1)
    parte3 = _cacheable_N(n - 4, k - 2)
    parte4 = (k * (k - 1) // 2) * _cacheable_M(n - 2, k)
    parte5 = (k - 1) * _cacheable_M(n - 3, k - 1)
    return parte1 + parte2 + parte3 + parte4 + parte5


def _cacheable_T_n_k(n: int, k: int):
    if n < k + 1:
        return 0
    if k == 1:
        return 1
    return _cacheable_T_n_k(n - 1, k - 1) + _cacheable_M(n, k) + _cacheable_N(n, k)


_cacheable_M = lru_cache(maxsize=None)(_cacheable_M)
_cacheable_N = lru_cache(maxsize=None)(_cacheable_N)
_cacheable_T_n_k = lru_cache(maxsize=None)(_cacheable_T_n_k)


def M(n: int, k: int):
    return _cacheable_M(n, k)


def N(n: int, k: int):
    return _cacheable_N(n, k)


def T_n_k(n: int, k: int):
    return _cacheable_T_n_k(n, k)


def gerarSequenciaN(N: int, kValue: int, pasta_destino: str | Path | None = None):
    paths = get_default_paths()
    destination = Path(pasta_destino) if pasta_destino else paths.sequences / f"{kValue}_caminhos"
    destination.mkdir(parents=True, exist_ok=True)

    k = kValue
    T = generating_all_unlabeled_k_path_graph(k, N)
    arr = np.array(T)

    valueTNK = int(T_n_k(N, k))
    if valueTNK == len(arr):
        nome_arquivo = f"{k}_caminhos_n_{N}_T_{valueTNK}.txt"
        caminho_completo = destination / nome_arquivo
        np.savetxt(caminho_completo, arr, fmt="%i")
        return caminho_completo
    return None


def gerarNSequencias(I: int, F: int, kValue: int, pasta_destino: str | Path | None = None):
    tempos: dict[int, float] = {}
    total_inicio = time.time()

    for i in range(I, F):
        inicio = time.time()
        gerarSequenciaN(i, kValue, pasta_destino=pasta_destino)
        duracao = time.time() - inicio
        tempos[i] = duracao

    total = time.time() - total_inicio
    return {"tempos": tempos, "total": total}


def gerarSequenciaN_stream(N: int, kValue: int, pasta_destino: str | Path | None = None):
    paths = get_default_paths()
    destination = Path(pasta_destino) if pasta_destino else paths.sequences / f"{kValue}_caminhos_stream"
    destination.mkdir(parents=True, exist_ok=True)

    k = kValue
    expected = int(T_n_k(N, k))
    nome_arquivo = f"{k}_caminhos_n_{N}_T_{expected}.txt"
    caminho_completo = destination / nome_arquivo

    count = 0
    with open(caminho_completo, "w", encoding="utf-8") as f:
        for seq in iter_unlabeled_k_path_graph_sequences(k, N):
            f.write(" ".join(map(str, seq)) + "\n")
            count += 1

    return {
        "path": caminho_completo,
        "expected": expected,
        "observed": count,
        "match": expected == count,
    }


def gerarNSequencias_stream(I: int, F: int, kValue: int, pasta_destino: str | Path | None = None):
    tempos: dict[int, float] = {}
    detalhes: dict[int, dict] = {}
    total_inicio = time.time()

    for i in range(I, F):
        inicio = time.time()
        info = gerarSequenciaN_stream(i, kValue, pasta_destino=pasta_destino)
        duracao = time.time() - inicio
        tempos[i] = duracao
        detalhes[i] = info

    total = time.time() - total_inicio
    return {"tempos": tempos, "detalhes": detalhes, "total": total}

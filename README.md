# k-path-graphs-toolkit

Toolkit de Grafos k-Caminhos: Gerador e Analisador.

Este repositorio contem uma implementacao para gerar grafos k-caminhos nao rotulados e dois a dois nao isomorfos, exporta-los em formato Graph6 e calcular a conectividade algebrica de cada grafo gerado.

O projeto esta organizado como um pipeline reprodutivel:

1. Gerar sequencias coloridas canonicas para `(k, n)` fixos.
2. Converter as sequencias em grafos e exportar para `.g6`.
3. Calcular a conectividade algebrica (`lambda_2`) de cada grafo.

## Fundamentacao Matematica

As funcoes de contagem sao baseadas em relacoes recursivas usadas na enumeracao de grafos k-caminhos nao rotulados:

```text
M(n,k) = k*M(n-2,k) + M(n-3,k-1) + M(n-4,k-2)
N(n,k) = k^2*N(n-2,k) + (2k-1)*N(n-3,k-1) + N(n-4,k-2)
         + (k(k-1)/2)*M(n-2,k) + (k-1)*M(n-3,k-1)
T(n,k) = T(n-1,k-1) + M(n,k) + N(n,k)
```

`T(n,k)` e usado como referencia de validacao durante a geracao e a conversao.

## Estrutura do Repositorio

```text
src/
  generators.py          geracao de sequencias (modo lista e stream)
  converters.py          conversao TXT -> Graph6
  analyzers.py           calculo de conectividade algebrica
  paths.py               caminhos padrao de saida

notebooks/
  generate_and_analyze_k_path_graphs.ipynb

data/
  sequences/
  g6/
  algebraic_connectivity/
```

## Instalacao

```bash
git clone <url-do-repositorio>
cd k-path-graphs-toolkit

python3 -m venv venv_grafos
source venv_grafos/bin/activate

pip install -r requirements.txt
```

## Uso

O fluxo principal reprodutivel esta disponivel em:

`notebooks/generate_and_analyze_k_path_graphs.ipynb`

O notebook esta configurado para execucao iterativa (com logica de `skip`), permitindo retomar execucoes parcialmente concluidas.

## Exemplo Programatico

```python
from src.generators import T_n_k, gerarSequenciaN_stream
from src.converters import generateOneG6_stream
from src.analyzers import verify_algebraic_connectivity_one_stream

k = 2
n = 10

esperado = int(T_n_k(n, k))
print(f"Objetos esperados para (n={n}, k={k}): {esperado}")

# 1) geracao de sequencias
gerarSequenciaN_stream(n, k, "data/sequences/2_caminhos")

# 2) conversao para Graph6
generateOneG6_stream(n, k, "data/sequences", "data/g6")

# 3) conectividade algebrica
verify_algebraic_connectivity_one_stream(n, k, "data/g6", "data/algebraic_connectivity")
```

## Arquivos de Saida

- Sequencias: `data/sequences/{k}_caminhos/{k}_caminhos_n_{n}_T_{T}.txt`
- Graph6: `data/g6/{k}_caminhos_g6/{k}_caminhos_n_{n}_T_{T}.g6`
- Conectividade algebrica: `data/algebraic_connectivity/CA_{k}_path_graph/ca_n_{n}.txt`
- Listas consolidadas: `data/algebraic_connectivity/{k}_CA_lista.txt`

## Observacoes de Desempenho

- As funcoes em modo stream sao recomendadas para valores grandes de `n`.
- Tempo de execucao e armazenamento crescem rapidamente com `n`, especialmente para `k=2` em ordens maiores.
- O fluxo do notebook foi desenhado para evitar recomputacao de saidas existentes.

## Referencias e Links Uteis

- Referencia do formato Graph6: http://users.cecs.anu.edu.au/~bdm/data/formats.html

Se voce pretende citar a base teorica desta implementacao, adicione aqui as referencias do artigo desejado.

## Licenca

A definicao da licenca esta pendente.

# Sistema de Otimização de Logística

Projeto da disciplina de Projeto e Análise de Algoritmos (UnB). Sistema simplificado de logística para uma transportadora, que integra três algoritmos de otimização (Knapsack, Minimize Lateness e Caminhoneiro) para planejar o transporte e a entrega de pedidos.

## Dupla

| Nome | Matrícula |
|---|---|
| Maria Clara Oleari de Araujo | 221008338 |
| Ana Júlia Mendes Santos | 221007798 |


## Descrição do problema

O sistema simula o planejamento logístico de uma transportadora: existe um **caminhão** com capacidade de carga e autonomia limitadas, vários **pedidos** com pesos, valores e prazos diferentes, e **postos de abastecimento** ao longo da rota. A partir desses dados, o sistema responde a três perguntas, cada uma resolvida por um algoritmo:

```
1. Quais pedidos devemos levar?   → KNAPSACK
2. Em qual ordem devemos entregar? → MINIMIZE LATENESS
3. Onde devemos abastecer?         → CAMINHONEIRO
```

Fluxo do sistema:

```
Pedidos → KNAPSACK → MINIMIZE LATENESS → CAMINHONEIRO → PLANO LOGÍSTICO
```

O resultado final apresenta as **cargas selecionadas, o valor total, a ordem das entregas, os atrasos e a quantidade de paradas para abastecimento**.

### Entrada

- **Pedidos:** id, peso, valor, prazo e distância
- **Caminhão:** capacidade de carga, autonomia e velocidade (converte a distância do pedido em tempo de entrega)
- **Rota:** destino e distância de cada posto na rota

Arquivo JSON, com exemplo em `data/exemplo.json`. Detalhes em [docs/formato-de-entrada.md](docs/formato-de-entrada.md).

### Algoritmos usados e por quê

| Etapa | Algoritmo | Estratégia | Por que é adequado |
|---|---|---|---|
| Seleção das cargas | Knapsack 0/1 | Guloso (maior valor/peso primeiro) | Escolhe sempre o pedido mais "rentável" por kg que ainda cabe; é rápido, mas no 0/1 não garante o ótimo (a DP serve de referência) |
| Ordem das entregas | Minimize Lateness | Guloso (Earliest Deadline First) | Ordenar por prazo crescente minimiza o maior atraso (prova por argumento de troca) |
| Paradas de abastecimento | Caminhoneiro | Guloso | Seguir até o posto mais distante ainda alcançável minimiza o número de paradas |

Cada algoritmo tem uma **versão principal** e uma **versão alternativa**, usada para comparação (por exemplo, a programação dinâmica no Knapsack, que é ótima e mostra quanto valor o guloso perde).

### Complexidade

| Algoritmo | Tempo | Espaço |
|---|---|---|
| Knapsack (guloso) | `O(n log n)` | `O(n)` |
| Knapsack (DP, referência) | `O(n·W)` | `O(n·W)` para reconstruir os pedidos escolhidos |
| Minimize Lateness (EDF) | `O(n log n)` | `O(n)` |
| Caminhoneiro (guloso) | `O(n)` com postos ordenados (`O(n log n)` se precisar ordenar) | `O(k)`, com `k` = número de paradas |

Onde `n` é o número de pedidos (ou postos) e `W` é a capacidade do caminhão. Detalhamento e resultados experimentais (10, 100, 1.000 e 10.000 pedidos) no relatório em [docs/](docs/).

## Estrutura do repositório

```
G1_Greedy_PA-26.2/
├── src/
│   ├── main.py          # fluxo completo: pedidos -> knapsack -> lateness -> caminhoneiro
│   ├── modelos.py       # tipos (Pedido, Caminhao, Rota, Entrega) e leitura da entrada
│   ├── knapsack.py      # Knapsack (guloso) + DP de referência
│   ├── lateness.py      # Minimize Lateness (EDF) + alternativa
│   ├── caminhoneiro.py  # Caminhoneiro (guloso) + alternativa
│   └── benchmark.py     # experimentos de tempo (n = 10, 100, 1.000, 10.000)
├── data/
│   └── exemplo.json     # exemplo de entrada (pedidos, caminhão, rota com postos)
├── tests/               # casos de teste de cada algoritmo
├── docs/
│   └── plano-de-commits-sistema-logistica.md  # plano de commits
├── LICENSE
└── README.md
```

## Como instalar

```bash
cd G1_Greedy_PA-26.2
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Como rodar

```bash
python src/main.py
```

Roda o fluxo completo com os dados de `data/exemplo` e imprime o plano logístico no terminal.

Benchmark — mede o tempo de cada algoritmo (versão principal e alternativa) para `n` = 10, 100, 1.000 e 10.000 pedidos:

```bash
python src/benchmark.py
```

## Como rodar os testes

```bash
pytest tests/ -v
```

## Cronograma

O plano de commits detalhado está em [docs/plano-de-commits-sistema-logistica.md](docs/plano-de-commits-sistema-logistica.md).

## Relatório e vídeo de apresentação

- Formato de entrada: [docs/formato-de-entrada.md](docs/formato-de-entrada.md)
- Plano e análise de cada algoritmo (estratégia, complexidade, alternativa): [docs/](docs/)
- Vídeo de apresentação: _a ser adicionado_

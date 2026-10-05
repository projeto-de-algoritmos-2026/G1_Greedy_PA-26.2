# Assinaturas das funções

Contrato de cada algoritmo, combinado entre Maria Clara e Ana Júlia. Os tipos (`Pedido`, `Caminhao`, `Rota`, `Entrega`) ficam em [src/modelos.py](../src/modelos.py); o formato do arquivo de entrada está em [formato-de-entrada.md](formato-de-entrada.md).

Cada algoritmo tem uma **versão principal** (gulosa, usada pelo `main.py`) e uma **alternativa**, usada só na comparação do benchmark.

## Algoritmos

| Módulo | Função | Papel | Entrada | Saída |
|---|---|---|---|---|
| `knapsack` | `knapsack_guloso` | principal | `pedidos`, `capacidade` | `list[Pedido]` selecionados |
| `knapsack` | `knapsack_dp` | alternativa (ótima) | `pedidos`, `capacidade` | `list[Pedido]` selecionados |
| `lateness` | `minimize_lateness` | principal (EDF) | `pedidos`, `caminhao` | `list[Entrega]` na ordem de entrega |
| `lateness` | `lateness_fifo` | alternativa | `pedidos`, `caminhao` | `list[Entrega]` na ordem de chegada |
| `lateness` | `maior_atraso` | auxiliar | `entregas` | `float` (0 se ninguém atrasar) |
| `caminhoneiro` | `caminhoneiro_guloso` | principal | `rota`, `autonomia` | `list[float]` com a posição (km) dos postos escolhidos |
| `caminhoneiro` | `caminhoneiro_todos_os_postos` | alternativa | `rota`, `autonomia` | `list[float]` com todos os postos |

`Entrega` tem três campos: `pedido`, `conclusao` (horas desde o início da rota) e `atraso` (`max(0, conclusao - prazo)`). O tempo de cada entrega é `distancia / velocidade` (`tempo_entrega` em `modelos.py`), e as entregas acontecem em sequência, sem tempo ocioso.

## Fluxo principal

`planejar(pedidos, caminhao, rota)` em [src/main.py](../src/main.py) encadeia os três algoritmos e devolve um `Plano`:

```
pedidos ──► knapsack_guloso ──► cargas ──► minimize_lateness ──► entregas
rota    ──► caminhoneiro_guloso ──► paradas
```

| Campo de `Plano` | Origem |
|---|---|
| `cargas` | `knapsack_guloso(pedidos, caminhao.capacidade)` |
| `valor_total` | soma dos valores das `cargas` |
| `entregas` | `minimize_lateness(cargas, caminhao)` (só as cargas selecionadas) |
| `maior_atraso` | `maior_atraso(entregas)` |
| `paradas` | `caminhoneiro_guloso(rota, caminhao.autonomia)` |

## Erros

| Situação | Erro |
|---|---|
| Capacidade negativa (knapsack) | `ValueError` |
| Peso de pedido menor ou igual a zero (knapsack) | `ValueError` |
| Peso ou capacidade fracionário em `knapsack_dp` (a DP usa unidades inteiras) | `ValueError` |
| Velocidade do caminhão menor ou igual a zero, ou distância negativa (lateness) | `ValueError` |
| Autonomia menor ou igual a zero, destino negativo ou posto fora do trecho entre o início e o destino (caminhoneiro) | `ValueError` |
| Postos insuficientes para chegar ao destino (caminhoneiro) | `ValueError` |

`main.py` captura o `ValueError` do fluxo e imprime "Não foi possível montar o plano", em vez de encerrar com erro.

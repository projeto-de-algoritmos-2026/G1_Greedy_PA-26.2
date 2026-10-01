# Formato de entrada

Combinado entre Maria Clara e Ana Júlia no commit de 30/09. Os tipos ficam em [src/modelos.py](../src/modelos.py).

## Formato de entrada

Arquivo JSON (exemplo em [data/exemplo.json](../data/exemplo.json)):

```json
{
  "pedidos": [
    {"id": "A", "peso": 100, "valor": 500, "prazo": 8, "distancia": 180}
  ],
  "caminhao": {"capacidade": 300, "autonomia": 200, "velocidade": 60},
  "rota": {"destino": 500, "postos": [80, 170, 250, 330, 410]}
}
```

| Campo | Unidade | Significado |
|---|---|---|
| `pedidos[].id` | - | identificador do pedido |
| `pedidos[].peso` | kg | usado pelo Knapsack |
| `pedidos[].valor` | R$ | usado pelo Knapsack |
| `pedidos[].prazo` | horas | prazo de entrega, usado pelo Minimize Lateness |
| `pedidos[].distancia` | km | distância até o cliente; vira tempo de entrega (ver abaixo) |
| `caminhao.capacidade` | kg | capacidade de carga (Knapsack) |
| `caminhao.autonomia` | km | distância máxima entre abastecimentos (Caminhoneiro) |
| `caminhao.velocidade` | km/h | converte distância em tempo de entrega |
| `rota.destino` | km | tamanho total da rota (Caminhoneiro) |
| `rota.postos` | km | posição de cada posto ao longo da rota |

**Tempo de entrega:** o Minimize Lateness precisa de um tempo por pedido, mas a entrada traz distância. Por isso `tempo = distancia / velocidade` (função `tempo_entrega` em `modelos.py`). No exemplo, com 60 km/h, os pedidos A, B e C levam 3h, 1h e 2h.

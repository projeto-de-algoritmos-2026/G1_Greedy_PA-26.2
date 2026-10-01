"""Knapsack 0/1: escolhe quais pedidos levar (maximiza o valor sem passar da capacidade).

Entrada:  lista de Pedido e a capacidade do caminhao (kg).
Saida:    lista com os Pedido selecionados.
"""

from modelos import Pedido


def knapsack_guloso(pedidos: list[Pedido], capacidade: float) -> list[Pedido]:
    """Versao principal: guloso por valor/peso, O(n log n). Rapido, mas nao garante o otimo."""
    raise NotImplementedError("knapsack_guloso: implementar (01/10, Ana Julia)")


def knapsack_dp(pedidos: list[Pedido], capacidade: float) -> list[Pedido]:
    """Versao alternativa (referencia): programacao dinamica, O(n*W). Solucao otima, para comparar."""
    raise NotImplementedError("knapsack_dp: implementar (01/10, Ana Julia)")

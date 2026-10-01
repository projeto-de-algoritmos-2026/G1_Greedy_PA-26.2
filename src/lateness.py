"""Minimize Lateness: define a ordem das entregas minimizando o maior atraso.

Entrada:  lista de Pedido e o Caminhao (a velocidade converte distancia em tempo).
Saida:    lista de Entrega na ordem em que os pedidos serao entregues.
"""

from modelos import Caminhao, Entrega, Pedido


def minimize_lateness(pedidos: list[Pedido], caminhao: Caminhao) -> list[Entrega]:
    """Versao principal: guloso Earliest Deadline First, O(n log n) tempo, O(n) espaco."""
    raise NotImplementedError("minimize_lateness: implementar (02/10, Ana Julia)")


def lateness_fifo(pedidos: list[Pedido], caminhao: Caminhao) -> list[Entrega]:
    """Versao alternativa: ordem de chegada (FIFO), para comparar o maior atraso."""
    raise NotImplementedError("lateness_fifo: implementar (02/10, Ana Julia)")

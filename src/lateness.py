"""Minimize Lateness: define a ordem das entregas minimizando o maior atraso.

Entrada:  lista de Pedido e o Caminhao (a velocidade converte distancia em tempo).
Saida:    lista de Entrega na ordem em que os pedidos serao entregues.
"""

from modelos import Caminhao, Entrega, Pedido, tempo_entrega


def minimize_lateness(pedidos: list[Pedido], caminhao: Caminhao) -> list[Entrega]:
    """Versao principal: guloso Earliest Deadline First, O(n log n) tempo, O(n) espaco."""
    # Earliest Deadline First: pedidos com o menor prazo sao processados antes.
    # A ordenacao e estavel, portanto prazos iguais preservam a ordem de entrada.
    pedidos_por_prazo = sorted(pedidos, key=lambda pedido: pedido.prazo)
    return _montar_entregas(pedidos_por_prazo, caminhao)


def lateness_fifo(pedidos: list[Pedido], caminhao: Caminhao) -> list[Entrega]:
    """Versao alternativa: ordem de chegada (FIFO), para comparar o maior atraso."""
    return _montar_entregas(pedidos, caminhao)


def _montar_entregas(pedidos: list[Pedido], caminhao: Caminhao) -> list[Entrega]:
    """Calcula conclusao e atraso de uma ordem de pedidos, sem tempo ocioso."""
    if caminhao.velocidade <= 0:
        raise ValueError("a velocidade do caminhao deve ser positiva")

    entregas: list[Entrega] = []
    tempo_atual = 0.0

    for pedido in pedidos:
        duracao = tempo_entrega(pedido, caminhao)
        if duracao < 0:
            raise ValueError(f"a distancia do pedido {pedido.id} nao pode ser negativa")

        tempo_atual += duracao
        atraso = max(0.0, tempo_atual - pedido.prazo)
        entregas.append(
            Entrega(
                pedido=pedido,
                conclusao=tempo_atual,
                atraso=atraso,
            )
        )

    return entregas

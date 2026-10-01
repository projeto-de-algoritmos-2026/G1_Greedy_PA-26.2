"""Knapsack 0/1: escolhe quais pedidos levar (maximiza o valor sem passar da capacidade).

Entrada:  lista de Pedido e a capacidade do caminhao (kg).
Saida:    lista com os Pedido selecionados.
"""

from modelos import Pedido


def knapsack_guloso(pedidos: list[Pedido], capacidade: float) -> list[Pedido]:
    """Versao principal: guloso por valor/peso, O(n log n). Rapido, mas nao garante o otimo."""
    _validar_entrada(pedidos, capacidade)

    # A ordenacao do Python e estavel: em caso de empate, a ordem de entrada
    # dos pedidos e preservada.
    pedidos_ordenados = sorted(
        pedidos,
        key=lambda pedido: pedido.valor / pedido.peso,
        reverse=True,
    )

    selecionados: list[Pedido] = []
    peso_total = 0.0

    for pedido in pedidos_ordenados:
        if peso_total + pedido.peso <= capacidade:
            selecionados.append(pedido)
            peso_total += pedido.peso

    return selecionados


def knapsack_dp(pedidos: list[Pedido], capacidade: float) -> list[Pedido]:
    """Versao alternativa (referencia): programacao dinamica, O(n*W). Solucao otima, para comparar."""
    _validar_entrada(pedidos, capacidade)

    capacidade_inteira = _como_inteiro(capacidade, "capacidade")
    pesos = [_como_inteiro(pedido.peso, f"peso do pedido {pedido.id}") for pedido in pedidos]

    # tabela[i][w] guarda o maior valor usando os i primeiros pedidos e
    # capacidade w. A tabela completa permite reconstruir os escolhidos.
    tabela = [[0.0] * (capacidade_inteira + 1) for _ in range(len(pedidos) + 1)]

    for i, pedido in enumerate(pedidos, start=1):
        peso = pesos[i - 1]
        for limite in range(capacidade_inteira + 1):
            sem_pedido = tabela[i - 1][limite]
            if peso > limite:
                tabela[i][limite] = sem_pedido
                continue

            com_pedido = pedido.valor + tabela[i - 1][limite - peso]
            tabela[i][limite] = max(sem_pedido, com_pedido)

    selecionados: list[Pedido] = []
    limite = capacidade_inteira

    for i in range(len(pedidos), 0, -1):
        if tabela[i][limite] != tabela[i - 1][limite]:
            selecionados.append(pedidos[i - 1])
            limite -= pesos[i - 1]

    selecionados.reverse()
    return selecionados


def _validar_entrada(pedidos: list[Pedido], capacidade: float) -> None:
    if capacidade < 0:
        raise ValueError("a capacidade nao pode ser negativa")

    for pedido in pedidos:
        if pedido.peso <= 0:
            raise ValueError(f"o peso do pedido {pedido.id} deve ser positivo")


def _como_inteiro(valor: float, nome: str) -> int:
    """A DP O(n*W) usa peso e capacidade medidos em unidades inteiras."""
    valor_inteiro = int(valor)
    if valor != valor_inteiro:
        raise ValueError(f"{nome} deve ser inteiro para o knapsack por DP")
    return valor_inteiro

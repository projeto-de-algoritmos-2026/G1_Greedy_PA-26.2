"""Caminhoneiro: escolhe os postos de abastecimento minimizando o numero de paradas.

Entrada:  Rota (destino e posicao dos postos) e a autonomia do caminhao (km).
Saida:    lista com a posicao (km) dos postos em que o caminhao para.
          Levanta ValueError se os postos nao permitem chegar ao destino.
"""

from modelos import Rota


def caminhoneiro_guloso(rota: Rota, autonomia: float) -> list[float]:
    """Versao principal: guloso, vai ate o posto mais distante alcancavel. O(n) com postos ordenados."""
    postos = _preparar_entrada(rota, autonomia)
    paradas: list[float] = []
    posicao_atual = 0.0
    indice = 0

    while rota.destino - posicao_atual > autonomia:
        posto_escolhido = posicao_atual

        # Avanca por todos os postos alcancaveis e guarda o mais distante.
        while indice < len(postos) and postos[indice] - posicao_atual <= autonomia:
            posto_escolhido = postos[indice]
            indice += 1

        if posto_escolhido == posicao_atual:
            raise ValueError("nao e possivel chegar ao destino com os postos disponiveis")

        paradas.append(posto_escolhido)
        posicao_atual = posto_escolhido

    return paradas


def caminhoneiro_todos_os_postos(rota: Rota, autonomia: float) -> list[float]:
    """Versao alternativa: abastece em todos os postos, para comparar o numero de paradas."""
    postos = _preparar_entrada(rota, autonomia)
    posicao_atual = 0.0

    for posto in postos:
        if posto - posicao_atual > autonomia:
            raise ValueError("nao e possivel chegar ao destino com os postos disponiveis")
        posicao_atual = posto

    if rota.destino - posicao_atual > autonomia:
        raise ValueError("nao e possivel chegar ao destino com os postos disponiveis")

    return postos


def _preparar_entrada(rota: Rota, autonomia: float) -> list[float]:
    if rota.destino < 0:
        raise ValueError("o destino nao pode ser negativo")
    if autonomia <= 0:
        raise ValueError("a autonomia deve ser positiva")

    for posto in rota.postos:
        if posto <= 0 or posto >= rota.destino:
            raise ValueError("os postos devem estar entre o inicio e o destino da rota")

    # A entrada normalmente ja vem ordenada. Se nao vier, a ordenacao faz a
    # complexidade passar de O(n) para O(n log n).
    postos = list(rota.postos)
    if any(atual > proximo for atual, proximo in zip(postos, postos[1:])):
        postos.sort()

    return postos

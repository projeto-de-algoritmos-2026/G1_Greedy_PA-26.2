"""Caminhoneiro: escolhe os postos de abastecimento minimizando o numero de paradas.

Entrada:  Rota (destino e posicao dos postos) e a autonomia do caminhao (km).
Saida:    lista com a posicao (km) dos postos em que o caminhao para.
          Levanta ValueError se os postos nao permitem chegar ao destino.
"""

from modelos import Rota


def caminhoneiro_guloso(rota: Rota, autonomia: float) -> list[float]:
    """Versao principal: guloso, vai ate o posto mais distante alcancavel. O(n) com postos ordenados."""
    raise NotImplementedError("caminhoneiro_guloso: implementar (03/10, Ana Julia)")


def caminhoneiro_todos_os_postos(rota: Rota, autonomia: float) -> list[float]:
    """Versao alternativa: abastece em todos os postos, para comparar o numero de paradas."""
    raise NotImplementedError("caminhoneiro_todos_os_postos: implementar (03/10, Ana Julia)")

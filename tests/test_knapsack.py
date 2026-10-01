import pytest

from knapsack import knapsack_dp, knapsack_guloso
from modelos import Pedido


def pedido(id: str, peso: float, valor: float) -> Pedido:
    return Pedido(id=id, peso=peso, valor=valor, prazo=0, distancia=0)


def ids(pedidos: list[Pedido]) -> list[str]:
    return [item.id for item in pedidos]


def test_knapsack_sem_pedidos():
    assert knapsack_guloso([], 100) == []
    assert knapsack_dp([], 100) == []


def test_guloso_ordena_por_valor_por_peso():
    pedidos = [
        pedido("A", 100, 500),
        pedido("B", 200, 800),
        pedido("C", 150, 700),
    ]

    assert ids(knapsack_guloso(pedidos, 300)) == ["A", "C"]


def test_dp_encontra_solucao_otima_do_contraexemplo():
    pedidos = [
        pedido("A", 100, 500),
        pedido("B", 200, 800),
        pedido("C", 150, 700),
    ]

    assert ids(knapsack_dp(pedidos, 300)) == ["A", "B"]


@pytest.mark.parametrize("algoritmo", [knapsack_guloso, knapsack_dp])
def test_todos_os_pedidos_cabem(algoritmo):
    pedidos = [pedido("A", 10, 20), pedido("B", 20, 30)]

    assert set(ids(algoritmo(pedidos, 30))) == {"A", "B"}


@pytest.mark.parametrize("algoritmo", [knapsack_guloso, knapsack_dp])
def test_nenhum_pedido_cabe(algoritmo):
    pedidos = [pedido("A", 11, 20), pedido("B", 12, 30)]

    assert algoritmo(pedidos, 10) == []


@pytest.mark.parametrize("algoritmo", [knapsack_guloso, knapsack_dp])
def test_pedido_com_peso_igual_a_capacidade(algoritmo):
    unico = pedido("A", 100, 500)

    assert algoritmo([unico], 100) == [unico]


def test_dp_rejeita_peso_fracionario():
    with pytest.raises(ValueError, match="deve ser inteiro"):
        knapsack_dp([pedido("A", 1.5, 10)], 2)

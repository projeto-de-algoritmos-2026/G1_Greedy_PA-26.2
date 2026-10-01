import pytest

from lateness import lateness_fifo, minimize_lateness
from modelos import Caminhao, Pedido


CAMINHAO = Caminhao(capacidade=300, autonomia=200, velocidade=60)


def pedido(id: str, prazo: float, distancia: float) -> Pedido:
    return Pedido(id=id, peso=1, valor=1, prazo=prazo, distancia=distancia)


def test_minimize_lateness_sem_pedidos():
    assert minimize_lateness([], CAMINHAO) == []


def test_edf_reproduz_exemplo_documentado_sem_atrasos():
    pedidos = [
        pedido("A", prazo=8, distancia=180),
        pedido("B", prazo=4, distancia=60),
        pedido("C", prazo=10, distancia=120),
    ]

    entregas = minimize_lateness(pedidos, CAMINHAO)

    assert [entrega.pedido.id for entrega in entregas] == ["B", "A", "C"]
    assert [entrega.conclusao for entrega in entregas] == [1, 4, 6]
    assert [entrega.atraso for entrega in entregas] == [0, 0, 0]


def test_edf_calcula_atraso_e_conclusao_acumulada():
    pedidos = [
        pedido("A", prazo=2, distancia=180),
        pedido("B", prazo=4, distancia=120),
    ]

    entregas = minimize_lateness(pedidos, CAMINHAO)

    assert [entrega.conclusao for entrega in entregas] == [3, 5]
    assert [entrega.atraso for entrega in entregas] == [1, 1]


def test_edf_preserva_ordem_de_entrada_quando_prazos_sao_iguais():
    pedidos = [
        pedido("A", prazo=5, distancia=60),
        pedido("B", prazo=5, distancia=120),
        pedido("C", prazo=5, distancia=180),
    ]

    entregas = minimize_lateness(pedidos, CAMINHAO)

    assert [entrega.pedido.id for entrega in entregas] == ["A", "B", "C"]


def test_fifo_mantem_ordem_de_chegada_para_comparacao():
    pedidos = [
        pedido("A", prazo=8, distancia=180),
        pedido("B", prazo=4, distancia=60),
        pedido("C", prazo=10, distancia=120),
    ]

    entregas = lateness_fifo(pedidos, CAMINHAO)

    assert [entrega.pedido.id for entrega in entregas] == ["A", "B", "C"]
    assert [entrega.conclusao for entrega in entregas] == [3, 4, 6]


def test_edf_nao_tem_maior_atraso_que_fifo():
    pedidos = [
        pedido("A", prazo=10, distancia=300),
        pedido("B", prazo=2, distancia=120),
        pedido("C", prazo=4, distancia=60),
    ]

    edf = minimize_lateness(pedidos, CAMINHAO)
    fifo = lateness_fifo(pedidos, CAMINHAO)

    assert max(entrega.atraso for entrega in edf) <= max(entrega.atraso for entrega in fifo)


def test_rejeita_velocidade_nao_positiva():
    caminhao_parado = Caminhao(capacidade=300, autonomia=200, velocidade=0)

    with pytest.raises(ValueError, match="velocidade"):
        minimize_lateness([pedido("A", prazo=1, distancia=1)], caminhao_parado)

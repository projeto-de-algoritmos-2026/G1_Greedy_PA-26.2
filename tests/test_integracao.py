from pathlib import Path

import pytest

from knapsack import knapsack_dp, knapsack_guloso
from main import formatar_reais, planejar
from modelos import Caminhao, Pedido, Rota, carregar_entrada

EXEMPLO = Path(__file__).resolve().parent.parent / "data" / "exemplo.json"


def test_fluxo_completo_com_o_exemplo():
    pedidos, caminhao, rota = carregar_entrada(str(EXEMPLO))

    plano = planejar(pedidos, caminhao, rota)

    # o guloso por valor/peso escolhe A + C (o otimo seria A + B, R$ 1.300)
    assert [p.id for p in plano.cargas] == ["A", "C"]
    assert plano.valor_total == 1200
    assert [e.pedido.id for e in plano.entregas] == ["A", "C"]
    assert [e.conclusao for e in plano.entregas] == [3, 5]
    assert plano.maior_atraso == 0
    assert plano.paradas == [170, 330]


def test_fluxo_sem_pedidos():
    _, caminhao, rota = carregar_entrada(str(EXEMPLO))

    plano = planejar([], caminhao, rota)

    assert plano.cargas == []
    assert plano.valor_total == 0
    assert plano.entregas == []
    assert plano.maior_atraso == 0
    assert plano.paradas == [170, 330]


def test_fluxo_com_pedido_atrasado():
    pedido = Pedido(id="X", peso=10, valor=100, prazo=1, distancia=180)
    caminhao = Caminhao(capacidade=50, autonomia=200, velocidade=60)

    plano = planejar([pedido], caminhao, Rota(destino=100, postos=[]))

    assert plano.maior_atraso == 2  # conclui em 3h, prazo 1h
    assert plano.paradas == []


def test_fluxo_levanta_erro_se_a_rota_for_inviavel():
    pedidos, caminhao, _ = carregar_entrada(str(EXEMPLO))

    with pytest.raises(ValueError):
        planejar(pedidos, caminhao, Rota(destino=500, postos=[80]))


def test_knapsack_com_um_unico_pedido():
    unico = Pedido(id="A", peso=10, valor=50, prazo=0, distancia=0)

    assert knapsack_guloso([unico], 10) == [unico]
    assert knapsack_dp([unico], 10) == [unico]


def test_formatar_reais():
    assert formatar_reais(1200) == "R$ 1.200,00"
    assert formatar_reais(3450.5) == "R$ 3.450,50"

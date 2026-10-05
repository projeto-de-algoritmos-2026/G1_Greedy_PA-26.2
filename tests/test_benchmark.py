import random

import pytest

from benchmark import gerar_pedidos, gerar_rota, knapsack_forca_bruta, medir, rodar
from caminhoneiro import caminhoneiro_guloso
from knapsack import knapsack_dp, knapsack_guloso


def valor(pedidos):
    return sum(p.valor for p in pedidos)


def test_gerar_pedidos_e_deterministico_e_tem_pesos_inteiros():
    assert gerar_pedidos(50) == gerar_pedidos(50)
    assert len(gerar_pedidos(50)) == 50
    assert all(isinstance(p.peso, int) for p in gerar_pedidos(50))


def test_rota_gerada_e_ordenada_e_viavel():
    rota = gerar_rota(100)

    assert rota.postos == sorted(rota.postos)
    assert caminhoneiro_guloso(rota, 200)  # nao levanta ValueError


@pytest.mark.parametrize("seed", range(20))
def test_dp_bate_com_a_forca_bruta(seed):
    rng = random.Random(seed)
    pedidos = gerar_pedidos(rng.randint(0, 12), seed=seed)
    capacidade = rng.randint(0, 400)

    assert valor(knapsack_dp(pedidos, capacidade)) == valor(knapsack_forca_bruta(pedidos, capacidade))


@pytest.mark.parametrize("seed", range(20))
def test_guloso_nunca_passa_do_otimo_nem_da_capacidade(seed):
    rng = random.Random(seed)
    pedidos = gerar_pedidos(rng.randint(0, 12), seed=seed)
    capacidade = rng.randint(0, 400)

    escolhidos = knapsack_guloso(pedidos, capacidade)

    assert sum(p.peso for p in escolhidos) <= capacidade
    assert valor(escolhidos) <= valor(knapsack_dp(pedidos, capacidade))


def test_medir_devolve_tempo_e_resultado():
    tempo, resultado = medir(sorted, [3, 1, 2], repeticoes=2)

    assert tempo >= 0
    assert resultado == [1, 2, 3]


def test_rodar_n_pequeno_compara_as_versoes():
    linha = rodar(10)

    assert linha["n"] == 10
    assert linha["knapsack_forca_bruta_s"] is not None
    assert linha["valor_dp"] >= linha["valor_guloso"]
    assert linha["maior_atraso_edf_h"] <= linha["maior_atraso_fifo_h"]
    assert linha["paradas_guloso"] <= linha["paradas_todos"]

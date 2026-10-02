import pytest

from caminhoneiro import caminhoneiro_guloso, caminhoneiro_todos_os_postos
from modelos import Rota


def test_destino_alcancavel_sem_parada():
    rota = Rota(destino=150, postos=[50, 100])

    assert caminhoneiro_guloso(rota, autonomia=200) == []


def test_destino_exige_uma_parada():
    rota = Rota(destino=300, postos=[100, 180, 250])

    assert caminhoneiro_guloso(rota, autonomia=200) == [180]


def test_exemplo_com_varias_paradas():
    rota = Rota(destino=500, postos=[80, 170, 250, 330, 410])

    assert caminhoneiro_guloso(rota, autonomia=200) == [170, 330]


def test_funciona_com_postos_fora_de_ordem():
    rota = Rota(destino=500, postos=[330, 80, 410, 170, 250])

    assert caminhoneiro_guloso(rota, autonomia=200) == [170, 330]


def test_levanta_erro_quando_os_postos_sao_insuficientes():
    rota = Rota(destino=500, postos=[80, 170, 250])

    with pytest.raises(ValueError, match="nao e possivel"):
        caminhoneiro_guloso(rota, autonomia=200)


def test_alternativa_abastece_em_todos_os_postos():
    rota = Rota(destino=500, postos=[80, 170, 250, 330, 410])

    assert caminhoneiro_todos_os_postos(rota, autonomia=200) == [80, 170, 250, 330, 410]


def test_alternativa_tambem_detecta_rota_inviavel():
    rota = Rota(destino=500, postos=[80, 300, 410])

    with pytest.raises(ValueError, match="nao e possivel"):
        caminhoneiro_todos_os_postos(rota, autonomia=200)


def test_rejeita_autonomia_nao_positiva():
    rota = Rota(destino=100, postos=[])

    with pytest.raises(ValueError, match="autonomia"):
        caminhoneiro_guloso(rota, autonomia=0)

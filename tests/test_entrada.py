from pathlib import Path

from modelos import carregar_entrada, tempo_entrega

EXEMPLO = Path(__file__).resolve().parent.parent / "data" / "exemplo.json"


def test_carrega_exemplo():
    pedidos, caminhao, rota = carregar_entrada(str(EXEMPLO))

    assert [p.id for p in pedidos] == ["A", "B", "C"]
    assert caminhao.capacidade == 300
    assert caminhao.autonomia == 200
    assert rota.destino == 500
    assert rota.postos == [80, 170, 250, 330, 410]


def test_tempo_de_entrega_do_exemplo():
    pedidos, caminhao, _ = carregar_entrada(str(EXEMPLO))

    assert [tempo_entrega(p, caminhao) for p in pedidos] == [3, 1, 2]

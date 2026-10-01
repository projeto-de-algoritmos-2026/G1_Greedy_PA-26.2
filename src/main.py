"""Fluxo completo: Pedidos -> KNAPSACK -> MINIMIZE LATENESS -> CAMINHONEIRO -> RESULTADO.

Por enquanto so carrega e mostra a entrada. A integracao dos algoritmos entra em 04/10.
"""

import sys
from pathlib import Path

from modelos import carregar_entrada

ENTRADA_PADRAO = Path(__file__).resolve().parent.parent / "data" / "exemplo.json"


def main(caminho: Path = ENTRADA_PADRAO) -> None:
    pedidos, caminhao, rota = carregar_entrada(str(caminho))

    print("=================================")
    print("       SISTEMA DE LOGÍSTICA")
    print("=================================\n")

    print(f"Pedidos recebidos: {len(pedidos)}")
    print(f"Caminhão: capacidade {caminhao.capacidade:g} kg, autonomia {caminhao.autonomia:g} km")
    print(f"Rota: {rota.destino:g} km, {len(rota.postos)} postos\n")

    # TODO (04/10): cargas = knapsack_dp(pedidos, caminhao.capacidade)
    # TODO (04/10): entregas = minimize_lateness(cargas, caminhao)
    # TODO (04/10): paradas = caminhoneiro_guloso(rota, caminhao.autonomia)
    print("[em construção] algoritmos ainda não integrados")
    print("=================================")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ENTRADA_PADRAO)

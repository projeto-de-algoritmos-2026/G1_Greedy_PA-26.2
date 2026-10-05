"""Fluxo completo: Pedidos -> KNAPSACK -> MINIMIZE LATENESS -> CAMINHONEIRO -> RESULTADO."""

import sys
from dataclasses import dataclass
from pathlib import Path

from caminhoneiro import caminhoneiro_guloso
from knapsack import knapsack_guloso
from lateness import maior_atraso, minimize_lateness
from modelos import Caminhao, Entrega, Pedido, Rota, carregar_entrada

ENTRADA_PADRAO = Path(__file__).resolve().parent.parent / "data" / "exemplo.json"


@dataclass(frozen=True)
class Plano:
    cargas: list[Pedido]       # pedidos escolhidos pelo Knapsack
    valor_total: float         # soma dos valores das cargas
    entregas: list[Entrega]    # ordem das entregas (Minimize Lateness)
    maior_atraso: float        # horas
    paradas: list[float]       # postos escolhidos (Caminhoneiro), em km


def planejar(pedidos: list[Pedido], caminhao: Caminhao, rota: Rota) -> Plano:
    """Encadeia os tres algoritmos. Levanta ValueError se a rota for inviavel."""
    cargas = knapsack_guloso(pedidos, caminhao.capacidade)
    entregas = minimize_lateness(cargas, caminhao)
    paradas = caminhoneiro_guloso(rota, caminhao.autonomia)

    return Plano(
        cargas=cargas,
        valor_total=sum(p.valor for p in cargas),
        entregas=entregas,
        maior_atraso=maior_atraso(entregas),
        paradas=paradas,
    )


def formatar_reais(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def imprimir_plano(plano: Plano) -> None:
    print("Cargas selecionadas:")
    for pedido in plano.cargas:
        print(f"- Pedido {pedido.id}")

    print(f"\nLucro esperado:\n{formatar_reais(plano.valor_total)}\n")

    print("Ordem das entregas:")
    for i, entrega in enumerate(plano.entregas, start=1):
        print(f"{i}. Pedido {entrega.pedido.id} "
              f"(conclusão em {entrega.conclusao:g} h, prazo {entrega.pedido.prazo:g} h, "
              f"atraso {entrega.atraso:g} h)")

    print(f"\nMaior atraso:\n{plano.maior_atraso:g} horas\n")

    print("Paradas para abastecimento:")
    for km in plano.paradas:
        print(f"- Posto {km:g} km")
    print(f"\nTotal de paradas:\n{len(plano.paradas)}")


def main(caminho: Path = ENTRADA_PADRAO) -> None:
    pedidos, caminhao, rota = carregar_entrada(str(caminho))

    print("=================================")
    print("       SISTEMA DE LOGÍSTICA")
    print("=================================\n")

    print(f"Pedidos recebidos: {len(pedidos)}")
    print(f"Caminhão: capacidade {caminhao.capacidade:g} kg, autonomia {caminhao.autonomia:g} km")
    print(f"Rota: {rota.destino:g} km, {len(rota.postos)} postos\n")

    try:
        imprimir_plano(planejar(pedidos, caminhao, rota))
    except ValueError as erro:
        print(f"Não foi possível montar o plano: {erro}")

    print("=================================")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else ENTRADA_PADRAO)

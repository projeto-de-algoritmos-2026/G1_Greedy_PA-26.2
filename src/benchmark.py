"""Mede o tempo de cada algoritmo (versao principal e alternativa) para n = 10, 100, 1.000 e 10.000.

Tambem compara a qualidade das solucoes: valor da carga (guloso vs DP), maior atraso (EDF vs FIFO)
e numero de paradas (guloso vs todos os postos). Imprime a tabela e salva em data/resultados_benchmark.csv.
"""

import csv
import itertools
import random
import time
from pathlib import Path

from caminhoneiro import caminhoneiro_guloso, caminhoneiro_todos_os_postos
from knapsack import knapsack_dp, knapsack_guloso
from lateness import lateness_fifo, maior_atraso, minimize_lateness
from modelos import Caminhao, Pedido, Rota

TAMANHOS = [10, 100, 1000, 10000]
LIMITE_FORCA_BRUTA = 20  # O(2^n): so roda para n pequeno
CAPACIDADE = 1000        # fixa: a tabela da DP tem (n+1)*(W+1) celulas, W proporcional a n estouraria a memoria
CAMINHAO = Caminhao(capacidade=CAPACIDADE, autonomia=200, velocidade=60)
ESPACO_ENTRE_POSTOS = 50
SAIDA_CSV = Path(__file__).resolve().parent.parent / "data" / "resultados_benchmark.csv"


def gerar_pedidos(n: int, seed: int = 42) -> list[Pedido]:
    """Pedidos aleatorios com peso inteiro (a DP exige), valor, prazo e distancia."""
    rng = random.Random(seed)
    return [
        Pedido(
            id=str(i + 1),
            peso=rng.randint(1, 100),
            valor=rng.randint(10, 1000),
            prazo=rng.randint(1, 2 * n),
            distancia=rng.randint(1, 200),
        )
        for i in range(n)
    ]


def gerar_rota(n: int, seed: int = 42) -> Rota:
    """Rota com n postos aproximadamente igualmente espacados (ja ordenados e sempre viavel)."""
    rng = random.Random(seed)
    postos = [ESPACO_ENTRE_POSTOS * (i + 1) + rng.randint(-10, 10) for i in range(n)]
    return Rota(destino=ESPACO_ENTRE_POSTOS * (n + 1), postos=postos)


def knapsack_forca_bruta(pedidos: list[Pedido], capacidade: float) -> list[Pedido]:
    """Testa todos os subconjuntos, O(2^n). So para validar a DP em n pequeno."""
    melhor: list[Pedido] = []
    melhor_valor = 0.0
    for tamanho in range(len(pedidos) + 1):
        for combinacao in itertools.combinations(pedidos, tamanho):
            if sum(p.peso for p in combinacao) <= capacidade:
                valor = sum(p.valor for p in combinacao)
                if valor > melhor_valor:
                    melhor, melhor_valor = list(combinacao), valor
    return melhor


def medir(funcao, *args, repeticoes: int = 1):
    """Devolve (menor tempo em segundos entre as repeticoes, resultado)."""
    menor = float("inf")
    resultado = None
    for _ in range(repeticoes):
        inicio = time.perf_counter()
        resultado = funcao(*args)
        menor = min(menor, time.perf_counter() - inicio)
    return menor, resultado


def valor_total(pedidos: list[Pedido]) -> float:
    return sum(p.valor for p in pedidos)


def rodar(n: int) -> dict:
    pedidos = gerar_pedidos(n)
    rota = gerar_rota(n)
    repeticoes = 5 if n <= 1000 else 1

    t_guloso, cargas_guloso = medir(knapsack_guloso, pedidos, CAPACIDADE, repeticoes=repeticoes)
    t_dp, cargas_dp = medir(knapsack_dp, pedidos, CAPACIDADE)
    t_edf, entregas_edf = medir(minimize_lateness, pedidos, CAMINHAO, repeticoes=repeticoes)
    t_fifo, entregas_fifo = medir(lateness_fifo, pedidos, CAMINHAO, repeticoes=repeticoes)
    t_cam, paradas = medir(caminhoneiro_guloso, rota, CAMINHAO.autonomia, repeticoes=repeticoes)
    t_todos, todos = medir(caminhoneiro_todos_os_postos, rota, CAMINHAO.autonomia, repeticoes=repeticoes)

    t_bruta = None
    if n <= LIMITE_FORCA_BRUTA:
        t_bruta, cargas_bruta = medir(knapsack_forca_bruta, pedidos, CAPACIDADE)
        assert valor_total(cargas_bruta) == valor_total(cargas_dp), "DP diverge da forca bruta"

    return {
        "n": n,
        "knapsack_guloso_s": t_guloso,
        "knapsack_dp_s": t_dp,
        "knapsack_forca_bruta_s": t_bruta,
        "lateness_edf_s": t_edf,
        "lateness_fifo_s": t_fifo,
        "caminhoneiro_guloso_s": t_cam,
        "caminhoneiro_todos_s": t_todos,
        "valor_guloso": valor_total(cargas_guloso),
        "valor_dp": valor_total(cargas_dp),
        "maior_atraso_edf_h": maior_atraso(entregas_edf),
        "maior_atraso_fifo_h": maior_atraso(entregas_fifo),
        "paradas_guloso": len(paradas),
        "paradas_todos": len(todos),
    }


def formatar(valor) -> str:
    if valor is None:
        return "-"
    if isinstance(valor, float):
        return f"{valor:.6f}" if valor < 1000 else f"{valor:.0f}"
    return str(valor)


def main() -> None:
    linhas = [rodar(n) for n in TAMANHOS]
    colunas = list(linhas[0])

    print(" | ".join(colunas))
    for linha in linhas:
        print(" | ".join(formatar(linha[c]) for c in colunas))

    SAIDA_CSV.parent.mkdir(exist_ok=True)
    with open(SAIDA_CSV, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(colunas)
        for linha in linhas:
            escritor.writerow([formatar(linha[c]) for c in colunas])
    print(f"\nResultados salvos em {SAIDA_CSV}")


if __name__ == "__main__":
    main()

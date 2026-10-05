"""Grafico do tempo dos tres algoritmos gulosos contra o crescimento teorico.

Le data/resultados_benchmark.csv (gerado por benchmark.py) e salva docs/grafico_gulosos.png.
Requer matplotlib.
"""

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parent.parent
ENTRADA_CSV = RAIZ / "data" / "resultados_benchmark.csv"
SAIDA_PNG = RAIZ / "docs" / "grafico_gulosos.png"

SUPERFICIE = "#fcfcfb"
TEXTO = "#0b0b0b"
TEXTO_SECUNDARIO = "#52514e"
GRADE = "#e3e2de"
REFERENCIA = "#8a8984"

# (coluna do CSV, titulo, complexidade, cor da serie, funcao do crescimento teorico)
ALGORITMOS = [
    ("knapsack_guloso_s", "Knapsack (guloso)", "O(n log n)", "#2a78d6", lambda n: n * math.log2(n)),
    ("lateness_edf_s", "Minimize Lateness (EDF)", "O(n log n)", "#eb6834", lambda n: n * math.log2(n)),
    ("caminhoneiro_guloso_s", "Caminhoneiro (guloso)", "O(n)", "#1baf7a", lambda n: n),
]
PONTO_DE_ANCORAGEM = 2  # a curva teorica passa pelo ponto de n = 1.000 (n = 10 e ruido de medicao)


def ler_resultados() -> list[dict]:
    with open(ENTRADA_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> None:
    linhas = ler_resultados()
    ns = [int(l["n"]) for l in linhas]

    fig, eixos = plt.subplots(1, 3, figsize=(12, 4), sharey=True, facecolor=SUPERFICIE)

    for eixo, (coluna, titulo, complexidade, cor, crescimento) in zip(eixos, ALGORITMOS):
        ms = [float(l[coluna]) * 1000 for l in linhas]
        escala = ms[PONTO_DE_ANCORAGEM] / crescimento(ns[PONTO_DE_ANCORAGEM])

        eixo.set_facecolor(SUPERFICIE)
        eixo.plot(ns, [escala * crescimento(n) for n in ns], linestyle="--", linewidth=1.5,
                  color=REFERENCIA, label=f"teórico {complexidade}")
        eixo.plot(ns, ms, color=cor, linewidth=2, marker="o", markersize=8,
                  markeredgecolor=SUPERFICIE, markeredgewidth=2, label="medido")

        eixo.set_xscale("log")
        eixo.set_yscale("log")
        eixo.set_xticks(ns)
        eixo.set_xticklabels([f"{n:,}".replace(",", ".") for n in ns])
        eixo.set_title(f"{titulo}\n{complexidade}", color=TEXTO, fontsize=11, loc="left")
        eixo.set_xlabel("número de pedidos (n)", color=TEXTO_SECUNDARIO)
        eixo.grid(True, which="major", color=GRADE, linewidth=0.8)
        eixo.set_axisbelow(True)
        eixo.tick_params(colors=TEXTO_SECUNDARIO, which="both")
        for lado in ("top", "right"):
            eixo.spines[lado].set_visible(False)
        for lado in ("left", "bottom"):
            eixo.spines[lado].set_color(GRADE)
        eixo.legend(loc="upper left", frameon=False, labelcolor=TEXTO_SECUNDARIO, fontsize=9)

    eixos[0].set_ylabel("tempo (ms)", color=TEXTO_SECUNDARIO)
    fig.suptitle("Tempo dos algoritmos gulosos × crescimento teórico", color=TEXTO, fontsize=13, x=0.01, ha="left")
    fig.tight_layout()

    SAIDA_PNG.parent.mkdir(exist_ok=True)
    fig.savefig(SAIDA_PNG, dpi=150, facecolor=SUPERFICIE)
    print(f"Gráfico salvo em {SAIDA_PNG}")


if __name__ == "__main__":
    main()

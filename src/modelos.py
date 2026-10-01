"""Tipos de dados compartilhados e leitura do arquivo de entrada."""

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Pedido:
    id: str
    peso: float       # kg
    valor: float      # R$
    prazo: float      # horas (prazo de entrega)
    distancia: float  # km


@dataclass(frozen=True)
class Caminhao:
    capacidade: float  # kg
    autonomia: float   # km
    velocidade: float  # km/h (converte a distancia do pedido em tempo de entrega)


@dataclass(frozen=True)
class Rota:
    destino: float       # km totais da rota
    postos: list[float]  # posicao de cada posto na rota (km)


@dataclass(frozen=True)
class Entrega:
    """Saida do Minimize Lateness: um pedido na ordem de entrega."""
    pedido: Pedido
    conclusao: float  # horas desde o inicio da rota
    atraso: float     # max(0, conclusao - prazo)


def tempo_entrega(pedido: Pedido, caminhao: Caminhao) -> float:
    return pedido.distancia / caminhao.velocidade


def carregar_entrada(caminho: str) -> tuple[list[Pedido], Caminhao, Rota]:
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)

    pedidos = [Pedido(**p) for p in dados["pedidos"]]
    caminhao = Caminhao(**dados["caminhao"])
    rota = Rota(**dados["rota"])
    return pedidos, caminhao, rota

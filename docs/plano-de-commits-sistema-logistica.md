# 📅 Plano de Commits — Sistema de Logística (PAA)

**Equipe:** Maria Clara e Ana Júlia
**Período:** 30/09 (quarta) a 05/10 (segunda)
**Regra:** 1 commit por dia. Vídeo gravado na segunda (05/10).

---

## Visão geral

| Data | Dia | Responsável | Commit | Entrega do dia |
|------|-----|-------------|--------|----------------|
| 30/09 | Quarta | Maria Clara | `feat: cria estrutura inicial do projeto` | Repo + estrutura + entrada de dados |
| 01/10 | Quinta | Ana Júlia | `feat: implementa algoritmo knapsack` | Knapsack (DP) + alternativa gulosa + complexidade |
| 02/10 | Sexta | Ana Júlia | `feat: implementa algoritmo minimize lateness` | Lateness (guloso) + alternativa + complexidade |
| 03/10 | Sábado | Ana Júlia | `feat: implementa algoritmo caminhoneiro` | Caminhoneiro (guloso) + alternativa + complexidade |
| 04/10 | Domingo | Maria Clara | `feat: integra algoritmos, testes e benchmark` | Fluxo completo + testes + script de experimentos |
| 05/10 | Segunda | Maria Clara + Ana Júlia | `docs: finaliza projeto e adiciona apresentacao` | Resultados + README com análise + vídeo |

**Fluxo final do sistema:**

```
Pedidos → KNAPSACK → MINIMIZE LATENESS → CAMINHONEIRO → RESULTADO
```

**O que torna o trabalho "de PAA" (vale para todos os dias):**
1. Explicar a estratégia de cada algoritmo (e por que ela funciona)
2. Complexidade de tempo e espaço de cada implementação
3. Comparar com uma solução alternativa
4. Resultados experimentais: 10, 100, 1.000 e 10.000 pedidos, medindo o tempo

---

## 🟦 30/09 (quarta) — Estrutura do projeto

**Responsável:** Maria Clara
**Commit:** `feat: cria estrutura inicial do projeto`

**Tarefas:**
- Criar o repositório no GitHub e adicionar a Ana Júlia como colaboradora
- Criar a estrutura de pastas:

```
sistema-logistica/
│
├── src/
│   ├── main
│   ├── knapsack
│   ├── lateness
│   ├── caminhoneiro
│   └── benchmark
│
├── data/
│   └── exemplo
│
├── tests/
│
└── README.md
```

- Definir o formato de entrada:

```
Pedidos:
- id
- peso
- valor
- prazo
- distância

Caminhão:
- capacidade
- autonomia
- velocidade

Rota:
- destino
- postos (distância na rota)
```

  Acréscimos em relação ao combinado inicial: `id` (identificar o pedido na saída), `velocidade` (o Minimize Lateness precisa de tempo, e `tempo = distância ÷ velocidade`) e `destino` (o Caminhoneiro precisa saber até onde vai). Detalhes em [formato-de-entrada.md](formato-de-entrada.md).

- Combinar com a Ana Júlia a assinatura das funções (entrada e saída de cada algoritmo)
- Combinar que cada algoritmo terá uma versão principal e uma versão alternativa (para comparação)

**Objetivo:** terminar o dia com o projeto rodando, mesmo sem os algoritmos implementados.

---

## 🟩 01/10 (quinta) — Knapsack

**Responsável:** Ana Júlia
**Commit:** `feat: implementa algoritmo knapsack`

```
Pedidos → KNAPSACK → Cargas selecionadas
```

**Exemplo:**

```
Pedido A → 100 kg → R$ 500
Pedido B → 200 kg → R$ 800
Pedido C → 150 kg → R$ 700

Capacidade do caminhão = 300 kg

Cargas escolhidas (DP, ótimo): A + B
Peso total: 300 kg
Valor total: R$ 1.300

Para comparar, o guloso por valor/peso escolhe: A + C
Peso total: 250 kg
Valor total: R$ 1.200  ← não é ótimo
```

**Análise (anotar para o README):**
- **Estratégia:** programação dinâmica. O knapsack 0/1 **não** é guloso: a solução ótima exige DP.
- **Complexidade:** tempo O(n·W), espaço O(n·W) para reconstruir os pedidos escolhidos (O(W) se só quiser o valor).
- **Alternativa para comparar:** guloso por valor/peso, O(n log n). É rápido, mas não é ótimo.
  Contra-exemplo útil pro vídeo: o próprio exemplo acima (razões: A = 5, C ≈ 4,67, B = 4). O guloso pega A + C (R$ 1.200) e a DP pega A + B (R$ 1.300).
- **Opcional:** força bruta O(2ⁿ) só para n pequeno, para validar a DP.

**Atenção:** deixar uma função pronta para ser chamada no programa principal.

---

## 🟨 02/10 (sexta) — Minimize Lateness

**Responsável:** Ana Júlia
**Commit:** `feat: implementa algoritmo minimize lateness`

**Entrada:**

| Pedido | Tempo | Prazo |
|--------|-------|-------|
| A | 3h | 8h |
| B | 1h | 4h |
| C | 2h | 10h |

O algoritmo determina a ordem das entregas. Depois, calcular:
- Tempo de conclusão
- Prazo
- Atraso
- Maior atraso

**Resultado esperado:**

```
Ordem: B → A → C
Conclusões: B em 1h (prazo 4h), A em 4h (prazo 8h), C em 6h (prazo 10h)
Maior atraso: 0 horas (nenhum pedido atrasa)
```

**Análise (anotar para o README):**
- **Estratégia:** gulosa, Earliest Deadline First (ordenar por prazo crescente). A prova de corretude é por argumento de troca (exchange argument): trocar dois pedidos fora de ordem de prazo nunca diminui o maior atraso.
- **Complexidade:** tempo O(n log n) (dominado pela ordenação), espaço O(n).
- **Alternativa para comparar:** ordem de chegada (FIFO) ou menor tempo primeiro, mostrando que o maior atraso fica pior ou igual.

---

## 🟧 03/10 (sábado) — Caminhoneiro

**Responsável:** Ana Júlia
**Commit:** `feat: implementa algoritmo caminhoneiro`

**Entrada:**

```
Destino: 500 km
Autonomia: 200 km
Postos: 80 km, 170 km, 250 km, 330 km, 410 km
```

**Resultado esperado:**

```
Postos escolhidos: 170 km, 330 km
Número de paradas: 2
```

**Objetivo:** minimizar a quantidade de paradas, respeitando a autonomia.

**Análise (anotar para o README):**
- **Estratégia:** gulosa. Sempre seguir até o posto mais distante que ainda é alcançável e parar nele. Argumento de corretude: o guloso nunca fica atrás de qualquer outra solução.
- **Complexidade:** tempo O(n) com postos já ordenados (O(n log n) se precisar ordenar), espaço O(k), com k = número de paradas.
- **Alternativa para comparar:** abastecer em todos os postos, ou DP O(n²).

---

## 🟪 04/10 (domingo) — Integração + testes + benchmark

**Responsável:** Maria Clara
**Commit:** `feat: integra algoritmos, testes e benchmark`

> Se ficar muito pesado, dá pra dividir em 2 commits no mesmo dia (`feat: integra os algoritmos no fluxo principal` e `test: adiciona testes e benchmark`) ou pedir pra Ana Júlia ajudar no benchmark.

### Integração

```
                 ENTRADA
                    ↓
              Lista de pedidos
                    ↓
             ┌─────────────┐
             │  KNAPSACK   │
             └──────┬──────┘
                    ↓
          Cargas selecionadas
                    ↓
          ┌──────────────────┐
          │ MINIMIZE LATENESS│
          └────────┬─────────┘
                    ↓
            Ordem das entregas
                    ↓
          ┌──────────────────┐
          │   CAMINHONEIRO   │
          └────────┬─────────┘
                    ↓
            Paradas escolhidas
                    ↓
                RESULTADO
```

**Exemplo de saída no terminal:**

```
=================================
       SISTEMA DE LOGÍSTICA
=================================

Cargas selecionadas:
- Pedido 01
- Pedido 03
- Pedido 05

Lucro esperado:
R$ 3.450,00

Ordem das entregas:
1. Pedido 03
2. Pedido 01
3. Pedido 05

Maior atraso:
2 horas

Paradas para abastecimento:
- Posto 170 km
- Posto 330 km

Total de paradas:
2
=================================
```

### Casos de teste

**Knapsack**
- [ ] nenhum pedido
- [ ] um pedido
- [ ] todos os pedidos cabem
- [ ] nenhum pedido cabe
- [ ] capacidade exatamente igual ao peso
- [ ] vários pedidos

**Minimize Lateness**
- [ ] nenhum atraso
- [ ] um pedido atrasado
- [ ] vários pedidos
- [ ] prazos iguais

**Caminhoneiro**
- [ ] destino alcançável sem parada
- [ ] uma parada
- [ ] várias paradas
- [ ] postos insuficientes para chegar ao destino

Depois de rodar os testes, corrigir os bugs encontrados (se precisar mexer em algum algoritmo, avisar a Ana Júlia).

### Script de benchmark (`src/benchmark`)
- Gerar pedidos aleatórios com n = **10, 100, 1.000 e 10.000**
- Medir o tempo de execução de cada algoritmo (versão principal e alternativa)
- Salvar os resultados numa tabela (CSV ou print no terminal)
- A força bruta só entra para n pequeno (ex.: n = 10)

---

## 🎥 05/10 (segunda) — Resultados + README + vídeo

**Responsáveis:** Maria Clara e Ana Júlia
**Commit:** `docs: finaliza projeto e adiciona apresentacao`

> Esse dia **não** é para começar funcionalidade nova.

### 1. Rodar o benchmark e montar os resultados

| n | Knapsack (DP) | Knapsack (guloso) | Lateness (EDF) | Lateness (FIFO) | Caminhoneiro |
|---|---------------|-------------------|----------------|-----------------|--------------|
| 10 | | | | | |
| 100 | | | | | |
| 1.000 | | | | | |
| 10.000 | | | | | |

Comentar: o crescimento observado bate com a complexidade teórica? Onde o guloso do knapsack perde valor em relação à DP?

### 2. Revisar o código
- [ ] Knapsack funcionando
- [ ] Minimize Lateness funcionando
- [ ] Caminhoneiro funcionando
- [ ] Integração funcionando
- [ ] Casos de teste passando

### 3. Finalizar o README
1. Introdução
2. Problema
3. Objetivo
4. Entrada
5. Saída
6. Knapsack (estratégia, complexidade, alternativa)
7. Minimize Lateness (estratégia, complexidade, alternativa)
8. Caminhoneiro (estratégia, complexidade, alternativa)
9. Resultados experimentais
10. Conclusão
11. Exemplo de execução

### 4. Gravar o vídeo (5–8 min)

| Tempo | Conteúdo | Quem |
|-------|----------|------|
| 00:00 – 00:40 | Apresentação do problema | Maria Clara |
| 00:40 – 02:00 | Explicação do sistema e da integração | Maria Clara |
| 02:00 – 03:00 | Knapsack (DP vs guloso) | Ana Júlia |
| 03:00 – 04:00 | Minimize Lateness | Ana Júlia |
| 04:00 – 05:00 | Caminhoneiro | Ana Júlia |
| 05:00 – 06:00 | Demonstração do programa | Maria Clara |
| 06:00 – 07:00 | Resultados experimentais e complexidade | As duas |
| 07:00 – 07:30 | Conclusão | As duas |

---

## 📌 Resumo para o grupo

```
30/09 (qua) — MARIA CLARA
feat: cria estrutura inicial do projeto
→ repo + estrutura + entrada de dados

01/10 (qui) — ANA JÚLIA
feat: implementa algoritmo knapsack
→ DP + alternativa gulosa + complexidade

02/10 (sex) — ANA JÚLIA
feat: implementa algoritmo minimize lateness
→ EDF + alternativa + complexidade

03/10 (sáb) — ANA JÚLIA
feat: implementa algoritmo caminhoneiro
→ guloso + alternativa + complexidade

04/10 (dom) — MARIA CLARA
feat: integra algoritmos, testes e benchmark
→ fluxo completo + testes + experimentos

05/10 (seg) — MARIA CLARA + ANA JÚLIA
docs: finaliza projeto e adiciona apresentacao
→ resultados + README + GRAVAÇÃO DO VÍDEO
```

**Ideia central:** chegar no domingo com o sistema pronto e o benchmark rodando. A segunda fica reservada para resultados, README e gravação, sem depender de terminar código no mesmo dia do vídeo.

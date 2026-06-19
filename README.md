# Analisando SNAP: MOOC User Action Dataset

Projeto desenvolvido para a disciplina MATA53 – Teoria dos Grafos.

O trabalho realiza o tratamento do dataset **MOOC User Action (SNAP)**, calcula métricas estruturais da rede, avalia o desempenho de algoritmos clássicos de grafos e investiga propriedades de redes complexas.

---

# Estrutura do Projeto

```text
.
├── dados/
│   ├── act-mooc/
│   │   ├── act-mooc.tsv
│   │   └── README do dataset original
│   └── grafo_tratado.graphml
│
├── resultados/
│   ├── imagens/
│   └── tabelas/
│
├── 0_tratamento-de-dados.py
├── 1_metricas-parte-1.py
├── 2_algoritmos-parte2.py
├── 3_small-word-parte3.py
├── 4_lei-potencia-parte3.py
├── 5_robustez-parte3.py
│
└── README.md
```

---

# Requisitos

- Python 3.10 ou superior

Bibliotecas utilizadas:

```bash
pip install pandas networkx numpy matplotlib scipy
```

Opcionalmente, crie um ambiente virtual:

```bash
python -m venv .venv
```

### Linux/Mac

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Depois instale as dependências:

```bash
pip install pandas networkx numpy matplotlib scipy
```

---

# Como Executar

Os scripts devem ser executados na ordem abaixo.

## 1. Tratamento dos Dados

Gera o grafo tratado a partir do dataset original.

```bash
python 0_tratamento-de-dados.py
```

Entrada:

```text
dados/act-mooc/act-mooc.tsv
```

Saída:

```text
dados/grafo_tratado.graphml
```

---

## 2. Métricas Estruturais

Calcula métricas da rede e gera visualizações.

```bash
python 1_metricas-parte-1.py
```

Saídas:

```text
resultados/tabelas/metricas_parte1.csv

resultados/imagens/distribuicao_graus.png

resultados/imagens/grafo_reduzido.png
```

---

## 3. Avaliação Experimental dos Algoritmos

Executa BFS, DFS, Dijkstra, Bellman-Ford, Prim, Kruskal, Tarjan e Floyd-Warshall.

```bash
python 2_algoritmos-parte2.py
```

Saída:

```text
resultados/tabelas/desempenho_algoritmos.csv
```

---

## 4. Análise Small-World

Calcula as métricas utilizadas na avaliação da propriedade small-world.

```bash
python 3_small-word-parte3.py
```

Saída:

```text
resultados/tabelas/smallworld.csv
```

---

## 5. Lei de Potência

Realiza o ajuste da distribuição de graus e o teste KS.

```bash
python 4_lei-potencia-parte3.py
```

Saídas:

```text
resultados/tabelas/lei_potencia.csv

resultados/imagens/distribuicao_graus_loglog.png

resultados/imagens/ccdf_lei_potencia.png
```

---

## 6. Robustez da Rede

Executa os experimentos de remoção aleatória e remoção dos vértices mais centrais.

```bash
python 5_robustez-parte3.py
```

Saída:

```text
resultados/tabelas/robustez.csv
```

---

# Dataset Utilizado

MOOC User Action Dataset (SNAP)

https://snap.stanford.edu/data/act-mooc.html

---

# Autora

Priscila Anjos Santos

Universidade Federal da Bahia (UFBA)
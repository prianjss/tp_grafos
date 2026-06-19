import networkx as nx
import pandas as pd
import random
import numpy as np

G = nx.read_graphml("dados/grafo_tratado.graphml")
N = G.number_of_nodes()

print(f"Nós: {N}")
print(f"Arestas: {G.number_of_edges()}")

lcc_original = len(max(nx.connected_components(G), key=len))

print(f"LCC original: {lcc_original}")

G_random = G.copy()
n_remove = int(0.05 * N)

nos_aleatorios = random.sample(
    list(G_random.nodes()),
    n_remove
)

G_random.remove_nodes_from(nos_aleatorios)

lcc_random = len(
    max(nx.connected_components(G_random), key=len)
)

print(f"LCC após remoção aleatória: {lcc_random}")

G_target = G.copy()

centralidade = nx.degree_centrality(G_target)

ordenados = sorted(
    centralidade.items(),
    key=lambda x: x[1],
    reverse=True
)

nos_centrais = [
    no for no, _ in ordenados[:n_remove]
]

G_target.remove_nodes_from(nos_centrais)

lcc_target = len(
    max(nx.connected_components(G_target), key=len)
)

print(f"LCC após remoção dos hubs: {lcc_target}")

resultados = pd.DataFrame([
    {
        "cenario": "Original",
        "lcc": lcc_original,
        "percentual": 100
    },
    {
        "cenario": "Remoção aleatória (5%)",
        "lcc": lcc_random,
        "percentual": 100*lcc_random/lcc_original
    },
    {
        "cenario": "Remoção dos hubs (5%)",
        "lcc": lcc_target,
        "percentual": 100*lcc_target/lcc_original
    }
])

print(resultados)

resultados.to_csv(
    "resultados/tabelas/robustez.csv",
    index=False
)
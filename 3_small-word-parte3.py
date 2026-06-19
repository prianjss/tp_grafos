import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import random

G = nx.read_graphml("dados/grafo_tratado.graphml")
print(f"Grafo carregado: {G.number_of_nodes()} nós, {G.number_of_edges()} arestas")

nos = G.number_of_nodes()
arestas = G.number_of_edges()
Clustering_real = nx.average_clustering(G)
Length_real = nx.average_shortest_path_length(G)

print(f"\n--- Métricas do grafo real ---")
print(f"Coeficiente de clusterização médio: {Clustering_real:.6f}")
print(f"Comprimento médio dos caminhos:    {Length_real:.6f}")
print(f"Diâmetro:                          {nx.diameter(G)}")
print(f"Raio:                              {nx.radius(G)}")

usuarios = [n for n in G.nodes() if str(n).startswith('U_')]
atividades = [n for n in G.nodes() if str(n).startswith('T_')]
nos_user = len(usuarios)
nos_target = len(atividades)
p = arestas / (nos_user * nos_target)

Grafo_random = nx.Graph()
Grafo_random.add_nodes_from(usuarios, bipartite=0)
Grafo_random.add_nodes_from(atividades, bipartite=1)

for u in usuarios:
    for t in atividades:
        if random.random() < p:
            Grafo_random.add_edge(u, t)

print(f"\n--- Rede aleatória bipartida gerada ---")
print(f"Nós: {Grafo_random.number_of_nodes()}, Arestas: {Grafo_random.number_of_edges()}")
print(f"Densidade: {nx.density(Grafo_random):.6f}")

if nx.is_connected(Grafo_random):
    Clustering_random = nx.average_clustering(Grafo_random)
    Length_random = nx.average_shortest_path_length(Grafo_random)
else:
    lcClustering_random = max(nx.connected_components(Grafo_random), key=len)
    Grafo_random_lcc = Grafo_random.subgraph(lcClustering_random).copy()
    Clustering_random = nx.average_clustering(Grafo_random_lcc)
    Length_random = nx.average_shortest_path_length(Grafo_random_lcc)
    print("A rede aleatória não era conexa; usando a maior componente.")

print(f"Coeficiente de clusterização (aleatória): {Clustering_random:.6f}")
print(f"Comprimento médio dos caminhos (aleatória): {Length_random:.6f}")

if Clustering_random == 0:
    Clustering_random = 1e-10

smallworld = (Clustering_real / Clustering_random) / (Length_real / Length_random)

print(f"\n--- Índice de small-world ---")
print(f"σ = {smallworld:.6f}")
if smallworld > 1:
    print("A rede apresenta propriedade small-world (σ > 1).")
else:
    print("A rede NÃO apresenta propriedade small-world (σ ≤ 1).")

resultados_smallworld = {
    'Clustering_real': Clustering_real,
    'Length_real': Length_real,
    'Clustering_random': Clustering_random,
    'Length_random': Length_random,
    'smallworld': smallworld,
    'is_small_world': smallworld > 1
}
pd.DataFrame([resultados_smallworld]).to_csv("resultados/tabelas/smallworld.csv", index=False)

print("\nResultados salvos em 'resultados/tabelas/smallworld.csv'")
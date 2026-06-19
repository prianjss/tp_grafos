import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

Path("resultados/imagens").mkdir(parents=True, exist_ok=True)
Path("resultados/tabelas").mkdir(parents=True, exist_ok=True)


print("Carregando grafo tratado...")

G = nx.read_graphml("dados/grafo_tratado.graphml")

print(
    f"Grafo carregado: {G.number_of_nodes()} nós e "
    f"{G.number_of_edges()} arestas"
)


print("\nCalculando métricas básicas...")

#Número de vertices, Número de Arestas
num_vertices = G.number_of_nodes()
num_arestas = G.number_of_edges()

#Grau mínimo, máximo e médio
graus = dict(G.degree())
lista_graus = list(graus.values())
grau_min = min(lista_graus)
grau_max = max(lista_graus)
grau_medio = np.mean(lista_graus)

#densidade
densidade = nx.density(G)

#Número de componentes conexas
componentes = list(nx.connected_components(G))
numero_componentes = len(componentes)

#Tamanho de cada componente
tamanho_componentes = sorted(
    [len(c) for c in componentes],
    reverse=True
)

print("\nCalculando métricas de distância...")

#diâmetro, raio, comprimento médio dos caminhos

try:
    diametro = nx.diameter(G)
    raio = nx.radius(G)
    caminho_medio = nx.average_shortest_path_length(G)
    status_distancia = "Computado"

except Exception:
    diametro = None
    raio = None
    caminho_medio = None
    status_distancia = "Não computado"

#Coeficiente de clusterização médio
clusterizacao_media = nx.average_clustering(G)

#Número de triângulos não é viável pois grafo bipartido não possui ciclos ímpares
#Mas está aqui a função para fins de garantia
triangulos = sum(nx.triangles(G).values()) // 3

#tabela com os resultados
metricas = pd.DataFrame(
{
    "Métrica": [
        "Número de vértices",
        "Número de arestas",
        "Grau mínimo",
        "Grau máximo",
        "Grau médio",
        "Densidade",
        "Número de componentes conexas",
        "Tamanho das componentes",
        "Diâmetro",
        "Raio",
        "Comprimento médio dos caminhos",
        "Coeficiente médio de clusterização",
        "Número de triângulos"
    ],

    "Resultado": [
        num_vertices,
        num_arestas,
        grau_min,
        grau_max,
        round(grau_medio,4),
        round(densidade,6),
        numero_componentes,
        tamanho_componentes,
        diametro,
        raio,
        caminho_medio,
        round(clusterizacao_media,4),
        triangulos
    ],

    "Observação": [
        "Computado",
        "Computado",
        "Computado",
        "Computado",
        "Computado",
        "Computado",
        "Computado",
        "Computado",
        status_distancia,
        status_distancia,
        status_distancia,
        "Computado",
        "Grafo bipartido não possui ciclos de tamanho 3"
    ]

})

print(metricas)

metricas.to_csv(
    "resultados/tabelas/metricas_parte1.csv",
    index=False
)

#distribuição de graus
distribuicao = (
    pd.Series(lista_graus)
    .value_counts()
    .sort_index()
)

plt.figure(figsize=(10,5))

plt.plot(
    distribuicao.index,
    distribuicao.values,
    marker='o'
)

plt.xlabel("Grau do vértice")
plt.ylabel("Número de vértices")

plt.title(
    "Distribuição de graus dos vértices"
)

plt.grid(True)

plt.savefig(
    "resultados/imagens/distribuicao_graus.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

#Mini-mini vizualização do grafo
print("Gerando visualização mega reduzida do grafo.")

usuarios = [n for n in G.nodes() if str(n).startswith('U')]
atividades = [n for n in G.nodes() if str(n).startswith('T')]

graus_dict = dict(G.degree())

top_atividades = sorted(atividades, key=lambda x: graus_dict[x], reverse=True)[:5]

vizinhos_selecionados = set()
for ativ in top_atividades:
    vizinhos = list(G.neighbors(ativ))[:15]
    vizinhos_selecionados.update(vizinhos)

nos_amostrados = top_atividades + list(vizinhos_selecionados)
G_reduzido = G.subgraph(nos_amostrados)

plt.figure(figsize=(12, 10))

cores = ['skyblue' if str(n).startswith('U') else 'lightcoral' for n in G_reduzido.nodes()]
tamanhos = [(graus_dict[n] / 30) + 100 for n in G_reduzido.nodes()]
pos = nx.spring_layout(G_reduzido, seed=42, k=0.4)

nx.draw(
    G_reduzido,
    pos,
    node_color=cores,
    node_size=tamanhos,
    edge_color="silver",
    with_labels=False,
    alpha=0.9
)

import matplotlib.patches as mpatches
blue_patch = mpatches.Patch(color='skyblue', label='Usuários')
red_patch = mpatches.Patch(color='lightcoral', label='Atividades')
plt.legend(handles=[blue_patch, red_patch], loc='upper right')

plt.title("Visualização Reduzida (Top 5 Atividades e Amostra de Usuários Conectados)")

plt.savefig("resultados/imagens/grafo_reduzido.png", dpi=300, bbox_inches="tight")
plt.close()
print("Visualização gerada com sucesso!")
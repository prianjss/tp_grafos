import networkx as nx
import numpy as np
import pandas as pd
import time
from pathlib import Path
from scipy import stats

Path("resultados/tabelas").mkdir(parents=True, exist_ok=True)

print("Carregando grafo...")

G = nx.read_graphml("dados/grafo_tratado.graphml")

print(
    f"Grafo carregado: {G.number_of_nodes()} nós | "
    f"{G.number_of_edges()} arestas"
)

# Grafo temporáriamente direcionado para Tarjan
G_direcionado = G.to_directed()

#amostra para algoritmo com complexidade alta
nos_amostra = list(G.nodes())[:100]
G_floyd = G.subgraph(nos_amostra).copy()

# Escolhe um vértice inicial para buscas
origem = max(
    G.degree(),
    key=lambda x: x[1]
)[0]

print("Vértice escolhido:", origem)

#preparação para rodar os algoritmos e guardar valores necessários
def medir_algoritmo(
        nome,
        funcao,
        repeticoes=30,
        distribuicao="Normal (Z)"
):

    tempos = []

    for i in range(repeticoes):
        inicio = time.perf_counter()
        funcao()
        fim = time.perf_counter()
        tempos.append(fim - inicio)

    media = np.mean(tempos)

    desvio = np.std(
        tempos,
        ddof=1
    )

    confianca = 0.95

    if distribuicao == "Normal (Z)":
        valor = stats.norm.ppf(
            1-(1-confianca)/2
        )

    else:
        valor = stats.t.ppf(
            1-(1-confianca)/2,
            df=repeticoes-1
        )

    erro = valor * desvio / np.sqrt(repeticoes)

    return {
        "Algoritmo": nome,
        "Execuções": repeticoes,
        "Média (s)": media,
        "Desvio padrão": desvio,
        "IC 95%": erro,
        "Distribuição": distribuicao
    }

resultados = []

#BFS
resultados.append(
    medir_algoritmo(
        "BFS",
        lambda:
        nx.single_source_shortest_path_length(
            G,
            origem
        )
    )
)

#DFS
resultados.append(
    medir_algoritmo(
        "DFS",
        lambda:
        nx.dfs_tree(
            G,
            origem
        )
    )
)

#dijkstra
resultados.append(
    medir_algoritmo(
        "Dijkstra",
        lambda:
        nx.single_source_dijkstra_path_length(
            G,
            origem,
            weight="weight"
        )
    )
)

#bellman ford
resultados.append(
    medir_algoritmo(
        "Bellman-Ford",
        lambda:
        nx.single_source_bellman_ford_path_length(
            G,
            origem,
            weight="weight"
        ),
        repeticoes=10,
        distribuicao="t-Student"
    )
)

#kruskal
resultados.append(
    medir_algoritmo(
        "Kruskal",
        lambda:
        nx.minimum_spanning_tree(
            G,
            algorithm="kruskal",
            weight="weight"
        )
    )
)

#Prim
resultados.append(
    medir_algoritmo(
        "Prim",
        lambda:
        nx.minimum_spanning_tree(
            G,
            algorithm="prim",
            weight="weight"
        )
    )
)

#Tarjan
resultados.append(
    medir_algoritmo(
        "Tarjan SCC",
        lambda:
        list(
            nx.strongly_connected_components(
                G_direcionado
            )
        )
    )
)

#Floyd
resultados.append(
    medir_algoritmo(
        "Floyd-Warshall (100 nós)",
        lambda:
        nx.floyd_warshall(
            G_floyd,
            weight="weight"
        ),
        repeticoes=10,
        distribuicao="t-Student"
    )
)

#Complexidades
df = pd.DataFrame(resultados)

complexidades = {
"BFS":"O(V+E)",
"DFS":"O(V+E)",
"Dijkstra":"O((V+E)logV)",
"Bellman-Ford":"O(V*E)",
"Kruskal":"O(E log V)",
"Prim":"O(E log V)",
"Tarjan SCC":"O(V+E)",
"Floyd-Warshall (100 nós)":"O(V³)"
}

df.insert(
    1,
    "Complexidade",
    df["Algoritmo"].map(complexidades)
)

print(df)

df.to_csv(
    "resultados/tabelas/desempenho_algoritmos.csv",
    index=False
)

print("\nTabela salva!")
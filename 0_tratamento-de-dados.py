import pandas as pd
import networkx as nx

print("Carregando o dataset...")
caminho_arquivo = 'dados/act-mooc/mooc_actions.tsv'
df = pd.read_csv(caminho_arquivo, sep='\t', skiprows=1,
                names=['ACTIONID', 'USERID', 'TARGETID', 'TIMESTAMP'])

df['USERID'] = 'U_' + df['USERID'].astype(str)
df['TARGETID'] = 'T_' + df['TARGETID'].astype(str)

print("Agrupando arestas repetidas e calculando pesos...")
edges_weights = df.groupby(['USERID', 'TARGETID']).size().reset_index(name='weight')
G = nx.Graph() 
for _, row in edges_weights.iterrows():
    G.add_edge(row['USERID'], row['TARGETID'], weight=float(row['weight']))
connected_components = sorted(nx.connected_components(G), key=len, reverse=True)
largest_component_nodes = connected_components[0]
G_lcc = G.subgraph(largest_component_nodes).copy()

print(f"\nGrafo tratado! Nós: {G_lcc.number_of_nodes()} | Arestas: {G_lcc.number_of_edges()}")

nx.write_graphml(G_lcc, "dados/grafo_tratado.graphml")
print("Grafo tratado salvo em 'dados/grafo_tratado.graphml'!")
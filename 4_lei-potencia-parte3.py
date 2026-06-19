import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from pathlib import Path

G = nx.read_graphml("dados/grafo_tratado.graphml")
graus = np.array([d for _, d in G.degree()])

valores, contagens = np.unique(graus, return_counts=True)
pk = contagens / contagens.sum()

#grafico log log
plt.figure(figsize=(8,6))

plt.loglog(
    valores,
    pk,
    'o',
    markersize=5,
    alpha=0.7,
    label='Observado'
)

plt.xlabel("Grau (k)")
plt.ylabel("P(k)")
plt.title("Distribuição de Graus (log-log)")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(
    "resultados/imagens/distribuicao_graus_loglog.png",
    dpi=300
)
plt.close()

#ccdf
graus_ordenados = np.sort(graus)
ccdf_x = graus_ordenados
ccdf_y = 1.0 - np.arange(1, len(graus_ordenados)+1) / len(graus_ordenados)
xmin = np.percentile(graus, 90)
cauda = graus[graus >= xmin]
gamma = 1 + len(cauda) / np.sum(np.log(cauda / xmin))

print(f"\nxmin escolhido = {xmin:.0f}")
print(f"Nós na cauda = {len(cauda)}")
print(f"Expoente γ = {gamma:.4f}")

x_teorico = np.logspace(
    np.log10(xmin),
    np.log10(max(graus)),
    200
)

ccdf_teorica = (x_teorico / xmin) ** (-(gamma - 1))

#grafico ccdf
plt.figure(figsize=(8,6))

plt.loglog(
    ccdf_x,
    ccdf_y,
    'o',
    markersize=4,
    alpha=0.5,
    label='CCDF observada'
)

plt.loglog(
    x_teorico,
    ccdf_teorica,
    '--',
    linewidth=2,
    label=f'Lei de potência (γ={gamma:.2f})'
)

plt.xlabel("Grau (k)")
plt.ylabel("P(K ≥ k)")
plt.title("CCDF da Distribuição de Graus")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(
    "resultados/imagens/ccdf_lei_potencia.png",
    dpi=300
)
plt.close()

u = np.random.random(len(cauda))

sintetica = xmin * (1 - u) ** (-1 / (gamma - 1))

ks_stat, ks_p = stats.ks_2samp(
    cauda,
    sintetica
)

print("\nTeste KS (cauda):")
print(f"KS = {ks_stat:.4f}")
print(f"p-valor = {ks_p:.4f}")

if ks_p > 0.05:
    print("Não rejeitamos a hipótese de lei de potência.")
else:
    print("Rejeitamos a hipótese de lei de potência.")

pd.DataFrame([{
    "xmin": xmin,
    "gamma": gamma,
    "ks_stat": ks_stat,
    "ks_p": ks_p
}]).to_csv(
    "resultados/tabelas/lei_potencia.csv",
    index=False
)

print("\nResultados salvos.")
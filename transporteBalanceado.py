# Ejemplo de transporte balanceado

import pulp
import networkx as nx
import matplotlib.pyplot as plt

# Definir los nodos
fabricas = ["F1", "F2", "F3"]
almacenes = ["A1", "A2", "A3"]

# Oferta (capacidad de cada fábrica)
oferta = {"F1": 20, "F2": 30, "F3": 50}

# Demanda (cantidad requerida por cada almacén)
demanda = {"A1": 30, "A2": 30, "A3": 40}

# Costos de transporte por unidad (matriz de costos)
costos = {
    ("F1", "A1"): 8,  ("F1", "A2"): 6,  ("F1", "A3"): 10,
    ("F2", "A1"): 9,  ("F2", "A2"): 12, ("F2", "A3"): 13,
    ("F3", "A1"): 14, ("F3", "A2"): 9,  ("F3", "A3"): 16,
}

# Crear el problema de minimización de costos
problema = pulp.LpProblem("Transporte_Balanceado", pulp.LpMinimize)

# Variables de decisión: x_ij (cantidad transportada de Fi a Aj)
x = {(i, j): pulp.LpVariable(f"x_{i}_{j}", lowBound=0, cat="Continuous") for i in fabricas for j in almacenes}

# Función objetivo: minimizar el costo total de transporte
problema += pulp.lpSum(x[i, j] * costos[i, j] for i in fabricas for j in almacenes)

# Restricciones de oferta (cada fábrica no puede enviar más de lo que tiene)
for i in fabricas:
    problema += pulp.lpSum(x[i, j] for j in almacenes) == oferta[i]

# Restricciones de demanda (cada almacén debe recibir exactamente lo que necesita)
for j in almacenes:
    problema += pulp.lpSum(x[i, j] for i in fabricas) == demanda[j]

# Resolver el problema
problema.solve()

# Mostrar la solución óptima
print("Estado de la solución:", pulp.LpStatus[problema.status])
for i, j in x:
    print(f"Transporte de {i} a {j}: {x[i, j].varValue} unidades")

# --- Visualización con NetworkX ---
G = nx.DiGraph()

# Agregar nodos
for i in fabricas:
    G.add_node(i, color="lightblue")
for j in almacenes:
    G.add_node(j, color="lightgreen")

# Agregar aristas con las cantidades óptimas transportadas
edges = []
edge_labels = {}
for (i, j), var in x.items():
    cantidad = var.varValue
    if cantidad > 0:  # Solo dibujar las conexiones activas
        G.add_edge(i, j, weight=cantidad)
        edges.append((i, j))
        edge_labels[(i, j)] = f"{cantidad:.0f}"

# Dibujar el grafo
pos = {**{i: (0, idx) for idx, i in enumerate(fabricas)}, **{j: (1, idx) for idx, j in enumerate(almacenes)}}
colors = [G.nodes[n]["color"] for n in G.nodes]

plt.figure(figsize=(8, 5))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color=colors, font_size=10, edge_color="gray", width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
plt.title("Solución Óptima del Problema de Transporte")
plt.show()

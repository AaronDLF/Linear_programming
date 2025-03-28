from pulp import LpMinimize, LpProblem, LpVariable, lpSum
import networkx as nx
import matplotlib.pyplot as plt

# Definir el problema de minimización
model = LpProblem(name="minimizar_costo_energia", sense=LpMinimize)

# Variables de decisión (energía enviada desde cada planta a cada ciudad)
x = {
    (i, j): LpVariable(name=f"x_{i}_{j}", lowBound=0)
    for i in range(1, 4) for j in range(1, 5)
}

# Costos unitarios de envío
costos = {
    (1, 1): 8, (1, 2): 6, (1, 3): 10, (1, 4): 9,
    (2, 1): 9, (2, 2): 12, (2, 3): 13, (2, 4): 7,
    (3, 1): 14, (3, 2): 9, (3, 3): 16, (3, 4): 5,
}

# Función objetivo: minimizar el costo total
model += lpSum(costos[i, j] * x[i, j] for i in range(1, 4) for j in range(1, 5)), "Costo_Total"

# Restricciones de oferta (capacidad máxima de cada planta)
ofera = {1: 35, 2: 50, 3: 40}
for i in range(1, 4):
    model += lpSum(x[i, j] for j in range(1, 5)) <= ofera[i], f"Oferta_P{i}"

# Restricciones de demanda (cada ciudad debe recibir la energía requerida)
demanda = {1: 45, 2: 20, 3: 30, 4: 30}
for j in range(1, 5):
    model += lpSum(x[i, j] for i in range(1, 4)) >= demanda[j], f"Demanda_C{j}"

# Resolver el problema
model.solve()

# Imprimir resultados
print("Estado de la solución:", model.status)
for i in range(1, 4):
    for j in range(1, 5):
        print(f"Energía enviada de Planta {i} a Ciudad {j}: {x[i, j].varValue} millones de kWh")
print("Costo total mínimo:", model.objective.value())

# Graficar el problema
G = nx.DiGraph()

# Agregar nodos
plantas = ["Planta 1", "Planta 2", "Planta 3"]
ciudades = ["Ciudad 1", "Ciudad 2", "Ciudad 3", "Ciudad 4"]
G.add_nodes_from(plantas, bipartite=0)
G.add_nodes_from(ciudades, bipartite=1)

# Agregar aristas con los valores de energía enviada
edges = []
labels = {}
for i in range(1, 4):
    for j in range(1, 5):
        valor = x[i, j].varValue
        if valor > 0:
            G.add_edge(f"Planta {i}", f"Ciudad {j}", weight=valor)
            labels[(f"Planta {i}", f"Ciudad {j}")] = f"{valor}"

# Posicionamiento de nodos
pos = {
    **{plantas[i]: (0, -i) for i in range(3)},
    **{ciudades[i]: (1, -i) for i in range(4)},
}

# Dibujar el gráfico
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=3000, font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')
plt.title("Flujo de Energía entre Plantas y Ciudades")
plt.show()
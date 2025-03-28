from pulp import LpMinimize, LpProblem, LpVariable, lpSum
import networkx as nx
import matplotlib.pyplot as plt

# Definir la matriz de costos (en millones de u.m.)
cost_matrix = [
    [280, 320, 360],  # Costos del contratista C1
    [360, 280, 300],  # Costos del contratista C2
    [380, 340, 400]   # Costos del contratista C3
]

num_contratistas = len(cost_matrix)
num_proyectos = len(cost_matrix[0])

# Definir el problema de optimización
prob = LpProblem("Asignacion_de_Proyectos", LpMinimize)

# Variables de decisión: x[i][j] = 1 si el contratista i hace el proyecto j, 0 en caso contrario
x = [[LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(num_proyectos)] for i in range(num_contratistas)]

# Función objetivo: minimizar el costo total de asignación
prob += lpSum(cost_matrix[i][j] * x[i][j] for i in range(num_contratistas) for j in range(num_proyectos))

# Restricciones: Cada proyecto debe ser asignado a un solo contratista
for j in range(num_proyectos):
    prob += lpSum(x[i][j] for i in range(num_contratistas)) == 1

# Restricciones: Cada contratista debe recibir solo un proyecto
for i in range(num_contratistas):
    prob += lpSum(x[i][j] for j in range(num_proyectos)) == 1

# Resolver el problema
prob.solve()

# Imprimir la asignación óptima
print("Asignación óptima:")
total_cost = 0
asignaciones = []
for i in range(num_contratistas):
    for j in range(num_proyectos):
        if x[i][j].varValue == 1:
            print(f"Proyecto P{j+1} asignado a C{i+1} con costo {cost_matrix[i][j]} millones de u.m.")
            total_cost += cost_matrix[i][j]
            asignaciones.append((f"C{i+1}", f"P{j+1}"))

print(f"Costo total mínimo: {total_cost} millones de u.m.")

# Visualización con NetworkX
G = nx.Graph()

# Agregar nodos
contratistas_nodos = [f"C{i+1}" for i in range(num_contratistas)]
proyectos_nodos = [f"P{j+1}" for j in range(num_proyectos)]

G.add_nodes_from(contratistas_nodos, bipartite=0)
G.add_nodes_from(proyectos_nodos, bipartite=1)

# Agregar aristas según la asignación óptima
G.add_edges_from(asignaciones)

# Posiciones para visualizar en dos columnas
pos = {}
pos.update((n, (0, i)) for i, n in enumerate(contratistas_nodos))  # Contratistas a la izquierda
pos.update((n, (1, i)) for i, n in enumerate(proyectos_nodos))  # Proyectos a la derecha

# Dibujar el grafo
plt.figure(figsize=(6, 4))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", edge_color="black", font_size=12)
plt.title("Asignación Óptima de Contratistas a Proyectos")
plt.show()

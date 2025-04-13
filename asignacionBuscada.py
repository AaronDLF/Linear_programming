import pulp
import networkx as nx
import matplotlib.pyplot as plt

# Definimos los conjuntos de empleados y tareas
empleados = ["Empleado 1", "Empleado 2", "Empleado 3"]
tareas = ["Tarea 1", "Tarea 2", "Tarea 3"]

# Costos de asignación
costos = {
    ("Empleado 1", "Tarea 1"): 10, ("Empleado 1", "Tarea 2"): 2, ("Empleado 1", "Tarea 3"): 8,
    ("Empleado 2", "Tarea 1"): 7, ("Empleado 2", "Tarea 2"): 5, ("Empleado 2", "Tarea 3"): 3,
    ("Empleado 3", "Tarea 1"): 4, ("Empleado 3", "Tarea 2"): 9, ("Empleado 3", "Tarea 3"): 6,
}

# Definir el problema de optimización
problema = pulp.LpProblem("Problema_de_Asignacion", pulp.LpMinimize)

# Variables de decisión
x = pulp.LpVariable.dicts("Asignacion", costos, cat=pulp.LpBinary)

# Función objetivo: Minimizar el costo total
problema += pulp.lpSum(costos[i] * x[i] for i in costos), "Costo_Total"

# Restricción: Cada empleado solo realiza una tarea
for e in empleados:
    problema += pulp.lpSum(x[(e, t)] for t in tareas) == 1

# Restricción: Cada tarea debe ser asignada a un único empleado
for t in tareas:
    problema += pulp.lpSum(x[(e, t)] for e in empleados) == 1

# Resolver el problema
problema.solve()

# Obtener los resultados
asignaciones = [(e, t) for e in empleados for t in tareas if x[(e, t)].varValue == 1]

# Crear y graficar el grafo
G = nx.DiGraph()
for e, t in asignaciones:
    G.add_edge(e, t, weight=costos[(e, t)])

pos = nx.bipartite_layout(G, nodes=empleados)
labels = {(e, t): costos[(e, t)] for e, t in asignaciones}

plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", edge_color="gray", font_size=10)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)
plt.title("Asignación Óptima de Empleados a Tareas")
plt.show()

# Mostrar las asignaciones óptimas
asignaciones

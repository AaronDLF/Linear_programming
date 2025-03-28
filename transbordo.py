from pulp import LpMinimize, LpProblem, LpVariable, lpSum
import networkx as nx
import matplotlib.pyplot as plt


# Definir nodos y capacidades
plantas = {"Texas": 100, "Iowa": 200, "Oregon": 150}
almacenes_regionales = ["Hungría", "Hawai"]
almacenes_campo = ["Filipinas", "Fiji"]
clientes = {"Japón": 120, "Corea del Sur": 80, "Nueva Zelanda": 70, "Australia": 110}

# Costos de embarque (tablas 1, 2 y 3)
costos_plantas_regionales = {
    ("Texas", "Hungría"): 2, ("Texas", "Hawai"): 4,
    ("Iowa", "Hungría"): 3, ("Iowa", "Hawai"): 4,
    ("Oregon", "Hawai"): 5  # Oregon no puede enviar a Hungría
}
costos_regionales_campo = {
    ("Hungría", "Filipinas"): 8, ("Hungría", "Fiji"): 6,
    ("Hawai", "Filipinas"): 7, ("Hawai", "Fiji"): 4
}
costos_campo_clientes = {
    ("Filipinas", "Japón"): 7, ("Filipinas", "Corea del Sur"): 6, ("Filipinas", "Nueva Zelanda"): 8,
    ("Fiji", "Corea del Sur"): 7, ("Fiji", "Nueva Zelanda"): 5, ("Fiji", "Australia"): 6
}

# Definir el problema de optimización
problema = LpProblem("Problema_Transbordo", LpMinimize)

# Variables de decisión
x = {}
for (origen, destino) in list(costos_plantas_regionales.keys()) + list(costos_regionales_campo.keys()) + list(costos_campo_clientes.keys()):
    x[(origen, destino)] = LpVariable(f"x_{origen}_{destino}", lowBound=0, cat='Continuous')

# Función objetivo: Minimizar costo total
total_cost = lpSum(x[(o, d)] * c for (o, d), c in {**costos_plantas_regionales, **costos_regionales_campo, **costos_campo_clientes}.items())
problema += total_cost

# Restricciones de oferta (producción de plantas)
for planta, capacidad in plantas.items():
    problema += lpSum(x[(planta, almacen)] for almacen in almacenes_regionales if (planta, almacen) in x) <= capacidad

# Restricciones de demanda (requerimiento de clientes)
for cliente, demanda in clientes.items():
    problema += lpSum(x[(almacen, cliente)] for almacen in almacenes_campo if (almacen, cliente) in x) >= demanda

# Restricciones de flujo (lo que entra a un almacén debe salir)
for almacen in almacenes_regionales:
    problema += lpSum(x[(planta, almacen)] for planta in plantas if (planta, almacen) in x) == lpSum(x[(almacen, campo)] for campo in almacenes_campo if (almacen, campo) in x)
for almacen in almacenes_campo:
    problema += lpSum(x[(regional, almacen)] for regional in almacenes_regionales if (regional, almacen) in x) == lpSum(x[(almacen, cliente)] for cliente in clientes if (almacen, cliente) in x)

# Resolver el problema
problema.solve()

# Mostrar resultados
print("Estado de la solución:", problema.status)
print("Costo mínimo total:", problema.objective.value())
for (origen, destino), var in x.items():
    if var.value() > 0:
        print(f"Enviar {var.value()} equipos desde {origen} a {destino}")

# Crear un grafo dirigido
G = nx.DiGraph()

# Agregar nodos
nodos = ["Fiji", "Nueva Zelanda", "Australia", "Corea del Sur", "Japón", "Hungría", "Texas", "Filipinas"]
G.add_nodes_from(nodos)

# Agregar aristas con pesos
aristas = [
    ("Fiji", "Nueva Zelanda", 70),
    ("Fiji", "Australia", 110),
    ("Fiji", "Corea del Sur", 80),
    ("Fiji", "Japón", 20),
    ("Japón", "Hungría", 10),
    ("Japón", "Texas", 15),
    ("Japón", "Filipinas", 5)
]
G.add_weighted_edges_from(aristas)

# Aplicar un layout más ordenado
pos = nx.spring_layout(G, k=1.2, seed=42)  # k ajusta la distancia entre nodos

# Configurar el tamaño de la figura
plt.figure(figsize=(10, 8))

# Dibujar nodos y aristas
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=2000, edge_color="gray", font_size=12, font_weight="bold", arrowsize=15)

# Dibujar los pesos de las aristas
labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)

# Mostrar el gráfico
plt.show()



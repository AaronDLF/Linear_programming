import pulp

def transporte_ple():
    # Crear el problema de minimización
    prob = pulp.LpProblem("Transporte_Vehiculos", pulp.LpMinimize)

    # Definición de variables de decisión (cantidad de vehículos enviados de cada fábrica a cada destino)
    x_AD1 = pulp.LpVariable("x_AD1", lowBound=0, cat='Integer')
    x_AD2 = pulp.LpVariable("x_AD2", lowBound=0, cat='Integer')
    x_BD1 = pulp.LpVariable("x_BD1", lowBound=0, cat='Integer')
    x_BD2 = pulp.LpVariable("x_BD2", lowBound=0, cat='Integer')
    x_CD1 = pulp.LpVariable("x_CD1", lowBound=0, cat='Integer')
    x_CD2 = pulp.LpVariable("x_CD2", lowBound=0, cat='Integer')

    # Función objetivo: minimizar el costo total (distancia * cantidad transportada)
    prob += (
        1000 * x_AD1 + 2690 * x_AD2 +
        1250 * x_BD1 + 1350 * x_BD2 +
        1275 * x_CD1 + 850 * x_CD2
    ), "Costo_Total_Transporte"

    # Restricciones de capacidad por factoría
    prob += x_AD1 + x_AD2 <= 1000, "Capacidad_Fabrica_A"
    prob += x_BD1 + x_BD2 <= 1500, "Capacidad_Fabrica_B"
    prob += x_CD1 + x_CD2 <= 1200, "Capacidad_Fabrica_C"

    # Restricciones de demanda por centro de distribución
    prob += x_AD1 + x_BD1 + x_CD1 == 2300, "Demanda_D1"
    prob += x_AD2 + x_BD2 + x_CD2 == 1400, "Demanda_D2"

    # Resolver el problema
    prob.solve()

    # Mostrar resultados
    print("Estado de la solución:", pulp.LpStatus[prob.status])
    print("Costo total de transporte =", pulp.value(prob.objective))
    print("Vehículos transportados:")
    print(f"  A -> D1: {x_AD1.varValue}")
    print(f"  A -> D2: {x_AD2.varValue}")
    print(f"  B -> D1: {x_BD1.varValue}")
    print(f"  B -> D2: {x_BD2.varValue}")
    print(f"  C -> D1: {x_CD1.varValue}")
    print(f"  C -> D2: {x_CD2.varValue}")

transporte_ple()
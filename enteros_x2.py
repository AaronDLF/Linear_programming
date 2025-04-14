import pulp

def branch_and_bound():
    # Paso 1: Crear el problema de optimización
    prob = pulp.LpProblem("Maximizar_Z", pulp.LpMaximize)

    # Paso 2: Definir las variables de decisión (como variables continuas)
    x1 = pulp.LpVariable("x1", lowBound=0, cat='Continuous')
    x2 = pulp.LpVariable("x2", lowBound=0, cat='Continuous')

    # Paso 3: Definir la función objetivo
    prob += 80*x1 + 45*x2, "Z"

    # Paso 4: Añadir las restricciones
    prob += x1 + x2 <= 7, "Restricción 1"
    prob += 12 * x1 + 5 * x2 <= 60, "Restricción 2"
    prob += x1 >= 4, "Restricción 3"
    prob += x2 <= 2, "Restricción 4"
    prob += x1 <= 4, "Restricción 5"

    # Paso 5: Resolver el problema relajado
    prob.solve()

    # Paso 6: Comprobar si la solución es entera
    if x1.varValue.is_integer() and x2.varValue.is_integer():
        print(f"Solución entera encontrada: x1 = {x1.varValue}, x2 = {x2.varValue}")
        print(f"Valor de la función objetivo Z = {pulp.value(prob.objective)}")
        return pulp.value(prob.objective)

    else:
        print(f"Solución relajada (no entera): x1 = {x1.varValue}, x2 = {x2.varValue}")
        print(f"Valor de la función objetivo Z = {pulp.value(prob.objective)}")

        # Primero ramificar sobre x2
        if not x2.varValue.is_integer():
            ceil_x2 = int(x2.varValue) + 1
            floor_x2 = int(x2.varValue)

            # Subproblema 3: x2 >= ceil(x2)
            prob3 = pulp.LpProblem("Subproblema 3", pulp.LpMaximize)
            x1_3 = pulp.LpVariable("x1", lowBound=0, cat='Continuous')
            x2_3 = pulp.LpVariable("x2", lowBound=ceil_x2, cat='Continuous')
            prob3 += 80*x1_3 + 45*x2_3, "Z"
            prob3 += x1_3 + x2_3 <= 7
            prob3 += 12 * x1_3 + 5 * x2_3 <= 60
            prob3 += x1_3 >= 4
            prob3 += x2_3 <= 2
            prob3 += x1_3 <= 4
            prob3.solve()
            print(f"\nSubproblema 3 (x2 >= {ceil_x2}):")
            print(f"x1 = {x1_3.varValue}, x2 = {x2_3.varValue}")
            print(f"Valor de Z = {pulp.value(prob3.objective)}")

            # Subproblema 4: x2 <= floor(x2)
            prob4 = pulp.LpProblem("Subproblema 4", pulp.LpMaximize)
            x1_4 = pulp.LpVariable("x1", lowBound=0, cat='Continuous')
            x2_4 = pulp.LpVariable("x2", lowBound=0, upBound=floor_x2, cat='Continuous')
            prob4 += 80*x1_4 + 45*x2_4, "Z"
            prob4 += x1_4 + x2_4 <= 7
            prob4 += 12 * x1_4 + 5 * x2_4 <= 60
            prob4 += x1_4 >= 4
            prob4 += x2_4 <= 2
            prob4 += x1_4 <= 4
            prob4.solve()
            print(f"\nSubproblema 4 (x2 <= {floor_x2}):")
            print(f"x1 = {x1_4.varValue}, x2 = {x2_4.varValue}")
            print(f"Valor de Z = {pulp.value(prob4.objective)}")

            # Recursión si es necesario
            result = branch_and_bound()
            return result

        # Luego ramificar sobre x1 si es necesario
        elif not x1.varValue.is_integer():
            ceil_x1 = int(x1.varValue) + 1
            floor_x1 = int(x1.varValue)

            # Subproblema 1: x1 >= ceil(x1)
            prob1 = pulp.LpProblem("Subproblema 1", pulp.LpMaximize)
            x1_1 = pulp.LpVariable("x1", lowBound=ceil_x1, cat='Continuous')
            x2_1 = pulp.LpVariable("x2", lowBound=0, cat='Continuous')
            prob1 += 80*x1_1 + 45*x2_1, "Z"
            prob1 += x1_1 + x2_1 <= 7
            prob1 += 12 * x1_1 + 5 * x2_1 <= 60
            prob1 += x1_1 >= 4
            prob1 += x2_1 <= 2
            prob1 += x1_1 <= 4
            prob1.solve()
            print(f"\nSubproblema 1 (x1 >= {ceil_x1}):")
            print(f"x1 = {x1_1.varValue}, x2 = {x2_1.varValue}")
            print(f"Valor de Z = {pulp.value(prob1.objective)}")

            # Subproblema 2: x1 <= floor(x1)
            prob2 = pulp.LpProblem("Subproblema 2", pulp.LpMaximize)
            x1_2 = pulp.LpVariable("x1", lowBound=0, upBound=floor_x1, cat='Continuous')
            x2_2 = pulp.LpVariable("x2", lowBound=0, cat='Continuous')
            prob2 += 80*x1_2 + 45*x2_2, "Z"
            prob2 += x1_2 + x2_2 <= 7
            prob2 += 12 * x1_2 + 5 * x2_2 <= 60
            prob2 += x1_2 >= 4
            prob2 += x2_2 <= 2
            prob2 += x1_2 <= 4
            prob2.solve()
            print(f"\nSubproblema 2 (x1 <= {floor_x1}):")
            print(f"x1 = {x1_2.varValue}, x2 = {x2_2.varValue}")
            print(f"Valor de Z = {pulp.value(prob2.objective)}")

            result = branch_and_bound()
            return result

#se evalua finalmente la función para verificar el resultado 
branch_and_bound()

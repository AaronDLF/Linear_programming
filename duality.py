import numpy as np
import pulp

# Función para resolver el primal y generar su dual automáticamente
def solve_primal_and_dual_pdf_case():
    # === DATOS DEL PROBLEMA DEL PDF ===
    # Max Z = 50x1 + 40x2
    # s.a.
    #   3x1 + 5x2 ≤ 150
    #         1x2 ≤ 20
    #   8x1 + 5x2 ≤ 300
    #   x1, x2 ≥ 0

    c = [50, 40]  # coeficientes de la función objetivo
    A = [
        [3, 5],
        [0, 1],
        [8, 5]
    ]
    b = [150, 20, 300]

    n = len(c)     # variables (x1, x2)
    m = len(b)     # restricciones

    # === PRIMAL ===
    primal = pulp.LpProblem("Problema_Primal", pulp.LpMaximize)
    x_vars = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(n)]
    primal += pulp.lpDot(c, x_vars)

    # Guardar restricciones para calcular holguras después
    constraints = []
    for i in range(m):
        constraint = pulp.lpDot(A[i], x_vars) <= b[i]
        primal += constraint
        constraints.append(constraint)

    primal.solve()
    x_sol = [var.varValue for var in x_vars]
    z_opt = pulp.value(primal.objective)

    # Calcular valores de holgura (slacks)
    slacks = [constraint.slack for constraint in constraints]

    # === DUAL ===
    A_T = np.array(A).T.tolist()
    dual = pulp.LpProblem("Problema_Dual", pulp.LpMinimize)
    y_vars = [pulp.LpVariable(f"y{i+1}", lowBound=0) for i in range(m)]
    dual += pulp.lpDot(b, y_vars)

    for j in range(n):
        coeff = [-A_T[j][i] for i in range(m)]
        dual += pulp.lpDot(coeff, y_vars) <= -c[j]

    dual.solve()
    y_sol = [var.varValue for var in y_vars]
    w_opt = pulp.value(dual.objective)

    # === RESULTADOS ===
    print("===== PRIMAL =====")
    for i, val in enumerate(x_sol):
        print(f"x{i+1} = {val}")
    print(f"Valor óptimo Z = {z_opt}")
    print("Estado:", pulp.LpStatus[primal.status])

    print("\n--- Holguras (Slack variables) ---")
    for i, slack in enumerate(slacks):
        print(f"s{i+1} = {slack}")

    print("\n===== DUAL =====")
    for i, val in enumerate(y_sol):
        print(f"y{i+1} = {val}")
    print(f"Valor óptimo W = {w_opt}")
    print("Estado:", pulp.LpStatus[dual.status])

# Ejecutar la función
solve_primal_and_dual_pdf_case()

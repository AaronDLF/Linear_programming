import pulp
import numpy as np

def solve_custom_example():
    # === Datos transformados del problema ===
    # Max Z = -2x1 + 3x2
    # s.a.
    # x1 + 2x2           ≤ 12
    # -4x1 + x2          ≤ -3
    # 6x1 - x2           ≤ 10
    # -6x1 + x2          ≤ -10
    # x1, x2 ≥ 0

    c = [-2, 3]  # función objetivo transformada (max en vez de min)
    A = [
        [1, 2],
        [-4, 2],
        [6, -1],
        [-6, 1]
    ]
    b = [12, -3, 10, -10]

    n = len(c)
    m = len(b)

    # === PRIMAL ===
    primal = pulp.LpProblem("Problema_Primal", pulp.LpMaximize)
    x_vars = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(n)]
    primal += pulp.lpDot(c, x_vars)

    primal_constraints = []
    for i in range(m):
        constraint = pulp.lpDot(A[i], x_vars) <= b[i]
        primal += constraint
        primal_constraints.append(constraint)

    primal.solve()
    x_sol = [var.varValue for var in x_vars]
    z_opt = pulp.value(primal.objective)
    primal_slacks = [con.slack for con in primal_constraints]

    # === DUAL ===
    A_T = np.array(A).T.tolist()
    dual = pulp.LpProblem("Problema_Dual", pulp.LpMinimize)
    y_vars = [pulp.LpVariable(f"y{i+1}", lowBound=0) for i in range(m)]
    dual += pulp.lpDot(b, y_vars)

    dual_constraints = []
    for j in range(n):
        coeff = [-A_T[j][i] for i in range(m)]
        constraint = pulp.lpDot(coeff, y_vars) <= -c[j]
        dual += constraint
        dual_constraints.append(constraint)

    dual.solve()
    y_sol = [var.varValue for var in y_vars]
    w_opt = pulp.value(dual.objective)

    # === RESULTADOS ===
    print("===== PRIMAL =====")
    for i, val in enumerate(x_sol):
        print(f"x{i+1} = {val}")
    print(f"Valor óptimo Z (max) = {z_opt}")
    print(f"Valor original de f (min) = {-z_opt}")
    print("Estado:", pulp.LpStatus[primal.status])

    print("\n--- Holguras del PRIMAL ---")
    for i, slack in enumerate(primal_slacks):
        print(f"s{i+1} = {slack}")

    print("\n===== DUAL =====")
    for i, val in enumerate(y_sol):
        print(f"y{i+1} = {val}")
    print(f"Valor óptimo W = {w_opt}")
    print("Estado:", pulp.LpStatus[dual.status])

solve_custom_example()

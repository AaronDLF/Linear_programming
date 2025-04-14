import pulp

# Función para resolver el modelo y comprobar optimalidad
def resolver_modelo_y_comprobar(c1, c2, c3, b1, b2, b3, b4, descripcion, base_referencia=None):
    modelo = pulp.LpProblem("Sensibilidad_Validacion", pulp.LpMaximize)

    # Variables de decisión
    x1 = pulp.LpVariable("x1", lowBound=0)
    x2 = pulp.LpVariable("x2", lowBound=0)
    x3 = pulp.LpVariable("x3", lowBound=0)

    # Función objetivo
    modelo += c1 * x1 + c2 * x2 + c3 * x3, "Z"

    # Restricciones
    modelo += x1 + 2 * x2 + x3 <= b1, "R1"
    modelo += 2 * x1 + x2 + x3 <= b2, "R2"
    modelo += x1 + x3 >= b3, "R3"
    modelo += x2 + x3 == b4, "R4"

    modelo.solve()

    print("\n--- {} ---".format(descripcion))
    print("Coeficientes: c1 = {}, c2 = {}, c3 = {} | RHS: b1 = {}, b2 = {}, b3 = {}, b4 = {}".format(c1, c2, c3, b1, b2, b3, b4))
    print("Estado:", pulp.LpStatus[modelo.status])
    print("Valor óptimo de Z:", pulp.value(modelo.objective))

    # Obtener base actual
    base_actual = set(v.name for v in modelo.variables() if v.varValue > 0)
    print("Variables básicas:")
    for v in modelo.variables():
        estado = "básica" if v.name in base_actual else "no básica"
        print(f"  {v.name} = {v.varValue} ({estado})")

    # Comparación con la base de referencia si se proporciona
    if base_referencia is not None:
        if base_actual == base_referencia:
            print("✅ La base óptima se mantiene igual.")
        else:
            print("❌ La base óptima cambió respecto al caso original.")

    return base_actual


# Caso original (condición óptima garantizada)
base_original = resolver_modelo_y_comprobar(2, 3, 4, 300, 400, 120, 80, "Caso original del ejercicio")

# Caso dentro del intervalo de sensibilidad (misma base óptima)
resolver_modelo_y_comprobar(2, 6, 4, 300, 400, 120, 80, "Caso fuera del intervalo de sensibilidad", base_referencia=base_original)

# Caso fuera del intervalo de sensibilidad (la base óptima cambia)
resolver_modelo_y_comprobar(2.1, 2.9, 4, 310, 390, 120, 80, "Caso dentro del intervalo de sensibilidad", base_referencia=base_original)



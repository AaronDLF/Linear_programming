import math
def modelo_mm3(lam, mu, k):
  print("🔹 Modelo M/M/3")
  print(f"λ = {lam}, μ = {mu}, k = {k}")
  A = lam / mu
  rho = lam / (k * mu)

  # Verificación de estabilidad
  if rho >= 1:
      print(f"❌ El sistema NO es estable (ρ = {round(rho, 4)} ≥ 1)")
      return
  else:
      print(f"✅ El sistema es estable (ρ = {round(rho, 4)} < 1)")

  # a) Cálculo de P0
  sumatoria = sum([(1 / math.factorial(n)) * (A ** n) for n in range(k)])
  termino_final = (1 / math.factorial(k)) * (A ** k) * ((k * mu) / (k * mu - lam))
  denominador = sumatoria + termino_final
  P0 = 1 / denominador
  print(f"Probabilidad de que el sistema esté vacío (P₀): {round(P0, 4)}")

  # b) Lq
  Lq = (P0 * (A ** k) * rho) / (math.factorial(k) * ((1 - rho) ** 2))
  print(f"Número promedio de estudiantes en la cola (Lq): {round(Lq, 3)}")

  # c) L, Wq, W
  Wq = Lq / lam
  W = Wq + (1 / mu)
  L = W * lam
  print(f"Tiempo promedio en la cola (Wq): {round(Wq * 60, 2)} segundos")
  print(f"Tiempo promedio en el sistema (W): {round(W * 60, 2)} segundos")
  print(f"Número promedio de estudiantes en el sistema (L): {round(L, 3)}")
  print(f"Utilización promedio del sistema (ρ): {round(rho, 4)} ({round(rho*100, 2)}%)")
  print("-" * 50)

modelo_mm3(lam=100, mu=40, k=3)

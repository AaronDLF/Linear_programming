def modelo_mm1(lam, mu):
  print("🔹 Modelo M/M/1")
  print(f"λ = {lam}, μ = {mu}")
  # a) Utilización del servidor
  rho = lam / mu
  print(f"Utilización del servidor (ρ): {round(rho, 4)} ({round(rho*100, 2)}%)")

  # b) Número promedio de estudiantes en el sistema y en la cola
  L = rho / (1 - rho)
  Lq = rho**2 / (1 - rho)
  print(f"Número promedio de estudiantes en el sistema (L): {round(L, 2)}")
  print(f"Número promedio de estudiantes en la cola (Lq): {round(Lq, 2)}")

  # c) Tiempos promedio en el sistema y en la cola
  W = 1 / (mu - lam)
  Wq = lam / (mu * (mu - lam))
  print(f"Tiempo promedio en el sistema (W): {round(W*60, 2)} segundos")
  print(f"Tiempo promedio en la cola (Wq): {round(Wq*60, 2)} segundos")

  # d) Estabilidad
  es_estable = lam < mu
  print(f"¿Sistema estable?: {'Sí' if es_estable else 'No'}")
  print("-" * 50)

modelo_mm1(lam=100, mu=120)
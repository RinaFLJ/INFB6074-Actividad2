import multiprocessing as mp
import time
import numpy as np
import pandas as pd
import os

# Tarea pesada: Calcular la suma de cuadrados de un array grande
def tarea_pesada(data_chunk):
    return np.sum(np.square(data_chunk))

def ejecutar_experimento_c():
    # Tamaños de datos (1M a 20M de elementos)
    tamanos = [1000000, 5000000, 10000000, 20000000]
    n_repeticiones = 5
    cores_disponibles = mp.cpu_count()
    resultados = []

    print(f"Detectados {cores_disponibles} hilos en tu Ryzen 5.")
    print(f"{'Elementos':<12} | {'Secuencial(s)':<15} | {'Paralelo(s)':<15} | {'Speedup'}")
    print("-" * 70)

    for n in tamanos:
        data = np.random.rand(n)
        
        tiempos_sec = []
        tiempos_par = []

        for _ in range(n_repeticiones):
            # --- Modo Secuencial ---
            start = time.perf_counter()
            _ = tarea_pesada(data)
            tiempos_sec.append(time.perf_counter() - start)

            # --- Modo Paralelo ---
            # Dividimos la data en partes según los cores
            chunks = np.array_split(data, cores_disponibles)
            start = time.perf_counter()
            with mp.Pool(processes=cores_disponibles) as pool:
                _ = pool.map(tarea_pesada, chunks)
            tiempos_par.append(time.perf_counter() - start)

        # Promedios
        avg_sec = sum(tiempos_sec) / n_repeticiones
        avg_par = sum(tiempos_par) / n_repeticiones
        speedup = avg_sec / avg_par

        resultados.append({
            "Elementos": n,
            "Tiempo_Secuencial_s": avg_sec,
            "Tiempo_Paralelo_s": avg_par,
            "Speedup": speedup
        })

        print(f"{n:<12} | {avg_sec:<15.4f} | {avg_par:<15.4f} | {speedup:.2f}x")

    # Guardar resultados (Compatibilidad Excel Chile)
    df = pd.DataFrame(resultados).round(4)
    output_path = "../datos/resultados_experimento_c.csv"
    os.makedirs("../datos", exist_ok=True)
    df.to_csv(output_path, sep=';', decimal=',', index=False, encoding='utf-8-sig')
    print(f"\n[OK] Experimento C finalizado. Datos en: {output_path}")

if __name__ == "__main__":
    ejecutar_experimento_c()
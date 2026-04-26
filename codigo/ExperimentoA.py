import numpy as np
import time
import os
import pandas as pd

def benchmark_utem_final():
    tamanos_mb = [1, 10, 100, 500, 1000]
    n_repeticiones = 5
    resultados_finales = []

    # Encabezado con los nombres simples que sugeriste
    print(f"{'Tamaño':<8} | {'Prom. RAM':<12} | {'Prom. Disco':<12} | {'MB/s RAM':<12} | {'MB/s Disco'}")
    print("-" * 75)

    for mb in tamanos_mb:
        tiempos_ram = []
        tiempos_disco = []
        n_elementos = (mb * 1024 * 1024) // 8

        for i in range(n_repeticiones):
            # Medición RAM
            start = time.perf_counter()
            data = np.random.rand(n_elementos)
            tiempos_ram.append(max(time.perf_counter() - start, 1e-9))

            # Medición Disco
            file_path = f"test_{mb}mb_{i}.bin"
            start = time.perf_counter()
            data.tofile(file_path)
            tiempos_disco.append(max(time.perf_counter() - start, 1e-9))
            
            if os.path.exists(file_path): os.remove(file_path)

        # Promedios de tiempo
        avg_ram = sum(tiempos_ram) / n_repeticiones
        avg_disco = sum(tiempos_disco) / n_repeticiones
        
        # MB/s basados en el promedio: $$Throughput = \frac{Size}{Time}$$
        mbs_ram = mb / avg_ram
        mbs_disco = mb / avg_disco

        resultados_finales.append({
            "Tamaño_MB": mb,
            "Tiempo RAM (s)": avg_ram,
            "Tiempo Disco (s)": avg_disco,
            "MB/s RAM": mbs_ram,
            "MB/s Disco": mbs_disco
        })

        # Ahora la terminal te muestra TODO
        print(f"{mb:<8}MB | {avg_ram:<12.4f} | {avg_disco:<12.4f} | {mbs_ram:<12.2f} | {mbs_disco:.2f}")

    # Guardado final para Excel
    df = pd.DataFrame(resultados_finales).round(4)
    df.to_csv("../datos/resultados_experimento_a.csv", sep=';', decimal=',', index=False, encoding='utf-8-sig')
    print("\n[OK] Experimento completado y promediado.")

if __name__ == "__main__":
    benchmark_utem_final()
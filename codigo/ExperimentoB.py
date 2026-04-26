import pandas as pd
import numpy as np
import time
import os

def experimento_formatos_data():
    # Tamaños de prueba (filas) para notar la diferencia
    # 100k, 500k, 1M, 2M de filas
    filas_prueba = [100000, 500000, 1000000, 2000000]
    n_repeticiones = 5
    resultados = []

    print(f"{'Filas':<10} | {'Formato':<8} | {'Escritura(s)':<12} | {'Lectura(s)':<12} | {'Tamaño MB'}")
    print("-" * 75)

    for n in filas_prueba:
        # Generar un DataFrame con datos mixtos (Num, String, Float)
        df = pd.DataFrame({
            'id': np.arange(n),
            'valor': np.random.randn(n),
            'categoria': np.random.choice(['A', 'B', 'C', 'D'], n),
            'flag': np.random.choice([True, False], n)
        })

        for formato in ['csv', 'parquet']:
            tiempos_escritura = []
            tiempos_lectura = []
            file_path = f"test_data.{formato}"

            for _ in range(n_repeticiones):
                # --- Medir Escritura ---
                start_w = time.perf_counter()
                if formato == 'csv':
                    df.to_csv(file_path, index=False)
                else:
                    df.to_parquet(file_path, engine='pyarrow')
                tiempos_escritura.append(time.perf_counter() - start_w)

                # --- Medir Lectura ---
                start_r = time.perf_counter()
                if formato == 'csv':
                    _ = pd.read_csv(file_path)
                else:
                    _ = pd.read_parquet(file_path, engine='pyarrow')
                tiempos_lectura.append(time.perf_counter() - start_r)

            # Obtener tamaño del archivo en MB
            size_mb = os.path.getsize(file_path) / (1024 * 1024)
            
            # Promedios
            avg_w = sum(tiempos_escritura) / n_repeticiones
            avg_r = sum(tiempos_lectura) / n_repeticiones

            resultados.append({
                "Filas": n,
                "Formato": formato,
                "Escritura_s": avg_w,
                "Lectura_s": avg_r,
                "Tamano_MB": size_mb
            })

            print(f"{n:<10} | {formato:<8} | {avg_w:<12.4f} | {avg_r:<12.4f} | {size_mb:.2f} MB")
            
            if os.path.exists(file_path): os.remove(file_path)

    # Guardar resultados para el informe
    res_df = pd.DataFrame(resultados).round(4)
    res_df.to_csv("../datos/resultados_experimento_b.csv", sep=';', decimal=',', index=False, encoding='utf-8-sig')
    print("\n[OK] Experimento B finalizado.")

if __name__ == "__main__":
    experimento_formatos_data()
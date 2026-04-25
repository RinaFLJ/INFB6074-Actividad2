import numpy as np
import time
import os
import pandas as pd

def benchmark_memoria_vs_disco():
    # Tamaños de prueba en MB (Requisito: al menos 5 tamaños) [cite: 49]
    tamanos_mb = [1, 10, 100, 500, 1000]
    resultados = []

    print(f"{'Tamaño (MB)':<15} | {'RAM (s)':<10} | {'Disco (s)':<10} | {'Throughput RAM'}")
    print("-" * 65)

    for mb in tamanos_mb:
        # float64 ocupa 8 bytes por elemento
        n_elementos = (mb * 1024 * 1024) // 8
        
        # --- MEDICIÓN RAM (Alta precisión) ---
        start_ram = time.perf_counter()
        data = np.random.rand(n_elementos)
        end_ram = time.perf_counter()
        
        tiempo_ram = end_ram - start_ram
        if tiempo_ram == 0: tiempo_ram = 1e-9 

        # --- MEDICIÓN DISCO (SSD Kingston) [cite: 44] ---
        file_path = f"test_{mb}mb.bin"
        start_disco = time.perf_counter()
        data.tofile(file_path)
        end_disco = time.perf_counter()
        
        tiempo_disco = end_disco - start_disco
        if tiempo_disco == 0: tiempo_disco = 1e-9

        # --- CÁLCULOS ---
        # Throughput = Tamaño / Tiempo [cite: 90]
        # $$Throughput = \frac{MB}{s}$$
        tp_ram = mb / tiempo_ram
        tp_disco = mb / tiempo_disco

        resultados.append({
            "Tamaño_MB": mb,
            "Tiempo_RAM_s": tiempo_ram,
            "Tiempo_Disco_s": tiempo_disco,
            "Throughput_RAM_MBs": tp_ram,
            "Throughput_Disco_MBs": tp_disco
        })

        print(f"{mb:<15} | {tiempo_ram:<10.6f} | {tiempo_disco:<10.6f} | {tp_ram:>10.2f} MB/s")

        # Limpieza de archivos temporales
        if os.path.exists(file_path):
            os.remove(file_path)

    # --- GUARDAR RESULTADOS (Corrección para Excel) ---
    df = pd.DataFrame(resultados)
    
    # Usamos ';' como separador para Excel en español y 'utf-8-sig' para la 'ñ' [cite: 59, 86]
    output_path = "../datos/resultados_experimento_a.csv"
    df.to_csv(output_path, sep=';', index=False, encoding='utf-8-sig')
    
    print(f"\n[OK] Experimento A finalizado. Archivo corregido en: {output_path}")

if __name__ == "__main__":
    benchmark_memoria_vs_disco()
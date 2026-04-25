import numpy as np
import time
import os
import pandas as pd

def benchmark_memoria_vs_disco():
    """
    Experimento A: Comparativa de rendimiento entre jerarquía de memoria (RAM) 
    y almacenamiento secundario (SSD).
    """
    # Tamaños de prueba en MB (Requisito: al menos 5 tamaños) 
    tamanos_mb = [1, 10, 100, 500, 1000]
    resultados = []

    print(f"{'Tamaño (MB)':<12} | {'RAM (s)':<12} | {'Disco (s)':<12} | {'Throughput RAM'}")
    print("-" * 70)

    for mb in tamanos_mb:
        # Cada elemento float64 ocupa 8 bytes en memoria
        n_elementos = (mb * 1024 * 1024) // 8
        
        # --- MEDICIÓN RAM (Uso de perf_counter para alta resolución) ---
        start_ram = time.perf_counter()
        data = np.random.rand(n_elementos)
        end_ram = time.perf_counter()
        
        tiempo_ram = end_ram - start_ram
        # Evitar división por cero si el hardware es extremadamente rápido
        if tiempo_ram == 0: tiempo_ram = 1e-9 

        # --- MEDICIÓN DISCO (Escritura en SSD Kingston) ---
        file_path = f"test_{mb}mb.bin"
        start_disco = time.perf_counter()
        data.tofile(file_path)
        end_disco = time.perf_counter()
        
        tiempo_disco = end_disco - start_disco
        if tiempo_disco == 0: tiempo_disco = 1e-9

        # --- CÁLCULOS DE RENDIMIENTO ---
        # Throughput = Tamaño / Tiempo (MB/s)
        tp_ram = mb / tiempo_ram
        tp_disco = mb / tiempo_disco

        resultados.append({
            "Tamaño_MB": mb,
            "Tiempo_RAM_s": tiempo_ram,
            "Tiempo_Disco_s": tiempo_disco,
            "Throughput_RAM_MBs": tp_ram,
            "Throughput_Disco_MBs": tp_disco
        })

        print(f"{mb:<12} | {tiempo_ram:<12.6f} | {tiempo_disco:<12.6f} | {tp_ram:>12.2f} MB/s")

        # Limpieza de archivos temporales para cumplir con el orden del entorno [cite: 29]
        if os.path.exists(file_path):
            os.remove(file_path)

    # --- PROCESAMIENTO Y GUARDADO DE DATOS [cite: 59] ---
    df = pd.DataFrame(resultados)
    
    # Redondeo para evitar problemas de visualización en Excel
    df = df.round(4)
    
    # Configuración de exportación para Excel (Chile):
    # - sep=';': Punto y coma para separar columnas.
    # - decimal=',': Coma para decimales según configuración regional.
    # - encoding='utf-8-sig': Para que Excel lea correctamente la 'ñ' y acentos.
    output_path = "../datos/resultados_experimento_a.csv"
    
    # Asegurar que la carpeta datos existe
    os.makedirs("../datos", exist_ok=True)
    
    df.to_csv(output_path, sep=';', decimal=',', index=False, encoding='utf-8-sig')
    
    print(f"\n[OK] Experimento A finalizado.")
    print(f"Archivo tabular generado en: {output_path}")

if __name__ == "__main__":
    benchmark_memoria_vs_disco()
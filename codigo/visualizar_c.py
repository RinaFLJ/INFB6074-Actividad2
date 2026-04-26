import pandas as pd
import matplotlib.pyplot as plt
import os

def generar_grafico_c():
    archivo_datos = "../datos/resultados_experimento_c.csv"
    
    try:
        # Cargamos los datos con los ajustes de Excel Chile
        df = pd.read_csv(archivo_datos, sep=';', decimal=',')
    except FileNotFoundError:
        print("Error: No se encontró el archivo de resultados del Experimento C.")
        return

    # Creamos la figura con dos sub-gráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # --- GRÁFICO 1: Comparativa de Tiempos ---
    ax1.plot(df['Elementos'], df['Tiempo_Secuencial_s'], marker='o', label='Secuencial (1 núcleo)', linewidth=2)
    ax1.plot(df['Elementos'], df['Tiempo_Paralelo_s'], marker='s', label='Paralelo (8 hilos)', linewidth=2)
    ax1.set_title('Tiempos de Cómputo: Secuencial vs Paralelo', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Número de Elementos')
    ax1.set_ylabel('Tiempo (Segundos)')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)

    # --- GRÁFICO 2: Análisis del Speedup ---
    # El Speedup ideal sería una línea recta subiendo, pero aquí veremos el impacto del overhead
    ax2.bar(df['Elementos'].astype(str), df['Speedup'], color='salmon', alpha=0.7)
    ax2.axhline(y=1, color='black', linestyle='--', label='Límite de eficiencia (S=1)')
    ax2.set_title('Métrica de Speedup (S)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Número de Elementos')
    ax2.set_ylabel('Speedup (Veces más rápido)')
    ax2.legend()
    ax2.grid(True, axis='y', linestyle='--', alpha=0.6)

    plt.suptitle('Experimento C: Impacto del Overhead en Computación Paralela (Ryzen 5)', fontsize=14)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Guardar en la carpeta de visualizaciones
    os.makedirs("../visualizaciones", exist_ok=True)
    output_path = "../visualizaciones/grafico_experimento_c.png"
    plt.savefig(output_path, dpi=300)
    print(f"[OK] Visualización C generada en: {output_path}")
    plt.show()

if __name__ == "__main__":
    generar_grafico_c()
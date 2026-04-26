import pandas as pd
import matplotlib.pyplot as plt
import os

def generar_grafico_b():
    archivo_datos = "../datos/resultados_experimento_b.csv"
    
    try:
        # Cargamos los datos con los ajustes regionales de Chile
        df = pd.read_csv(archivo_datos, sep=';', decimal=',')
    except FileNotFoundError:
        print("Error: No se encontró el archivo de resultados del Experimento B.")
        return

    # Separamos los datos por formato para graficar
    df_csv = df[df['Formato'] == 'csv']
    df_pq = df[df['Formato'] == 'parquet']

    # Creamos una figura con dos sub-gráficos (1 fila, 2 columnas)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # --- GRÁFICO 1: TIEMPOS DE LECTURA (Rendimiento) ---
    ax1.plot(df_csv['Filas'], df_csv['Lectura_s'], marker='o', label='CSV', linewidth=2)
    ax1.plot(df_pq['Filas'], df_pq['Lectura_s'], marker='s', label='Parquet', linewidth=2)
    ax1.set_title('Tiempo de Lectura (Menos es mejor)', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Número de Filas')
    ax1.set_ylabel('Segundos')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)

    # --- GRÁFICO 2: TAMAÑO EN DISCO (Eficiencia) ---
    width = 0.35
    x = range(len(df_csv['Filas']))
    ax2.bar([p - width/2 for p in x], df_csv['Tamano_MB'], width, label='CSV', color='#1f77b4')
    ax2.bar([p + width/2 for p in x], df_pq['Tamano_MB'], width, label='Parquet', color='#ff7f0e')
    ax2.set_title('Tamaño del Archivo (Menos es mejor)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Millones de Filas')
    ax2.set_ylabel('Megabytes (MB)')
    ax2.set_xticks(x)
    ax2.set_xticklabels([f"{int(n/1000000)}M" for n in df_csv['Filas']])
    ax2.legend()
    ax2.grid(True, axis='y', linestyle='--', alpha=0.6)

    plt.suptitle('Experimento B: Eficiencia de Formatos (CSV vs Parquet)', fontsize=14)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])

    # Guardar visualización
    os.makedirs("../visualizaciones", exist_ok=True)
    output_path = "../visualizaciones/grafico_experimento_b.png"
    plt.savefig(output_path, dpi=300)
    print(f"[OK] Visualización B generada en: {output_path}")
    plt.show()

if __name__ == "__main__":
    generar_grafico_b()
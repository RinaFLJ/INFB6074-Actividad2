import pandas as pd
import matplotlib.pyplot as plt
import os

def generar_grafico_a():
    print("1. Iniciando script de visualización...")
    
    archivo_datos = "../datos/resultados_experimento_a.csv"
    carpeta_visual = "../visualizaciones"
    
    # Crear carpeta si no existe (importante para evitar errores)
    os.makedirs(carpeta_visual, exist_ok=True)

    try:
        print(f"2. Intentando leer: {archivo_datos}")
        # Leemos con la configuración de Excel Chile que usamos en el Experimento A
        df = pd.read_csv(archivo_datos, sep=';', decimal=',')
        print("3. Datos cargados correctamente.")
    except Exception as e:
        print(f"ERROR: No se pudo leer el archivo. Detalle: {e}")
        return

    # Crear el gráfico
    plt.figure(figsize=(12, 7))
    
    print("4. Generando curvas de rendimiento...")
    plt.plot(df['Tamaño_MB'], df['MB/s RAM'], marker='o', label='Memoria RAM', linewidth=2.5)
    plt.plot(df['Tamaño_MB'], df['MB/s Disco'], marker='s', label='SSD Kingston', linewidth=2.5)

    # Configuración estética
    plt.title('Experimento A: Jerarquía de Memoria (RAM vs SSD)', fontsize=14, fontweight='bold')
    plt.xlabel('Tamaño de Carga (MB)', fontsize=12)
    plt.ylabel('Velocidad de Transferencia (MB/s)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Usamos escala logarítmica para ver bien la diferencia abismal
    plt.yscale('log')

    # Guardar el archivo PNG (Requisito de la actividad)
    output_png = f"{carpeta_visual}/grafico_experimento_a.png"
    plt.savefig(output_png, dpi=300, bbox_inches='tight')
    print(f"5. [OK] Imagen guardada en: {output_png}")
    
    print("6. Abriendo ventana del gráfico...")
    plt.show()

# --- ESTO ES LO QUE HACE QUE EL SCRIPT FUNCIONE ---
if __name__ == "__main__":
    generar_grafico_a()
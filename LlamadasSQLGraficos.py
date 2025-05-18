import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

def obtener_tendencia_reciclaje_por_anio(conn, anio):
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                m.nombre_material,
                EXTRACT(MONTH FROM r.fecha) AS mes,
                SUM(r.peso_kg) AS total_kg
            FROM recolecciones r
            JOIN materiales m ON r.id_material = m.id_material
            WHERE EXTRACT(YEAR FROM r.fecha) = %s
            GROUP BY m.nombre_material, mes
            ORDER BY m.nombre_material, mes;
        """, (anio,))

        resultados = cur.fetchall()

        if resultados:
            df = pd.DataFrame(resultados, columns=["material", "mes", "total_kg"])
            plt.figure(figsize=(12, 6))
            for material, data in df.groupby("material"):
                plt.plot(data["mes"], data["total_kg"], marker='o', label=material)

            plt.xlabel("Mes")
            plt.ylabel("Total reciclado (kg)")
            plt.title(f"Tendencia mensual de reciclaje por material en {anio}")
            plt.legend()
            plt.grid(True)
            plt.xticks(range(1, 13))
            plt.tight_layout()
            plt.show()

        cur.close()

    except Exception as e:
        print("Error al obtener datos:", e)

def obtener_tendencia_reciclaje_por_zona(conn, anio):
    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                p.zona,
                EXTRACT(MONTH FROM r.fecha) AS mes,
                SUM(r.peso_kg) AS total_kg
            FROM recolecciones r
            JOIN puntos_recoleccion p ON r.id_punto_recoleccion = p.id_punto_recoleccion
            WHERE EXTRACT(YEAR FROM r.fecha) = %s
            GROUP BY p.zona, mes
            ORDER BY p.zona, mes;
        """, (anio,))

        resultados = cur.fetchall()

        if resultados:
            df = pd.DataFrame(resultados, columns=["zona", "mes", "total_kg"])
            plt.figure(figsize=(12, 6))
            for zona, data in df.groupby("zona"):
                plt.plot(data["mes"], data["total_kg"], marker='o', label=zona)

            plt.xlabel("Mes")
            plt.ylabel("Total reciclado (kg)")
            plt.title(f"Tendencia mensual de reciclaje por zona en {anio}")
            plt.legend()
            plt.grid(True)
            plt.xticks(range(1, 13))
            plt.tight_layout()
            plt.show()

        cur.close()

    except Exception as e:
        print("Error al obtener datos:", e)

def graficar_frecuencia_recoleccion(conn,anio):
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.zona,
            EXTRACT(MONTH FROM r.fecha) AS mes,
            COUNT(*) AS cantidad_recolecciones
        FROM recolecciones r
        JOIN puntos_recoleccion p ON r.id_punto_recoleccion = p.id_punto_recoleccion
        WHERE EXTRACT(YEAR FROM r.fecha) = %s
        GROUP BY p.zona, mes
        ORDER BY p.zona, mes;
    """, (anio,))
    
    resultados = cur.fetchall()
    cur.close()

    # Organizar los datos para graficar por zona
    zonas = set()
    datos = defaultdict(lambda: [0]*12)  # 12 meses

    for zona, mes, cantidad in resultados:
        zonas.add(zona)
        datos[zona][int(mes)-1] = cantidad

    # Graficar
    plt.figure(figsize=(10, 6))
    for zona in sorted(zonas):
        plt.plot(range(1, 13), datos[zona], label=zona, marker='o')

    plt.title(f'Frecuencia mensual de recolección por zona - {anio}')
    plt.xlabel('Mes')
    plt.ylabel('Cantidad de recolecciones')
    plt.xticks(range(1, 13))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(title='Zona')
    plt.tight_layout()
    plt.show()

def graficar_materiales_reciclados(conn,anio):
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            m.nombre_material,
            SUM(r.peso_kg) AS total_kg
        FROM recolecciones r
        JOIN materiales m ON r.id_material = m.id_material
        WHERE EXTRACT(YEAR FROM r.fecha) = %s
        GROUP BY m.nombre_material
        ORDER BY total_kg DESC;
    """, (anio,))

    resultados = cur.fetchall()
    cur.close()

    materiales = [fila[0] for fila in resultados]
    cantidades = [fila[1] for fila in resultados]

    plt.figure(figsize=(12, 7)) 
    bars = plt.bar(materiales, cantidades, color='mediumseagreen')

    plt.title(f'Comparación de materiales reciclados - Año {anio}', fontsize=14)
    plt.xlabel('Material', fontsize=12)
    plt.ylabel('Kg reciclados', fontsize=12)
    
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.tight_layout()

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 10, f'{yval:.0f}', 
                 ha='center', va='bottom', fontsize=9)

    plt.grid(axis='y', linestyle='--', alpha=0.4)
    plt.show()

def graficar_recoleccion_por_punto(conn, anio):
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            p.direccion,
            SUM(r.peso_kg) AS total_kg
        FROM recolecciones r
        JOIN puntos_recoleccion p ON r.id_punto_recoleccion = p.id_punto_recoleccion
        WHERE EXTRACT(YEAR FROM r.fecha) = %s
        GROUP BY p.direccion
        ORDER BY total_kg DESC;
    """, (anio,))

    resultados = cur.fetchall()
    cur.close()

    direcciones = [fila[0] for fila in resultados]
    cantidades = [fila[1] for fila in resultados]

    plt.figure(figsize=(14, 7))
    bars = plt.bar(direcciones, cantidades, color='steelblue')

    plt.title(f'Recolección por punto - Año {anio}', fontsize=14)
    plt.xlabel('Punto de recolección (dirección)', fontsize=12)
    plt.ylabel('Kg reciclados', fontsize=12)
    
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.tight_layout()

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 10, f'{yval:.0f}', 
                 ha='center', va='bottom', fontsize=8)

    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.show()

def graficar_costos_por_material(conn, anio):
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            m.nombre_material,
            SUM(r.peso_kg * m.costo_kg) AS costo_total
        FROM recolecciones r
        JOIN materiales m ON r.id_material = m.id_material
        WHERE EXTRACT(YEAR FROM r.fecha) = %s
        GROUP BY m.nombre_material
        ORDER BY costo_total DESC;
    """, (anio,))

    resultados = cur.fetchall()
    cur.close()

    materiales = [fila[0] for fila in resultados]
    costos = [float(fila[1]) for fila in resultados]

    costos_miles = [c / 1000 for c in costos]

    plt.figure(figsize=(12,7))
    bars = plt.bar(materiales, costos_miles, color='coral')

    plt.title(f'Costos por kg reciclado por material - Año {anio}', fontsize=14)
    plt.xlabel('Material', fontsize=12)
    plt.ylabel('Costo total (miles de pesos Chilenos)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    for bar, c in zip(bars, costos_miles):
        yval = bar.get_height()
        texto = f'{yval:.2f}k'
        plt.text(bar.get_x() + bar.get_width()/2, yval + max(costos_miles)*0.01, texto,
                 ha='center', va='bottom', fontsize=9)

    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.show()

if __name__ == "__main__":
    anio = input("Ingrese el año:\t")
    conexion = psycopg2.connect(
        host="localhost",
        database="reciclaje",
        user="python_user",
        password="1234"
    )
    obtener_tendencia_reciclaje_por_anio(conexion, anio)
    obtener_tendencia_reciclaje_por_zona(conexion, anio)
    graficar_frecuencia_recoleccion(conexion, anio)
    graficar_materiales_reciclados(conexion,anio)
    graficar_recoleccion_por_punto(conexion, anio)
    graficar_costos_por_material(conexion, anio)
    conexion.close()
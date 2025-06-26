import psycopg2
import pandas as pd

# 1. Extract: Conexión y consulta
conn = psycopg2.connect(
    host="localhost",
    database="dbreciclaje",
    user="python_user",
    password="1234"
)
query = """
SELECT 
    r.id, r.fecha, 
    p.direccion AS punto, 
    m.nombre AS material, 
    o.nombre AS operario, 
    v.patente AS vehiculo, 
    r.peso, 
    r.costo_total,
    rg.nombre AS region
FROM recolecciones r
JOIN puntos_recoleccion p ON r.punto_id = p.id
JOIN materiales m ON r.material_id = m.id
JOIN operarios o ON r.operario_id = o.id
JOIN vehiculos v ON r.vehiculo_id = v.id
JOIN comuna c ON p.comuna_id = c.id
JOIN region rg ON c.region_id = rg.id
ORDER BY r.id ASC, r.fecha DESC
"""

df = pd.read_sql(query, conn)

df.to_csv("detalle_recolecciones.csv", index=False)

gastos_region = df.groupby('region')['costo_total'].sum().reset_index()
gastos_region.to_csv("gastos_reciclaje_por_region.csv", index=False)

kilos_region = df.groupby('region')['peso'].sum().reset_index()
kilos_region.to_csv("kilos_reciclados_por_region.csv", index=False)

gastos_operario = df.groupby('operario')['costo_total'].sum().reset_index()
gastos_operario.to_csv("gastos_por_operario.csv", index=False)

kilos_operario = df.groupby('operario')['peso'].sum().reset_index()
kilos_operario.to_csv("kilos_por_operario.csv", index=False)

ranking_puntos = df.groupby('punto')['peso'].sum().reset_index().sort_values('peso', ascending=False)
ranking_puntos.to_csv("ranking_puntos_kilos.csv", index=False)

conn.close()
import psycopg2
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

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


conn2 = psycopg2.connect(
    host="localhost",
    database="reciclaje",
    user="python_user",
    password="1234"
)
cur2 = conn2.cursor()

cur2.execute("DROP TABLE IF EXISTS recolecciones CASCADE;")
cur2.execute("DROP TABLE IF EXISTS vehiculos CASCADE;")
cur2.execute("DROP TABLE IF EXISTS operarios CASCADE;")
cur2.execute("DROP TABLE IF EXISTS puntos_recoleccion CASCADE;")
cur2.execute("DROP TABLE IF EXISTS materiales CASCADE;")
conn2.commit()

cur2.execute("""
CREATE TABLE materiales (
    id_material SERIAL PRIMARY KEY,
    nombre_material VARCHAR(50) NOT NULL UNIQUE,
    costo_kg DECIMAL(10,2) NOT NULL
);
""")
cur2.execute("""
CREATE TABLE puntos_recoleccion (
    id_punto_recoleccion SERIAL PRIMARY KEY,
    direccion VARCHAR(100) UNIQUE,
    zona VARCHAR(50),
    tipo_punto VARCHAR(50)
);
""")
cur2.execute("""
CREATE TABLE operarios (
    id_operario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE,
    turno VARCHAR(20),
    zona_asignada VARCHAR(50)
);
""")
cur2.execute("""
CREATE TABLE vehiculos (
    id_vehiculo SERIAL PRIMARY KEY,
    patente VARCHAR(20) NOT NULL UNIQUE,
    tipo_vehiculo VARCHAR(50),
    capacidad_kg INT,
    estado VARCHAR(30)
);
""")
cur2.execute("""
CREATE TABLE recolecciones (
    id_recoleccion SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    id_punto_recoleccion INT,
    id_material INT,
    id_operario INT,
    id_vehiculo INT,
    peso_kg DECIMAL(10,2),
    costo_total DECIMAL(10,2),
    FOREIGN KEY (id_punto_recoleccion) REFERENCES puntos_recoleccion(id_punto_recoleccion),
    FOREIGN KEY (id_material) REFERENCES materiales(id_material),
    FOREIGN KEY (id_operario) REFERENCES operarios(id_operario),
    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo)
);
""")
conn2.commit()

materiales = df[['material']].drop_duplicates().reset_index(drop=True)
for _, row in materiales.iterrows():
    cur2.execute(
        "INSERT INTO materiales (nombre_material, costo_kg) VALUES (%s, %s) ON CONFLICT (nombre_material) DO NOTHING;",
        (row['material'], 0)
    )

puntos = df[['punto']].drop_duplicates().reset_index(drop=True)
for _, row in puntos.iterrows():
    cur2.execute(
        "INSERT INTO puntos_recoleccion (direccion, zona, tipo_punto) VALUES (%s, %s, %s) ON CONFLICT (direccion) DO NOTHING;",
        (row['punto'], '', '')
    )

operarios = df[['operario']].drop_duplicates().reset_index(drop=True)
for _, row in operarios.iterrows():
    cur2.execute(
        "INSERT INTO operarios (nombre, turno, zona_asignada) VALUES (%s, %s, %s) ON CONFLICT (nombre) DO NOTHING;",
        (row['operario'], '', '')
    )

vehiculos = df[['vehiculo']].drop_duplicates().reset_index(drop=True)
for _, row in vehiculos.iterrows():
    cur2.execute(
        "INSERT INTO vehiculos (patente, tipo_vehiculo, capacidad_kg, estado) VALUES (%s, %s, %s, %s) ON CONFLICT (patente) DO NOTHING;",
        (row['vehiculo'], '', 0, '')
    )

conn2.commit()

for _, row in df.iterrows():
    cur2.execute("SELECT id_material FROM materiales WHERE nombre_material=%s", (row['material'],))
    id_material = cur2.fetchone()[0]
    cur2.execute("SELECT id_punto_recoleccion FROM puntos_recoleccion WHERE direccion=%s", (row['punto'],))
    id_punto = cur2.fetchone()[0]
    cur2.execute("SELECT id_operario FROM operarios WHERE nombre=%s", (row['operario'],))
    id_operario = cur2.fetchone()[0]
    cur2.execute("SELECT id_vehiculo FROM vehiculos WHERE patente=%s", (row['vehiculo'],))
    id_vehiculo = cur2.fetchone()[0]

    cur2.execute("""
        INSERT INTO recolecciones (
            fecha, id_punto_recoleccion, id_material, id_operario, id_vehiculo, peso_kg, costo_total
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        row['fecha'], id_punto, id_material, id_operario, id_vehiculo, row['peso'], row['costo_total']
    ))
conn2.commit()

cur2.close()
conn2.close()
print("Migración completada.")
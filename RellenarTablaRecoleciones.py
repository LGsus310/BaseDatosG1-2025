import psycopg2
import random
from datetime import datetime, timedelta

# Conectar a la base de datos
conn = psycopg2.connect(
    host="localhost",
    database="reciclaje",
    user="python_user",
    password="1234"
)
cur = conn.cursor()

# Obtener IDs disponibles de las otras tablas
def get_ids(table, column):
    cur.execute(f"SELECT {column} FROM {table}")
    return [row[0] for row in cur.fetchall()]

material_ids = get_ids('materiales', 'id_material')
punto_ids = get_ids('puntos_recoleccion', 'id_punto_recoleccion')
operario_ids = get_ids('operarios', 'id_operario')
vehiculo_ids = get_ids('vehiculos', 'id_vehiculo')

# Obtener costos por tonelada de materiales
cur.execute("SELECT id_material, costo_kg FROM materiales")
material_costos = dict(cur.fetchall())

# Generar 100 registros aleatorios
recolecciones = []
for _ in range(100):
    fecha = datetime.today() - timedelta(days=random.randint(0, 365))
    id_punto = random.choice(punto_ids)
    id_material = random.choice(material_ids)
    id_operario = random.choice(operario_ids)
    id_vehiculo = random.choice(vehiculo_ids)
    peso_kg = round(random.uniform(100, 2000), 2)
    
    # Calcular el costo total
    costo_kg = material_costos[id_material]
    costo_total = round((peso_kg) * float(costo_kg), 2)

    recolecciones.append((
        fecha.date(),
        id_punto,
        id_material,
        id_operario,
        id_vehiculo,
        peso_kg,
        costo_total
    ))

# Insertar en la base de datos
cur.executemany("""
    INSERT INTO recolecciones (
        fecha, id_punto_recoleccion, id_material, id_operario, id_vehiculo, peso_kg, costo_total
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
""", recolecciones)

conn.commit()
print("¡100 recolecciones insertadas exitosamente!")
cur.close()
conn.close()

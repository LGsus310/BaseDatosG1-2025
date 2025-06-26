import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="dbreciclaje",
    user="python_user",
    password="1234"
)
cur = conn.cursor()

# Insertar materiales
materiales = [
    ('Papel', 120.00),
    ('Cartón', 100.00),
    ('Botellas PET (plástico)', 250.00),
    ('Plásticos HDPE (envases de detergente, etc.)', 400.00),
    ('Vidrio', 80.00),
    ('Latas de aluminio', 500.00),
    ('Latas de acero', 150.00),
    ('Cobre (cables eléctricos, tuberías)', 6000.00),
    ('Chatarra de hierro', 150.00),
    ('Textiles (ropa en buen estado o fibras)', 90.00),
    ('Tetra Pak', 300.00),
    ('Neumáticos fuera de uso (NFU)', 50.00),
    ('Residuos orgánicos (para compostaje)', 30.00),
    ('Aceite vegetal usado (para biodiésel)', 700.00),
    ('Electrónicos (componentes reciclables)', 200.00)
]

cur.executemany("""
    INSERT INTO materiales (nombre, costo_kg)
    VALUES (%s, %s);
""", materiales)

# Insertar operarios
operarios = [
    ('Juan Pérez', 'Mañana', 'Norte'),
    ('Ana Gómez', 'Tarde', 'Centro'),
    ('Carlos Ruiz', 'Noche', 'Sur'),
    ('María Torres', 'Mañana', 'Este'),
    ('Luis Ramírez', 'Tarde', 'Oeste'),
    ('Carmen Salas', 'Noche', 'Norte'),
    ('José Martínez', 'Mañana', 'Centro'),
    ('Laura Díaz', 'Tarde', 'Sur'),
    ('Miguel Herrera', 'Noche', 'Este'),
    ('Paola Castillo', 'Mañana', 'Oeste'),
    ('Andrés Vega', 'Tarde', 'Norte'),
    ('Lucía Fernández', 'Noche', 'Centro'),
    ('Ricardo Morales', 'Mañana', 'Sur'),
    ('Verónica Mendoza', 'Tarde', 'Este'),
    ('Fernando Soto', 'Noche', 'Oeste')
]

cur.executemany("""
    INSERT INTO operarios (nombre, turno, zona)
    VALUES (%s, %s, %s);
""", operarios)

conn.commit()
print("Materiales y operarios insertados correctamente.")

cur.close()
conn.close()
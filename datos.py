import psycopg2

# Conexión a PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="reciclaje",
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
    INSERT INTO materiales (nombre_material, costo_tonelada)
    VALUES (%s, %s)
""", materiales)

# Insertar puntos de recolección
puntos = [
    ('Av. Los Pinos 123', 'Norte', 'Cliente Residencial'),
    ('Calle 45 #210', 'Centro', 'Cliente Empresa'),
    ('Plaza Central s/n', 'Sur', 'Punto Verde Propio'),
    ('Escuela San Martín', 'Este', 'Centro Educativo'),
    ('Mercado Municipal', 'Oeste', 'Centro Comercial'),
    ('Calle 12 #432', 'Norte', 'Cliente Residencial'),
    ('Universidad del Este', 'Este', 'Centro Educativo'),
    ('Parque Industrial', 'Sur', 'Cliente Empresa'),
    ('Centro de Reciclaje Verde', 'Centro', 'Punto Verde Propio'),
    ('Colegio Nacional', 'Oeste', 'Centro Educativo'),
    ('Hospital Central', 'Centro', 'Entidad Gubernamental'),
    ('Avenida Libertad 456', 'Norte', 'Cliente Empresa'),
    ('Comisaría 4ta', 'Sur', 'Entidad Gubernamental'),
    ('Estación de tren', 'Este', 'Entidad Gubernamental'),
    ('Junta Vecinal Barrio Nuevo', 'Oeste', 'Cliente Residencial'),
    ('Torre EcoHabitat', 'Norte', 'Cliente Residencial'),
    ('Fábrica AceroPlus', 'Sur', 'Cliente Empresa'),
    ('Centro Comercial El Molino', 'Centro', 'Centro Comercial'),
    ('Escuela Técnica 8', 'Este', 'Centro Educativo'),
    ('Municipalidad de Zona Oeste', 'Oeste', 'Entidad Gubernamental'),
    ('Barrio Alto Verde', 'Norte', 'Cliente Residencial'),
    ('Planta Industrial LIMSA', 'Sur', 'Cliente Empresa'),
    ('Condominio Los Álamos', 'Centro', 'Cliente Residencial'),
    ('Centro de Reciclaje EcoPlan', 'Este', 'Punto Verde Propio'),
    ('Oficinas Delta S.A.', 'Oeste', 'Cliente Empresa'),
    ('Hospital de Niños', 'Centro', 'Entidad Gubernamental'),
    ('Complejo Educativo Siglo XXI', 'Este', 'Centro Educativo'),
    ('Centro Comercial La Estación', 'Sur', 'Centro Comercial'),
    ('Punto Verde Av. Mitre', 'Norte', 'Punto Verde Propio'),
    ('Residencial Las Rosas', 'Oeste', 'Cliente Residencial')
]


cur.executemany("""
    INSERT INTO puntos_recoleccion (direccion, zona, tipo_punto)
    VALUES (%s, %s, %s)
""", puntos)

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
    INSERT INTO operarios (nombre, turno, zona_asignada)
    VALUES (%s, %s, %s)
""", operarios)

# Insertar vehículos
vehiculos = [
    ('ABC123', 'Camión', 3000, 'Activo'),
    ('XYZ789', 'Furgoneta', 1500, 'Activo'),
    ('DEF456', 'Camión', 2500, 'En mantenimiento'),
    ('GHI321', 'Camión', 3200, 'Activo'),
    ('JKL654', 'Furgoneta', 1400, 'Activo'),
    ('MNO987', 'Camión', 2800, 'En mantenimiento'),
    ('PQR741', 'Furgoneta', 1600, 'Activo'),
    ('STU852', 'Camión', 3500, 'Activo'),
    ('VWX963', 'Furgoneta', 1300, 'Inactivo'),
    ('YZA159', 'Camión', 3100, 'Activo'),
    ('BCD753', 'Furgoneta', 1450, 'En mantenimiento'),
    ('EFG258', 'Camión', 2700, 'Activo'),
    ('HIJ369', 'Camión', 2900, 'Inactivo'),
    ('KLM147', 'Furgoneta', 1550, 'Activo'),
    ('NOP258', 'Camión', 3050, 'Activo')
]

cur.executemany("""
    INSERT INTO vehiculos (patente, tipo_vehiculo, capacidad_kg, estado)
    VALUES (%s, %s, %s, %s)
""", vehiculos)


# Confirmar cambios
conn.commit()
print("Datos insertados correctamente.")

cur.close()
conn.close()
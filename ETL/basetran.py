import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import random
from datetime import datetime, timedelta
from tkinter import StringVar

conn = psycopg2.connect(
    host="localhost",
    database="dbreciclaje",
    user="python_user",
    password="1234"
)
cursor = conn.cursor()

def crear_tablas():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS estado (
            id SERIAL PRIMARY KEY,
            nombre TEXT UNIQUE
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tipo_vehiculo (
            id SERIAL PRIMARY KEY,
            nombre TEXT UNIQUE,
            capacidad_max_kg REAL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materiales (
            id SERIAL PRIMARY KEY,
            nombre TEXT,
            costo_kg REAL
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operarios (
            id SERIAL PRIMARY KEY,
            nombre TEXT,
            turno TEXT,
            zona TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS region (
            id SERIAL PRIMARY KEY,
            nombre TEXT UNIQUE
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comuna (
            id SERIAL PRIMARY KEY,
            nombre TEXT UNIQUE,
            region_id INTEGER REFERENCES region(id)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tipo_residuo (
            id SERIAL PRIMARY KEY,
            nombre TEXT UNIQUE
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehiculos (
            id SERIAL PRIMARY KEY,
            patente TEXT UNIQUE,
            tipo_id INTEGER REFERENCES tipo_vehiculo(id),
            estado_id INTEGER REFERENCES estado(id)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS puntos_recoleccion (
            id SERIAL PRIMARY KEY,
            direccion TEXT,
            comuna_id INTEGER REFERENCES comuna(id),
            tipo_residuo_id INTEGER REFERENCES tipo_residuo(id)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recolecciones (
            id SERIAL PRIMARY KEY,
            fecha DATE,
            punto_id INTEGER REFERENCES puntos_recoleccion(id),
            material_id INTEGER REFERENCES materiales(id),
            operario_id INTEGER REFERENCES operarios(id),
            vehiculo_id INTEGER REFERENCES vehiculos(id),
            peso REAL,
            costo_total REAL
        );
    ''')
    conn.commit()

def eliminar_tablas():
    try:
        cursor.execute("DROP TABLE IF EXISTS recolecciones CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS vehiculos CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS materiales CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS operarios CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS puntos_recoleccion CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS tipo_vehiculo CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS estado CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS comuna CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS region CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS tipo_residuo CASCADE;")
        conn.commit()
        messagebox.showinfo("Éxito", "Tablas eliminadas correctamente.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def inicializar_estados():
    estados = ["Disponible", "En mantenimiento", "Fuera de servicio"]
    for nombre in estados:
        cursor.execute("INSERT INTO estado (nombre) VALUES (%s) ON CONFLICT (nombre) DO NOTHING;", (nombre,))
    conn.commit()
  
crear_tablas()
inicializar_estados()

def agregar_material():
    nombre = entry_nombre.get()
    try:
        costo = float(entry_costo.get())
        cursor.execute("INSERT INTO materiales(nombre, costo_kg) VALUES (%s, %s)", (nombre, costo))
        conn.commit()
        actualizar_lista_materiales()
        messagebox.showinfo("Éxito", "Material agregado.")
    except Exception as e:
        print("Error", str(e))

def seleccionar_material(event):
    selected = lista_materiales.focus()
    if selected:
        values = lista_materiales.item(selected, 'values')
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, values[1])
        entry_costo.delete(0, tk.END)
        entry_costo.insert(0, values[2])

def actualizar_material():
    try:
        selected = lista_materiales.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un material para actualizar.")
            return
        values = lista_materiales.item(selected, 'values')
        id_ = values[0]
        nombre = entry_nombre.get()
        costo = float(entry_costo.get())
        cursor.execute("UPDATE materiales SET nombre=%s, costo_kg=%s WHERE id=%s", (nombre, costo, id_))
        conn.commit()
        actualizar_lista_materiales()
        messagebox.showinfo("Éxito", "Material actualizado.")
    except Exception as e:
        print("Error", str(e))

def eliminar_material():
    try:
        selected = lista_materiales.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un material para eliminar.")
            return
        values = lista_materiales.item(selected, 'values')
        id_ = values[0]
        cursor.execute("DELETE FROM materiales WHERE id=%s", (id_,))
        conn.commit()
        actualizar_lista_materiales()
        messagebox.showinfo("Éxito", "Material eliminado.")
    except Exception as e:
        print("Error", str(e))

def actualizar_lista_materiales():
    lista_materiales.delete(*lista_materiales.get_children())
    cursor.execute("SELECT * FROM materiales")
    for row in cursor.fetchall():
        lista_materiales.insert("", "end", values=row)

def agregar_operario():
    nombre = entry_op_nombre.get()
    turno = entry_op_turno.get()
    zona = entry_op_zona.get()
    try:
        cursor.execute("INSERT INTO operarios(nombre, turno, zona) VALUES (%s, %s, %s)",
                       (nombre, turno, zona))
        conn.commit()
        actualizar_lista_operarios()
        messagebox.showinfo("Éxito", "Operario agregado.")
    except Exception as e:
        print("Error", str(e))

def seleccionar_operario(event):
    selected = lista_operarios.focus()
    if selected:
        values = lista_operarios.item(selected, 'values')
        entry_op_nombre.delete(0, tk.END)
        entry_op_nombre.insert(0, values[1])
        entry_op_turno.delete(0, tk.END)
        entry_op_turno.insert(0, values[2])
        entry_op_zona.delete(0, tk.END)
        entry_op_zona.insert(0, values[3])

def actualizar_operario():
    try:
        selected = lista_operarios.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un operario para actualizar.")
            return
        values = lista_operarios.item(selected, 'values')
        id_ = values[0]
        nombre = entry_op_nombre.get()
        turno = entry_op_turno.get()
        zona = entry_op_zona.get()
        cursor.execute("UPDATE operarios SET nombre=%s, turno=%s, zona=%s WHERE id=%s",
                       (nombre, turno, zona, id_))
        conn.commit()
        actualizar_lista_operarios()
        messagebox.showinfo("Éxito", "Operario actualizado.")
    except Exception as e:
        print("Error", str(e))

def eliminar_operario():
    try:
        selected = lista_operarios.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un operario para eliminar.")
            return
        values = lista_operarios.item(selected, 'values')
        id_ = values[0]
        cursor.execute("DELETE FROM operarios WHERE id=%s", (id_,))
        conn.commit()
        actualizar_lista_operarios()
        messagebox.showinfo("Éxito", "Operario eliminado.")
    except Exception as e:
        print("Error", str(e))

def actualizar_lista_operarios():
    lista_operarios.delete(*lista_operarios.get_children())
    cursor.execute("SELECT * FROM operarios ORDER BY id")
    for row in cursor.fetchall():
        lista_operarios.insert("", "end", values=row)

def agregar_vehiculo():
    patente = entry_v_patente.get()
    tipo_nombre = entry_v_tipo.get()
    estado_nombre = entry_v_estado.get()
    try:
        cursor.execute("SELECT id FROM tipo_vehiculo WHERE nombre=%s", (tipo_nombre,))
        tipo_id = cursor.fetchone()
        cursor.execute("SELECT id FROM estado WHERE nombre=%s", (estado_nombre,))
        estado_id = cursor.fetchone()
        if not tipo_id or not estado_id:
            messagebox.showerror("Error", "Seleccione un tipo y estado válidos.")
            return
        cursor.execute("INSERT INTO vehiculos(patente, tipo_id, estado_id) VALUES (%s, %s, %s)",
                       (patente, tipo_id[0], estado_id[0]))
        conn.commit()
        actualizar_lista_vehiculos()
        messagebox.showinfo("Éxito", "Vehículo agregado.")
    except Exception as e:
        print("Error", str(e))

def seleccionar_vehiculo(event):
    selected = lista_vehiculos.focus()
    if selected:
        values = lista_vehiculos.item(selected, 'values')
        entry_v_patente.delete(0, tk.END)
        entry_v_patente.insert(0, values[1])
        entry_v_tipo.delete(0, tk.END)
        entry_v_tipo.insert(0, values[2])
        entry_v_capacidad.delete(0, tk.END)
        entry_v_capacidad.insert(0, values[3])
        entry_v_estado.delete(0, tk.END)
        entry_v_estado.insert(0, values[4])

def actualizar_vehiculo():
    try:
        selected = lista_vehiculos.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un vehículo para actualizar.")
            return
        values = lista_vehiculos.item(selected, 'values')
        id_ = values[0]
        patente = entry_v_patente.get()
        tipo_nombre = entry_v_tipo.get()
        estado_nombre = entry_v_estado.get()
        cursor.execute("SELECT id FROM tipo_vehiculo WHERE nombre=%s", (tipo_nombre,))
        tipo_id = cursor.fetchone()
        cursor.execute("SELECT id FROM estado WHERE nombre=%s", (estado_nombre,))
        estado_id = cursor.fetchone()
        if not tipo_id or not estado_id:
            messagebox.showerror("Error", "Seleccione un tipo y estado válidos.")
            return
        cursor.execute("UPDATE vehiculos SET patente=%s, tipo_id=%s, estado_id=%s WHERE id=%s",
                       (patente, tipo_id[0], estado_id[0], id_))
        conn.commit()
        actualizar_lista_vehiculos()
        messagebox.showinfo("Éxito", "Vehículo actualizado.")
    except Exception as e:
        print("Error", str(e))

def eliminar_vehiculo():
    try:
        selected = lista_vehiculos.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un vehículo para eliminar.")
            return
        values = lista_vehiculos.item(selected, 'values')
        id_ = values[0]
        cursor.execute("DELETE FROM vehiculos WHERE id=%s", (id_,))
        conn.commit()
        actualizar_lista_vehiculos()
        messagebox.showinfo("Éxito", "Vehículo eliminado.")
    except Exception as e:
        print("Error", str(e))

def actualizar_lista_vehiculos():
    lista_vehiculos.delete(*lista_vehiculos.get_children())
    cursor.execute("""
        SELECT v.id, v.patente, t.nombre, t.capacidad_max_kg, e.nombre
        FROM vehiculos v
        LEFT JOIN tipo_vehiculo t ON v.tipo_id = t.id
        LEFT JOIN estado e ON v.estado_id = e.id
        ORDER BY v.id
    """)
    for row in cursor.fetchall():
        lista_vehiculos.insert("", "end", values=row)

def agregar_punto():
    direccion = entry_p_direccion.get()
    comuna_nombre = entry_p_comuna.get()
    tipo_residuo_nombre = entry_p_tipo.get()
    try:
        cursor.execute("SELECT id FROM comuna WHERE nombre=%s", (comuna_nombre,))
        comuna_id = cursor.fetchone()
        cursor.execute("SELECT id FROM tipo_residuo WHERE nombre=%s", (tipo_residuo_nombre,))
        tipo_residuo_id = cursor.fetchone()
        if not comuna_id or not tipo_residuo_id:
            messagebox.showerror("Error", "Seleccione una comuna y tipo de residuo válidos.")
            return
        cursor.execute(
            "INSERT INTO puntos_recoleccion(direccion, comuna_id, tipo_residuo_id) VALUES (%s, %s, %s)",
            (direccion, comuna_id[0], tipo_residuo_id[0])
        )
        conn.commit()
        actualizar_lista_puntos()
        messagebox.showinfo("Éxito", "Punto de recolección agregado.")
    except Exception as e:
        print("Error", str(e))

def seleccionar_punto(event):
    selected = lista_puntos.focus()
    if selected:
        values = lista_puntos.item(selected, 'values')
        # id_ = values[0]
        entry_p_direccion.delete(0, tk.END)
        entry_p_direccion.insert(0, values[1])
        entry_p_comuna.delete(0, tk.END)
        entry_p_comuna.insert(0, values[2])
        entry_p_tipo.delete(0, tk.END)
        entry_p_tipo.insert(0, values[3])

def actualizar_punto():
    try:
        selected = lista_puntos.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un punto para actualizar.")
            return
        values = lista_puntos.item(selected, 'values')
        id_ = values[0]
        direccion = entry_p_direccion.get()
        comuna = entry_p_comuna.get()
        tipo = entry_p_tipo.get()
        cursor.execute("UPDATE puntos_recoleccion SET direccion=%s, comuna=%s, tipo_residuo=%s WHERE id=%s",
                       (direccion, comuna, tipo, id_))
        conn.commit()
        actualizar_lista_puntos()
        messagebox.showinfo("Éxito", "Punto actualizado.")
    except Exception as e:
        print("Error", str(e))

def eliminar_punto():
    try:
        selected = lista_puntos.focus()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un punto para eliminar.")
            return
        values = lista_puntos.item(selected, 'values')
        id_ = values[0]
        cursor.execute("DELETE FROM puntos_recoleccion WHERE id=%s", (id_,))
        conn.commit()
        actualizar_lista_puntos()
        messagebox.showinfo("Éxito", "Punto eliminado.")
    except Exception as e:
        print("Error", str(e))

def actualizar_lista_puntos():
    lista_puntos.delete(*lista_puntos.get_children())
    cursor.execute("SELECT * FROM puntos_recoleccion ORDER BY id")
    for row in cursor.fetchall():
        lista_puntos.insert("", "end", values=row)

def cargar_datos_prueba():
    try:
        cursor.execute("SELECT id FROM materiales")
        material_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT id FROM operarios")
        operario_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT id FROM vehiculos")
        vehiculo_ids = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT id FROM puntos_recoleccion")
        punto_ids = [row[0] for row in cursor.fetchall()]

        if not (material_ids and operario_ids and vehiculo_ids and punto_ids):
            messagebox.showwarning("Advertencia", "Debe haber al menos un registro en materiales, operarios, vehículos y puntos de recolección antes de cargar datos de prueba.")
            return

        inicio = datetime(2020, 1, 1)
        for mes in range(36):
            fecha_mes = inicio + timedelta(days=30 * mes)
            for _ in range(500):
                fecha = fecha_mes + timedelta(days=random.randint(0, 29))
                punto_id = random.choice(punto_ids)
                material_id = random.choice(material_ids)
                operario_id = random.choice(operario_ids)
                vehiculo_id = random.choice(vehiculo_ids)
                cursor.execute("SELECT tipo_id FROM vehiculos WHERE id=%s", (vehiculo_id,))
                tipo_id_row = cursor.fetchone()
                if not tipo_id_row:
                    continue
                tipo_id = tipo_id_row[0]
                cursor.execute("SELECT capacidad_max_kg FROM tipo_vehiculo WHERE id=%s", (tipo_id,))
                capacidad_row = cursor.fetchone()
                if not capacidad_row:
                    continue
                capacidad_max = capacidad_row[0]
                if capacidad_max < 100:
                    peso = round(capacidad_max, 2)
                else:
                    peso = round(random.uniform(100, capacidad_max/5), 2)
                cursor.execute("SELECT costo_kg FROM materiales WHERE id=%s", (material_id,))
                row = cursor.fetchone()
                if row:
                    costo_kg = row[0]
                    costo_total = round(peso * costo_kg, 2)
                    cursor.execute('''INSERT INTO recolecciones(fecha, punto_id, material_id,
                                      operario_id, vehiculo_id, peso, costo_total)
                                      VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                                   (fecha, punto_id, material_id, operario_id,
                                    vehiculo_id, peso, costo_total))
        conn.commit()
        actualizar_lista_recolecciones()
        messagebox.showinfo("Éxito", "Datos de prueba cargados.")
    except Exception as e:
        print("Error", str(e))

root = tk.Tk()
root.title("Sistema de Reciclaje")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_materiales = ttk.Frame(notebook)
notebook.add(tab_materiales, text="Materiales")

frame_inputs = tk.Frame(tab_materiales)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="Nombre").grid(row=0, column=0)
entry_nombre = tk.Entry(frame_inputs)
entry_nombre.grid(row=0, column=1)

tk.Label(frame_inputs, text="Costo/kg").grid(row=1, column=0)
entry_costo = tk.Entry(frame_inputs)
entry_costo.grid(row=1, column=1)

frame_botones = tk.Frame(tab_materiales)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Agregar", command=agregar_material).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Actualizar", command=actualizar_material).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Eliminar", command=eliminar_material).grid(row=0, column=2, padx=5)

lista_materiales = ttk.Treeview(tab_materiales, columns=("ID", "Nombre", "Costo"), show="headings")
lista_materiales.heading("ID", text="ID")
lista_materiales.heading("Nombre", text="Nombre")
lista_materiales.heading("Costo", text="Costo/kg")
lista_materiales.pack(pady=10, fill="both", expand=True)
lista_materiales.bind("<<TreeviewSelect>>", seleccionar_material)

tab_operarios = ttk.Frame(notebook)
notebook.add(tab_operarios, text="Operarios")

frame_op = tk.Frame(tab_operarios)
frame_op.pack(padx=10, pady=10, fill="x")

tk.Label(frame_op, text="Nombre").grid(row=0, column=0)
entry_op_nombre = tk.Entry(frame_op)
entry_op_nombre.grid(row=0, column=1)

tk.Label(frame_op, text="Turno").grid(row=1, column=0)
entry_op_turno = tk.Entry(frame_op)
entry_op_turno.grid(row=1, column=1)

tk.Label(frame_op, text="Zona").grid(row=2, column=0)
entry_op_zona = tk.Entry(frame_op)
entry_op_zona.grid(row=2, column=1)

frame_op_botones = tk.Frame(tab_operarios)
frame_op_botones.pack(pady=5)
tk.Button(frame_op_botones, text="Agregar", command=agregar_operario).grid(row=0, column=0, padx=5)
tk.Button(frame_op_botones, text="Actualizar", command=actualizar_operario).grid(row=0, column=1, padx=5)
tk.Button(frame_op_botones, text="Eliminar", command=eliminar_operario).grid(row=0, column=2, padx=5)

lista_operarios = ttk.Treeview(tab_operarios, columns=("ID", "Nombre", "Turno", "Zona"), show="headings")
for col in ("ID", "Nombre", "Turno", "Zona"):
    lista_operarios.heading(col, text=col)
lista_operarios.pack(pady=5, fill="x")
lista_operarios.bind("<<TreeviewSelect>>", seleccionar_operario)

tab_vehiculos = ttk.Frame(notebook)
notebook.add(tab_vehiculos, text="Vehículos")

frame_v = tk.Frame(tab_vehiculos)
frame_v.pack(padx=10, pady=10, fill="x")

tk.Label(frame_v, text="Patente").grid(row=0, column=0)
entry_v_patente = tk.Entry(frame_v)
entry_v_patente.grid(row=0, column=1)

tk.Label(frame_v, text="Tipo de Vehículo").grid(row=1, column=0)
tipo_var = StringVar()
entry_v_tipo = ttk.Combobox(frame_v, textvariable=tipo_var, state="readonly")
cursor.execute("SELECT nombre FROM tipo_vehiculo ORDER BY id")
tipos_lista = [row[0] for row in cursor.fetchall()]
entry_v_tipo['values'] = tipos_lista
entry_v_tipo.grid(row=1, column=1)

tk.Label(frame_v, text="Capacidad (kg)").grid(row=2, column=0)
entry_v_capacidad = tk.Entry(frame_v, state="readonly")
entry_v_capacidad.grid(row=2, column=1)

tk.Label(frame_v, text="Estado").grid(row=3, column=0)
estado_var = StringVar()
entry_v_estado = ttk.Combobox(frame_v, textvariable=estado_var, state="readonly")
cursor.execute("SELECT nombre FROM estado ORDER BY id")
estados_lista = [row[0] for row in cursor.fetchall()]
entry_v_estado['values'] = estados_lista
entry_v_estado.grid(row=3, column=1)

frame_v_botones = tk.Frame(tab_vehiculos)
frame_v_botones.pack(pady=5)
tk.Button(frame_v_botones, text="Agregar", command=agregar_vehiculo).grid(row=0, column=0, padx=5)
tk.Button(frame_v_botones, text="Actualizar", command=actualizar_vehiculo).grid(row=0, column=1, padx=5)
tk.Button(frame_v_botones, text="Eliminar", command=eliminar_vehiculo).grid(row=0, column=2, padx=5)

lista_vehiculos = ttk.Treeview(tab_vehiculos, columns=("ID", "Patente", "Tipo", "Capacidad", "Estado"), show="headings")
for col in ("ID", "Patente", "Tipo", "Capacidad", "Estado"):
    lista_vehiculos.heading(col, text=col)
lista_vehiculos.pack(pady=5, fill="x")
lista_vehiculos.bind("<<TreeviewSelect>>", seleccionar_vehiculo)

tab_puntos = ttk.Frame(notebook)
notebook.add(tab_puntos, text="Puntos de Recolección")

frame_p = tk.Frame(tab_puntos)
frame_p.pack(padx=10, pady=10, fill="x")

tk.Label(frame_p, text="Dirección").grid(row=0, column=0)
entry_p_direccion = tk.Entry(frame_p)
entry_p_direccion.grid(row=0, column=1)

tk.Label(frame_p, text="Comuna").grid(row=1, column=0)
comuna_var = StringVar()
entry_p_comuna = ttk.Combobox(frame_p, textvariable=comuna_var, state="readonly")
cursor.execute("SELECT nombre FROM comuna ORDER BY nombre")
comunas_lista = [row[0] for row in cursor.fetchall()]
entry_p_comuna['values'] = comunas_lista
entry_p_comuna.grid(row=1, column=1)

tk.Label(frame_p, text="Tipo Residuos").grid(row=2, column=0)
tipo_residuo_var = StringVar()
entry_p_tipo = ttk.Combobox(frame_p, textvariable=tipo_residuo_var, state="readonly")
cursor.execute("SELECT nombre FROM tipo_residuo ORDER BY nombre")
tipos_residuo_lista = [row[0] for row in cursor.fetchall()]
entry_p_tipo['values'] = tipos_residuo_lista
entry_p_tipo.grid(row=2, column=1)

frame_p_botones = tk.Frame(tab_puntos)
frame_p_botones.pack(pady=5)
tk.Button(frame_p_botones, text="Agregar", command=agregar_punto).grid(row=0, column=0, padx=5)
tk.Button(frame_p_botones, text="Actualizar", command=actualizar_punto).grid(row=0, column=1, padx=5)
tk.Button(frame_p_botones, text="Eliminar", command=eliminar_punto).grid(row=0, column=2, padx=5)

lista_puntos = ttk.Treeview(tab_puntos, columns=("ID", "Dirección", "Comuna", "Tipo"), show="headings")
for col in ("ID", "Dirección", "Comuna", "Tipo"):
    lista_puntos.heading(col, text=col)
lista_puntos.pack(pady=5, fill="x")
lista_puntos.bind("<<TreeviewSelect>>", seleccionar_punto)

tab_prueba = ttk.Frame(notebook)
notebook.add(tab_prueba, text="Datos de Prueba")

tk.Label(tab_prueba, text="Cargar datos de prueba masivos para recolecciones").pack(pady=20)
tk.Button(tab_prueba, text="Cargar Datos de Prueba", command=cargar_datos_prueba).pack(pady=10)

tk.Button(root, text="Salir", command=root.quit).pack(pady=10)

actualizar_lista_operarios()
actualizar_lista_vehiculos()
actualizar_lista_puntos()
actualizar_lista_materiales()

def actualizar_capacidad(event):
    tipo_nombre = entry_v_tipo.get()
    cursor.execute("SELECT capacidad_max_kg FROM tipo_vehiculo WHERE nombre=%s", (tipo_nombre,))
    row = cursor.fetchone()
    if row:
        entry_v_capacidad.config(state="normal")
        entry_v_capacidad.delete(0, tk.END)
        entry_v_capacidad.insert(0, str(row[0]))
        entry_v_capacidad.config(state="readonly")
    else:
        entry_v_capacidad.config(state="normal")
        entry_v_capacidad.delete(0, tk.END)
        entry_v_capacidad.config(state="readonly")

entry_v_tipo.bind("<<ComboboxSelected>>", actualizar_capacidad)

tab_recolecciones = ttk.Frame(notebook)
notebook.add(tab_recolecciones, text="Recolecciones")

columnas_recolecciones = (
    "ID", "Fecha", "Punto", "Material", "Operario", "Vehículo", "Peso", "Costo Total"
)

lista_recolecciones = ttk.Treeview(
    tab_recolecciones, columns=columnas_recolecciones, show="headings"
)
for col in columnas_recolecciones:
    lista_recolecciones.heading(col, text=col)
lista_recolecciones.pack(pady=5, fill="both", expand=True)

def actualizar_lista_recolecciones():
    lista_recolecciones.delete(*lista_recolecciones.get_children())
    cursor.execute("""
        SELECT 
            r.id, r.fecha, 
            p.direccion, 
            m.nombre, 
            o.nombre, 
            v.patente, 
            r.peso, 
            r.costo_total
        FROM recolecciones r
        LEFT JOIN puntos_recoleccion p ON r.punto_id = p.id
        LEFT JOIN materiales m ON r.material_id = m.id
        LEFT JOIN operarios o ON r.operario_id = o.id
        LEFT JOIN vehiculos v ON r.vehiculo_id = v.id
        ORDER BY r.id DESC, r.fecha DESC
    """)
    for row in cursor.fetchall():
        lista_recolecciones.insert("", "end", values=row)

actualizar_lista_recolecciones()

root.mainloop()
#eliminar_tablas()
cursor.close()
conn.close()
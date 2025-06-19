import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    host="localhost",
    database="dbreciclaje",
    user="python_user",
    password="1234"
)
cursor = conn.cursor()

def crear_tablas():
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
        CREATE TABLE IF NOT EXISTS vehiculos (
            patente TEXT PRIMARY KEY,
            tipo TEXT,
            capacidad_max_kg REAL,
            estado TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS puntos_recoleccion (
            id SERIAL PRIMARY KEY,
            direccion TEXT,
            comuna TEXT,
            tipo_residuo TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recolecciones (
            id SERIAL PRIMARY KEY,
            fecha DATE,
            punto_id INTEGER REFERENCES puntos_recoleccion(id),
            material_id INTEGER REFERENCES materiales(id),
            operario_id INTEGER REFERENCES operarios(id),
            vehiculo_patente TEXT REFERENCES vehiculos(patente),
            peso REAL,
            costo_total REAL
        );
    ''')
    conn.commit()

crear_tablas()

def agregar_material():
    nombre = entry_nombre.get()
    try:
        costo = float(entry_costo.get())
        cursor.execute("INSERT INTO materiales(nombre, costo_kg) VALUES (%s, %s)", (nombre, costo))
        conn.commit()
        actualizar_lista_materiales()
        messagebox.showinfo("Éxito", "Material agregado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def actualizar_material():
    try:
        id_ = int(entry_id.get())
        nombre = entry_nombre.get()
        costo = float(entry_costo.get())
        cursor.execute("UPDATE materiales SET nombre=%s, costo_kg=%s WHERE id=%s", (nombre, costo, id_))
        conn.commit()
        actualizar_lista_materiales()
        messagebox.showinfo("Éxito", "Material actualizado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def eliminar_material():
    try:
        id_ = int(entry_id.get())
        cursor.execute("DELETE FROM materiales WHERE id=%s", (id_,))
        conn.commit()
        actualizar_lista_materiales()
        messagebox.showinfo("Éxito", "Material eliminado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

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
        messagebox.showerror("Error", str(e))

def seleccionar_operario(event):
    selected = lista_operarios.focus()
    if selected:
        values = lista_operarios.item(selected, 'values')
        entry_op_id.delete(0, tk.END)
        entry_op_id.insert(0, values[0])
        entry_op_nombre.delete(0, tk.END)
        entry_op_nombre.insert(0, values[1])
        entry_op_turno.delete(0, tk.END)
        entry_op_turno.insert(0, values[2])
        entry_op_zona.delete(0, tk.END)
        entry_op_zona.insert(0, values[3])

def actualizar_operario():
    try:
        id_ = int(entry_op_id.get())
        nombre = entry_op_nombre.get()
        turno = entry_op_turno.get()
        zona = entry_op_zona.get()
        cursor.execute("UPDATE operarios SET nombre=%s, turno=%s, zona=%s WHERE id=%s",
                       (nombre, turno, zona, id_))
        conn.commit()
        actualizar_lista_operarios()
        messagebox.showinfo("Éxito", "Operario actualizado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def eliminar_operario():
    try:
        id_ = int(entry_op_id.get())
        cursor.execute("DELETE FROM operarios WHERE id=%s", (id_,))
        conn.commit()
        actualizar_lista_operarios()
        messagebox.showinfo("Éxito", "Operario eliminado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def actualizar_lista_operarios():
    lista_operarios.delete(*lista_operarios.get_children())
    cursor.execute("SELECT * FROM operarios ORDER BY id")
    for row in cursor.fetchall():
        lista_operarios.insert("", "end", values=row)

def agregar_vehiculo():
    patente = entry_v_patente.get()
    tipo = entry_v_tipo.get()
    capacidad = entry_v_capacidad.get()
    estado = entry_v_estado.get()
    try:
        cursor.execute("INSERT INTO vehiculos(patente, tipo, capacidad_max_kg, estado) VALUES (%s, %s, %s, %s)",
                       (patente, tipo, float(capacidad), estado))
        conn.commit()
        actualizar_lista_vehiculos()
        messagebox.showinfo("Éxito", "Vehículo agregado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def seleccionar_vehiculo(event):
    selected = lista_vehiculos.focus()
    if selected:
        values = lista_vehiculos.item(selected, 'values')
        entry_v_patente.delete(0, tk.END)
        entry_v_patente.insert(0, values[0])
        entry_v_tipo.delete(0, tk.END)
        entry_v_tipo.insert(0, values[1])
        entry_v_capacidad.delete(0, tk.END)
        entry_v_capacidad.insert(0, values[2])
        entry_v_estado.delete(0, tk.END)
        entry_v_estado.insert(0, values[3])

def actualizar_vehiculo():
    try:
        patente = entry_v_patente.get()
        tipo = entry_v_tipo.get()
        capacidad = float(entry_v_capacidad.get())
        estado = entry_v_estado.get()
        cursor.execute("UPDATE vehiculos SET tipo=%s, capacidad_max_kg=%s, estado=%s WHERE patente=%s",
                       (tipo, capacidad, estado, patente))
        conn.commit()
        actualizar_lista_vehiculos()
        messagebox.showinfo("Éxito", "Vehículo actualizado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def eliminar_vehiculo():
    try:
        patente = entry_v_patente.get()
        cursor.execute("DELETE FROM vehiculos WHERE patente=%s", (patente,))
        conn.commit()
        actualizar_lista_vehiculos()
        messagebox.showinfo("Éxito", "Vehículo eliminado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def actualizar_lista_vehiculos():
    lista_vehiculos.delete(*lista_vehiculos.get_children())
    cursor.execute("SELECT * FROM vehiculos ORDER BY patente")
    for row in cursor.fetchall():
        lista_vehiculos.insert("", "end", values=row)

def agregar_punto():
    direccion = entry_p_direccion.get()
    comuna = entry_p_comuna.get()
    tipo = entry_p_tipo.get()
    try:
        cursor.execute("INSERT INTO puntos_recoleccion(direccion, comuna, tipo_residuo) VALUES (%s, %s, %s)",
                       (direccion, comuna, tipo))
        conn.commit()
        actualizar_lista_puntos()
        messagebox.showinfo("Éxito", "Punto de recolección agregado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def seleccionar_punto(event):
    selected = lista_puntos.focus()
    if selected:
        values = lista_puntos.item(selected, 'values')
        entry_p_id.delete(0, tk.END)
        entry_p_id.insert(0, values[0])
        entry_p_direccion.delete(0, tk.END)
        entry_p_direccion.insert(0, values[1])
        entry_p_comuna.delete(0, tk.END)
        entry_p_comuna.insert(0, values[2])
        entry_p_tipo.delete(0, tk.END)
        entry_p_tipo.insert(0, values[3])

def actualizar_punto():
    try:
        id_ = int(entry_p_id.get())
        direccion = entry_p_direccion.get()
        comuna = entry_p_comuna.get()
        tipo = entry_p_tipo.get()
        cursor.execute("UPDATE puntos_recoleccion SET direccion=%s, comuna=%s, tipo_residuo=%s WHERE id=%s",
                       (direccion, comuna, tipo, id_))
        conn.commit()
        actualizar_lista_puntos()
        messagebox.showinfo("Éxito", "Punto actualizado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def eliminar_punto():
    try:
        id_ = int(entry_p_id.get())
        cursor.execute("DELETE FROM puntos_recoleccion WHERE id=%s", (id_,))
        conn.commit()
        actualizar_lista_puntos()
        messagebox.showinfo("Éxito", "Punto eliminado.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

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
        cursor.execute("SELECT patente FROM vehiculos")
        vehiculo_patentes = [row[0] for row in cursor.fetchall()]
        cursor.execute("SELECT id FROM puntos_recoleccion")
        punto_ids = [row[0] for row in cursor.fetchall()]

        if not (material_ids and operario_ids and vehiculo_patentes and punto_ids):
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
                vehiculo_patente = random.choice(vehiculo_patentes)
                peso = round(random.uniform(10, 100), 2)
                cursor.execute("SELECT costo_kg FROM materiales WHERE id=%s", (material_id,))
                row = cursor.fetchone()
                if row:
                    costo_kg = row[0]
                    costo_total = round(peso * costo_kg, 2)
                    cursor.execute('''INSERT INTO recolecciones(fecha, punto_id, material_id,
                                      operario_id, vehiculo_patente, peso, costo_total)
                                      VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                                   (fecha, punto_id, material_id, operario_id,
                                    vehiculo_patente, peso, costo_total))
        conn.commit()
        messagebox.showinfo("Éxito", "Datos de prueba cargados.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
def seleccionar_material(event):
    selected = lista_materiales.focus()
    if selected:
        values = lista_materiales.item(selected, 'values')
        entry_id.delete(0, tk.END)
        entry_id.insert(0, values[0])
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, values[1])
        entry_costo.delete(0, tk.END)
        entry_costo.insert(0, values[2])

root = tk.Tk()
root.title("Sistema de Reciclaje")
root.geometry("800x600")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab_materiales = ttk.Frame(notebook)
notebook.add(tab_materiales, text="Materiales")

frame_inputs = tk.Frame(tab_materiales)
frame_inputs.pack(pady=10)

tk.Label(frame_inputs, text="ID").grid(row=0, column=0)
entry_id = tk.Entry(frame_inputs)
entry_id.grid(row=0, column=1)

tk.Label(frame_inputs, text="Nombre").grid(row=1, column=0)
entry_nombre = tk.Entry(frame_inputs)
entry_nombre.grid(row=1, column=1)

tk.Label(frame_inputs, text="Costo/kg").grid(row=2, column=0)
entry_costo = tk.Entry(frame_inputs)
entry_costo.grid(row=2, column=1)

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

# --- Pestaña Operarios ---
tab_operarios = ttk.Frame(notebook)
notebook.add(tab_operarios, text="Operarios")

frame_op = tk.Frame(tab_operarios)
frame_op.pack(padx=10, pady=10, fill="x")

tk.Label(frame_op, text="ID").grid(row=0, column=0)
entry_op_id = tk.Entry(frame_op)
entry_op_id.grid(row=0, column=1)

tk.Label(frame_op, text="Nombre").grid(row=1, column=0)
entry_op_nombre = tk.Entry(frame_op)
entry_op_nombre.grid(row=1, column=1)

tk.Label(frame_op, text="Turno").grid(row=2, column=0)
entry_op_turno = tk.Entry(frame_op)
entry_op_turno.grid(row=2, column=1)

tk.Label(frame_op, text="Zona").grid(row=3, column=0)
entry_op_zona = tk.Entry(frame_op)
entry_op_zona.grid(row=3, column=1)

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

tk.Label(frame_v, text="Tipo").grid(row=1, column=0)
entry_v_tipo = tk.Entry(frame_v)
entry_v_tipo.grid(row=1, column=1)

tk.Label(frame_v, text="Capacidad (kg)").grid(row=2, column=0)
entry_v_capacidad = tk.Entry(frame_v)
entry_v_capacidad.grid(row=2, column=1)

tk.Label(frame_v, text="Estado").grid(row=3, column=0)
entry_v_estado = tk.Entry(frame_v)
entry_v_estado.grid(row=3, column=1)

frame_v_botones = tk.Frame(tab_vehiculos)
frame_v_botones.pack(pady=5)
tk.Button(frame_v_botones, text="Agregar", command=agregar_vehiculo).grid(row=0, column=0, padx=5)
tk.Button(frame_v_botones, text="Actualizar", command=actualizar_vehiculo).grid(row=0, column=1, padx=5)
tk.Button(frame_v_botones, text="Eliminar", command=eliminar_vehiculo).grid(row=0, column=2, padx=5)

lista_vehiculos = ttk.Treeview(tab_vehiculos, columns=("Patente", "Tipo", "Capacidad", "Estado"), show="headings")
for col in ("Patente", "Tipo", "Capacidad", "Estado"):
    lista_vehiculos.heading(col, text=col)
lista_vehiculos.pack(pady=5, fill="x")
lista_vehiculos.bind("<<TreeviewSelect>>", seleccionar_vehiculo)

# --- Pestaña Puntos de Recolección ---
tab_puntos = ttk.Frame(notebook)
notebook.add(tab_puntos, text="Puntos de Recolección")

frame_p = tk.Frame(tab_puntos)
frame_p.pack(padx=10, pady=10, fill="x")

tk.Label(frame_p, text="ID").grid(row=0, column=0)
entry_p_id = tk.Entry(frame_p)
entry_p_id.grid(row=0, column=1)

tk.Label(frame_p, text="Dirección").grid(row=1, column=0)
entry_p_direccion = tk.Entry(frame_p)
entry_p_direccion.grid(row=1, column=1)

tk.Label(frame_p, text="Comuna").grid(row=2, column=0)
entry_p_comuna = tk.Entry(frame_p)
entry_p_comuna.grid(row=2, column=1)

tk.Label(frame_p, text="Tipo Residuos").grid(row=3, column=0)
entry_p_tipo = tk.Entry(frame_p)
entry_p_tipo.grid(row=3, column=1)

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

root.mainloop()

cursor.close()
conn.close()
# Sistema de Gestión de Reciclaje

## Descripción

Este proyecto gestiona información de reciclaje, incluyendo materiales, puntos de recolección, operarios, vehículos y las recolecciones diarias. Permite almacenar los datos en una base PostgreSQL y generar reportes gráficos para analizar tendencias, costos y frecuencias de recolección.

---

## Requisitos previos

- Python 3.x instalado
- Librerías Python:
  - `psycopg2`
  - `pandas`
  - `matplotlib`
- Base de datos PostgreSQL instalada y configurada
- Usuario PostgreSQL con permisos para crear tablas e insertar datos

---

## Configuración inicial

### 1. Crear la base de datos y tablas

Cree la base de datos y despues usando el documento CreacionDeTablas.txt use el scrip necesario

### 2. Rellenar la base de datos

Para poder rellenar la base de datos es necesario:
- Cambie los nombres de las conecciones con la base de datos y asegurese de que el usuario tenga permisos
- Primero ejecute RellenarTablasSecundarios.py antes de RellenarTablaRecolecciones o no obtendra datos para los que trabajar
- Puede usar el recolecciones.csv si quiere usar los datos con los que se trabajaron

### 3. Generar graficos

- Para hacer uso del programa LlamadasSQLGraficos.py cambie los nombres de las conecciones con la base de datos y asegurese de que el usuario tenga permisos
- Recuerde que para generar los gráficos debe tener claro el año o los años que desea consultar, ya que el programa RellenarTablaRecolecciones.py genera datos correspondientes al año anterior a la fecha actual. Si necesita hacer algún cambio en ese rango, ajuste el programa según corresponda:
  - Para modificar la cantidad de datos generados, cambia el valor 100 en la línea 30 por la cantidad que desees. De esta forma, podrás controlar cuántos registros se crearán.
  - Para ajustar el rango de días que se resta en la línea 31, modifica el valor 365 (que representa un año en días). Puedes cambiarlo por un número mayor o menor según el periodo de tiempo que desees considerar

---

## Solución de problemas comunes
- Error de permisos en PostgreSQL: asegúrate que el usuario tenga permisos para insertar y modificar secuencias
- Tipos de datos incompatibles: revisa que los costos estén definidos como DECIMAL y que los cálculos conviertan Decimal a float si es necesario
- Problemas con fechas: utiliza el módulo datetime y asegúrate que los formatos sean compatibles con PostgreSQL

## Detalles de la base de datos

La base de datos a trabajar permite registrar, organizar y analizar los datos relacionados con la recolección y procesamiento de residuos reciclables en distintas zonas. Su objetivo principal es optimizar los procesos logísticos y operativos, fomentar la participación ciudadana en el reciclaje y evaluar su impacto ambiental y social en la comunidad.

A continuación se mencionan los elementos de la base de datos:

-Materiales: Cada tipo de residuo reciclable tiene un identificador único, su nombre y el costo asociado por kilogramo.

-Operarios: Se registran los datos de los trabajadores encargados de la recolección. Cada operario tiene un ID, su nombre, el turno en que trabaja y la zona asignada.

-Vehículos: Cada vehículo utilizado en las recolecciones tiene una patente única, tipo (camión, camioneta, etc.), capacidad máxima en kilogramos y estado operativo.

-Puntos de Recolección: Estos representan las ubicaciones físicas donde se recolectan los materiales reciclables. Cada punto incluye su dirección, comuna y tipo (que residuos acepta). 

-Recolecciones: Contiene la fecha, el punto de recolección, el material recolectado, el operario asignado y el vehículo utilizado. También se especifica el peso recolectado y el costo total asociado.

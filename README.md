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
-Cambie los nombres de las conecciones con la base de datos y asegurese de que el usuario tenga permisos
-Primero ejecute RellenarTablasSecundarios.py antes de RellenarTablaRecolecciones o no obtendra datos para los que trabajar
-Puede usar el recolecciones.csv si quiere usar los datos con los que se trabajaron

### 3. Generar graficos

-Para hacer uso del programa LlamadasSQLGraficos.py cambie los nombres de las conecciones con la base de datos y asegurese de que el usuario tenga permisos
-Recuerde para Generar los graficos asegurese de tener claro los años a buscar, ya que el programa RellenarTablaRecolecciones genera los datos un año atras a la fecha que se encuentra
cualquier cambio que necesite:
  -Cambiar la cantidad de datos cambie el 100 en la linea 30 para agregar los datos que quiera
  -Para cambiar la diferencia de los años en la linea 31 cambie el 365 (que son los dias antes) y cambielo por un valor mayor o menor dependiendo de que quiera hacer

---

## Solución de problemas comunes
-Error de permisos en PostgreSQL: asegúrate que el usuario tenga permisos para insertar y modificar secuencias
-Tipos de datos incompatibles: revisa que los costos estén definidos como DECIMAL y que los cálculos conviertan Decimal a float si es necesario
-Problemas con fechas: utiliza el módulo datetime y asegúrate que los formatos sean compatibles con PostgreSQL

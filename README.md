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

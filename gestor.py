import sqlite3
import re  # Importamos el módulo re para validar el correo con expresiones regulares

# Conexión y creación de tabla
conn = sqlite3.connect("alumnos.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS estudiantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    edad INTEGER,
    correo TEXT
)
""")
conn.commit()

# Funciones principales
def agregar_estudiante(nombre, edad, correo):
    # Validar formato del correo electrónico
    patron_correo = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(patron_correo, correo):
        print("Error: Formato de correo electrónico inválido.")
        return False
    
    try:
        cursor.execute("""
        INSERT INTO estudiantes (nombre, edad, correo)
        VALUES (?, ?, ?)
        """, (nombre, edad, correo))
        conn.commit()
        print(f"Estudiante {nombre} agregado correctamente.")
        return True
    except sqlite3.Error as e:
        print(f"Error al agregar estudiante: {e}")
        return False

def mostrar_estudiantes():
    cursor.execute("SELECT * FROM estudiantes")
    filas = cursor.fetchall()
    
    if not filas:
        print("No hay estudiantes registrados.")
        return
    
    print("\n----- LISTA DE ESTUDIANTES -----")
    print("ID | NOMBRE | EDAD | CORREO")
    print("-" * 50)
    for fila in filas:
        print(f"{fila[0]} | {fila[1]} | {fila[2]} | {fila[3]}")

def buscar_por_nombre(nombre):
    # Utilizamos LIKE para buscar coincidencias parciales
    cursor.execute("SELECT * FROM estudiantes WHERE nombre LIKE ?", (f"%{nombre}%",))
    resultados = cursor.fetchall()
    
    if not resultados:
        print(f"No se encontraron estudiantes con el nombre '{nombre}'.")
        return
    
    print(f"\n----- RESULTADOS DE BÚSQUEDA PARA '{nombre}' -----")
    print("ID | NOMBRE | EDAD | CORREO")
    print("-" * 50)
    for resultado in resultados:
        print(f"{resultado[0]} | {resultado[1]} | {resultado[2]} | {resultado[3]}")

# Menú principal
while True:
    print("\n===== SISTEMA DE GESTIÓN DE ESTUDIANTES =====")
    print("1. Agregar estudiante")
    print("2. Mostrar todos")
    print("3. Buscar por nombre")
    print("4. Salir")
    op = input("Elige una opción: ")
    
    if op == '1':
        nombre = input("Nombre: ")
        try:
            edad = int(input("Edad: "))
            if edad <= 0:
                print("La edad debe ser un número positivo.")
                continue
        except ValueError:
            print("Edad inválida. Debe ser un número entero.")
            continue
        correo = input("Correo: ")
        agregar_estudiante(nombre, edad, correo)
    elif op == '2':
        mostrar_estudiantes()
    elif op == '3':
        nombre = input("Nombre a buscar: ")
        buscar_por_nombre(nombre)
    elif op == '4':
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Intente nuevamente.")

# Cierre de conexión
conn.close()
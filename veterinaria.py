import sqlite3

# Nombre del archivo de base de datos
DB_NAME = "clinica_veterinaria.db"

# ---------------- Conexión ----------------
def abrir_conexion():
    """
    Abre la conexión con la base de datos SQLite.
    """
    try:
        return sqlite3.connect(DB_NAME)
    except sqlite3.Error as e:
        print("Error al abrir conexión:", e)
        return None

def cerrar_conexion(conexion):
    """
    Cierra la conexión con la base de datos.
    """
    if conexion:
        conexion.close()

# ---------------- Inserción ----------------
def insertar_especialidad(nombre):
    """
    Inserta una nueva especialidad en la tabla Especialidades.
    """
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        if not nombre.strip():
            return "Error: nombre vacío."
        cursor.execute("INSERT INTO Especialidades (nombre) VALUES (?)", (nombre,))
        conexion.commit()
        return "Especialidad insertada."
    except sqlite3.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        cerrar_conexion(conexion)

def insertar_veterinario(nombre, telefono, id_especialidad):
    """
    Inserta un nuevo veterinario en la tabla Veterinarios.
    """
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        if not nombre.strip():
            return "Error: nombre vacío."
        if not isinstance(telefono, int):
            return "Error: teléfono debe ser número entero."
        if not isinstance(id_especialidad, int):
            return "Error: id_especialidad debe ser número entero."

        cursor.execute("INSERT INTO Veterinarios (nombre, telefono, id_especialidad) VALUES (?, ?, ?)",
                       (nombre, telefono, id_especialidad))
        conexion.commit()
        return "Veterinario insertado."
    except sqlite3.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        cerrar_conexion(conexion)

# ---------------- Listado ----------------
def listar_especialidades():
    """
    Devuelve todas las especialidades registradas.
    """
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM Especialidades")
        return cursor.fetchall()
    except sqlite3.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        cerrar_conexion(conexion)

def listar_veterinarios_con_especialidad():
    """
    Devuelve veterinarios junto con su especialidad usando JOIN.
    """
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT Veterinarios.id, Veterinarios.nombre, Veterinarios.telefono, Especialidades.nombre
            FROM Veterinarios
            JOIN Especialidades ON Veterinarios.id_especialidad = Especialidades.id
        """)
        return cursor.fetchall()
    except sqlite3.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        cerrar_conexion(conexion)

# ---------------- Eliminación ----------------
def eliminar_veterinario(id_veterinario):
    """
    Elimina un veterinario por su ID.
    """
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM Veterinarios WHERE id = ?", (id_veterinario,))
        conexion.commit()
        if cursor.rowcount == 0:
            return "No se encontró el veterinario."
        return "Veterinario eliminado."
    except sqlite3.Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        cerrar_conexion(conexion)

# ---------------- Bloque de prueba ----------------
if __name__ == "__main__":
    print("Prueba de conexión:")
    conexion = abrir_conexion()
    if conexion:
        print("Conexión OK")
        cerrar_conexion(conexion)

    print("\nInsertar especialidad:")
    print(insertar_especialidad("Prueba Especialidad"))

    print("\nInsertar veterinario:")
    print(insertar_veterinario("Prueba Veterinario", 3001234567, 1))

    print("\nListar especialidades:")
    print(listar_especialidades())

    print("\nListar veterinarios con especialidad:")
    print(listar_veterinarios_con_especialidad())

    print("\nEliminar veterinario con ID 1:")
    print(eliminar_veterinario(1))


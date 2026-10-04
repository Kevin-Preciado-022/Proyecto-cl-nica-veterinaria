import sqlite3

DB_NAME = "clinica_veterinaria.db"

def tablas():
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()

        # Crear tabla Especialidades
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Especialidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
        """)

        # Crear tabla Veterinarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Veterinarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono INTEGER,
            id_especialidad INTEGER NOT NULL,
            FOREIGN KEY (id_especialidad) REFERENCES Especialidades(id)
        )
        """)

        conexion.commit()
        print("Tablas creadas correctamente.")
    except sqlite3.Error as e:
        print("Error al crear tablas:", e)
    finally:
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    tablas()

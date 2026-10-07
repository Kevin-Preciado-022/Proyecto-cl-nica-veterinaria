import tkinter as tk
from tkinter import messagebox, ttk

import veterinaria  # Importamos el backend

# ---------------- Ventana principal ----------------
root = tk.Tk()
root.title("Clínica Veterinaria")
root.geometry("700x500")

# ---------------- Frame superior: formulario ----------------
frame_form = tk.Frame(root)
frame_form.pack(pady=10)

# Campo nombre especialidad
tk.Label(frame_form, text="Nombre Especialidad:").grid(row=0, column=0, padx=5, pady=5)
entry_especialidad = tk.Entry(frame_form)
entry_especialidad.grid(row=0, column=1, padx=5, pady=5)

# Botón agregar especialidad
def agregar_especialidad():
    nombre = entry_especialidad.get()
    resultado = veterinaria.insertar_especialidad(nombre)
    messagebox.showinfo("Resultado", resultado)
    actualizar_combobox()
    entry_especialidad.delete(0, tk.END)

tk.Button(frame_form, text="Agregar Especialidad", command=agregar_especialidad).grid(row=0, column=2, padx=5, pady=5)

# Campo nombre veterinario
tk.Label(frame_form, text="Nombre Veterinario:").grid(row=1, column=0, padx=5, pady=5)
entry_veterinario = tk.Entry(frame_form)
entry_veterinario.grid(row=1, column=1, padx=5, pady=5)

# Campo teléfono
tk.Label(frame_form, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
entry_telefono = tk.Entry(frame_form)
entry_telefono.grid(row=2, column=1, padx=5, pady=5)

# Combobox especialidad
tk.Label(frame_form, text="Especialidad:").grid(row=3, column=0, padx=5, pady=5)
combo_especialidad = ttk.Combobox(frame_form, state="readonly")
combo_especialidad.grid(row=3, column=1, padx=5, pady=5)

def actualizar_combobox():
    especialidades = veterinaria.listar_especialidades()
    if isinstance(especialidades, list):
        combo_especialidad["values"] = [f"{e[0]} - {e[1]}" for e in especialidades]

actualizar_combobox()

# Botón agregar veterinario
def agregar_veterinario():
    nombre = entry_veterinario.get()
    telefono = entry_telefono.get()
    especialidad = combo_especialidad.get()

    if not nombre or not telefono or not especialidad:
        messagebox.showerror("Error", "Todos los campos son obligatorios.")
        return

    try:
        telefono = int(telefono)
        id_especialidad = int(especialidad.split(" - ")[0])
        resultado = veterinaria.insertar_veterinario(nombre, telefono, id_especialidad)
        messagebox.showinfo("Resultado", resultado)
        actualizar_treeview()
        entry_veterinario.delete(0, tk.END)
        entry_telefono.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "El teléfono debe ser un número.")

tk.Button(frame_form, text="Agregar Veterinario", command=agregar_veterinario).grid(row=4, column=1, padx=5, pady=10)

# ---------------- Frame inferior: listado ----------------
frame_list = tk.Frame(root)
frame_list.pack(pady=10)

# Treeview para mostrar veterinarios con especialidad
tree = ttk.Treeview(frame_list, columns=("ID", "Nombre", "Teléfono", "Especialidad"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Teléfono", text="Teléfono")
tree.heading("Especialidad", text="Especialidad")
tree.pack()

def actualizar_treeview():
    for row in tree.get_children():
        tree.delete(row)
    registros = veterinaria.listar_veterinarios_con_especialidad()
    if isinstance(registros, list):
        for r in registros:
            tree.insert("", tk.END, values=r)

actualizar_treeview()

# Botón eliminar veterinario
def eliminar_veterinario():
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showerror("Error", "Debe seleccionar un registro.")
        return

    confirmacion = messagebox.askyesno("Confirmar", "¿Desea eliminar este veterinario?")
    if confirmacion:
        id_vet = tree.item(seleccionado[0])["values"][0]
        resultado = veterinaria.eliminar_veterinario(id_vet)
        messagebox.showinfo("Resultado", resultado)
        actualizar_treeview()

tk.Button(frame_list, text="Eliminar Veterinario", command=eliminar_veterinario).pack(pady=5)

# ---------------- Ejecutar ventana ----------------
root.mainloop()

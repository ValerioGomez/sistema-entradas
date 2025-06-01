import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Entry, Button, Combobox
from services import crud
from tkinter import messagebox
import threading
from sync_manager import sincronizar_datos_periodicamente

def agregar_usuario():
    nombre = entry_nombre.get()
    email = entry_email.get()
    if nombre and email:
        try:
            crud.crear_usuario(nombre, email)
            messagebox.showinfo("Éxito", "Usuario agregado")
            listar_usuarios_en_gui()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showerror("Error", "Campos vacíos")

def listar_usuarios_en_gui():
    lista_usuarios.delete(0, tk.END)
    usuarios = crud.listar_usuarios()
    for u in usuarios:
        lista_usuarios.insert(tk.END, f"{u.id} - {u.nombre} - {u.email}")

def cargar_conciertos():
    conciertos = crud.listar_eventos()
    nombres_conciertos = [c.nombre_evento for c in conciertos]
    combo_conciertos['values'] = nombres_conciertos
    if nombres_conciertos:
        combo_conciertos.current(0)  # seleccionar el primero por defecto

def comprar_entrada():
    nombre = entry_compra_nombre.get()
    email = entry_compra_email.get()
    cantidad = entry_compra_cantidad.get()
    concierto_nombre = combo_conciertos.get()

    if not nombre or not email or not cantidad or not concierto_nombre:
        messagebox.showerror("Error", "Complete todos los campos para la compra")
        return
    
    try:
        cantidad_int = int(cantidad)
        if cantidad_int <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Cantidad debe ser un número entero positivo")
        return

    try:
        # Opción 1: Si tu crud.crear_compra acepta solo nombre concierto (string)
        crud.crear_compra(nombre, email, concierto_nombre, cantidad_int)
        messagebox.showinfo("Éxito", "Compra registrada")
        # Limpiar campos compra
        entry_compra_nombre.delete(0, tk.END)
        entry_compra_email.delete(0, tk.END)
        entry_compra_cantidad.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Sistema Distribuido de Compra de Entradas")
app.geometry("700x450")

style = Style("flatly")

frame = Frame(app, padding=15)
frame.pack(expand=True, fill="both")

# --- Sección Usuarios ---
Label(frame, text="Agregar Usuario", font=("Helvetica", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,10))

Label(frame, text="Nombre:").grid(row=1, column=0, sticky="e")
entry_nombre = Entry(frame)
entry_nombre.grid(row=1, column=1)

Label(frame, text="Email:").grid(row=2, column=0, sticky="e")
entry_email = Entry(frame)
entry_email.grid(row=2, column=1)

btn_agregar = Button(frame, text="Agregar Usuario", command=agregar_usuario)
btn_agregar.grid(row=3, column=0, columnspan=2, pady=10)

Label(frame, text="Usuarios:", font=("Helvetica", 12, "bold")).grid(row=4, column=0, sticky="w", pady=(10,0))
lista_usuarios = tk.Listbox(frame, height=8, width=40)
lista_usuarios.grid(row=5, column=0, columnspan=2, sticky="w")

listar_usuarios_en_gui()

# --- Sección Compra de Entradas ---
Label(frame, text="Comprar Entradas", font=("Helvetica", 14, "bold")).grid(row=0, column=3, columnspan=2, pady=(0,10), padx=(40,0))

Label(frame, text="Nombre:").grid(row=1, column=3, sticky="e", padx=(40,0))
entry_compra_nombre = Entry(frame)
entry_compra_nombre.grid(row=1, column=4)

Label(frame, text="Email:").grid(row=2, column=3, sticky="e", padx=(40,0))
entry_compra_email = Entry(frame)
entry_compra_email.grid(row=2, column=4)

Label(frame, text="Concierto:").grid(row=3, column=3, sticky="e", padx=(40,0))
combo_conciertos = Combobox(frame, state="readonly")
combo_conciertos.grid(row=3, column=4)

Label(frame, text="Cantidad:").grid(row=4, column=3, sticky="e", padx=(40,0))
entry_compra_cantidad = Entry(frame)
entry_compra_cantidad.grid(row=4, column=4)

btn_comprar = Button(frame, text="Comprar", command=comprar_entrada)
btn_comprar.grid(row=5, column=3, columnspan=2, pady=10, padx=(40,0))

# Cargar conciertos disponibles
cargar_conciertos()

# Iniciar sincronización en segundo plano
threading.Thread(target=sincronizar_datos_periodicamente, daemon=True).start()

app.mainloop()

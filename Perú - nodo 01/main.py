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
            cargar_usuarios_en_combo()  
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
        combo_conciertos.current(0) 

def cargar_usuarios_en_combo():
    usuarios = crud.listar_usuarios()
    opciones = [f"{u.id} - {u.nombre}" for u in usuarios]
    combo_usuarios_compra['values'] = opciones
    if opciones:
        combo_usuarios_compra.current(0)

def comprar_entrada():
    seleccion_usuario = combo_usuarios_compra.get()
    concierto_nombre = combo_conciertos.get()
    cantidad = entry_compra_cantidad.get()

    if not seleccion_usuario or not concierto_nombre or not cantidad:
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
        usuario_id = int(seleccion_usuario.split(" - ")[0])  # obtener id usuario
        eventos = crud.listar_eventos()
        evento_id = None
        for e in eventos:
            if e.nombre_evento == concierto_nombre:
                evento_id = e.id
                break

        if evento_id is None:
            messagebox.showerror("Error", "Evento no encontrado")
            return

        crud.comprar_entradas(usuario_id, evento_id, cantidad_int)
        messagebox.showinfo("Éxito", "Compra registrada")

        # Limpiar campo cantidad
        entry_compra_cantidad.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Configuración ventana principal

app = tk.Tk()
app.title("Sistema Distribuido de Compra de Entradas")
app.geometry("750x450")

titulo = tk.Label(app, text="TeleBoletos - Perú", font=("Helvetica", 20, "bold"), fg="#2c3e50")
titulo.pack(pady=10)

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

Label(frame, text="Usuario:").grid(row=1, column=3, sticky="e", padx=(40,0))
combo_usuarios_compra = Combobox(frame, state="readonly")
combo_usuarios_compra.grid(row=1, column=4)

Label(frame, text="Concierto:").grid(row=2, column=3, sticky="e", padx=(40,0))
combo_conciertos = Combobox(frame, state="readonly")
combo_conciertos.grid(row=2, column=4)

Label(frame, text="Cantidad:").grid(row=3, column=3, sticky="e", padx=(40,0))
entry_compra_cantidad = Entry(frame)
entry_compra_cantidad.grid(row=3, column=4)

btn_comprar = Button(frame, text="Comprar", command=comprar_entrada)
btn_comprar.grid(row=4, column=3, columnspan=2, pady=10, padx=(40,0))

# Cargar datos iniciales
cargar_conciertos()
cargar_usuarios_en_combo()

# Iniciar sincronización en segundo plano (si tienes esa función)
threading.Thread(target=sincronizar_datos_periodicamente, daemon=True).start()

app.mainloop()

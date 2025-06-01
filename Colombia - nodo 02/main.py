import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Entry, Button, Combobox
from tkinter import Text
from services import crud
from tkinter import messagebox
from datetime import datetime
import threading
from sync_manager import sincronizar_datos_periodicamente

def cargar_conciertos():
    conciertos = crud.listar_eventos()
    conciertos_ordenados = sorted(conciertos, key=lambda c: c.fecha_evento)
    combo_visualizar['values'] = [c.nombre_evento for c in conciertos_ordenados]
    combo_visualizar.eventos_disponibles = conciertos_ordenados
    if conciertos_ordenados:
        combo_visualizar.current(0)
        mostrar_estadistica()
    else:
        combo_visualizar.set('')
        text_estadistica.delete("1.0", tk.END)

def crear_concierto():
    try:
        nombre = entry_evento_nombre.get()
        descripcion = entry_evento_descripcion.get()
        fecha = entry_evento_fecha.get()
        lugar = entry_evento_lugar.get()
        precio = float(entry_evento_precio.get())
        aforo = int(entry_evento_aforo.get())

        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()

        crud.crear_evento(nombre, descripcion, fecha_obj, lugar, precio, aforo)
        messagebox.showinfo("Éxito", "Concierto creado")
        cargar_conciertos()

        # Limpiar campos evento
        entry_evento_nombre.delete(0, tk.END)
        entry_evento_descripcion.delete(0, tk.END)
        entry_evento_fecha.delete(0, tk.END)
        entry_evento_lugar.delete(0, tk.END)
        entry_evento_precio.delete(0, tk.END)
        entry_evento_aforo.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def mostrar_estadistica():
    nombre_evento = combo_visualizar.get()
    if not nombre_evento:
        text_estadistica.delete("1.0", tk.END)
        return
    evento = next((e for e in combo_visualizar.eventos_disponibles if e.nombre_evento == nombre_evento), None)
    if not evento:
        text_estadistica.delete("1.0", tk.END)
        return
    
    # Obtener todas las entradas para ese evento y sumar la cantidad
    entradas = crud.listar_entradas_por_evento(evento.id)
    total_entradas = sum(e.cantidad for e in entradas)

    text_estadistica.delete("1.0", tk.END)
    texto = (
        f"Concierto: {evento.nombre_evento}\n"
        f"Fecha: {evento.fecha_evento}\n"
        f"Lugar: {evento.lugar}\n"
        f"Precio: S/. {evento.precio:.2f}\n"
        f"Aforo: {evento.aforo}\n"
        f"\nEntradas vendidas: {total_entradas}"
    )
    text_estadistica.insert(tk.END, texto)

app = tk.Tk()
app.title("TeleBoletos - CENTRAL EVENTOS")
app.geometry("400x700")

titulo = tk.Label(app, text="TeleBoletos - Colombia", font=("Helvetica", 20, "bold"), fg="#2c3e50")
titulo.pack(pady=10)

style = Style("flatly")
frame = Frame(app, padding=15)
frame.pack(expand=True, fill="both")

# TÍTULO
Label(frame, text="TeleBoletos - Colombia", font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 20))

# --- Sección Crear Concierto ---
Label(frame, text="Crear Concierto", font=("Helvetica", 14, "bold")).grid(row=1, column=0, columnspan=2, pady=(0, 10))

Label(frame, text="Nombre:").grid(row=2, column=0, sticky="e")
entry_evento_nombre = Entry(frame)
entry_evento_nombre.grid(row=2, column=1)

Label(frame, text="Descripción:").grid(row=3, column=0, sticky="e")
entry_evento_descripcion = Entry(frame)
entry_evento_descripcion.grid(row=3, column=1)

Label(frame, text="Fecha (YYYY-MM-DD):").grid(row=4, column=0, sticky="e")
entry_evento_fecha = Entry(frame)
entry_evento_fecha.grid(row=4, column=1)

Label(frame, text="Lugar:").grid(row=5, column=0, sticky="e")
entry_evento_lugar = Entry(frame)
entry_evento_lugar.grid(row=5, column=1)

Label(frame, text="Precio:").grid(row=6, column=0, sticky="e")
entry_evento_precio = Entry(frame)
entry_evento_precio.grid(row=6, column=1)

Label(frame, text="Aforo:").grid(row=7, column=0, sticky="e")
entry_evento_aforo = Entry(frame)
entry_evento_aforo.grid(row=7, column=1)

btn_crear_evento = Button(frame, text="Crear Concierto", command=crear_concierto)
btn_crear_evento.grid(row=8, column=0, columnspan=2, pady=15)

# --- Sección Visualizar Concierto ---
Label(frame, text="Visualizar Concierto", font=("Helvetica", 14, "bold")).grid(row=9, column=0, columnspan=2, pady=(20, 10))

Label(frame, text="Selecciona concierto:").grid(row=10, column=0, sticky="e")
combo_visualizar = Combobox(frame, state="readonly")
combo_visualizar.grid(row=10, column=1)
combo_visualizar.bind("<<ComboboxSelected>>", lambda e: mostrar_estadistica())

text_estadistica = Text(frame, width=50, height=10, state="normal")
text_estadistica.grid(row=11, column=0, columnspan=2, pady=(10,0))

# Cargar conciertos actuales
cargar_conciertos()

# Iniciar sincronización en segundo plano
threading.Thread(target=sincronizar_datos_periodicamente, daemon=True).start()

app.mainloop()

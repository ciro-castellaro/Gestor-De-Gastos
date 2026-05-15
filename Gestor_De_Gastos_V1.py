import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk

# ---------- Ventana principal ----------
ventana_principal = tk.Tk()
ventana_principal.geometry("400x250")
ventana_principal.title("Gestor de gastos")

titulo_app = tk.Label(ventana_principal, text="Gestor de gastos", font="Arial, 16")
titulo_app.grid(row="1",column="2",padx="10", pady="10", sticky="s")

label_categoria = tk.Label(ventana_principal, text="Categoría", font="Arial, 16")
label_categoria.grid(row="2",column="1",padx="5", pady="5", sticky="w")

entry_categoria = tk.Entry(ventana_principal)
entry_categoria.grid(row="2",column="2",padx="5", pady="5", sticky="w")

label_monto = tk.Label(ventana_principal, text="Monto", font="Arial, 16")
label_monto.grid(row="3",column="1",padx="5", pady="5", sticky="w")

entry_monto = tk.Entry(ventana_principal)
entry_monto.grid(row="3",column="2",padx="5", pady="5", sticky="w")

# ---------- Función botón ----------
def guardar_datos():
    categoria = entry_categoria.get()
    monto= entry_monto.get()

    if categoria =="" or monto =="": #SI NO HAY CATEGORIA O MONTO = ERROR
        messagebox.showerror("Error inesperado", "No se proporcionó una categoría o monto.")
        return
    
    if "," in monto: #SI HAY "," EN MONTO = ERROR
        messagebox.showerror("Error inesperado", "Solo se puede usar puntos para numeros decimales.")
        return
    
    if monto == 0: #SI EL MONTO ES 0 = ERROR
        messagebox.showerror("Error Inesperado", "El monto no puede ser 0")
        return
    
    try: #SI EL MONTO TIENE LETRAS/ES INVALIDO = ERROR
        monto = float(monto.replace(",", "."))
    except ValueError:
        messagebox.showerror("Error", "Ingresá un número válido (ej: 10.5)")
        return

    #SI ESTÁ CORRECTO SE ANOTA EN EL EXCEL
    nuevo_dato = pd.DataFrame({
    "categoria": [categoria],
    "monto": [float(monto)]
    })

    try:
        df_existente = pd.read_csv("gastos.csv")
        df_total = pd.concat([df_existente, nuevo_dato], ignore_index=True)
    except:
        df_total = nuevo_dato

    #SE MUESTRA QUE EL GASTO FUÉ ANOTADO CORECTAMENTE
    df_total.to_csv("gastos.csv", index=False)

    ventana_ok = tk.Toplevel()
    ventana_ok.geometry("450x100")
    ventana_ok.title("Guardado exitoso")

    tk.Label(
        ventana_ok,
        text="Gasto guardado correctamente",
        font=("Arial", 16)
    ).pack(pady=10)

    tk.Label(
        ventana_ok,
        text="Puede cerrar esta ventana",
        font=("Arial", 16)
    ).pack(pady=10)

    entry_categoria.delete(0, tk.END)
    entry_monto.delete(0, tk.END)

# ---------- Botón de guardado ----------
boton_guardar = tk.Button(ventana_principal, text= "Guardar gasto", font=("Arial", 16), command=guardar_datos)
boton_guardar.grid(row="4",column="2",padx="5", pady="5", sticky="s")

def ver_gastos():
    try:
        df = pd.read_csv("gastos.csv")
    except FileNotFoundError:
        messagebox.showerror("Sin datos", "Todavía no hay gastos registrados.")
        return
 
    if df.empty:
        messagebox.showerror("Sin datos", "El archivo de gastos está vacío.")
        return
 
    ventana_gastos = tk.Toplevel()
    ventana_gastos.title("Revisión de gastos")
    ventana_gastos.geometry("450x400")
    ventana_gastos.resizable(True, True)
 
    # --- Título ---
    tk.Label(ventana_gastos, text="Gastos registrados", font=("Arial", 16, "bold")).pack(pady=(10, 5))
 
    # --- Frame con scrollbar para la tabla ---
    frame_tabla = tk.Frame(ventana_gastos)
    frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)
 
    scrollbar_y = tk.Scrollbar(frame_tabla, orient="vertical")
    scrollbar_y.pack(side="right", fill="y")
 
    scrollbar_x = tk.Scrollbar(frame_tabla, orient="horizontal")
    scrollbar_x.pack(side="bottom", fill="x")
 
    tabla = ttk.Treeview(
        frame_tabla,
        columns=list(df.columns),
        show="headings",
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )
 
    scrollbar_y.config(command=tabla.yview)
    scrollbar_x.config(command=tabla.xview)
 
    # --- Encabezados y columnas ---
    for col in df.columns:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, anchor="center", width=150)
 
    # --- Filas ---
    for _, fila in df.iterrows():
        valores = []
        for col in df.columns:
            if col == "monto":
                valores.append(f"${fila[col]:,.2f}")
            else:
                valores.append(fila[col])
        tabla.insert("", "end", values=valores)
 
    tabla.pack(fill="both", expand=True)
 
    # --- Total ---
    total = df["monto"].sum()
    frame_total = tk.Frame(ventana_gastos)
    frame_total.pack(fill="x", padx=10, pady=10)
 
    tk.Label(
        frame_total,
        text=f"Total de gastos:  ${total:,.2f}",
        font=("Arial", 14, "bold"),
        anchor="e"
    ).pack(side="right")

# ---------- Botón de revisar gastos ----------
boton_revision_gastos = tk.Button(ventana_principal, text="Revisar Gastos", font=("Arial", 16), command=ver_gastos)
boton_revision_gastos.grid(row="5", column="2", padx="5", pady="5", sticky="s")

ventana_principal.mainloop()
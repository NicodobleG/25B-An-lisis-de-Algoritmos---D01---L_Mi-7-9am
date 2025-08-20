import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# --- Algoritmos de búsqueda ---
def busqueda_lineal(lista, valor):
    inicio = time.perf_counter()
    for i, num in enumerate(lista):
        if num == valor:
            fin = time.perf_counter()
            return i, (fin - inicio) * 1000
    fin = time.perf_counter()
    return -1, (fin - inicio) * 1000

def busqueda_binaria(lista, valor):
    lista = np.sort(lista)
    inicio = time.perf_counter()
    izq, der = 0, len(lista) - 1
    while izq <= der:
        medio = (izq + der) // 2
        if lista[medio] == valor:
            fin = time.perf_counter()
            return medio, (fin - inicio) * 1000
        elif lista[medio] < valor:
            izq = medio + 1
        else:
            der = medio - 1
    fin = time.perf_counter()
    return -1, (fin - inicio) * 1000

# --- Experimentos y resultados ---
def promedio_tiempo(algoritmo, lista, valor, rep=5):
    tiempos = []
    for _ in range(rep):
        _, t = algoritmo(lista, valor)
        tiempos.append(t)
    return np.mean(tiempos)

# --- GUI ---
def generar_lista():
    valor = entrada.get().strip()
    if valor.isdigit() and int(valor) > 0:
        n = int(valor)
        lista[:] = np.random.randint(0, n, size=n)  # sobrescribimos lista global
        lblInfo.config(fg="green", text=f"Lista de {n} elementos generada")
    else:
        lblInfo.config(fg="red", text="Dato inválido")

def ejecutar_busqueda(tipo):
    if len(lista) == 0:
        lblInfo.config(fg="red", text="Primero genera una lista")
        return

    try:
        valor = int(entradaBuscar.get().strip())
    except:
        lblInfo.config(fg="red", text="Ingrese un número válido")
        return

    if tipo == "lineal":
        idx, t = busqueda_lineal(lista, valor)
    else:
        idx, t = busqueda_binaria(lista, valor)

    if idx != -1:
        lblInfo.config(fg="black", 
            text=f"Búsqueda {tipo}:\nLista: {len(lista)} elementos\n"
                 f"Encontrado en índice {idx}\nTiempo: {t:.6f} ms")
    else:
        lblInfo.config(fg="black", 
            text=f"Búsqueda {tipo}:\nLista: {len(lista)} elementos\n"
                 f"No encontrado\nTiempo: {t:.6f} ms")

    # Guardar datos para graficar
    if len(lista) not in resultados:
        resultados[len(lista)] = {"lineal": [], "binaria": []}
    resultados[len(lista)][tipo].append(t)

def mostrar_grafica():
    if not resultados:
        lblInfo.config(fg="red", text="No hay datos para graficar")
        return

    magnitudes = sorted(resultados.keys())
    tiempos_lineal = [np.mean(resultados[n]["lineal"]) for n in magnitudes]
    tiempos_binaria = [np.mean(resultados[n]["binaria"]) for n in magnitudes]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(magnitudes, tiempos_lineal, marker="o", color="blue", label="Lineal")
    ax.plot(magnitudes, tiempos_binaria, marker="s", color="red", label="Binaria")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Tamaño de lista")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_title("Comparación de búsquedas")
    ax.legend()
    ax.grid(True)

    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(pady=15)
    canvas.draw()

def limpiar():
    resultados.clear()
    lblInfo.config(fg="dark green", text="Datos limpiados")
    global canvas
    if canvas:
        canvas.get_tk_widget().destroy()
        canvas = None

# --- Programa principal ---
root = tk.Tk()
root.title("Búsquedas - GUI simplificada")
root.geometry("800x700")

lista = []           # lista de datos generados
resultados = {}      # para graficar
canvas = None

# Widgets
tk.Label(root, text="Cantidad de datos a generar").pack(pady=5)
entrada = tk.Entry(root, bg="light goldenrod")
entrada.pack(pady=5)
tk.Button(root, text="Generar", command=generar_lista, bg="pale green").pack(pady=5)

tk.Label(root, text="Valor a buscar").pack(pady=5)
entradaBuscar = tk.Entry(root, bg="light goldenrod")
entradaBuscar.pack(pady=5)

frame_busqueda = tk.Frame(root)
frame_busqueda.pack(pady=5)
tk.Button(frame_busqueda, text="Lineal", command=lambda: ejecutar_busqueda("lineal"), bg="cornflower blue").pack(side="left", padx=5)
tk.Button(frame_busqueda, text="Binaria", command=lambda: ejecutar_busqueda("binaria"), bg="salmon1").pack(side="left", padx=5)

lblInfo = tk.Label(root, text="", justify="left")
lblInfo.pack(pady=10)

frame_graf = tk.Frame(root)
frame_graf.pack(pady=5)
tk.Button(frame_graf, text="Gráfica", command=mostrar_grafica, bg="pale green").pack(side="left", padx=5)
tk.Button(frame_graf, text="Limpiar", command=limpiar, bg="aquamarine").pack(side="left", padx=5)

root.mainloop()

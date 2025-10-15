import tkinter as tk
import time
import tracemalloc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------------------------------------------
# Algoritmos trabajados
# ---------------------------------------------------------
def Fibonacci(n):  # Sin programación dinámica (recursivo)
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return Fibonacci(n-1) + Fibonacci(n-2)

def Fibonacci_DP(n):  # Con programación dinámica
    if n == 0 or n == 1:
        return 1
    ultimo_valor = 0
    valor_actual = 1
    for i in range(n-1):
        valor_auxiliar = valor_actual
        valor_actual += ultimo_valor
        ultimo_valor = valor_auxiliar
    return valor_actual

# ---------------------------------------------------------
# Funciones de medición
# ---------------------------------------------------------
def medir_tiempo(algoritmo, n):
    inicio = time.perf_counter()
    algoritmo(n)
    fin = time.perf_counter()
    return fin - inicio

def medir_memoria(algoritmo, n):
    tracemalloc.start()
    algoritmo(n)
    mem_actual, mem_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return mem_pico / 1024  # En KB

# ---------------------------------------------------------
# Funciones de interfaz
# ---------------------------------------------------------
def actualizar_Resultado(modo):
    try:
        n = int(entrada.get())
        if modo == "normal":
            resultado = Fibonacci(n)
            lblInfo.config(text=f"Fibonacci normal de {n}: {resultado}")
        elif modo == "dp":
            resultado = Fibonacci_DP(n)
            lblInfoPD.config(text=f"Fibonacci con P. Dinámica de {n}: {resultado}")
    except ValueError:
        lblInfo.config(text="Valor inválido, inténtelo de nuevo.")

# ---------------------------------------------------------
# Gráfica de complejidad temporal
# ---------------------------------------------------------
def generar_grafica_tiempo():
    valores_n = list(range(1, 31))
    tiempos_normal = []
    tiempos_dp = []

    for n in valores_n: # Calculamos y guardamos los resultados obtenidos
        tiempos_normal.append(medir_tiempo(Fibonacci, n) * 1000)
        tiempos_dp.append(medir_tiempo(Fibonacci_DP, n) * 1000)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(valores_n, tiempos_normal, label="Fibonacci Recursivo (O(2ⁿ))", marker='o')
    ax.plot(valores_n, tiempos_dp, label="Fibonacci con P. Dinámica (O(n))", marker='s')
    ax.set_xlabel("Valor de n")
    ax.set_ylabel("Tiempo (ms)")
    ax.set_title("Comparación de complejidad temporal")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=5, side = "left")

# ---------------------------------------------------------
# Gráfica de complejidad espacial
# ---------------------------------------------------------
def generar_grafica_memoria():
    valores_n = list(range(1, 31))
    mem_normal = []
    mem_dp = []

    for n in valores_n: # Calculamos y guardamos los resultados obtenidos
        mem_normal.append(medir_memoria(Fibonacci, n))
        mem_dp.append(medir_memoria(Fibonacci_DP, n))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(valores_n, mem_normal, label="Fibonacci Recursivo (O(n))", marker='o')
    ax.plot(valores_n, mem_dp, label="Fibonacci con P. Dinámica (O(1))", marker='s')
    ax.set_xlabel("Valor de n")
    ax.set_ylabel("Memoria máxima usada (KB)")
    ax.set_title("Comparación de complejidad espacial")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=5, side = "right")

# ---------------------------------------------------------
# Interfaz Tkinter
# ---------------------------------------------------------
root = tk.Tk()
root.title("Participación - Complejidad temporal y espacial (Fibonacci)")
anchura_pantalla = root.winfo_screenwidth()
altura_pantalla = root.winfo_screenheight()
root.geometry(f"{anchura_pantalla}x{altura_pantalla}")

tk.Label(root, text="Ingrese número al cual aplicar Fibonacci:").pack(pady=5)
entrada = tk.Entry(root, bg="Light goldenrod")
entrada.pack(pady=5)

tk.Button(root, text="Calcular (Normal)", command=lambda: actualizar_Resultado("normal")).pack(pady=5)
tk.Button(root, text="Calcular (PD)", command=lambda: actualizar_Resultado("dp")).pack(pady=5)
tk.Button(root, text="Mostrar gráfica de TIEMPO", command=generar_grafica_tiempo, bg="lightblue").pack(pady=5)
tk.Button(root, text="Mostrar gráfica de MEMORIA", command=generar_grafica_memoria, bg="lightgreen").pack(pady=5)
tk.Button(root, text="Salir", command=root.destroy, bg="pink").pack(pady=5)
lblInfo = tk.Label(root, text=f"Resultado recursivo: ", justify="left")
lblInfo.pack(pady=5)
lblInfoPD = tk.Label(root, text=f"Resultado PD: ", justify="left")
lblInfoPD.pack(pady=0)

root.mainloop()

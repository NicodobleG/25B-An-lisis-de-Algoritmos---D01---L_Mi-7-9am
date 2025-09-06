import tkinter as tk
import random
import time
from typing import final
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------------------
# Parámetros generales
# ---------------------------
ANCHO = 1200
ALTO = 350
N_BARRAS = 30
VAL_MIN, VAL_MAX = 5, 100
RETARDO_MS = 40  # velocidad en milisegundos

# Elementos para la gráfica
TIEMPOS = {
    "Selection Sort": {},
    "Bubble Sort": {},
    "Merge Sort": {},
    "Quick Sort": {}
}


# ---------------------------
# Algoritmo: Selection Sort
# ---------------------------
def selection_sort_steps(data, draw_callback):
    """
    Selection Sort paso a paso.
    - data: lista (se modifica in-place)
    - draw_callback: función que redibuja el Canvas y puede resaltar índices
    """
    n = len(data)
    inicio = time.perf_counter()
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            draw_callback(activos=[i, j, min_idx])
            yield
            if data[j] < data[min_idx]:
                min_idx = j
        # Intercambio
        data[i], data[min_idx] = data[min_idx], data[i]
        draw_callback(activos=[i, min_idx])
        yield
    draw_callback(activos=[])
    fin = time.perf_counter()
    if RETARDO_MS <= 1:
        tiempo_ms = (fin - inicio) * 1000
    else:
        tiempo_ms = ((fin - inicio) * 1000)/RETARDO_MS
    TIEMPOS["Selection Sort"][N_BARRAS] = tiempo_ms


def bubble_sort_steps(data, draw_callback):
    """Esta función ordenara el vector que le pases como argumento con el Método de Bubble Sort"""
    n = 0  # Establecemos un contador del largo del vector
    inicio = time.perf_counter()
    for _ in data:
        n += 1  # Contamos la cantidad de caracteres dentro del vector

    for i in range(n - 1):
        # Le damos un rango n para que complete el proceso.
        for j in range(0, n - i - 1):
            # Revisa la matriz de 0 hasta n-i-1
            draw_callback(activos=[i, j])
            yield
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
            draw_callback(activos=[i, j + 1, j])
            yield
            # Se intercambian si el elemento encontrado es mayor
            # Luego pasa al siguiente

    # print("El vector ordenado es: ", data)
    draw_callback(activos=[])
    yield
    fin = time.perf_counter()
    if RETARDO_MS <= 1:
        tiempo_ms = (fin - inicio) * 1000
    else:
        tiempo_ms = ((fin - inicio) * 1000) / RETARDO_MS
    TIEMPOS["Bubble Sort"][N_BARRAS] = tiempo_ms

def merge_sort_steps(data, draw_callback):
    inicio = time.perf_counter()
    def merge(data):

        def largo(vec):
            largovec = 0  # Establecemos un contador del largovec
            for _ in vec:
                largovec += 1  # Obtenemos el largo del vector
            return largovec

        if largo(data) > 1:
            medio = largo(data) // 2  # Buscamos el medio del vector

            # Lo dividimos en 2 partes
            izq = data[:medio]
            der = data[medio:]

            yield from merge(izq)  # Mismo procedimiento a la primer mitad
            yield from merge(der)  # Mismo procedimiento a la segunda mitad

            i = j = k = 0

            # Copiamos los datos a los vectores temporales izq[] y der[]
            while i < largo(izq) and j < largo(der):
                draw_callback(activos=[i, j, k])
                yield
                if izq[i] < der[j]:
                    data[k] = izq[i]
                    draw_callback(activos=[i, k, j])
                    yield
                    i += 1
                else:
                    data[k] = der[j]
                    draw_callback(activos=[k, j, i])
                    yield
                    j += 1
                k += 1

            # Nos fijamos si quedaron elementos en la lista
            # tanto derecha como izquierda
            while i < largo(izq):
                data[k] = izq[i]
                draw_callback(activos=[k, i])
                yield
                i += 1
                k += 1

            while j < largo(der):
                data[k] = der[j]
                draw_callback(activos=[k, j])
                yield
                j += 1
                k += 1

    yield from merge(data)
    draw_callback(activos=[])
    yield

    fin = time.perf_counter()
    if RETARDO_MS <= 1:
        tiempo_ms = (fin - inicio) * 1000
    else:
        tiempo_ms = ((fin - inicio) * 1000) / RETARDO_MS
    TIEMPOS["Merge Sort"][N_BARRAS] = tiempo_ms


def quick_sort_steps(data, draw_callback, start=0, end=None):
    """Esta función ordenara el vector que le pases como argumento
    con el Método Quick Sort"""
    inicio = time.perf_counter()
    if end is None:
        end = len(data) - 1

    # Imprimimos la lista obtenida al principio (Desordenada)
    # print("El vector a ordenar con quick es:", data)

    def quick(data, start=0, end=len(data) - 1):

        if start >= end:
            return

        def particion(data, start=0, end=len(data) - 1):
            pivot = data[start]
            menor = start + 1
            mayor = end

            while True:
                # Si el valor actual es mayor que el pivot
                # está en el lugar correcto (lado derecho del pivot) y podemos
                # movernos hacia la izquierda, al siguiente elemento.
                # También debemos asegurarnos de no haber superado el puntero bajo, ya que indica
                # que ya hemos movido todos los elementos a su lado correcto del pivot

                while menor <= mayor and data[mayor] >= pivot:
                    mayor = mayor - 1

                # Proceso opuesto al anterior
                while menor <= mayor and data[menor] <= pivot:
                    menor = menor + 1

                # Encontramos un valor sea mayor o menor y que este fuera del arreglo
                # ó menor es más grande que mayor, en cuyo caso salimos del ciclo
                if menor <= mayor:
                    data[menor], data[mayor] = data[mayor], data[menor]
                    # Continua el bucle
                else:
                    # Salimos del bucle
                    break

            data[start], data[mayor] = data[mayor], data[start]

            return mayor

        p = particion(data, start, end)
        draw_callback(activos=[start, end, p])
        yield

        yield from quick(data, start, p - 1)
        yield from quick(data, p + 1, end)

    yield from quick(data, start, end)
    draw_callback(activos=[])
    # print("El vector ordenado con quick es:", data)
    fin = time.perf_counter()
    if RETARDO_MS <= 1:
        tiempo_ms = (fin - inicio) * 1000
    else:
        tiempo_ms = ((fin - inicio) * 1000) / RETARDO_MS
    TIEMPOS["Quick Sort"][N_BARRAS] = tiempo_ms

# ---------------------------
# Función de dibujo (énfasis)
# ---------------------------
def dibujar_barras(canvas, datos, activos=None):
    canvas.delete("all")
    if not datos:
        return
    n = len(datos)
    margen = 10
    ancho_disp = ANCHO - 2 * margen
    alto_disp = ALTO - 2 * margen
    w = ancho_disp / n
    esc = alto_disp / max(datos)

    for i, v in enumerate(datos):
        x0 = margen + i * w
        x1 = x0 + w * 0.9
        h = v * esc
        y0 = ALTO - margen - h
        y1 = ALTO - margen

        color = "#4e79a7"  # azul normal
        if activos and i in activos:
            color = "#f28e2b"  # naranja para comparaciones/intercambios
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    canvas.create_text(6, 6, anchor="nw", text=f"n={len(datos)}", fill="#666")


# ---------------------------
# Aplicación principal
# ---------------------------
datos = []
root = tk.Tk()
root.title("Visualizador sencillo - Algoritmos de ordenamiento")

canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="white")
canvas.pack(padx=10, pady=10)


def generar():
    """Genera lista de números aleatorios y dibuja."""
    global datos, copiaDatos
    random.seed(time.time())
    datos = [random.randint(VAL_MIN, VAL_MAX) for _ in range(N_BARRAS)]
    copiaDatos = datos.copy()
    dibujar_barras(canvas, datos)

def cambiar_numero_de_barras():
    global N_BARRAS
    valor = entrada.get().strip()
    if valor.isdigit() and int(valor) > 0:
        N_BARRAS = int(valor)
        lblInfo.config(fg="green", text="Barras actualizadas")
    else:
        lblInfo.config(fg="red", text="Dato inválido")

def ordenar_selection():
    """Ejecuta la animación del Selection Sort usando un generador + after()."""
    if not datos:
        return
    gen = selection_sort_steps(datos, lambda activos=None: dibujar_barras(canvas, datos, activos))

    def paso():
        try:
            next(gen)  # avanza un paso del algoritmo
            root.after(RETARDO_MS, paso)  # agenda el siguiente paso
        except StopIteration:
            pass  # terminó

    paso()

def ordenar_bubble():
    if not datos:
        return
    gen = bubble_sort_steps(datos, lambda activos=None: dibujar_barras(canvas, datos, activos))

    def paso():
        try:
            next(gen)
            root.after(RETARDO_MS, paso)
        except StopIteration:
            pass

    paso()

def ordenar_merge():
    if not datos:
        return
    gen = merge_sort_steps(datos, lambda activos=None: dibujar_barras(canvas, datos, activos))

    def paso():
        try:
            next(gen)
            root.after(RETARDO_MS, paso)
        except StopIteration:
            pass

    paso()

def ordenar_quick():
    if not datos:
        return
    gen = quick_sort_steps(datos, lambda activos=None: dibujar_barras(canvas, datos, activos), 0, None, )

    def paso():
        try:
            next(gen)
            root.after(RETARDO_MS, paso)
        except StopIteration:
            pass
    paso()

def graficar_tiempos():
    if not any(TIEMPOS.values()):
        return

    #Limpiar frame para evitar solapamiento
    for widget in frame_graf.winfo_children():
        widget.destroy()

    fig = plt.figure(figsize = (8, 4), dpi=100)
    ax = fig.add_subplot(111)

    for i, tiempos in TIEMPOS.items():
        if tiempos: # Solo si hay datos
            tam = sorted(tiempos.keys())
            valores = [tiempos[n] for n in tam]
            ax.plot(tam, valores, marker="o", label=i)

    ax.set_xlabel("Tamaño de la lista")
    ax.set_ylabel("Tiempo promedio (ms)")
    ax.set_title("Comparación de algoritmos de ordenamiento")
    ax.legend()
    ax.grid(True)

    # Incrustar en Tkinter
    graf_canvas = FigureCanvasTkAgg(fig, master=frame_graf)
    graf_canvas.draw()
    graf_canvas.get_tk_widget().pack()



# ---------------------------
# Botones (UI mínima)
# ---------------------------
panel = tk.Frame(root)
panel.pack(pady=6)

tk.Button(panel, text="Cambiar No. Barras", command=cambiar_numero_de_barras).pack(side="left", padx=5)
entrada = tk.Entry(panel, bg="light goldenrod")
entrada.pack(padx=5, side="left")
lblInfo = tk.Label(panel, text="")
lblInfo.pack(padx=5, side="left")

tk.Button(panel, text="Generar", command=generar).pack(side="left", padx=5)

# Dropdown para seleccionar algoritmo
algoritmos = {
    "Selection Sort": ordenar_selection,
    "Bubble Sort": ordenar_bubble,
    "Merge Sort": ordenar_merge,
    "Quick Sort": ordenar_quick
}

algoritmo_var = tk.StringVar(value="Selection Sort")
tk.Label(panel, text="Algoritmo:").pack(side="left", padx=5)
tk.OptionMenu(panel, algoritmo_var, *algoritmos.keys()).pack(side="left", padx=5)


# Botón único para ordenar
def ordenar():
    func = algoritmos.get(algoritmo_var.get())
    if func:
        func()


tk.Button(panel, text="Ordenar", command=ordenar).pack(side="left", padx=5)


def limpiarRes():
    global datos
    datos = copiaDatos.copy()
    dibujar_barras(canvas, datos)


tk.Button(panel, text="Limpiar Resultado", command=limpiarRes).pack(side="left", padx=5)
tk.Button(panel, text="Graficar Tiempos", command=graficar_tiempos).pack(side="left", padx=5)

def mezclar():
    """Mezcla la lista de números aleatorios y dibuja."""
    global datos, copiaDatos
    random.shuffle(datos)
    copiaDatos = datos.copy()
    dibujar_barras(canvas, datos)


tk.Button(panel, text="Mezclar", command=mezclar).pack(side="left", padx=5)

tk.Scale(panel, from_=0, to=200, label="Velocidad (ms)", orient="horizontal",
         variable=tk.IntVar(value=RETARDO_MS),
         command=lambda v: globals().update(RETARDO_MS=int(v))
         ).pack(side="left", padx=5)

#Gráfica

frame_graf = tk.Frame(root)
frame_graf.pack(pady=3)

# ---------------------------
# Estado inicial
# ---------------------------
#generar()  # crea y dibuja datos al abrir

root.mainloop()  # inicia la app
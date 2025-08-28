import tkinter as tk
import matplotlib.pyplot as plt
import time
from random import sample

# --- Variables globales ---
listaDatos = None
tamanios = []
tiempos_bubble = []
tiempos_merge = []
tiempos_quick = []

# --- Algoritmos de búsqueda ---
def bubble_sort(vector):
    vector = vector.copy()  # evitar modificar la original
    n = len(vector)
    inicio = time.perf_counter()
    for i in range(n-1):
        for j in range(0, n-i-1):
            if vector[j] > vector[j+1]:
                vector[j], vector[j+1] = vector[j+1], vector[j]
    fin = time.perf_counter()
    return vector, (fin - inicio) * 1000  # milisegundos

def merge_sort(lista):
    vec = lista.copy()  # No modificamos la original

    def merge(v):
        if len(v) > 1:
            medio = len(v)//2
            izq = v[:medio]
            der = v[medio:]

            merge(izq)
            merge(der)

            i = j = k = 0
            while i < len(izq) and j < len(der):
                if izq[i] < der[j]:
                    v[k] = izq[i]
                    i += 1
                else:
                    v[k] = der[j]
                    j += 1
                k += 1

            while i < len(izq):
                v[k] = izq[i]
                i += 1
                k += 1
            while j < len(der):
                v[k] = der[j]
                j += 1
                k += 1

    inicio = time.perf_counter()
    merge(vec)
    fin = time.perf_counter()
    return vec, (fin - inicio) * 1000  # milisegundos

def quick_sort(lista):
    vec = lista.copy()  # No modificamos la original

    def quick(v, start=0, end=None):
        if end is None:
            end = len(v) - 1
        if start >= end:
            return

        def particion(v, start, end):
            pivot = v[start]
            menor = start + 1
            mayor = end

            while True:
                while menor <= mayor and v[mayor] >= pivot:
                    mayor -= 1
                while menor <= mayor and v[menor] <= pivot:
                    menor += 1
                if menor <= mayor:
                    v[menor], v[mayor] = v[mayor], v[menor]
                else:
                    break

            v[start], v[mayor] = v[mayor], v[start]
            return mayor

        p = particion(v, start, end)
        quick(v, start, p-1)
        quick(v, p+1, end)

    inicio = time.perf_counter()
    quick(vec)
    fin = time.perf_counter()
    return vec, (fin - inicio) * 1000  # milisegundos

# --- GUI ---
def generar_lista(N):
    try:
        N = int(N)
        if N <= 0:
            raise ValueError
        listaDatos = sample(range(N*10), N)  # Generamos una lista con base en el valor definido en N
        lblInfo.config(fg="green", text=f"Lista de {N} elementos generada")
        return listaDatos
    except:
        lblInfo.config(fg="red", text="Ingrese un número válido")
        return None

def generar_y_ordenar(): #Genera, ordena, y guarda en las listas globales los valores necesarios para la actividad: tamaños y tiempos
    global listaDatos, tamanios, tiempos_bubble, tiempos_merge, tiempos_quick

    try:
        N = int(entrada.get())
        if N <= 0:
            raise ValueError
    except:
        lblInfo.config(fg="red", text="Ingrese un número válido")
        return

    # Generamos la lista a comparar
    listaDatos = generar_lista(N)

    # La copiamos para que cada algoritmo trate la misma lista para comparar
    vec_bubble = listaDatos.copy()
    vec_merge = listaDatos.copy()
    vec_quick = listaDatos.copy()

    # Ejecutamos algoritmos y medimos tiempos
    _, t_b = bubble_sort(vec_bubble)
    _, t_m = merge_sort(vec_merge)
    _, t_q = quick_sort(vec_quick)
    
    # Guardamos los valores obtenidos en los arreglos globales
    tamanios.append(N)
    tiempos_bubble.append(t_b)
    tiempos_merge.append(t_m)
    tiempos_quick.append(t_q)

def generar_y_ordenar_preset(): #Genera, ordena una cantidad de datos predeterminada
    global listaDatos, tamanios, tiempos_bubble, tiempos_merge, tiempos_quick
    
    # Nos aseguramos de resetear los valores globales para evitar conflictos
    tamanios = []
    tiempos_bubble = []
    tiempos_merge = []
    tiempos_quick = []
    N = 50

    # Bucle para llegar de 50 en 50 a 1000
    for i in range(20):
       # Generamos la lista a comparar
        listaDatos = generar_lista(N) 

        # La copiamos para que cada algoritmo trate la misma lista para comparar
        vec_bubble = listaDatos.copy()
        vec_merge = listaDatos.copy()
        vec_quick = listaDatos.copy()

        # Ejecutamos algoritmos y medimos tiempos
        _, t_b = bubble_sort(vec_bubble)
        _, t_m = merge_sort(vec_merge)
        _, t_q = quick_sort(vec_quick)

        # Guardamos los valores obtenidos en los arreglos globales
        tamanios.append(N)
        tiempos_bubble.append(t_b)
        tiempos_merge.append(t_m)
        tiempos_quick.append(t_q)

        N+=50

def graficar_tiempos():
    global tamanios, tiempos_bubble, tiempos_merge, tiempos_quick
    plt.figure(figsize=(10,6))
    plt.plot(tamanios, tiempos_bubble, marker="o", label="Bubble Sort")
    plt.plot(tamanios, tiempos_merge, marker="s", label="Merge Sort")
    plt.plot(tamanios, tiempos_quick, marker="^", label="Quick Sort")
    
    plt.xlabel("Tamaño de la lista")
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Comparación de algoritmos de ordenamiento")
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Ventana ---
root = tk.Tk()
root.title("Participación - Complejidad Temporal")
root.geometry("600x300")

# --- Generamos manualmente los valores ---
tk.Label(root, text="Cantidad de datos a generar").pack(pady=5)
entrada = tk.Entry(root, bg="light goldenrod")
entrada.pack(pady=5)
tk.Button(root, text="Generar y ordenar", command=generar_y_ordenar, bg="pale green").pack(pady=5)

# --- Generamos una cantidad de valores predeterminada ---
tk.Label(root, text="Generar valores de 50 hasta 1000 con incrementos de 50").pack(pady=5)
entrada.pack(pady=5)
tk.Button(root, text="Generar y ordenar", command=generar_y_ordenar_preset, bg="pale green").pack(pady=5)

lblInfo = tk.Label(root, text="", justify="left")
lblInfo.pack(pady=10)

frame_graf = tk.Frame(root)
frame_graf.pack(pady=5)
tk.Button(frame_graf, text="Gráficar resultados", command=graficar_tiempos, bg="pale green").pack(side="left", padx=5)

root.mainloop()

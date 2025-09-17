import tkinter as tk
import random
import math

root = tk.Tk()
root.title("Visualizador sencillo - Puntos cercanos")

# ---------------------------
# Entradas para 5 puntos
# ---------------------------
tk.Label(root, text="Puntos").grid(row=0, column=0)
tk.Label(root, text="X").grid(row=0, column=1)
tk.Label(root, text="Y").grid(row=0, column=2)

entries = []  # guardará (entry_x, entry_y)
for i in range(5): # función que abre posibilidad a expandir la cantidad de coordenadas ingresadas
    tk.Label(root, text=f"P{i+1}:").grid(row=i+1, column=0, padx=5, pady=5)
    ex = tk.Entry(root, width=10)
    ex.grid(row=i+1, column=1, padx=5)
    ey = tk.Entry(root, width=10)
    ey.grid(row=i+1, column=2, padx=5)
    entries.append((ex, ey))

# ---------------------------
# Funciones
# ---------------------------
def distancia(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def calcular():
    puntos = []
    for ex, ey in entries: # cada _for ex, ey in entries_ recorre todas las entradas del grid
        try:
            x = float(ex.get())
            y = float(ey.get())
            puntos.append((x, y))
        except ValueError:
            pass  # ignora si está vacío

    if len(puntos) < 2:
        print("Necesitas al menos 2 puntos válidos")
        return

    min_dist = float("inf") # tenemos un valor de comparación muy grande, para que jale el for de abajo así chido
    mejor = None
    for i in range(len(puntos)): # for anidado para comparar los puntos de uno por uno
        for j in range(i+1, len(puntos)): # for para recorrer los puntos de uno por uno exceptuando el anterior
            print("Puntos: "f"{puntos[i]} y {puntos[j]}") # Depuración
            d = distancia(puntos[i], puntos[j])
            if d < min_dist:
                min_dist = d
                mejor = (puntos[i], puntos[j])

    print("Los puntos más cercanos son:", mejor, "con una distancia de", min_dist) # Depuración
    P1.config(text = str(mejor[0]))
    P2.config(text = str(mejor[1]))
    Dist.config(text = str(min_dist))

def llenar_random():
    for ex, ey in entries: # cada _for ex, ey in entries_ recorre todas las entradas del grid
        ex.delete(0, tk.END)
        ey.delete(0, tk.END)
        ex.insert(0, random.randint(0, 40))
        ey.insert(0, random.randint(0, 40))

def limpiar():
    for ex, ey in entries: # cada _for ex, ey in entries_ recorre todas las entradas del grid
        ex.delete(0, tk.END)
        ey.delete(0, tk.END)


# ---------------------------
# Resultado
# ---------------------------

tk.Label(root, text = "Resultado").grid(row = 6, column = 1, padx = 5, pady = 5)
tk.Label(root, text = "Punto 1: ").grid(row = 7, column = 0, padx = 5, pady = 5)
tk.Label(root, text = "Punto 2: ").grid(row = 8, column = 0, padx = 5, pady = 5)
tk.Label(root, text = "Distancia: ").grid(row = 9, column = 0, padx = 5, pady = 5)
P1 = tk.Label(root, text="")
P1.grid(row=7, column=1, padx=5, pady=5)
P2 = tk.Label(root, text="")
P2.grid(row=8, column=1, padx=5, pady=5)
Dist = tk.Label(root, text="")
Dist.grid(row=9, column=1, padx=5, pady=5)


# ---------------------------
# Botones
# ---------------------------
tk.Button(root, text="Calcular", bg="lightgreen", command=calcular).grid(row=1, column=3, padx=10)
tk.Button(root, text="Llenar random", bg="lightblue", command=llenar_random).grid(row=3, column=3, padx=10)
tk.Button(root, text="Limpiar", bg="lightpink", command=limpiar).grid(row=5, column=3, padx=10)

root.mainloop()

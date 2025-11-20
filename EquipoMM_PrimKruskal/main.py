import heapq
import tkinter as tk
from tkinter import ttk
import math
import time

#Ventana
ventana = tk.Tk()
ventana.title("Algoritmos voraces: PRIM & KRUSKAL")
ventana.geometry("600x720")

"""--- Grafo utilizado --- obtenido de: https://es.scribd.com/document/403078422/Algoritmo-PRIM, primer página"""

grafo = [[] for _ in range(9)]
grafo[0] = [(1, 4), (7, 9)]
grafo[1] = [(0, 4), (2, 9), (7, 11)]
grafo[2] = [(1, 9), (3, 7), (5, 4), (8, 2)]
grafo[3] = [(2, 7), (4, 10), (5, 15)]
grafo[4] = [(3, 10), (5, 11)]
grafo[5] = [(2, 4), (3, 15), (4, 11), (6, 2)]
grafo[6] = [(5, 2), (7, 1), (8, 6)]
grafo[7] = [(0, 9), (1, 11), (6, 1), (8, 7)]
grafo[8] = [(2, 2), (6, 6), (7, 7)]

"""########################## Inicio PRIM ##########################"""



"""########################## Fin PRIM ##########################"""

"""######################## Inicio KRUSKAL ########################"""
# Kruskal algorithm
class kruskalAlg:
    #Inicializar la clase obtiniendo el grafo
    def __init__(self, grafo):
        self.grafo = grafo
        self.parent = []
        self.rango = []

    #Encontrar el ancestro o "padre" de un nodo dentro del arbol
    def find(self, nodo):
        if self.parent[nodo] != nodo:
            self.parent[nodo] = self.find(self.parent[nodo])
            return self.parent[nodo]
        return self.parent[nodo] #Si solo es un nodo (no tiene padre) retorna a si mismo

    def union(self, nodo1, nodo2):#Enlazar dos nodos
        xroot = self.find(nodo1)
        yroot = self.find(nodo2)

        if xroot != yroot: #Que no tengan el mismo nodo padre(evitar que se genere un ciclo)
            #asignar segun sea el rango, el mayor sera el padre
            if self.rango[xroot] > self.rango[yroot]:
                self.parent[yroot] = xroot
            elif self.rango[xroot] < self.rango[yroot]:
                self.parent[xroot] = yroot
            elif self.rango[xroot] == self.rango[yroot]: #Si son iguales asiganar uno y aumentar su rango
                self.parent[yroot] = xroot
                self.rango[xroot] += 1

    def kruskal(self):
        # obtner aristar formato weight, nodo, nodo
        edges = []
        for u in range(len(self.grafo)):
            for v, weight in self.grafo[u]:
                if u < v:
                    edges.append((weight, u, v))

        # ordenar las aristas
        edges.sort()

        # Inicializar conjuntos disjuntos, Por cada nodo en el grafo
        for node in range(len(self.grafo)):
            self.parent.append(node)  # Cada nodo es su propio padre inicialmente
            self.rango.append(0)  # Rango inicial es 0

        # Formar el arbol
        AEM = []
        for weight, u, v in edges:
            if self.find(u) != self.find(v):
                self.union(u, v)
                AEM.append((u, v, weight))
        return AEM

"""######################## Fin KRUSKAL ########################"""

"""####################### Inicio Tkinter #######################"""



"""####################### Fin Tkinter #######################"""


#Ejecución de PRIM
def ejecutar_PRIM(nodo_inicial):
    tiempo_inicial = time.time()
    numero_de_nodos = len(grafo)  # Obtiene la cantidad de nodos dentro del grafo
    if (numero_de_nodos - 1 < nodo_inicial) or (nodo_inicial < 0):
        return tk.Label(ventana, text=f"{nodo_inicial}- no es válido", fg = "red").grid(row=6, column=0)
    heap = []  # Lista que contendrá tuplas con los siguientes datos (peso, nodo_inicial, vecino)
    miembros = [False] * numero_de_nodos  # Lista para marcar nodos como miembros del árbol de expansión mínima (MST)
    seleccionadas = []  # Lista para guardar aristas seleccionadas en otro orden (nodo_inicial, vecino, peso)
    peso_Total = 0  # Variable para almacenar peso total del MST

    def visita(nodo):
        miembros[nodo] = True
        for v, p in grafo[nodo]:  # v = vecino | p = peso
            if not miembros[v]:
                heapq.heappush(heap, (p, nodo, v))

    visita(nodo_inicial)

    while heap and len(seleccionadas) < numero_de_nodos - 1:
        peso, origen, destino = heapq.heappop(heap)

        # Si el nodo destino ya está incluido en el MST, descartamos y ámonos
        if miembros[destino]:
            continue

        # Aquí se agregan las aristas al MST
        seleccionadas.append((origen, destino, peso))
        peso_Total += peso

        # Ahora vamos a visitar el nuevo nodo
        visita(destino)
    tiempo_final = time.time()
    tiempo_total = (tiempo_final - tiempo_inicial) * 1000
    # RESULTADOS
    """
    print("Nodo inicial:", nodo_inicial)
    print("Aristas seleccionadas:", seleccionadas)
    print("Peso total:", peso_Total, "\n")
    """

    tk.Label(ventana, text=f"Nodo inicial: {nodo_inicial}").grid(row=6, column=0)
    tk.Label(ventana, text=f"Aristas seleccionadas:").grid(row=7, column=0)
    i = 1
    for nodo_in, nodo_vec, peso in seleccionadas:
        tk.Label(ventana, text=f"Arista {i}: ({nodo_in}, {nodo_vec}) | Peso: {peso}").grid(row=7 + i, column=0)
        i += 1
    tk.Label(ventana, text=f"Peso total: {peso_Total}").grid(row=7 + i, column=0)
    tk.Label(ventana, text=f"Tiempo de ejecución: {tiempo_total:.5f} ms").grid(row=8 + i, column=0)
    return None

#Ejecución de KRUSKAL
def ejecutar_KRUSKAL():
    tiempo_inicial = time.time()
    algkrusk = kruskalAlg(grafo)
    res = algkrusk.kruskal()
    tiempo_final = time.time()
    tiempo_total = (tiempo_final - tiempo_inicial) * 1000
    """
    for u, v, weight in res:
        print(f"{u} - {v} | Peso = {weight}")
    """
    tk.Label(ventana, text = f"Aristas seleccionadas:").grid(row=6, column=1)
    i = 0
    for u, v, weight in res:
        tk.Label(ventana, text = f"{u} - {v} | Peso = {weight}").grid(row = 8 + i, column = 1)
        i += 1
    tk.Label(ventana, text=f"Tiempo de ejecución: {tiempo_total:.5f} ms").grid(row=9 + i, column=1)
    return None

"""############### Widget: Dibujo del grafo ###############"""
#Posiciones para dibujar el grafo en Tkinter
tk.Label(ventana, text="Grafo utilizado:", fg = "blue").grid(row = 0 , column = 0, columnspan = 2)
canvas = tk.Canvas(ventana, width = 600, height = 200, bg = "white")
canvas.grid(row = 1, column = 0, columnspan = 2)

#Centro del dibujo
cx = 300
cy = 300
#Radio donde están los nodos
r = 200
#Posiciones | Acomodadas de forma manual para que se parezca al grafo inspiración
posiciones = [ #Nodo, X, Y
    (0, 150, 100),
    (1, 200, 50),
    (2, 300, 50),
    (3, 400, 50),
    (4, 450, 100),
    (5, 400, 150),
    (6, 300, 150),
    (7, 200, 150),
    (8, 250, 100)
]

#Aristas | Se refiere a las conexiones que hay entre cada nodo y su peso
aristas = [ #Nodo1, Nodo2, Peso
    (0, 1, 4), (0, 7, 9),
    (1, 7, 11), (1, 2, 9),
    (2, 3, 7), (2, 5, 4), (2, 8, 2),
    (3, 4, 10), (3, 5, 15),
    (4, 5, 11),
    (5, 6, 2),
    (6, 7, 1), (6, 8, 6),
    (7, 8, 7)
]

for nodo, x, y in posiciones:
    canvas.create_oval(x-15, y-15, x+15, y+15, fill = "lightyellow") #Se crea cada nodo en las posiciones seleccionadas
    canvas.create_text(x, y, text = f"{nodo}") #Se añade su nombre o en este caso número respectivo

for u, v, peso in aristas:
    _, x1, y1 = posiciones[u]
    _, x2, y2 = posiciones[v]

    #Se decide acortar las líneas porque se encimaban sobre los nodos y no se entendía visualmente
    acortamiento = 15 / math.dist((x1, y1), (x2, y2)) #  15 - radio del nodo
    x1r = x1 + (x2 - x1) * acortamiento
    y1r = y1 + (y2 - y1) * acortamiento
    x2r = x2 - (x2 - x1) * acortamiento
    y2r = y2 - (y2 - y1) * acortamiento

    canvas.create_line(x1r, y1r, x2r, y2r)

    #peso
    px = ((x1 + x2) / 2)
    py = ((y1 + y2) / 2)
    canvas.create_text(px, py, text=str(peso), fill = "blue")

"""############### Widgets: El resto de elementos visuales ###############"""

#Widgets de PRIM
tk.Label(ventana, text = "Prim").grid(row = 2, column = 0)
tk.Label(ventana, text = "Ingrese un nodo inicial", bg = "yellow").grid(row = 3, column = 0)
PrimEntry = tk.Entry(ventana) #Entrada para determinar el nodo inicial (requisito para su uso óptimo)
PrimEntry.grid(row = 4, column = 0)
#Botón que ejecuta el algoritmo de PRIM, tomando como parámetro el número digitado en la entrada anterior
tk.Button(ventana, text = "Ejecutar", bg = "lightgreen", command = lambda: ejecutar_PRIM(int(PrimEntry.get()))).grid(row = 5, column = 0)

#Widgets de KRUSKAL
tk.Label(ventana, text = "Kruskal").grid(row = 2, column = 1)
tk.Label(ventana, text = "Sin entrada inicial", fg = "red").grid(row = 3, column = 1)
#Botón que ejecuta el algoritmo de KRUSKAL
tk.Button(ventana, text = "Ejecutar", bg = "lightblue", command = ejecutar_KRUSKAL).grid(row = 5, column = 1)
tk.Label(ventana, text = "").grid(row = 6, column = 1)

#run
ventana.mainloop()
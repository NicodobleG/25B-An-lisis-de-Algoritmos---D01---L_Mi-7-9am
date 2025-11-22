import tkinter as tk

ventana = tk.Tk()
ventana.geometry("450x470")
ventana.title("Actividad: Limitaciones de los algoritmos | Problema del Viajero")

"""
Actividad: Problema del Viajero (Travelling Salesman Problem)

Consiste en que dado un conjunto de ciudades y las distancias entre cada par de ellas, encontrar una ruta que:
1. Visite cada ciudad exactamente una vez
2. Regrese a la ciudad de origen.
3. Tenga la menor distancia total posible.

Para este caso elijo usar 6 ciudades como muestra.

Mi matriz de distancias será la siguiente:
  A  B  C  D  E  F
A 0  3  10 6  14 2
B 3  0  9  7  12 5
C 10 9  0  19 20 1
D 6  7  19 0  8  4
E 14 12 20 8  0  2
F 2  5  1  4  2  0

Utilizaré backtracking y poda porque anteriormente a un proyecto que tengo con un compañero le añadimos alpha-beta prunning a un
algoritmo llamado Minimax, que aparentemente hace cosas similares, pero no funcionan para lo mismo, entonces decido utilizar
backtraking
"""
#La matriz que elegí tendrá una muestra de 6 ciudades
distancias = [
    [0, 3, 10, 6, 14, 2],
    [3, 0, 9, 7, 12, 5],
    [10, 9, 0, 19, 20, 1],
    [6, 7, 19, 0, 8, 4],
    [14, 12, 20, 8, 0, 2],
    [2, 5, 1, 4, 2, 0]
]
#Número total de ciudades
total_de_ciudades = len(distancias)
ciudades = ["A", "B", "C", "D", "E", "F"]

#Arreglo que definirá si una ciudad fue visitada o no
visitado = []
for n in range(total_de_ciudades):
    visitado.append(False)
    #print(visitado)

"""
Ciudad de inicio
Ciudades disponibles:
A = 0, B = 1, C = 2, D = 3, E = 4, F = 5 | y si fueran más, serían más números, vaya
"""
CIUDAD_INICIAL = 0

#El costo inicial es 0, ya que aún no hemos salido de la ciudad
costo_actual = distancias[CIUDAD_INICIAL][CIUDAD_INICIAL]

#Definimos como visitado la ciudad inicial para evitar problemas al incio de las recursiones
visitado[CIUDAD_INICIAL] = True

#Inicializamos el mejor precio actual disponible como algo muy alto, este número funcionará para este caso
mejor_precio = 999
mejor_ruta = []

#Lista temporal para almacenar la ruta temporal durante las recursiones
ruta_actual = [CIUDAD_INICIAL]

#Función principal para explorar todas las posibles rutas y, con la poda evitar explorar
#rutas con costo peor
def backtracking(ciudad_actual, costo_actual, visitadas, ruta_actual, visitado):
    global mejor_precio, mejor_ruta

    #Caso base: todas las ciudades fueron visitadas
    if visitadas == total_de_ciudades:

        #Sumamos la distancia para volver a la ciudad inicial
        costo_final = costo_actual + distancias[ciudad_actual][CIUDAD_INICIAL]
        #print("Costo_final: ", costo_final) #debug

        #Si el costo final es mejor que el registrado, entonces lo actualizamos
        if costo_final < mejor_precio:
            mejor_precio = costo_final
            #print("mejor_precio: ", mejor_precio) #debug
            mejor_ruta = ruta_actual.copy()
            #print("ruta_actual: ", ruta_actual) #debug

        return

    #Exploración de todas las ciudades posibles
    for i in range(total_de_ciudades):

        #Solo se consideran ciudades no visitadas
        if visitado[i] == False:
            costo_temporal = costo_actual + distancias[ciudad_actual][i]

            #Poda: aquí comprobamos si es peor que la mejor solución, si lo es, se descarta
            if costo_temporal >= mejor_precio:
              continue

            #Se marca como visitado y se agrega a la ruta
            visitado[i] = True
            ruta_actual.append(i)

            #Llamada recursiva
            backtracking(i, costo_temporal, visitadas + 1, ruta_actual, visitado)

            #Se deshacen los cambios para explorar otras rutas
            ruta_actual.remove(i)
            visitado[i] = False

"""Pruebas antes de implementar UI
#print("DEBUG:") #debug
backtracking(CIUDAD_INICIAL, costo_actual, 1, ruta_actual, visitado)
#print("FIN DE DEBUG") #debug

print("Mejor ruta encontrada: ", mejor_ruta)
print(f"Costo total: {mejor_precio}")
"""

c = 0
def Matriz():
    global c
    #Para la matriz, colocamos los nombres de las ciudades
    for i in range(total_de_ciudades):
        tk.Label(ventana, text = f"{ciudades[i]} = {i}", relief = "solid").grid(row = 7, column = i + 1)
        tk.Label(ventana, text= f"{ciudades[i]} = {i}", relief = "solid").grid(row = 8 + i, column = 0)

    #Para la matriz, colocamos los costos de ir a cada ciudad
    for i in range(total_de_ciudades):
        for j in range(total_de_ciudades):
            tk.Label(ventana, text = distancias[i][j]).grid(row = 8 + i, column = j + 1)
        c += 1

def resetear_valores():
    global mejor_precio, mejor_ruta, ruta_actual, visitado
    #Se resetean TODOS los valores necesarios para que el programa vuelva a funcionar
    mejor_precio = 999
    mejor_ruta = []

    for i in range(total_de_ciudades):
        visitado[i] = False

    ruta_actual.clear()

def encontrar_ruta(entrada):
    global CIUDAD_INICIAL, costo_actual, visitado, ruta_actual

    #Comprobamos que el valor ingresado sea válido
    if entrada not in range(total_de_ciudades) :
        return Mejor_rutaTK.configure(text = "¡La entrada igresada no es válida!", fg = "red"), Costo_totalTK.configure(text = "")

    #Función para resetear TODOS los valores necesarios para que el programa vuelva a funcionar
    resetear_valores()

    #Se redefinen los valores iniciales necesarios para el correcto funcionamiento del algoritmo
    CIUDAD_INICIAL = entrada
    costo_actual = distancias[CIUDAD_INICIAL][CIUDAD_INICIAL]
    visitado[CIUDAD_INICIAL] = True
    ruta_actual = [CIUDAD_INICIAL]

    #Comienza la ejecución del algoritmo
    backtracking(CIUDAD_INICIAL, costo_actual, 1, ruta_actual, visitado)

    #Se re-escriben los labels previamente creados con los resultados obtenidos
    Mejor_rutaTK.configure(text = f"Mejor ruta: {mejor_ruta}", fg = "black")
    Costo_totalTK.configure(text = f"Costo total: {mejor_precio}")

#UI: texto mostrando el problema
tk.Label(ventana, text = "Problema del viajero (Travelling Salesman Problem)").grid(row = 0, column = 0, columnspan = 7)
tk.Label(ventana, text = "Consiste en que dado un conjunto de ciudades y las distancias entre cada par de").grid(row = 1, column = 0, columnspan = 7, sticky = "w")
tk.Label(ventana, text = "ellas, encontrar una ruta que:\n").grid(row = 2, column = 0, columnspan = 7, sticky = "w")
tk.Label(ventana, text = "1. Visite cada ciudad exactamente una vez").grid(row = 3, column = 0, columnspan = 7, sticky = "w")
tk.Label(ventana, text = "2. Regrese a la ciudad de origen").grid(row = 4, column = 0, columnspan = 7, sticky = "w")
tk.Label(ventana, text = "3. Tenga la menor distancia total posible\n").grid(row = 5, column = 0, columnspan = 7, sticky = "w")

#UI: Se muestra la matriz seleccionada para la actividad
tk.Label(ventana, text = "La matriz de distancias será la siguiente:").grid(row = 6, column = 0, columnspan = 7, sticky = "w")
Matriz()

#UI: Parte funcional de la actividad
tk.Label(ventana, text = "\nSeleccione una ciudad inicial (0 - 5)").grid(row = 8 + c, column = 0, columnspan = 7)
Entrada = (tk.Entry(ventana))
Entrada.grid(row = 9 + c, column = 0, columnspan = 7)
tk.Button(ventana, text = "Encontrar ruta", bg = "lightblue", command = lambda: encontrar_ruta(int(Entrada.get()))).grid(row = 10 + c, column = 0, columnspan = 7)

#UI: Se crean previamente los labels referentes a las respuestas para ser alterados luego por encontrar_ruta()
Mejor_rutaTK = (tk.Label(ventana, text = ""))
Mejor_rutaTK.grid(row = 11 + c, column = 0, columnspan = 7, sticky = "w")

Costo_totalTK = (tk.Label(ventana, text = ""))
Costo_totalTK.grid(row= 12 + c, column=0, columnspan=7, sticky="w")

ventana.mainloop()
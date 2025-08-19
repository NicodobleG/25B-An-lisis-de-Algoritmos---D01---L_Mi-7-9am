import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# Clase para los algoritmos
class AlgoritmoBusqueda:
    @staticmethod
    def lineal(lista, valor):
        inicio = time.perf_counter()
        for i, num in enumerate(lista):
            if num == valor:
                fin = time.perf_counter()
                return i, (fin - inicio) * 1000
        fin = time.perf_counter()
        return -1, (fin - inicio) * 1000

    @staticmethod
    def binaria(lista, valor):
        lista_ordenada = np.sort(lista)
        inicio = time.perf_counter()
        izquierda, derecha = 0, len(lista_ordenada) - 1

        while izquierda <= derecha:
            medio = (izquierda + derecha) // 2
            if lista_ordenada[medio] == valor:
                fin = time.perf_counter()
                return medio, (fin - inicio) * 1000
            elif lista_ordenada[medio] < valor:
                izquierda = medio + 1
            else:
                derecha = medio - 1
        fin = time.perf_counter()
        return -1, (fin - inicio) * 1000

# Clase para pruebas comparativas, guardar datos y demás
class Busquedas:
    def __init__(self, repeticiones=5):
        self.repeticiones = repeticiones
        self.listas = []  # Almacena tuples: (lista, valor_a_buscar)
        self.magnitudes = []
        self.tiempos_lineal = []
        self.tiempos_binaria = []

    def agregar_lista_valor(self, lista, valor): # Guardar lista
        self.listas.append((np.sort(lista), valor)) 

    def correr(self): # Calcula los promedios de todas los valores guardados
        self.magnitudes.clear()
        self.tiempos_lineal.clear()
        self.tiempos_binaria.clear()

        for lista, valor in self.listas:
            n = len(lista)
            t_lineal = []
            t_binaria = []

            for _ in range(self.repeticiones):
                _, tiempo_l = AlgoritmoBusqueda.lineal(lista, valor)
                _, tiempo_b = AlgoritmoBusqueda.binaria(lista, valor)
                t_lineal.append(tiempo_l)
                t_binaria.append(tiempo_b)

            self.magnitudes.append(n)
            self.tiempos_lineal.append(np.mean(t_lineal))
            self.tiempos_binaria.append(np.mean(t_binaria))

# Aquí va todo lo relacionado a la ventana, botones y demás funciones relacionadas con estos mismos.
class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Act01 - Búsqueda con GUI. Garín Gutiérrez, Nicolás Alejandro")
        self.root.geometry("900x750")

        self.listaDatos = None
        self.valorGenerado = None
        self.experimento = Busquedas()

        self.canvas = None

        self._crear_widgets()
        self.root.mainloop()

    def _crear_widgets(self):

        
        # Generación
        tk.Label(self.root, text="Cantidad de datos a generar").pack(pady=10)
        self.entrada = tk.Entry(self.root, bg="light goldenrod")
        self.entrada.pack(pady=5)
        tk.Button(self.root, text="Generar", command=self.generar_lista, bg="pale green").pack(pady=5)

        # Buscar
        tk.Label(self.root, text="Ingrese el valor a buscar").pack(pady=10)
        self.entradaBuscar = tk.Entry(self.root, bg="light goldenrod")
        self.entradaBuscar.pack(pady=5)

        frame_busqueda = tk.Frame(self.root)
        frame_busqueda.pack(pady=5)

        tk.Button(frame_busqueda, text="Búsqueda Lineal", command=self.busqueda_lineal, bg="cornflower blue").pack(side="left", padx=5)
        tk.Button(frame_busqueda, text="Búsqueda Binaria", command=self.busqueda_binaria, bg="salmon1").pack(padx=5)

        # Resultados
        self.lblInfo = tk.Label(self.root, text="", justify="left")
        self.lblInfo.pack(pady=10)

        # Botones para gráfica
        frame_grafica = tk.Frame(self.root)
        frame_grafica.pack(pady=5)
        
        tk.Button(frame_grafica, text="Comparación gráfica", command=self.mostrar_grafica, bg="pale green").pack(side="left", padx=5)
        tk.Button(frame_grafica, text="Limpiar listas y resultados", command=self.limpiar_experimento, bg="aquamarine").pack(padx=5)

    def generar_lista(self):
        valorLista = self.entrada.get().strip()
        if valorLista.isdigit() and int(valorLista) > 0:
            self.valorGenerado = int(valorLista)
            self.listaDatos = np.random.randint(0, self.valorGenerado, size=self.valorGenerado)
            self.lblInfo.config(fg="green", text=f"Lista de {self.valorGenerado} elementos generada con éxito")
        else:
            self.lblInfo.config(fg="red", text="Dato inválido")

    def busqueda_lineal(self):
        self._buscar("Lineal")

    def busqueda_binaria(self):
        self._buscar("Binaria")

    def _buscar(self, tipo):
        if self.listaDatos is None:
            self.lblInfo.config(fg="red", text="Primero genera una lista")
            return
        try:
            valor = int(self.entradaBuscar.get().strip())
        except:
            self.lblInfo.config(fg="red", text="Ingrese un número válido")
            return

        # Ejecutar búsqueda 5 veces y calcular promedio
        tiempos = []
        for _ in range(self.experimento.repeticiones):
            if tipo == "Lineal":
                _, tiempo = AlgoritmoBusqueda.lineal(self.listaDatos, valor)
            else:
                _, tiempo = AlgoritmoBusqueda.binaria(self.listaDatos, valor)
            tiempos.append(tiempo)
        tiempo_promedio = np.mean(tiempos)

        # Guardar lista + valor en experimento si es primera vez
        # Evita duplicados: solo guarda si la combinación lista+valor no existe
        existe = any((np.array_equal(lista, self.listaDatos) and v == valor) for lista, v in self.experimento.listas)
        if not existe:
            self.experimento.agregar_lista_valor(self.listaDatos, valor)

        # Mostrar resultado
        indice, _ = AlgoritmoBusqueda.lineal(self.listaDatos, valor) if tipo == "Lineal" else AlgoritmoBusqueda.binaria(self.listaDatos, valor)
        self._mostrar_resultado(tipo, valor, indice, tiempo_promedio)

    def _mostrar_resultado(self, tipo, valor, indice, tiempo):
        if indice != -1:
            msg = f"Búsqueda {tipo}:\nTamaño de la lista: {len(self.listaDatos)}\nElemento {valor} encontrado en índice {indice}\nTiempo promedio: {tiempo:.6f} ms"
        else:
            msg = f"Búsqueda {tipo}:\nTamaño de la lista: {len(self.listaDatos)}\nElemento {valor} NO encontrado\nTiempo promedio: {tiempo:.6f} ms"
        self.lblInfo.config(fg="black", text=msg)

    def mostrar_grafica(self):
        if not self.experimento.listas:
            self.lblInfo.config(fg="red", text="No hay listas o búsquedas para graficar")
            return

        # Agrupar por tamaño y sacar promedios de todos los tiempos para ese tamaño
        resultados = {}
        for lista, valor in self.experimento.listas:
            n = len(lista)
            if n not in resultados:
                resultados[n] = {'lineal': [], 'binaria': []}

            # Usar los promedios guardados en Busquedas
            _, t_lineal = AlgoritmoBusqueda.lineal(lista, valor)
            _, t_binaria = AlgoritmoBusqueda.binaria(lista, valor)

            resultados[n]['lineal'].append(t_lineal)
            resultados[n]['binaria'].append(t_binaria)

        # Calcular promedios por tamaño
        magnitudes = sorted(resultados.keys())
        tiempos_lineal = [np.mean(resultados[n]['lineal']) for n in magnitudes]
        tiempos_binaria = [np.mean(resultados[n]['binaria']) for n in magnitudes]

        # Graficar
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(magnitudes, tiempos_lineal, marker="o", linestyle="-", color="blue", label="Lineal")
        ax.plot(magnitudes, tiempos_binaria, marker="s", linestyle="--", color="red", label="Binaria")

        ax.set_xlabel("Tamaño de la lista", fontsize=12)
        ax.set_ylabel("Tiempo promedio (ms)", fontsize=12)
        ax.set_title("Comparación de algoritmos de búsqueda", fontsize=14)
        ax.legend(fontsize=12)
        ax.grid(True)

        ax.relim()
        ax.set_xscale("log")
        ax.set_yscale("log")

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas.get_tk_widget().pack(pady=20)
        self.canvas.draw()

        resumen = f"Se graficaron {len(magnitudes)} tamaños de listas, usando el promedio de tiempo de las búsquedas realizadas en cada lista"
        self.lblInfo.config(fg="blue", text=resumen)

    def limpiar_experimento(self):
        self.experimento.listas.clear()
        self.experimento.magnitudes.clear()
        self.experimento.tiempos_lineal.clear()
        self.experimento.tiempos_binaria.clear()
        self.lblInfo.config(fg="dark green", text="Datos limpiados con éxito")
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

# Ejecutar app
GUI()

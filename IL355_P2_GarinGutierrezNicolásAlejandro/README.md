# Visualizador de metodos de Ordenamiento

Programa con finalidad de visualizar, graficar, y comparar un grupo de algoritmos de ordenamiento.

# Instrucciones de Instalación

- Python 3.13
- contourpy 1.3.3
- cycler 0.12.1
- fonttools 4.59.1
- kiwisolver 1.4.9
- matplotlib 3.10.5
- numpy 2.3.2
- packaging 25.0
- pillow 11.3.0
- pyparsing 3.2.3
- python-dateutil 2.9.0.post0
- six 1.17.0

2. **Instalación:**

- Clona el repositorio: 
``` python
git clone https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/tree/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro
```
- Navega al directorio del proyecto: ```cd IL355_P2_GarinGutierrezNicolásAlejandro```
- Instala las dependencias: 
```pip install -r requirements.txt ```

## Ejecución

1. **Modo de ejecución:**
- Para ejecutar el script principal, usa el siguiente comando: `python main.py`

2. **Ejemplos de uso**

#Al ejecutar el programa visualizaremos lo siguiente:

![Ejecutar](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/1.Al%20ejecutar%20el%20programa.png)

#Dentro del campo situado a la derecha del botón "Cambiár No. Barras" introducir un número entero.
#Presionaremos Cambiar No. Barras para determinar el número de barras a generar.

![Cambiar Barras](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/2.Al%20cambiar%20el%20n%C3%BAmero%20de%20barras.gif)

#Presionaremos el botón "Generar" para crear la lista de datos y comenzar a visualizarlos.

![Generar](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/3.%20Al%20generar%20las%20barras.gif)

#Dentro del dropdown situado a la derecha del texto "Algoritmo: " podremos seleccionar lo siguientes métodos de ordenamiento:
  a) Selection sort
  b) Bubble sort
  c) Merge sort
  d) Quick sort
#Seleccionamos un algoritmo de ordenamiento.

![Dropdown](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/3.%20Al%20seleccionar%20el%20algoritmo%20de%20ordenamiento.gif)

NOTA: antes de presionar ordenar, se puede alterar la velocidad de visualización con el slider situado hasta la derecha llamado "Velocidad (ms)" que tendrá como rango de velocidades de 0 a 200.

![Velocidades](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/7.%20Al%20cambiar%20la%20velocidad%20de%20visualizaci%C3%B3n.gif)

#Presionaremos el botón "Ordenar" para comenzar con el proceso de ordenamiento que podrá ser visualizado a la velocidad seleccionada.
Selection sort:

![SelectionSort](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/4.1.%20Ordenamiento%20selection.gif)

Bubble sort:

![BubbleSort](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/4.2%20Ordenamiento%20bubble.gif)

Merge sort:

![MergeSort](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/4.3%20Ordenamiento%20merge.gif)

Quick sort:

![QuickSort](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/4.4%20Ordenamiento%20quick.gif)

#Después de ordenar, se pueden hacer dos cosas con los datos:
  a) Presionaremos el botón "Limpiar Resultados" si lo que deseamos es regresar los datos a su estado desordenado original.
  
![LimpiarResultado](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/5.%20Al%20limpiar%20resultados.gif)

  b) Presionaremos el botón "Mezclar" si lo que deseamos es barajear los datos, volviéndolos el nuevo estado desordenado original.
  
![Mezclar](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/6.%20Al%20mezclar%20los%20datos.gif)

NOTA: antes del siguiente paso, es recomendable realizar varios ordenamientos de distintos tamaños de barras con los distintos métodos de ordenamiento.
#Presionaremos el botón "Graficar Tiempos" cuando deseemos visualizar los datos recabados, generando una gráfica que tiene como ejes el tiempo de ejecución en milisegundos, y la cantidad de datos ordenados.

![Graficar](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/IL355_P2_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/8.%20Al%20graficar%20los%20tiempos%20recabados.png)

#Cerrar el programa al terminar

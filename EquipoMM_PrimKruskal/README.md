# Visualizador de metodos de Ordenamiento

Programa con el objetivo de mostrar los algoritmos voraces de Prim y Kruskal en python, para poder observar y entender de mejor manera su funcionamiento, utilizando un grafo ya definido obtenido de la primer pagina de: https://es.scribd.com/document/403078422/Algoritmo-PRIM.

![Grafo](https://estrucuturas2unincca.wordpress.com/wp-content/uploads/2018/11/imagen8.png?w=556&h=232)

# Instrucciones de Instalación

Se requiere de un intérprete de la siguiente versión para que el programa funcione correctamente:
- Python 3.10 (o superior)

**Instalación:**

- Clona el repositorio: 
``` python
git clone https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/tree/a2accca6eeab70770c004c15d14fc9f11883001b/EquipoMM_PrimKruskal
```

## Ejecución

1. **Modo de ejecución:**
- Navega al directorio: ```cd EquipoMM_PrimKruskal/src```
- Para ejecutar el script principal, usa el siguiente comando: `python main.py`

2. **Instrucciones de uso**

- Al ejecutar el programa visualizaremos una ventana que contiene el grafo a tratar, dos botones y un campo:

![Ejecutar](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_PrimKruskal/img/EquipoMM_PrimKruskal1.png?raw=true)

- Para ejecutar el algoritmo de Prim, se deberá seleccionar un nodo inicial válido, siendo este alguno de los mostrados en el grafo, después presionar el botón verde claro que dice "Ejecutar":

![Prim usado](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_PrimKruskal/img/EquipoMM_PrimKruskal2.png?raw=true)

-  Para ejecutar el algoritmo de Kruskal, solo se deberá presionar el botón azul claro que dice "Ejecutar":

![Kruskal usado](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_PrimKruskal/img/EquipoMM_PrimKruskal3.png?raw=true)
 
Como podemos observar, al menos del lado de Prim usando el nodo inicial 0, los resultados son prácticamente los mismos, y aunque, diferentes metodologías fueron usadas, observamos que obtiene un árbol de expansión mínima igual, esto cambia ligeramente si se elige otro nodo inicial con Prim, pero el peso total no se altera, al menos en este caso.

- Una vez se termine de usar el programa, se puede finalizar presionando el botón "X" situado en la parte superior derecha de la ventana.

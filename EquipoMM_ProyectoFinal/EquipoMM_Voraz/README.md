# Proyecto final

Programa con finalidad de implementar (si es posible) la mayoría de los algoritmos y métodos contemplados en clase, en este caso se aplican los siguientes:

- minimax (Fuerza bruta)
- Alpha-Beta Pruning (Divide y vencerás)
- Codificación de Huffman (Algoritmos voráces)
- Backtracking (por parte de minimax y Alpha-Beta Pruning)
- Ramificación (por parte de minimax y Alpha-Beta Pruning)
- Poda (por parte de Alpha-Beta Puning)

# Instrucciones de Instalación

Se requiere de un intérprete de la siguiente versión para que el programa funcione correctamente:
- Python 3.13 (de preferencia)

**Instalación:**

- Clona el repositorio: 
``` python
git clone https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/tree/01a76875c6696553916e36e935b4fc4b2ba87e8c/EquipoMM_ProyectoFinal
```
- Navega al directorio del proyecto: ```cd EquipoMM_ProyectoFinal/EquipoMM_Voraz```
- Instala las dependencias: 
```pip install -r requirements.txt ```

## Ejecución

1. **Modo de ejecución:**
- Navega al directorio: ```cd EquipoMM_ProyectoFinal/EquipoMM_Voraz/src```
- Para ejecutar el script principal, usa el siguiente comando: `python main.py`

2. **Ejemplos de uso**

- Al ejecutar el programa visualizaremos el menú de selección de IA coloreadas por su dificultad:

![Ejecutar](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_ProyectoFinal/EquipoMM_Voraz/img/1%20-%20Al%20inicializar%20el%20programa%20(selecci%C3%B3n%20de%20IA).png?raw=true)

- Al seleccionar una dificultad la partida iniciará:

![Comienza el juego](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_ProyectoFinal/EquipoMM_Voraz/img/2%20-%20Inicia%20el%20juego.png?raw=true)

-  En caso de elegir Minimax:
 el jugador siempre hará el primer movimiento a lo que la IA responderá con movimientos que considere adecuados:

![Primeros 5 movimientos | Minimax](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_ProyectoFinal/EquipoMM_Voraz/img/3MM%20-%20Primeros%205%20movimientos.png?raw=true)

-  En caso de elegir Alpha-Beta:
 el jugador siempre hará el primer movimiento a lo que la IA responderá más rápido, con movimientos más difíciles de contrarestar:

![Primeros 5 movimientos | Alpha-Beta](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_ProyectoFinal/EquipoMM_Voraz/img/3AB%20-%20Primeros%205%20movimientos.png?raw=true)

- Al finalizar la partida se esperan dos posibles resultados:
- - Al ganar:

![Victoria](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_ProyectoFinal/EquipoMM_Voraz/img/4MM%20-%20Final%20de%20la%20partida.png?raw=true)

- - Al perder:

![Derrota](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_ProyectoFinal/EquipoMM_Voraz/img/4AB%20-%20Final%20de%20la%20partida.png?raw=true)

- Al presionar el botón **"Ok"** se mostrará una gráfica con los tiempos de respuesta por turno de la IA, esto con fines comparativos:

- - Minimax:

![Grafica Minimax](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_ProyectoFinal/EquipoMM_Voraz/img/5MM%20-%20Tiempos%20de%20respuesta.jpg?raw=true)

- - Alpha-Beta prunning:

![Grafica Alpha-Beta](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_ProyectoFinal/EquipoMM_Voraz/img/5AB%20-%20Tiempos%20de%20respuesta.jpg?raw=true)

- En caso de presionar el botón "Reproducir", se abrirá el explorador de archivos, permitiendo elegir entre guardados .txt y .bin, ambos cargaran la partida de igual forma, existen dos versiones para demostrar el funcionamiento de la compresión y descompresión de archivos por parte de la codificación de Huffman.

![Seleccion de guardado](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/main/EquipoMM_ProyectoFinal/EquipoMM_Voraz/img/5%20-%20Selecci%C3%B3n%20de%20replay.png?raw=true)

Luego de seleccionar el archivo de guardado, comenzará a reproducir la partida con los movimientos registrados tanto del jugador como de la IA contenidos en el archivo .txt o .bin, y al terminar serán devueltos al menú principal.

#Nota: El programa se cerrará automáticamente al presionar el botón **"Ok"** en caso de haber jugado

#Nota2: El programa se tendrá que cerrar manualmente con el botón **"X"** situado arriba a la derecha en caso de haber jugado un replay

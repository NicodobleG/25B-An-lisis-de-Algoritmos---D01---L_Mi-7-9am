# Damas

Programa con finalidad de visualizar la diferencia entre un algoritmo de fuerza bruta **(Minimax)** y otro divide y venceras **(Alpha-Beta Prunning)** en juegos de 2 jugadores modalidad 1 contra 1 con la utilización de **pygame** para jugar una partida de Damas.

# Instrucciones de Instalación

Se requiere de un intérprete de la siguiente versión para que el programa funcione correctamente:
- Python 3.13 (de preferencia)

**Instalación:**

- Clona el repositorio: 
``` python
git clone https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/67186133cafee3aa278e8fc09e6a8f75ef4c7cc4/EquipoMM_DivideVenceras
```
- Navega al directorio del proyecto: ```cd EquipoMM_DivideVenceras```
- Instala las dependencias: 
```pip install -r requirements.txt ```

## Ejecución

1. **Modo de ejecución:**
- Navega al directorio: ```cd EquipoMM_DivideVenceras/src```
- Para ejecutar el script principal, usa el siguiente comando: `python main.py`

2. **Ejemplos de uso**

- Al ejecutar el programa visualizaremos el menú de selección de IA coloreadas por su dificultad:

![Ejecutar](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/67186133cafee3aa278e8fc09e6a8f75ef4c7cc4/EquipoMM_DivideVenceras/img/1%20-%20Al%20inicializar%20el%20programa%20(selecci%C3%B3n%20de%20IA).png)

- Al seleccionar una dificultad la partida iniciará:

![Comienza el juego](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/67186133cafee3aa278e8fc09e6a8f75ef4c7cc4/EquipoMM_DivideVenceras/img/2%20-%20Inicia%20el%20juego.png)

-  En caso de elegir Minimax:
 el jugador siempre hará el primer movimiento a lo que la IA responderá con movimientos que considere adecuados:

![Primeros 5 movimientos | Minimax](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/67186133cafee3aa278e8fc09e6a8f75ef4c7cc4/EquipoMM_DivideVenceras/img/3MM%20-%20Primeros%205%20movimientos.png)

-  En caso de elegir Alpha-Beta:
 el jugador siempre hará el primer movimiento a lo que la IA responderá más rápido, con movimientos más difíciles de contrarestar:

![Primeros 5 movimientos | Alpha-Beta](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/67186133cafee3aa278e8fc09e6a8f75ef4c7cc4/EquipoMM_DivideVenceras/img/3AB%20-%20Primeros%205%20movimientos.png)

- Al finalizar la partida se esperan dos posibles resultados:
- - Al ganar:

![Victoria](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/67186133cafee3aa278e8fc09e6a8f75ef4c7cc4/EquipoMM_DivideVenceras/img/4MM%20-%20Final%20de%20la%20partida.png)

- - Al perder:

![Derrota](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/67186133cafee3aa278e8fc09e6a8f75ef4c7cc4/EquipoMM_DivideVenceras/img/4AB%20-%20Final%20de%20la%20partida.png)

- Al presionar el botón **"Ok"** se mostrará una gráfica con los tiempos de respuesta por turno de la IA, esto con fines comparativos:

- - Minimax:

![Grafica Minimax](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/97f56c82d65d3073cb1347b954011d8f9f5567a2/EquipoMM_DivideVenceras/img/5MM%20-%20Tiempos%20de%20respuesta.jpg)

- - Alpha-Beta prunning:

![Grafica Minimax](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/97f56c82d65d3073cb1347b954011d8f9f5567a2/EquipoMM_DivideVenceras/img/5AB%20-%20Tiempos%20de%20respuesta.jpg)

#Nota: El programa se cerrará automáticamente al presionar el botón **"Ok"**

# Visualizador de metodos de Ordenamiento

Programa con el objetivo de entender la manera en la que el algoritmo de Huffman funciona, siguiendo esto, el programa comprime archivos de extensión **.txt** y también los descomprime, en el proceso, mostrando el porcentaje de reducción logrado con la compresión.

# Instrucciones de Instalación

Se requiere de un intérprete de la siguiente versión para que el programa funcione correctamente:
- Sistema operativo: Windows 10 o superior, macOS, o distribuciones Linux (Ubuntu 20.04+, Debian, etc)
- Python 3.10 (o superior)
- Acceso a archivos de extensión **.txt**
- Permisos de **lectura/escritura**

**Instalación:**

- Clona el repositorio: 
``` python
git clone https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/tree/9c111004e9363f10c6a1028de764b46bafb47991/EquipoMM_C%C3%B3digo%20Huffman
```
- Navega al directorio del proyecto: ```cd EquipoMM_Código Huffman```
- Instala las dependencias: 
```pip install -r requirements.txt ```

## Ejecución

1. **Modo de ejecución:**
- Navega al directorio: ```cd EquipoMM_Código Huffman/src```
- Para ejecutar el script principal, usa el siguiente comando: `python main.py`

2. **Instrucciones de uso**

- Al ejecutar el programa visualizaremos una ventana que contiene varios botones y campos tal que así:

![Ejecutar](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/9c111004e9363f10c6a1028de764b46bafb47991/EquipoMM_C%C3%B3digo%20Huffman/Funcionamiento/1.Programa%20inicia.png)

- Se deberá presionar el botón verde con un ícono de carpeta abierta para seleccionar un archivo **.txt**; asímismo se deberá presionar el botón azul con ícono de carpeta para seleccionar una ruta donde se almacenarán los archivos generados:

![Selección de rutas](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/9c111004e9363f10c6a1028de764b46bafb47991/EquipoMM_C%C3%B3digo%20Huffman/Funcionamiento/2.Directorios%20seleccionados.png)

-  Una vez seleccionados el archivo de texto y la ruta de salida, se podrá presionar el botón "Comprimir" sin problema alguno:

![Comprime](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/9c111004e9363f10c6a1028de764b46bafb47991/EquipoMM_C%C3%B3digo%20Huffman/Funcionamiento/3.Comprime.png)

 Al presionar el botón se mostrará una ventana que confirma el éxito de la operación, adicionalmente debajo se mostrarán los siguientes datos:
 | Dato  |
| ------------- | 
| Tamaño original  |
| Tamaño comprimido  |
| Porcentaje de reducción lograda  |

Aquí una muestra de cómo debe quedar el archivo comprimido:

![Resultado_compresión](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/9c111004e9363f10c6a1028de764b46bafb47991/EquipoMM_C%C3%B3digo%20Huffman/Funcionamiento/3.1%20Resultado%201.png)

- Una vez generado un archivo comprimido, podremos utilizar el botón "Descomprimir" para realizar el proceso de descompresión:

![Descomprime](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/9c111004e9363f10c6a1028de764b46bafb47991/EquipoMM_C%C3%B3digo%20Huffman/Funcionamiento/4.Descomprime.png)
Al presionar el botón se mostrará una ventana que confirma el éxito de la operación.

Aquí una muestra de cómo debe quedar el archivo descomprimido:

![Resultado_descompresión](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/9c111004e9363f10c6a1028de764b46bafb47991/EquipoMM_C%C3%B3digo%20Huffman/Funcionamiento/4.%20Resultado%202.png)

- Y ya puede finalizar el programa

- Adicionalmente se adjuntará una muestra de un archivo **.txt* original, un archivo **.bin** resultado de una compresión, y otro archivo **.txt** resultado de la descompresión:

![Resultados visuales](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/9c111004e9363f10c6a1028de764b46bafb47991/EquipoMM_C%C3%B3digo%20Huffman/Funcionamiento/5.%20Pruebas.png)

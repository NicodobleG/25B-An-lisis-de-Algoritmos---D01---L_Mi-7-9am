# Visualizador de metodos de Ordenamiento

Programa con finalidad de visualizar clusters y sub-clusters de la base "fashion-mnist_test.csv" utilizando TMAP, Pandas, y demás.

# Instrucciones de Instalación

Se requiere de un intérprete de la siguiente versión para que el programa funcione correctamente:
- Python 3.9

**Instalación:**

- Clona el repositorio: 
``` python
git clone https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/tree/main/IL355_P3_GarinGutierrezNicol%C3%A1sAlejandro
```
- Navega al directorio del proyecto: ```cd IL355_P3_GarinGutierrezNicolásAlejandro```
- Instala las dependencias: 
```pip install -r requirements.txt ```

## Ejecución

1. **Modo de ejecución:**
- Para ejecutar el script principal, usa el siguiente comando: `python main.py`

2. **Ejemplos de uso**

- Al ejecutar el programa visualizaremos lo siguiente

![Ejecutar](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/df5e32a11a933767ba01ea8f71170f03537b911b/IL355_P3_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/1%20-%20Estado%20inicial.png)

- Al presionar el botón "Generar TMAP global (abrir navegador)" se generará el mapa principal clasificado por los labels encontrados en "fashion-mnist_test.csv" de la siguiente manera:

![Generar TMAP global_1](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/64cae72333cabedf837eccf99d88966d52169a79/IL355_P3_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/2%20-%20Generando%20TMAP%20gloibal.png)

Esto lo que provoca es que con la base anteriormente mencionada, se generen dos archivos para el correcto funcionamiento del programa, los cuales son "FashionMNIST_Global.html" y "FashionMNIST_Global.js".

![Generar TMAP global_2](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/64cae72333cabedf837eccf99d88966d52169a79/IL355_P3_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/2.1%20-%20TMAP%20Global%20generado.png)

- Al llenar los campos correspondientes a un subcluster debemos considerar que:
1. La prenda solo soporta 10 números distintos dentro del rango de números del 0 al 9
| Label | Prenda |
| --- | --- |
|<center> 0 </center> | T-shirt |
|<center> 1 </center> | Trouser |
|<center> 2 </center> | Pullover |
|<center> 3 </center> | Dress |
|<center> 4 </center> | Coat |
|<center> 5 </center> | Sandal |
|<center> 6 </center> | Shirt |
|<center> 7 </center> | Sneaker |
|<center> 8 </center> | Bag |
|<center> 9 </center> | Ankle boot |
2. el apartado "Imágenes de muestra (0 = por defecto (5))" representa la muestra que tomará de cada subcluster, es decir, si tomamos 3, en matplotlib se mostrarán 3 muestras de cada subcluster creado.

3. El apartado "Cantidad de subclusters (K)" determinará cuantas variaciones encontrará el programa.

- Al presionar "Generar subclusters (KMeans)" se tomarán en cuenta las cifras ingresadas en los campos anteriormente explicados, en el siguiente ejemplo tomaremos la prenda número 5 con las siguientes configuraciones:

![Generar subclusters_1](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/3c81e19c25c32cbaa0091f1b201c3f9056fadffe/IL355_P3_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/3%20-%20Generando%20subcluster.png)

De misma forma que con la versión global, se generarán dos archivos, uno .html, y otro .js, con un nombre referente a la prenda seleccionada junto con el prefijo "Subcluster_"

![Generar subclusters_2](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/3c81e19c25c32cbaa0091f1b201c3f9056fadffe/IL355_P3_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/3.1%20-%20Subcluster%20generado.png)

Aquí, las muestras de cada subcluster:

![Generar subclusters_3](https://github.com/NicodobleG/25B-An-lisis-de-Algoritmos---D01---L_Mi-7-9am/blob/3c81e19c25c32cbaa0091f1b201c3f9056fadffe/IL355_P3_GarinGutierrezNicol%C3%A1sAlejandro/Funcionamiento/3.2%20-%20Muestras%20de%20cada%20sub-cluster.png)

**Nota: Los .html y .js recién generados quedarán en el directorio del programa para consulta, tanto el global como los sub-cluster.**

#Cerrar el programa al terminar

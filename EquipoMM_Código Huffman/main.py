import tkinter as tk
from tkinter import filedialog, messagebox
from bitarray import bitarray
from collections import Counter
import heapq, pickle, struct, os

# --- Lógica de Huffman ---
class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def construir_arbol(frecuencias):
    heap = [NodoHuffman(c, f) for c, f in frecuencias.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        combinado = NodoHuffman(None, n1.frecuencia + n2.frecuencia)
        combinado.izquierda = n1
        combinado.derecha = n2
        heapq.heappush(heap, combinado)
    return heap[0]

def generar_codigos(nodo, codigo=None, codigos=None):
    if codigos is None:
        codigos = {}
    if codigo is None:
        codigo = bitarray()
    if nodo.caracter is not None:
        codigos[nodo.caracter] = codigo.copy()
    else:
        generar_codigos(nodo.izquierda, codigo + bitarray('0'), codigos)
        generar_codigos(nodo.derecha, codigo + bitarray('1'), codigos)
    return codigos

def codificar(texto, codigos):
    resultado = bitarray()
    for c in texto:
        resultado.extend(codigos[c])
    return resultado

def decodificar(codigo_binario, arbol):
    resultado = []
    nodo = arbol
    for bit in codigo_binario:
        nodo = nodo.izquierda if not bit else nodo.derecha
        if nodo.caracter is not None:
            resultado.append(nodo.caracter)
            nodo = arbol
    return ''.join(resultado)

def guardar_comprimido(ruta, arbol, bits):
    arbol_serializado = pickle.dumps(arbol)
    with open(ruta, 'wb') as f:
        f.write(struct.pack('I', len(arbol_serializado)))
        f.write(arbol_serializado)
        bits.tofile(f)

def cargar_comprimido(ruta):
    with open(ruta, 'rb') as f:
        tam_arbol = struct.unpack('I', f.read(4))[0]
        arbol = pickle.loads(f.read(tam_arbol))
        bits = bitarray()
        bits.fromfile(f)
    return arbol, bits


# --- Interfaz Tkinter ---
class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor Huffman")
        self.archivo_entrada = ""
        self.carpeta_salida = ""
        self.texto = ""

        # --- Sección de selección de archivos ---
        tk.Label(root, text="Archivo de texto (.txt):").pack()
        frame_in = tk.Frame(root)
        frame_in.pack(pady=2)
        self.entry_in = tk.Entry(frame_in, width=50, bg="DarkSeaGreen1")
        self.entry_in.pack(side=tk.LEFT)
        tk.Button(frame_in, text="📂", command=self.elegir_archivo, bg="PaleGreen3",
            fg="black", activebackground="PaleGreen2", activeforeground="black").pack(side=tk.LEFT)

        tk.Label(root, text="Carpeta de salida:").pack()
        frame_out = tk.Frame(root)
        frame_out.pack(pady=2)
        self.entry_out = tk.Entry(frame_out, width=50, bg="lightblue")
        self.entry_out.pack(side=tk.LEFT)
        tk.Button(frame_out, text="📁", command=self.elegir_carpeta, bg="lightcyan",
            fg="black", activebackground="lightblue", activeforeground="black").pack(side=tk.LEFT)

        # --- Botones principales ---
        frame_btn = tk.Frame(root)
        frame_btn.pack(pady=5)
        tk.Button(frame_btn, text="🗜️ Comprimir", command=self.comprimir, bg="#6a6acd",
            fg="white", activebackground="#836fff", activeforeground="white").pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="🔁 Descomprimir", command=self.descomprimir, bg="#4682b4",
            fg="white", activebackground="#5a9bd6", activeforeground="white").pack(side=tk.LEFT, padx=5)

        # --- Vista de texto y tamaños ---
        self.vista = tk.Text(root, height=15, width=70, bg="light goldenrod")
        self.vista.pack(pady=5)
        self.tamano = tk.Label(root, text="Esperando archivo...")
        self.tamano.pack()

    def elegir_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
        if ruta:
            self.archivo_entrada = ruta
            self.entry_in.delete(0, tk.END)
            self.entry_in.insert(0, ruta)
            with open(ruta, 'r', encoding='utf-8') as f:
                self.texto = f.read()
            self.vista.delete(1.0, tk.END)
            self.vista.insert(tk.END, self.texto)
            self.tamano.config(text=f"Tamaño original: {os.path.getsize(ruta)} bytes")

    def elegir_carpeta(self):
        carpeta = filedialog.askdirectory()
        if carpeta:
            self.carpeta_salida = carpeta
            self.entry_out.delete(0, tk.END)
            self.entry_out.insert(0, carpeta)

    def comprimir(self):
        if not self.archivo_entrada or not self.carpeta_salida:
            messagebox.showerror("Error", "Selecciona archivo y carpeta de salida.")
            return
        frecuencias = Counter(self.texto)
        arbol = construir_arbol(frecuencias)
        codigos = generar_codigos(arbol)
        bits = codificar(self.texto, codigos)

        # Nombramiento del archivo
        nombre_base = os.path.splitext(os.path.basename(self.archivo_entrada))[0]
        ruta_salida = os.path.join(self.carpeta_salida, f"{nombre_base}_comprimido.bin")

        guardar_comprimido(ruta_salida, arbol, bits)

        # Cálculo de tamaño y porcentaje
        tam_original = os.path.getsize(self.archivo_entrada)
        tam_comp = os.path.getsize(ruta_salida)
        reduccion = 100 * (1 - tam_comp / tam_original) if tam_original > 0 else 0

        self.tamano.config(text=f"Tamaño original: {tam_original} bytes | Comprimido: {tam_comp} bytes | Reducción: {reduccion:.2f} %")

        messagebox.showinfo("Éxito", f"Archivo comprimido guardado en:\n{ruta_salida}")

    def descomprimir(self):
        ruta = filedialog.askopenfilename(filetypes=[("Archivo Huffman", "*.bin")])
        if ruta:
            arbol, bits = cargar_comprimido(ruta)
            texto = decodificar(bits, arbol)
            self.vista.delete(1.0, tk.END)
            self.vista.insert(tk.END, texto)

            nombre_base = os.path.splitext(os.path.basename(ruta))[0]

            if self.carpeta_salida:
                ruta_txt = os.path.join(self.carpeta_salida or os.path.dirname(ruta), f"{nombre_base}_descomprimido.txt")
                with open(ruta_txt, 'w', encoding='utf-8') as f:
                    f.write(texto)
                messagebox.showinfo("Listo", f"Texto descomprimido guardado en:\n{ruta_txt}")
            else:
                messagebox.showinfo("Listo", "Texto descomprimido mostrado en pantalla.")

# --- Ejecución principal ---
if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()

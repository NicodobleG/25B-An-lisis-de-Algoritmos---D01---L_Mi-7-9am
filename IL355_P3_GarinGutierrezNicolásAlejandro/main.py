import os
import webbrowser
import base64
from io import BytesIO

import tkinter as tk
from tkinter import ttk, messagebox

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tmap as tm
from faerun import Faerun
from PIL import Image

from sklearn.cluster import KMeans

# -----------------------------------------------------
# Configuración TMAP / global
# -----------------------------------------------------
LABEL_NAMES = [
    "T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
    "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"
]

CFG = tm.LayoutConfiguration()
CFG.node_size = 1/55
DIMS = 1024
RND_STATE = 42

CSV_PATH = "fashion-mnist_test.csv"  # Asegúrate que está en la misma carpeta

# -----------------------------------------------------
# Funciones TMAP / utilidades
# -----------------------------------------------------
def compute_tmap(x, dims=DIMS):
    """Calcula layout TMAP para el DataFrame x (cada fila = 784 píxeles)."""
    enc = tm.Minhash(28*28, 42, dims)
    lf = tm.LSHForest(dims*2, 128)
    vectors = [tm.VectorFloat(row.astype(np.float32)/255) for row in x.values]
    lf.batch_add(enc.batch_from_weight_array(vectors))
    lf.index()
    return tm.layout_from_lsh_forest(lf, CFG)

def encode_images_base64(x):
    """Devuelve lista de data-URIs para tooltips en Faerun."""
    labels = []
    for row in x.values:
        img = Image.fromarray(np.uint8(row.reshape(28,28)))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue())
        labels.append("data:image/png;base64," + img_str.decode("utf-8"))
    return labels

def plot_faerun(name, layout_x, layout_y, s, t, y, img_labels, legend_labels=None):
    """Scatter + tree en Faerun y abrir en navegador."""
    safe_name = name.replace("/", "_").replace("\\", "_")
    faerun = Faerun(clear_color="#111111", view="front", coords=False)
    faerun.add_scatter(
        safe_name,
        {"x": layout_x, "y": layout_y, "c": y.tolist(), "labels": img_labels},
        colormap="tab10",
        shader="smoothCircle",
        point_scale=2.5,
        max_point_size=10,
        has_legend=(legend_labels is not None),
        categorical=True,
        legend_labels=legend_labels
    )
    faerun.add_tree(f"{safe_name}_tree", {"from": s, "to": t}, point_helper=safe_name, color="#666666")
    faerun.plot(safe_name, template="url_image")
    webbrowser.open(os.path.abspath(f"{safe_name}.html"))

def plot_faerun_highlight_examples(
    name, layout_x, layout_y, s, t, labels_subclusters, img_labels, n_examples=5
):
    """Mapa coloreado por subcluster y resalta ejemplos representativos (puntos más grandes)."""
    unique_labels = sorted([int(lbl) for lbl in np.unique(labels_subclusters) if lbl != -1])
    highlight_idxs = []
    for lbl in unique_labels:
        idxs = np.where(labels_subclusters == lbl)[0]
        if len(idxs) == 0:
            continue
        selected = np.random.choice(idxs, size=min(n_examples, len(idxs)), replace=False)
        highlight_idxs.extend(selected.tolist())

    faerun = Faerun(clear_color="#111111", view="front", coords=False)
    faerun.add_scatter(
        name,
        {"x": layout_x, "y": layout_y, "c": labels_subclusters.tolist(), "labels": img_labels},
        colormap="tab10",
        shader="smoothCircle",
        point_scale=2.0,
        max_point_size=8,
        has_legend=True,
        categorical=True,
        legend_labels=[(int(lbl), f"Subcluster {int(lbl)}") for lbl in unique_labels]
    )

    if highlight_idxs:
        faerun.add_scatter(
            f"{name}_examples",
            {
                "x": [float(layout_x[i]) for i in highlight_idxs],
                "y": [float(layout_y[i]) for i in highlight_idxs],
                "c": [int(labels_subclusters[i]) for i in highlight_idxs],
                "labels": [img_labels[i] for i in highlight_idxs]
            },
            colormap="tab10",
            shader="smoothCircle",
            point_scale=5.0,
            max_point_size=18,
            categorical=True,
            legend_labels=None
        )

    faerun.add_tree(f"{name}_tree", {"from": s, "to": t}, point_helper=name, color="#666666")
    faerun.plot(name, template="url_image")
    webbrowser.open(os.path.abspath(f"{name}.html"))

def show_subcluster_examples(subset_x, labels_subclusters, n_examples=5):
    """Matriz matplotlib con n_examples por subcluster (ignora -1)."""
    unique_labels = [lbl for lbl in np.unique(labels_subclusters) if lbl != -1]
    if len(unique_labels) == 0:
        messagebox.showinfo("Subclusters", "No se detectaron subclusters (todos -1).")
        return

    n_subclusters = len(unique_labels)
    n_cols = n_examples
    n_rows = n_subclusters
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 2.5, n_rows * 2.5))

    # Asegurar formato coherente si n_rows==1 o n_cols==1
    if n_rows == 1:
        axes = np.expand_dims(axes, 0)
    if n_cols == 1:
        axes = np.expand_dims(axes, 1)

    for i, lbl in enumerate(unique_labels):
        idxs = np.where(labels_subclusters == lbl)[0]
        if len(idxs) == 0:
            for j in range(n_cols):
                axes[i, j].axis("off")
            continue
        selected = np.random.choice(idxs, size=min(n_examples, len(idxs)), replace=False)
        for j, idx in enumerate(selected):
            axes[i, j].imshow(subset_x.iloc[idx].values.reshape(28, 28), cmap="gray")
            axes[i, j].set_title(f"Subcluster {int(lbl)}", fontsize=8)
            axes[i, j].axis("off")
        # si hay menos de n_examples, ocultar ejes sobrantes
        for j in range(len(selected), n_cols):
            axes[i, j].axis("off")

    plt.suptitle("Ejemplos representativos por subcluster", fontsize=14)
    plt.tight_layout()
    plt.show()

# -----------------------------------------------------
# Cargar dataset (una vez)
# -----------------------------------------------------
try:
    data = pd.read_csv(CSV_PATH)
except Exception as e:
    messagebox.showerror("Error", f"No se pudo cargar {CSV_PATH}: {e}")
    raise SystemExit(e)

x_all = data.drop("label", axis=1)
y_all = data["label"]

# -----------------------------------------------------
# Funciones que conectan la UI con el procesamiento
# -----------------------------------------------------
def generate_global_tmap():
    status_var.set("Calculando TMAP global... (esto puede tardar)")
    root.update_idletasks()
    try:
        layout_x, layout_y, s, t, _ = compute_tmap(x_all)
        img_labels = encode_images_base64(x_all)
        legend = [(i, n) for i, n in enumerate(LABEL_NAMES)]
        plot_faerun("FashionMNIST_Global", layout_x, layout_y, s, t, y_all, img_labels, legend)
        status_var.set("TMAP global generado.")
    except Exception as e:
        messagebox.showerror("Error TMAP global", str(e))
        status_var.set("Error al generar TMAP global.")

def run_subcluster_pipeline():
    """Lee inputs de la UI, filtra, calcula tmap local, aplica KMeans y visualiza."""
    try:
        lbl = int(entry_label.get())
        if lbl < 0 or lbl > 9:
            raise ValueError("Prenda debe ser un entero entre 0 y 9.")
    except Exception as e:
        messagebox.showerror("Input error", f"Prenda inválida: {e}")
        return

    try:
        sample_display = int(entry_sample.get())
        if sample_display < 0:
            raise ValueError("Tamaño de muestra no puede ser negativo.")
    except Exception as e:
        messagebox.showerror("Input error", f"Tamaño de muestra inválido: {e}")
        return

    try:
        n_clusters = int(entry_k.get())
        if n_clusters <= 0:
            raise ValueError("Cantidad de subclusters debe ser > 0.")
    except Exception as e:
        messagebox.showerror("Input error", f"Cantidad de subclusters inválida: {e}")
        return

    status_var.set(f"Procesando label={lbl} ({LABEL_NAMES[lbl]})...")
    root.update_idletasks()

    # --- Filtrar por prenda seleccionada ---
    subset_mask = (y_all == lbl)
    subset_x = x_all[subset_mask].reset_index(drop=True)
    subset_y = y_all[subset_mask].reset_index(drop=True)
    n_available = len(subset_x)

    if n_available == 0:
        messagebox.showinfo("Sin datos", f"No hay ejemplos para la prenda {lbl} ({LABEL_NAMES[lbl]}).")
        status_var.set("Listo.")
        return

    try:
        # --- TMAP ---
        status_var.set("Calculando TMAP del subset completo...")
        root.update_idletasks()
        layout_x_sub, layout_y_sub, s_sub, t_sub, _ = compute_tmap(subset_x)
        img_labels_sub = encode_images_base64(subset_x)

        # --- KMeans sobre coordenadas TMAP ---
        coords_sub = np.vstack((layout_x_sub, layout_y_sub)).T
        kmeans = KMeans(n_clusters=n_clusters, random_state=RND_STATE)
        labels_subclusters = kmeans.fit_predict(coords_sub)

        # --- Visualización Faerun ---
        status_var.set("Generando Faerun con subclusters (abrirá el navegador)...")
        root.update_idletasks()
        plot_faerun_highlight_examples(
            f"Subclusters_{LABEL_NAMES[lbl]}",
            layout_x_sub,
            layout_y_sub,
            s_sub,
            t_sub,
            labels_subclusters,
            img_labels_sub,
            n_examples=3
        )

        # --- Mostrar ejemplos representativos (controlado por sample_display) ---
        n_examples_show = sample_display if sample_display > 0 else 5
        status_var.set(f"Mostrando {n_examples_show} ejemplos por subcluster...")
        root.update_idletasks()
        show_subcluster_examples(subset_x, labels_subclusters, n_examples=n_examples_show)

        status_var.set("Listo.")
    except Exception as e:
        messagebox.showerror("Error pipeline", str(e))
        status_var.set("Error durante pipeline.")


# -----------------------------------------------------
# Interfaz Tkinter
# -----------------------------------------------------
root = tk.Tk()
root.title("TMAP + Subclusters (Fashion-MNIST)")
root.geometry("520x370")
root.resizable(False, False)

mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.pack(fill="both", expand=True)

# Botón para TMAP global
btn_global = ttk.Button(mainframe, text="Generar TMAP global (abrir navegador)", command=generate_global_tmap)
btn_global.grid(column=0, row=0, columnspan=3, pady=(0,10), sticky="ew")

# Separador
sep = ttk.Separator(mainframe, orient="horizontal")
sep.grid(column=0, row=1, columnspan=3, sticky="ew", pady=(6,10))

# Subcluster inputs
ttk.Label(mainframe, text="Prenda (0-9):").grid(column=0, row=2, sticky="w")
entry_label = ttk.Entry(mainframe, width=8)
entry_label.insert(0, "2")  # default Pullover
entry_label.grid(column=1, row=2, sticky="w")

ttk.Label(mainframe, text="Imágenes de muestra (0 = por defecto (5)):").grid(column=0, row=3, sticky="w")
entry_sample = ttk.Entry(mainframe, width=8)
entry_sample.insert(0, "0")
entry_sample.grid(column=1, row=3, sticky="w")

ttk.Label(mainframe, text="Cantidad subclusters (K):").grid(column=0, row=4, sticky="w")
entry_k = ttk.Entry(mainframe, width=8)
entry_k.insert(0, "3")
entry_k.grid(column=1, row=4, sticky="w")

btn_subcluster = ttk.Button(mainframe, text="Generar subclusters (KMeans)", command=run_subcluster_pipeline)
btn_subcluster.grid(column=0, row=5, columnspan=3, pady=(10,0), sticky="ew")

# Status label
status_var = tk.StringVar(value="Listo.")
status_label = ttk.Label(mainframe, textvariable=status_var, foreground="#007700")
status_label.grid(column=0, row=6, columnspan=3, pady=(12,0), sticky="w")

# Notas
note = ("Nota: los resultados abren en el navegador (Faerun) y las imágenes se muestran\n"
        "en ventanas matplotlib. Si usa muestra, se toma aleatorio reproducible.")
ttk.Label(mainframe, text=note, wraplength=480).grid(column=0, row=7, columnspan=3, pady=(10,0))
leyenda_datos = ("Prendas:\n0: T-shirt/top | 1: Trouser\n2: Pullover | 3: Dress\n4: Coat | 5: Sandal\n6: Shirt | 7: Sneaker\n8: Bag | 9: Ankle boot")
ttk.Label(mainframe, text=leyenda_datos, wraplength=480).grid(column=0, row=9, columnspan=3, pady=(10,0))

# Padding para todos hijos
for child in mainframe.winfo_children():
    child.grid_configure(padx=6, pady=4)

root.mainloop()
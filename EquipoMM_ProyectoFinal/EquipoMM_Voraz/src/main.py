import pygame
import copy
import time
import numpy as np
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import os, heapq, pickle, struct, re
from bitarray import bitarray

# -------------------- Huffman helpers --------------------
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
    if len(heap) == 0:
        return None
    if len(heap) == 1:
        # Edge: un solo caracter, crear nodo padre
        only = heapq.heappop(heap)
        root = NodoHuffman(None, only.frecuencia)
        root.izquierda = only
        return root
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
    if nodo is None:
        return codigos
    if nodo.caracter is not None:
        # Hoja
        codigos[nodo.caracter] = codigo.copy()
    else:
        if nodo.izquierda is not None:
            generar_codigos(nodo.izquierda, codigo + bitarray('0'), codigos)
        if nodo.derecha is not None:
            generar_codigos(nodo.derecha, codigo + bitarray('1'), codigos)
    return codigos

def codificar(texto, codigos):
    resultado = bitarray()
    for c in texto:
        resultado.extend(codigos[c])
    return resultado

def decodificar(codigo_binario, arbol):
    if arbol is None:
        return ""
    # Si el árbol tiene solo una hoja (un solo caracter frecuente):
    if arbol.izquierda is not None and arbol.derecha is None and arbol.izquierda.caracter is not None:
        # todo los bits representan repeticiones de arbol.izquierda.caracter
        return arbol.izquierda.caracter * len(codigo_binario)
    resultado = []
    nodo = arbol
    for bit in codigo_binario:
        nodo = nodo.izquierda if not bit else nodo.derecha
        if nodo is None:
            raise ValueError("Bitstream inválido para el árbol provisto")
        if nodo.caracter is not None:
            resultado.append(nodo.caracter)
            nodo = arbol
    return ''.join(resultado)

def guardar_comprimido(ruta, arbol, bits):
    """
    Serializa el árbol (pickle) con su longitud y luego escribe los bytes del bitarray.
    Formato: [4 bytes: len_arbol][arbol_serializado][bytes del bitarray]
    """
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

def huffman_compress(input_txt_path, output_bin_path):
    with open(input_txt_path, 'r', encoding='utf-8') as f:
        texto = f.read()
    frecuencias = Counter(texto)
    arbol = construir_arbol(frecuencias)
    codigos = generar_codigos(arbol)
    bits = codificar(texto, codigos)
    guardar_comprimido(output_bin_path, arbol, bits)
    return output_bin_path

def huffman_decompress(input_bin_path, output_txt_path):
    arbol, bits = cargar_comprimido(input_bin_path)
    texto = decodificar(bits, arbol)
    with open(output_txt_path, 'w', encoding='utf-8') as f:
        f.write(texto)
    return output_txt_path

# -------------------- Juego / UI / Replay --------------------

# Se crea directorio de replays
os.makedirs("replays", exist_ok=True)

# --- CONFIGURACIÓN DE LA VENTANA ---
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS # Tamaño de cada casilla

# Colores varios
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (128, 0, 0)
GREY = (128, 128, 128)
DARK_GREEN = (0, 128, 0)
YELLOW = (200, 200, 0)

# Iniciamos Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Damas con Al-BePr y Minimax")

# --- LÓGICA DE JUEGO ---
def create_board():
    board = [[0]*COLS for _ in range(ROWS)]
    for r in range(3):
        for c in range((r+1) % 2, COLS, 2):
            board[r][c] = -1
    for r in range(5, 8):
        for c in range((r+1) % 2, COLS, 2):
            board[r][c] = 1
    return board

def draw_board(win, board, selected=None):
    for r in range(ROWS):
        for c in range(COLS):
            color = GREY if (r + c) % 2 else WHITE
            pygame.draw.rect(win, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board[r][c]
            if piece != 0:
                col = RED if piece > 0 else BLACK
                pygame.draw.circle(win, col,
                                   (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 10)
                if abs(piece) == 2:
                    font = pygame.font.SysFont(None, 40)
                    text = font.render("*", True, (255, 215, 0))
                    text_rect = text.get_rect(center=(c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2))
                    win.blit(text, text_rect)
            if selected == (r, c):
                pygame.draw.circle(win, YELLOW,
                                   (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 5, 4)
    pygame.display.update()

def get_all_moves(board, player):
    moves = []
    captures = []
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != 0 and (board[r][c] * player > 0):
                for move in get_piece_moves(board, r, c, player):
                    if abs(move[0][0] - move[1][0]) == 2:
                        captures.append(move)
                    else:
                        moves.append(move)
    return captures if captures else moves

def get_piece_moves(board, r, c, player):
    moves = []
    piece = board[r][c]
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if abs(piece) == 2 else \
                 [(-1, -1), (-1, 1)] if piece == 1 else [(1, -1), (1, 1)]
    for dr, dc in directions:
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < ROWS and 0 <= new_c < COLS and board[new_r][new_c] == 0:
            moves.append(((r, c), (new_r, new_c)))
        jump_r, jump_c = r + 2*dr, c + 2*dc
        if 0 <= jump_r < ROWS and 0 <= jump_c < COLS:
            target = board[r + dr][c + dc]
            if target * piece < 0 and board[jump_r][jump_c] == 0:
                moves.append(((r, c), (jump_r, jump_c)))
    return moves

def make_move(board, move):
    new_board = copy.deepcopy(board)
    (r1, c1), (r2, c2) = move
    player = new_board[r1][c1]
    new_board[r2][c2] = player
    new_board[r1][c1] = 0
    if abs(r2 - r1) == 2:
        mid_r = (r1 + r2) // 2
        mid_c = (c1 + c2) // 2
        new_board[mid_r][mid_c] = 0
    if player == 1 and r2 == 0:
        new_board[r2][c2] = 2
    elif player == -1 and r2 == ROWS - 1:
        new_board[r2][c2] = -2
    return new_board

def is_terminal(board):
    return not get_all_moves(board, 1) or not get_all_moves(board, -1)

def evaluate_board(board):
    return sum(sum(row) for row in board)

# Alpha-beta y minimax con métricas (nodos y profundidad)
def alpha_beta(board, depth, alpha, beta, maximizing_player, current_depth=1):
    nodes_explored = 0
    max_depth_reached = current_depth

    if depth == 0 or is_terminal(board):
        return evaluate_board(board), None, {
            "nodos": 1,
            "profundidad": current_depth
        }

    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_all_moves(board, 1):
            new_board = make_move(board, move)
            evalv, _, metrics = alpha_beta(new_board, depth-1, alpha, beta, False, current_depth+1)
            nodes_explored += metrics["nodos"]
            max_depth_reached = max(max_depth_reached, metrics["profundidad"])
            if evalv > max_eval:
                max_eval, best_move = evalv, move
            alpha = max(alpha, evalv)
            if beta <= alpha:
                break
        return max_eval, best_move, {"nodos": nodes_explored, "profundidad": max_depth_reached}
    else:
        min_eval = float('inf')
        for move in get_all_moves(board, -1):
            new_board = make_move(board, move)
            evalv, _, metrics = alpha_beta(new_board, depth-1, alpha, beta, True, current_depth+1)
            nodes_explored += metrics["nodos"]
            max_depth_reached = max(max_depth_reached, metrics["profundidad"])
            if evalv < min_eval:
                min_eval, best_move = evalv, move
            beta = min(beta, evalv)
            if beta <= alpha:
                break
        return min_eval, best_move, {"nodos": nodes_explored, "profundidad": max_depth_reached}


def minimax(board, depth, maximizing_player, current_depth=1):
    nodes_explored = 0
    max_depth_reached = current_depth

    if depth == 0 or is_terminal(board):
        return evaluate_board(board), None, {
            "nodos": 1,
            "profundidad": current_depth
        }

    best_move = None
    if maximizing_player:
        max_eval = float('-inf')
        for move in get_all_moves(board, -1):
            new_board = make_move(board, move)
            evalv, _, metrics = minimax(new_board, depth-1, False, current_depth+1)
            nodes_explored += metrics["nodos"]
            max_depth_reached = max(max_depth_reached, metrics["profundidad"])
            if evalv > max_eval:
                max_eval, best_move = evalv, move
        return max_eval, best_move, {"nodos": nodes_explored, "profundidad": max_depth_reached}
    else:
        min_eval = float('inf')
        for move in get_all_moves(board, 1):
            new_board = make_move(board, move)
            evalv, _, metrics = minimax(new_board, depth-1, True, current_depth+1)
            nodes_explored += metrics["nodos"]
            max_depth_reached = max(max_depth_reached, metrics["profundidad"])
            if evalv < min_eval:
                min_eval, best_move = evalv, move
        return min_eval, best_move, {"nodos": nodes_explored, "profundidad": max_depth_reached}


# -------------------- Menú / Replay --------------------
def menu():
    run = True
    clock = pygame.time.Clock()
    choice = None
    font = pygame.font.SysFont(None, 50)
    while run:
        clock.tick(30)
        WIN.fill(GREY)
        title = font.render("Damas: Elige IA", True, BLACK)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        ab_rect = pygame.Rect(WIDTH//2 - 100, 250, 200, 60)
        pygame.draw.rect(WIN, DARK_GREEN, ab_rect)
        ab_text = font.render("Alpha-Beta", True, WHITE)
        WIN.blit(ab_text, (ab_rect.x + 8, ab_rect.y + 15))
        mm_rect = pygame.Rect(WIDTH//2 - 100, 350, 200, 60)
        pygame.draw.rect(WIN, DARK_RED, mm_rect)
        mm_text = font.render("Minimax", True, WHITE)
        WIN.blit(mm_text, (mm_rect.x + 30, mm_rect.y + 15))
        replay_rect = pygame.Rect(WIDTH // 2 - 100, 450, 200, 60)
        pygame.draw.rect(WIN, (0, 0, 128), replay_rect)
        replay_text = font.render("Reproducir", True, WHITE)
        WIN.blit(replay_text, (replay_rect.x + 8, replay_rect.y + 15))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if ab_rect.collidepoint(x, y):
                    choice = "alphabeta"
                    run = False
                elif mm_rect.collidepoint(x, y):
                    choice = "minimax"
                    run = False
                elif replay_rect.collidepoint(x, y):
                    from tkinter import filedialog
                    import tkinter as tk
                    root = tk.Tk()
                    root.withdraw()
                    filepath = filedialog.askopenfilename(
                        title = "Seleccionar replay (.txt o .bin)",
                        filetypes = [("Archivos de texto y binarios", "*.txt;*.bin"), ("Textos", "*.txt"), ("Binarios", "*.bin")],
                        initialdir = "replays"
                    )
                    if filepath:
                        # Si es .bin, descomprimir a archivo .txt de trabajo (no borra el .txt original si existe)
                        if filepath.lower().endswith('.bin'):
                            temp_txt = os.path.join("replays", "decompressed_" + os.path.basename(filepath).rsplit('.',1)[0] + ".txt")
                            print("Descomprimiendo", filepath, "->", temp_txt)
                            huffman_decompress(filepath, temp_txt)
                            replay_from(temp_txt)
                        else:
                            replay_from(filepath)
    return choice

def show_winner(winner_text):
    win_font = pygame.font.SysFont(None, 60)
    button_font = pygame.font.SysFont(None, 40)
    button_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 50, 100, 50)
    showing = True
    while showing:
        WIN.fill(GREY)
        text = win_font.render(winner_text, True, BLACK)
        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 80))
        pygame.draw.rect(WIN, YELLOW, button_rect)
        btn_text = button_font.render("OK", True, BLACK)
        WIN.blit(btn_text, (button_rect.x + 28, button_rect.y + 14))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_rect.collidepoint(x, y):
                    showing = False

def replay_from(filename, delay=0.8):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    board = create_board()
    draw_board(WIN, board)
    pygame.display.flip()
    pygame.time.wait(1000)

    moves = []
    for ln in lines:
        nums = re.findall(r"-?\d+", ln)
        if len(nums) == 4:
            r1, c1, r2, c2 = map(int, nums)
            moves.append(((r1, c1), (r2, c2)))

    if not moves:
        print("No se encontraron movimientos en el archivo:", filename)
        return

    clock = pygame.time.Clock()
    move_index = 0
    last_move_time = pygame.time.get_ticks()
    running = True

    while running:
        clock.tick(60)

        # Procesa eventos para que la ventana no se congele
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return

        now = pygame.time.get_ticks()
        if move_index < len(moves) and now - last_move_time >= delay * 1000:
            move = moves[move_index]
            board = make_move(board, move)
            draw_board(WIN, board)
            move_index += 1
            last_move_time = now
            print(f"Replay: movimiento {move_index}/{len(moves)} -> {move}")
        elif move_index >= len(moves):
            print("🎞️ Replay terminado.")
            pygame.time.wait(1000)
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        pygame.display.flip()

def board_to_text(board):
    lines = []
    for row in board:
        lines.append(" ".join(str(cell) for cell in row))
    return "\n".join(lines)

# -------------------- MAIN --------------------
def main(ai_choice):
    board = create_board()
    run = True
    clock = pygame.time.Clock()
    selected = None
    turn = 1  # 1 = jugador, -1 = IA
    ia_times = []
    replay_moves = []

    while run:
        clock.tick(30)
        draw_board(WIN, board, selected)

        if is_terminal(board):
            player_moves = get_all_moves(board, 1)
            ai_moves = get_all_moves(board, -1)
            if not player_moves and ai_moves:
                show_winner("¡Gana la IA!")
            elif not ai_moves and player_moves:
                show_winner("¡Ganaste!")
            else:
                show_winner("Empate")
            run = False
            continue

        # Turno IA
        if turn == -1:
            num_moves = len(get_all_moves(board, -1))
            start_time = time.time()
            if ai_choice == "alphabeta":
                _, move, metrics = alpha_beta(board, 4, float('-inf'), float('inf'), False)
            else:
                _, move, metrics = minimax(board, 4, True)

            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            ia_times.append((num_moves, elapsed_time))

            metrics["tiempo_ms"] = elapsed_time
            metrics["movimientos_posibles"] = num_moves

            print(
                f"Turno IA ({ai_choice}) - Movimientos: {num_moves}, Tiempo: {elapsed_time:.2f} ms, Nodos: {metrics['nodos']}, Profundidad: {metrics['profundidad']}")

            if move:
                board = make_move(board, move)
                replay_moves.append(("IA", move, [row[:] for row in board], metrics))

            turn = 1
            continue

        # Manejo jugador
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif turn == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                if selected:
                    move = (selected, (row, col))
                    if move in get_all_moves(board, 1):
                        board = make_move(board, move)
                        replay_moves.append(("Jugador", move, [row[:] for row in board], None))
                        turn = -1
                    selected = None
                elif board[row][col] > 0:
                    selected = (row, col)

    # === Estadísticas IA (graf) ===
    if ia_times:
        grouped = defaultdict(list)
        for moves, time_ms in ia_times:
            grouped[moves].append(time_ms)
        moves_avg = []
        times_avg = []
        for moves in sorted(grouped.keys()):
            avg_time = np.mean(grouped[moves])
            moves_avg.append(moves)
            times_avg.append(avg_time)
        smoothed_moves = []
        smoothed_times = []
        for i in range(len(moves_avg)):
            smoothed_moves.append(moves_avg[i])
            smoothed_times.append(times_avg[i])
            if i < len(moves_avg) - 1 and moves_avg[i + 1] - moves_avg[i] > 1:
                x_fill = np.arange(moves_avg[i] + 1, moves_avg[i + 1])
                y_fill = np.linspace(times_avg[i], times_avg[i + 1], len(x_fill))
                smoothed_moves.extend(x_fill)
                smoothed_times.extend(y_fill)
        plt.figure(figsize=(8, 4))
        plt.plot(smoothed_moves, smoothed_times, marker='o', linestyle='-', linewidth=2)
        plt.title(f"Complejidad temporal promedio IA ({ai_choice})")
        plt.xlabel("Movimientos posibles (get_all_moves)")
        plt.ylabel("Tiempo promedio (ms)")
        plt.grid(True)
        plt.xlim(min(smoothed_moves) - 1, max(smoothed_moves) + 1)
        plt.show()

    # === Guardado del replay como .txt y compresión a .bin ===
    if replay_moves:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"replay_{ai_choice}_{timestamp}"
        txt_path = os.path.join("replays", f"{filename}.txt")
        bin_path = os.path.join("replays", f"{filename}.bin")

        # Guardar .txt legible
        with open(txt_path, "w", encoding="utf-8") as f:
            for i, (turno, move, board_snapshot, metrics) in enumerate(replay_moves, start=1):
                (r1, c1), (r2, c2) = move
                f.write(f"[Turno {i} - {turno}]\n")
                f.write(f"Movimiento: ({r1}, {c1}) -> ({r2}, {c2})\n")
                if turno == "IA" and metrics:
                    f.write(f"Movimientos posibles: {metrics.get('movimientos_posibles', '-')}\n")
                    f.write(f"Nodos explorados: {metrics.get('nodos', '-')}\n")
                    f.write(f"Profundidad: {metrics.get('profundidad', '-')}\n")
                    f.write(f"Tiempo: {metrics.get('tiempo_ms', 0):.2f} ms\n")
                f.write("Tablero:\n")
                f.write(board_to_text(board_snapshot))
                f.write("\n\n")
        print(f"Replay guardado en {txt_path}")

        # Comprimir a .bin (no borra el .txt)
        try:
            huffman_compress(txt_path, bin_path)
            print(f"Replay comprimido en {bin_path}")
        except Exception as e:
            print("Error al comprimir replay:", e)

    pygame.quit()

if __name__ == "__main__":
    ai_choice = menu()
    if ai_choice:
        main(ai_choice)

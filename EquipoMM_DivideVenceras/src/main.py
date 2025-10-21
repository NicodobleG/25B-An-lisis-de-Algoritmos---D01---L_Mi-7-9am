import pygame
import copy
import time
import matplotlib.pyplot as plt

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
def create_board(): # Creación del tablero
    # Matriz 8 x 8 llena de ceros:
    # Cada número representa una celda:
    # 0: vacía | 1: Ficha del jugador | -1: Ficha de la IA | 2: Reina del jugador | -2: Reina de la IA
    board = [[0]*COLS for _ in range(ROWS)]
    for r in range(3): # Coloca las fichas de la IA (negras) en las tres primeras filas
        for c in range((r+1) % 2, COLS, 2):
            board[r][c] = -1  # IA
    for r in range(5, 8): # Coloca las fichas del jugador (rojas) en las últimas tres filas
        for c in range((r+1) % 2, COLS, 2):
            board[r][c] = 1   # Jugador
    return board # Tablero listo


def draw_board(win, board, selected=None): # Dibuja el tablero y fichas actuales
    win.fill(BLACK) # Pintamos el fondo de negro
    for r in range(ROWS):
        for c in range(COLS):
            color = GREY if (r + c) % 2 else WHITE # Alternamos entre gris y blanco ne el tablero real
            pygame.draw.rect(win, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = board[r][c]
            if piece != 0:
                # color de la ficha
                col = RED if piece > 0 else BLACK # Rojo: jugador | Negro: IA
                pygame.draw.circle(win, col,
                                   (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   SQUARE_SIZE // 2 - 10)

                # 👑 si es reina, dibujar encima la corona
                if abs(piece) == 2:
                    font = pygame.font.SysFont(None, 40)
                    text = font.render("*", True, (255, 215, 0))  # "Corona" dorada encima de la ficha
                    text_rect = text.get_rect(
                        center=(c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2))
                    win.blit(text, text_rect)
            # Si esta ficha está seleccionada, dibuja un borde brillante
            if selected == (r, c):
                pygame.draw.circle(
                    win,
                    YELLOW,  # color del borde
                    (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
                    SQUARE_SIZE // 2 - 5,  # radio ligeramente mayor que la ficha
                    4  # grosor del borde
                )

    pygame.display.update() # Actualiza el tablero


def get_all_moves(board, player): # Devuelve todos los movimientos posibles del jugador indicado
    moves = []
    captures = []
    for r in range(ROWS): #Recorre el tablero
        for c in range(COLS): #Recorre el tablero
            if board[r][c] != 0 and (board[r][c] * player > 0): #Filtra las fichas del jugador actual
                for move in get_piece_moves(board, r, c, player):
                    # Saltos de 2 filas = captura
                    if abs(move[0][0] - move[1][0]) == 2:
                        captures.append(move) #Las capturas son obligatorias, por lo que solo se puede capturar en caso de poderse
                    else:
                        moves.append(move) #Movimiento normal
    return captures if captures else moves



def get_piece_moves(board, r, c, player): #Devuelve movimientos válidos de una ficha específica
    moves = []
    piece = board[r][c]

    # Definir direcciones diagonales
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] if abs(piece) == 2 else \
                 [(-1, -1), (-1, 1)] if piece == 1 else [(1, -1), (1, 1)]
                # En el orden de las condiciones:
                # 1. Las reinas se mueven en todas direcciones
                # 2. Fichas del jugador (1) van hacia arriba
                # 3. Fichas de la IA (-1) van hacia abajo

    for dr, dc in directions:
        new_r, new_c = r + dr, c + dc

        # --- Movimiento simple ---
        if 0 <= new_r < ROWS and 0 <= new_c < COLS and board[new_r][new_c] == 0:
            moves.append(((r, c), (new_r, new_c)))

        # --- Captura ---
        jump_r, jump_c = r + 2*dr, c + 2*dc
        if 0 <= jump_r < ROWS and 0 <= jump_c < COLS:
            target = board[r + dr][c + dc]
            if target * piece < 0 and board[jump_r][jump_c] == 0: # Si hay un enemigo en diagonal y casilla detrás vacía -> Salto válido
                moves.append(((r, c), (jump_r, jump_c)))

    return moves


def make_move(board, move): #Aplica movimiento y devuelve un nuevo tablero
    new_board = copy.deepcopy(board) # Crea una copia profunda para no modificar el original
    (r1, c1), (r2, c2) = move
    player = new_board[r1][c1]

    #Mueve la ficha
    new_board[r2][c2] = player
    new_board[r1][c1] = 0

    # Si fue salto, elimina la ficha comida
    if abs(r2 - r1) == 2:
        mid_r = (r1 + r2) // 2
        mid_c = (c1 + c2) // 2
        new_board[mid_r][mid_c] = 0

    # 👑 Coronación
    if player == 1 and r2 == 0:
        new_board[r2][c2] = 2  # 2 representa una reina blanca
    elif player == -1 and r2 == ROWS - 1:
        new_board[r2][c2] = -2  # -2 representa una reina negra

    return new_board



def is_terminal(board): #El juego termina si no puedes moverte
    return not get_all_moves(board, 1) or not get_all_moves(board, -1)

def evaluate_board(board):
    # Heurística: piezas del jugador - piezas de la IA
    # +1 por ficha del jugador
    # -1 por ficha de la IA
    # Si el resultado es alto, el jugador va ganando
    return sum(sum(row) for row in board)

# --- IA CON ALPHA-BETA ---
def alpha_beta(board, depth, alpha, beta, maximizing_player):
    #Alpha: el mejor valor máximo encontrado hasta ahora por el jugador que maximiza.
    #Beta: el mejor valor mínimo encontrado hasta ahora por el jugador que minimiza.
    #Si en algún momento Beta <= Alpha, se detiene la exploración de esa rama.

    # Si llegamos al fondo del árbol o el juego terminó -> devolvemos una evaluación del tablero
    if depth == 0 or is_terminal(board):
        return evaluate_board(board), None

    best_move = None
    if maximizing_player:  # Jugador
        max_eval = float('-inf')
        for move in get_all_moves(board, 1):
            new_board = make_move(board, move)
            eval, _ = alpha_beta(new_board, depth-1, alpha, beta, False)
            if eval > max_eval:
                max_eval, best_move = eval, move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        # Actualiza Alpha con el mejor valor encontrado hasta ahora y comprueba Beta <= Alpha para cortar ramas
        return max_eval, best_move
    else:  # IA
        min_eval = float('inf')
        for move in get_all_moves(board, -1): #Obtenemos todas las jugadas posibles de la IA con get_all_moves(board, -1)
            new_board = make_move(board, move) #Se simula cada jugada con make_move(), generando un nuevo tablero hipotético
            # Se llama recursivamente al algoritmo para que el jugador responda
            eval, _ = alpha_beta(new_board, depth-1, alpha, beta, True)
            if eval < min_eval:
                min_eval, best_move = eval, move
            beta = min(beta, eval)
            if beta <= alpha:
                break

        # Actualiza Beta con el mejor valor encontrado hasta ahora y comprueba Beta <= Alpha para cortar ramas
        return min_eval, best_move

# --- IA CON MINIMAX ---
def minimax(board, depth, maximizing_player):
    """
    maximizing_player = True -> IA
    maximizing_player = False -> jugador
    """
    if depth == 0 or is_terminal(board):
        return evaluate_board(board), None

    best_move = None

    if maximizing_player:  # IA
        max_eval = float('-inf')
        for move in get_all_moves(board, -1): #Obtenemos todas las jugadas posibles de la IA con get_all_moves(board, -1)
            new_board = make_move(board, move) #Se simula cada jugada con make_move(), generando un nuevo tablero hipotético
            # Se llama recursivamente al algoritmo para que el jugador responda
            eval, _ = minimax(new_board, depth-1, False)
            if eval > max_eval:
                max_eval, best_move = eval, move
        return max_eval, best_move
    else:  # jugador
        max_eval = float('-inf')
        for move in get_all_moves(board, 1):
            new_board = make_move(board, move)
            eval, _ = minimax(new_board, depth-1, True)
            if eval > max_eval:
                max_eval, best_move = eval, move
        return max_eval, best_move

# --- LOOP PRINCIPAL ---
def menu():
    run = True
    clock = pygame.time.Clock()
    choice = None

    font = pygame.font.SysFont(None, 50)

    while run:
        clock.tick(30)
        WIN.fill(GREY)

        # Texto del título
        title = font.render("Damas: Elige IA", True, BLACK)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        # Botón Alpha-Beta
        ab_rect = pygame.Rect(WIDTH//2 - 100, 250, 200, 60)
        pygame.draw.rect(WIN, DARK_GREEN, ab_rect)
        ab_text = font.render("Alpha-Beta", True, WHITE)
        WIN.blit(ab_text, (ab_rect.x + 8, ab_rect.y + 15))

        # Botón Minimax
        mm_rect = pygame.Rect(WIDTH//2 - 100, 350, 200, 60)
        pygame.draw.rect(WIN, DARK_RED, mm_rect)
        mm_text = font.render("Minimax", True, WHITE)
        WIN.blit(mm_text, (mm_rect.x + 30, mm_rect.y + 15))

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

    return choice

def show_winner(winner_text): # Se muestra el resultado del juego
    win_font = pygame.font.SysFont(None, 60)
    button_font = pygame.font.SysFont(None, 40)

    button_rect = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 + 50, 100, 50)

    showing = True
    while showing:
        WIN.fill(GREY)

        # Texto de ganador
        text = win_font.render(winner_text, True, BLACK)
        WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 80))

        # Botón OK
        pygame.draw.rect(WIN, YELLOW, button_rect)
        btn_text = button_font.render("OK", True, BLACK)
        WIN.blit(btn_text, (button_rect.x + 28, button_rect.y + 14))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if button_rect.collidepoint(x, y):
                    showing = False


def main(ai_choice):
    board = create_board()
    run = True
    clock = pygame.time.Clock()
    selected = None
    turn = 1  # 1 = jugador, -1 = IA
    ia_times = []

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

        if turn == -1:  # turno IA
            start_time = time.time()
            # Selección de IA
            if ai_choice == "alphabeta":
                _, move = alpha_beta(board, 4, float('-inf'), float('inf'), False)
            else:  # minimax
                _, move = minimax(board, 4, True)

            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            ia_times.append(elapsed_time)

            print(f"Tiempo de respuesta ({ai_choice}): {elapsed_time:.3f} ms")

            if move:
                board = make_move(board, move)
            turn = 1
            continue

        # Manejo del jugador
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
                        turn = -1
                    selected = None
                elif board[row][col] > 0:
                    selected = (row, col)

    # === Al finalizar el juego ===
    if ia_times:
        plt.figure(figsize=(8, 4))
        plt.plot(range(1, len(ia_times) + 1), ia_times, marker='o')
        plt.title(f"Tiempos de respuesta de la IA ({ai_choice})")
        plt.xlabel("Número de turno de la IA")
        plt.ylabel("Tiempo (ms)")
        plt.grid(True)
        plt.show()

    pygame.quit()

if __name__ == "__main__":
    ai_choice = menu()
    if ai_choice:
        main(ai_choice)

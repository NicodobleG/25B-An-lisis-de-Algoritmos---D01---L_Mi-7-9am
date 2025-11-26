import tkinter as tk
import math

TARGET = 21

# ----------- Minimax -----------
def minimax(total, maximizing_player):
    if total == TARGET:
        return -1 if maximizing_player else 1  # si alguien llega justo, gana el que acaba de mover

    if maximizing_player:  # turno de la IA
        best_score = -math.inf
        for move in [1, 2, 3]:
            if total + move <= TARGET:
                score = minimax(total + move, False)
                best_score = max(best_score, score)
        return best_score
    else:  # turno humano
        best_score = math.inf
        for move in [1, 2, 3]:
            if total + move <= TARGET:
                score = minimax(total + move, True)
                best_score = min(best_score, score)
        return best_score

def best_move(total):
    best_score = -math.inf
    move_chosen = None
    for move in [1, 2, 3]:
        if total + move <= TARGET:
            score = minimax(total + move, False)
            if score > best_score:
                best_score = score
                move_chosen = move
    return move_chosen

# ----------- Interfaz Tkinter -----------
class Game21:
    def __init__(self, root):
        self.root = root
        self.total = 0

        root.title("Juego del 21 - Minimax")
        root.geometry("400x300")

        self.label = tk.Label(root, text="Juego del 21\nQuien llegue a 21 gana.", font=("Arial", 14))
        self.label.pack(pady=10)

        self.total_label = tk.Label(root, text=f"Total: {self.total}", font=("Arial", 16))
        self.total_label.pack(pady=10)

        self.message = tk.Label(root, text="Tu turno", font=("Arial", 12))
        self.message.pack(pady=5)

        # Botones para sumar 1, 2, 3
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(pady=10)

        for move in [1, 2, 3]:
            btn = tk.Button(self.buttons_frame, text=f"+{move}", font=("Arial", 14),
                            command=lambda m=move: self.player_move(m))
            btn.pack(side=tk.LEFT, padx=10)

    def player_move(self, move):
        if self.total + move > TARGET:
            self.message.config(text="Movimiento inválido. Intenta otra vez.")
            return

        self.total += move
        self.update_total()

        if self.total == TARGET:
            self.message.config(text="¡Ganaste! 🎉")
            self.disable_buttons()
            return

        # Turno computadora
        self.root.after(1000, self.computer_turn)

    def computer_turn(self):
        self.message.config(text="Turno de la computadora...")
        move = best_move(self.total)
        self.total += move
        self.update_total()

        if self.total == TARGET:
            self.message.config(text=f"La computadora suma {move} y gana 😎")
            self.disable_buttons()
        else:
            self.message.config(text=f"La computadora sumó {move}. Tu turno.")

    def update_total(self):
        self.total_label.config(text=f"Total: {self.total}")

    def disable_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    game = Game21(root)
    root.mainloop()

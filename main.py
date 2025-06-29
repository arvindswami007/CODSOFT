import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import random
import threading
import time
from playsound import playsound
import os

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("300x400")
        self.window.resizable(False, False)
        self.window.withdraw()
        self.player_name = simpledialog.askstring("Welcome!", "Enter your name:", parent=self.window) or "Player"
        self.window.deiconify()
        self.window.title("Tic-Tac-Toe AI 🎮")
        self.board = [[""] * 3 for _ in range(3)]
        self.score = {self.player_name: 0, "AI": 0, "Tie": 0}
        self.difficulty = tk.StringVar(value="Hard")
        self.x_img = ImageTk.PhotoImage(Image.open("x.png").resize((64, 64)))
        self.o_img = ImageTk.PhotoImage(Image.open("o.png").resize((64, 64)))
        self.bg_img = ImageTk.PhotoImage(Image.open("background.png").resize((300, 400)))
        self.bg_label = tk.Label(self.window, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.timer = 10
        self.buttons = []
        self.timer_label = None
        self.timer_thread = None
        self.build_ui()
        self.window.mainloop()

    def build_ui(self):
        tk.Label(self.window, text="Difficulty:", bg="#f0f8ff").place(x=10, y=10)
        for i, level in enumerate(["Easy", "Medium", "Hard"]):
            tk.Radiobutton(self.window, text=level, variable=self.difficulty, value=level, bg="#f0f8ff").place(x=90+i*70, y=10)

        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.window, width=64, height=64, command=lambda r=i, c=j: self.human_move(r, c))
                btn.place(x=10 + j*90, y=50 + i*90)
                row.append(btn)
            self.buttons.append(row)

        self.timer_label = tk.Label(self.window, text="Time left: 10s", fg="red", bg="#f0f8ff")
        self.timer_label.place(x=90, y=330)

        self.score_label = tk.Label(self.window, text=self.get_score_text(), fg="blue", bg="#f0f8ff")
        self.score_label.place(x=30, y=360)

    def get_score_text(self):
        return f"{self.player_name}: {self.score[self.player_name]} | AI: {self.score['AI']} | Ties: {self.score['Tie']}"

    def reset_timer(self):
        self.timer = 10
        if self.timer_thread and self.timer_thread.is_alive():
            return
        self.timer_thread = threading.Thread(target=self.countdown)
        self.timer_thread.start()

    def countdown(self):
        while self.timer > 0:
            self.timer_label.config(text=f"Time left: {self.timer}s")
            time.sleep(1)
            self.timer -= 1
        if self.timer == 0:
            playsound("timeout.wav", block=False)
            messagebox.showinfo("Time’s up!", "You were too slow! AI moves now.")
            self.ai_turn()

    def human_move(self, r, c):
        if self.board[r][c] or self.check_winner():
            return
        self.board[r][c] = "X"
        self.buttons[r][c].config(image=self.x_img, state="disabled")
        playsound("move.wav", block=False)
        self.reset_timer()
        if (winner := self.check_winner()):
            self.end_game(winner)
        else:
            self.window.after(400, self.ai_turn)

    def ai_turn(self):
        if self.check_winner():
            return
        r, c = self.pick_move()
        if r is not None:
            self.board[r][c] = "O"
            self.buttons[r][c].config(image=self.o_img, state="disabled")
        if (winner := self.check_winner()):
            self.end_game(winner)

    def pick_move(self):
        empty = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        if self.difficulty.get() == "Easy":
            return random.choice(empty) if empty else (None, None)
        if self.difficulty.get() == "Medium" and random.random() < 0.4:
            return random.choice(empty) if empty else (None, None)

        def score(board, is_max):
            winner = self.check_winner(board)
            if winner == "AI": return 1
            if winner == self.player_name: return -1
            if winner == "Tie": return 0

            best = -float("inf") if is_max else float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = "O" if is_max else "X"
                        s = score(board, not is_max)
                        board[i][j] = ""
                        best = max(best, s) if is_max else min(best, s)
            return best

        best_val = -float("inf")
        move = None
        for i, j in empty:
            self.board[i][j] = "O"
            val = score(self.board, False)
            self.board[i][j] = ""
            if val > best_val:
                best_val = val
                move = (i, j)
        return move

    def check_winner(self, board=None):
        b = board if board else self.board
        for i in range(3):
            if b[i][0] and b[i][0] == b[i][1] == b[i][2]: return self.translate_winner(b[i][0])
            if b[0][i] and b[0][i] == b[1][i] == b[2][i]: return self.translate_winner(b[0][i])
        if b[0][0] and b[0][0] == b[1][1] == b[2][2]: return self.translate_winner(b[0][0])
        if b[0][2] and b[0][2] == b[1][1] == b[2][0]: return self.translate_winner(b[0][2])
        if all(cell for row in b for cell in row): return "Tie"
        return None

    def translate_winner(self, symbol):
        return self.player_name if symbol == "X" else "AI"

    def end_game(self, winner):
        self.score[winner] += 1
        self.score_label.config(text=self.get_score_text())
        if winner != "Tie":
            playsound("win.wav", block=False)
        msg = "It's a Tie!" if winner == "Tie" else f"{winner} wins!"
        again = messagebox.askyesno("Game Over", f"{msg}\nPlay again?")
        if again:
            self.reset()
        else:
            self.window.destroy()

    def reset(self):
        self.board = [[""] * 3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(image=None, state="normal")
        self.reset_timer()

if __name__ == "__main__":
    TicTacToe()
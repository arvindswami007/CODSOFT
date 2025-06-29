import tkinter as tk
from tkinter import messagebox
import time
import threading
def print_board(board):
    for row in board:
        print("|".join(row))
        print("-" * 5)

def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]
def check_winner(board):
    # Rows, columns and diagonals
    lines = []

    # Rows & columns
    for i in range(3):
        lines.append(board[i])  # rows
        lines.append([board[0][i], board[1][i], board[2][i]])  # cols

    # Diagonals
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line == ["X", "X", "X"]:
            return "X"
        elif line == ["O", "O", "O"]:
            return "O"
    
    # Check for tie
    if all(cell != " " for row in board for cell in row):
        return "Tie"

    return None
def human_move(board):
    while True:
        try:
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter col (0-2): "))
            if board[row][col] == " ":
                board[row][col] = "X"
                break
            else:
                print("Cell is already taken.")
        except:
            print("Invalid input. Try again.")
def minimax(board, depth, is_maximizing):
    result = check_winner(board)
    if result == "X":
        return -1
    elif result == "O":
        return 1
    elif result == "Tie":
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    score = minimax(board, depth + 1, False)
                    board[i][j] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"
                    score = minimax(board, depth + 1, True)
                    board[i][j] = " "
                    best_score = min(score, best_score)
        return best_score
def ai_move(board):
    best_score = -float("inf")
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        board[move[0]][move[1]] = "O"
def play_game():
    board = create_board()
    print_board(board)

    while True:
        human_move(board)
        print_board(board)
        if check_winner(board):
            break

        ai_move(board)
        print("AI moved:")
        print_board(board)
        if check_winner(board):
            break

    winner = check_winner(board)
    if winner == "Tie":
        print("It's a tie!")
    else:
        print(f"{winner} wins!")

play_game()
import random

def check_winner(board):
    for i in range(3):
        if board[i][0] != "" and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] != "" and board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    if all(board[i][j] != "" for i in range(3) for j in range(3)):
        return "Tie"
    return None

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == "O": return 1
    elif winner == "X": return -1
    elif winner == "Tie": return 0

    if is_maximizing:
        best = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "O"
                    score = minimax(board, False)
                    board[i][j] = ""
                    best = max(score, best)
        return best
    else:
        best = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = "X"
                    score = minimax(board, True)
                    board[i][j] = ""
                    best = min(score, best)
        return best

def ai_move(board, difficulty):
    best_score = -float("inf")
    move = None

    available = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]

    if difficulty == "Easy":
        return random.choice(available)
    elif difficulty == "Medium" and random.random() < 0.5:
        return random.choice(available)

    for i, j in available:
        board[i][j] = "O"
        score = minimax(board, False)
        board[i][j] = ""
        if score > best_score:
            best_score = score
            move = (i, j)
    return move
class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe AI")
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = [[None]*3 for _ in range(3)]
        self.difficulty = tk.StringVar(value="Hard")
        self.timer_label = None
        self.timer = 10
        self.timer_thread = None
        self.create_widgets()
        self.window.mainloop()

    def create_widgets(self):
        tk.Label(self.window, text="Select Difficulty:").grid(row=0, column=0, columnspan=3)
        for i, level in enumerate(["Easy", "Medium", "Hard"]):
            tk.Radiobutton(self.window, text=level, variable=self.difficulty, value=level).grid(row=1, column=i)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.window, text="", font=('Helvetica', 32), width=5, height=2,
                                command=lambda row=i, col=j: self.human_move(row, col))
                btn.grid(row=i+2, column=j)
                self.buttons[i][j] = btn

        self.timer_label = tk.Label(self.window, text="Time left: 10", font=("Arial", 12), fg="red")
        self.timer_label.grid(row=5, column=0, columnspan=3)

    def reset_timer(self):
        self.timer = 10
        if self.timer_thread and self.timer_thread.is_alive():
            return
        self.timer_thread = threading.Thread(target=self.countdown)
        self.timer_thread.start()

    def countdown(self):
        while self.timer > 0:
            self.timer_label.config(text=f"Time left: {self.timer}")
            time.sleep(1)
            self.timer -= 1
        if self.timer == 0:
            messagebox.showinfo("Time’s up!", "You took too long! AI is playing.")
            self.make_ai_move()

    def human_move(self, row, col):
        if self.board[row][col] == "" and check_winner(self.board) is None:
            self.board[row][col] = "X"
            self.buttons[row][col].config(text="X", state="disabled")
            self.reset_timer()
            result = check_winner(self.board)
            if result:
                self.end_game(result)
            else:
                self.window.after(500, self.make_ai_move)

    def make_ai_move(self):
        if check_winner(self.board): return
        move = ai_move(self.board, self.difficulty.get())
        if move:
            i, j = move
            self.board[i][j] = "O"
            self.buttons[i][j].config(text="O", state="disabled")
        result = check_winner(self.board)
        if result:
            self.end_game(result)

    def end_game(self, winner):
        msg = "It's a tie!" if winner == "Tie" else f"{winner} wins!"
        messagebox.showinfo("Game Over", msg)
        self.window.destroy()
if __name__ == "__main__":
    TicTacToeGUI()

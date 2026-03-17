import tkinter as tk
import numpy as np
import random

class ModernTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe - Modern Edition")
        self.root.configure(bg="#1e1e1e")

        self.board = np.full((3, 3), " ")
        self.player = "X"
        self.computer = "O"

        self.player_score = 0
        self.computer_score = 0

        self.create_widgets()

    def create_widgets(self):
        self.title_label = tk.Label(self.root, text="Tic Tac Toe",
                                    font=("Segoe UI", 24, "bold"),
                                    fg="white", bg="#1e1e1e")
        self.title_label.pack(pady=10)

        self.score_label = tk.Label(self.root,
                                    text="Player: 0  |  Computer: 0",
                                    font=("Segoe UI", 14),
                                    fg="#00ffcc", bg="#1e1e1e")
        self.score_label.pack()

        self.frame = tk.Frame(self.root, bg="#1e1e1e")
        self.frame.pack(pady=20)

        self.buttons = [[None]*3 for _ in range(3)]

        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.frame,
                                text=" ",
                                font=("Segoe UI", 28, "bold"),
                                width=4, height=2,
                                bg="#2d2d2d",
                                fg="white",
                                activebackground="#3d3d3d",
                                bd=0,
                                command=lambda r=i, c=j: self.player_move(r, c))
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

        self.restart_btn = tk.Button(self.root,
                                     text="Restart Game",
                                     font=("Segoe UI", 12),
                                     bg="#00ffcc",
                                     fg="black",
                                     bd=0,
                                     command=self.restart_game)
        self.restart_btn.pack(pady=10)

    def player_move(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.player
            self.buttons[row][col].config(text=self.player, fg="#00ffcc")

            if self.check_winner(self.player):
                self.player_score += 1
                self.update_score()
                self.show_result("You Win!")
                return

            if self.is_draw():
                self.show_result("Draw!")
                return

            self.root.after(400, self.computer_move)

    def computer_move(self):
        for row, col in self.get_empty_cells():
            self.board[row][col] = self.computer
            if self.check_winner(self.computer):
                self.update_button(row, col)
                self.computer_score += 1
                self.update_score()
                self.show_result("Computer Wins!")
                return
            self.board[row][col] = " "

        for row, col in self.get_empty_cells():
            self.board[row][col] = self.player
            if self.check_winner(self.player):
                self.board[row][col] = self.computer
                self.update_button(row, col)
                return
            self.board[row][col] = " "

        row, col = random.choice(self.get_empty_cells())
        self.board[row][col] = self.computer
        self.update_button(row, col)

        if self.check_winner(self.computer):
            self.computer_score += 1
            self.update_score()
            self.show_result("Computer Wins!")
        elif self.is_draw():
            self.show_result("Draw!")

    def update_button(self, row, col):
        self.buttons[row][col].config(text=self.computer, fg="#ff4d4d")

    def get_empty_cells(self):
        return list(zip(*np.where(self.board == " ")))

    def check_winner(self, symbol):
        for i in range(3):
            if all(self.board[i, :] == symbol):
                return True
            if all(self.board[:, i] == symbol):
                return True

        if all(np.diag(self.board) == symbol):
            return True
        if all(np.diag(np.fliplr(self.board)) == symbol):
            return True

        return False

    def is_draw(self):
        return not np.any(self.board == " ")

    def update_score(self):
        self.score_label.config(
            text=f"Player: {self.player_score}  |  Computer: {self.computer_score}"
        )

    def show_result(self, message):
        result = tk.Toplevel(self.root)
        result.configure(bg="#1e1e1e")
        result.title("Game Over")

        tk.Label(result, text=message,
                 font=("Segoe UI", 18, "bold"),
                 fg="white", bg="#1e1e1e").pack(pady=20)

        tk.Button(result, text="Play Again",
                  font=("Segoe UI", 12),
                  bg="#00ffcc", fg="black",
                  bd=0,
                  command=lambda: [result.destroy(), self.restart_game()]
                  ).pack(pady=10)

    def restart_game(self):
        self.board = np.full((3, 3), " ")
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=" ")
root = tk.Tk()
app = ModernTicTacToe(root)
root.mainloop()

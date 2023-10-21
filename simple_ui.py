import tkinter as tk
import numpy as np

class TicTacToe:
    def __init__(self):
        self.size_of_board = 500
        self.symbol_size = (self.size_of_board / 3 - self.size_of_board / 8) / 2
        self.symbol_thickness = 35
        self.symbol_X_color = '#001524'
        self.symbol_O_color = '#D6CC99'
        self.green_color = '#445D48'
        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

        self.window = tk.Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = tk.Canvas(self.window, width=self.size_of_board, height=self.size_of_board)
        self.canvas.pack()

        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.initialize_game()
    
    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * self.size_of_board / 3, 0, (i + 1) * self.size_of_board / 3, self.size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * self.size_of_board / 3, self.size_of_board, (i + 1) * self.size_of_board / 3)

    def initialize_game(self):
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))
        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False
        
    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    def draw_symbol(self, logical_position, symbol_color, symbol):
        logical_position = np.array(logical_position, dtype=int)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        if symbol == 'X':
            self.canvas.create_line(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                                    grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size,
                                    width=self.symbol_thickness, fill=symbol_color)
            self.canvas.create_line(grid_position[0] - self.symbol_size, grid_position[1] + self.symbol_size,
                                    grid_position[0] + self.symbol_size, grid_position[1] - self.symbol_size,
                                    width=self.symbol_thickness, fill=symbol_color)
        else:
            self.canvas.create_oval(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                                    grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size,
                                    width=self.symbol_thickness, outline=symbol_color)

    def display_gameover(self):
        global X_score, O_score, tie_score
        
        #delay for a few sewingds before showing game over
        self.canvas.update()
        self.canvas.after(500)
        
        if self.X_wins:
            self.X_score += 1
            text = 'X wins!'
            color = self.symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'O wins!'
            color = self.symbol_O_color
        else:
            self.tie_score += 1
            text = "It's a tie!"
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(self.size_of_board / 2, self.size_of_board / 3, font="cmr 50 bold", fill=color, text=text)

        score_text = "Scores\n"
        self.canvas.create_text(self.size_of_board / 2, 5 * self.size_of_board / 8, font="cmr 30 bold",
                                fill=self.green_color, text=score_text)

        score_text = f"Player X: {self.X_score}\nPlayer O: {self.O_score}\nTie: {self.tie_score}"
        self.canvas.create_text(self.size_of_board / 2, 3 * self.size_of_board / 4, font="cmr 20 bold",
                                fill=self.green_color, text=score_text)

        self.reset_board = True
        score_text = "Click to play again"
        self.canvas.create_text(self.size_of_board / 2, 15 * self.size_of_board / 16, font="cmr 20 bold",
                                fill=self.green_color, text=score_text)

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (self.size_of_board / 3)*logical_position + self.size_of_board/6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position//(self.size_of_board/3), dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0], logical_position[1]] != 0

    def is_winner(self, player):
        player_val = -1 if player == 'X' else 1

        for i in range(3):
            if all(self.board_status[i] == player_val) or all(self.board_status[:, i] == player_val):
                return True

        if np.all(np.diag(self.board_status) == player_val) or np.all(np.diag(np.fliplr(self.board_status)) == player_val):
            return True

        return False

    def is_tie(self):
        return not np.any(self.board_status == 0)

    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')
        if not self.O_wins:
            self.tie = self.is_tie()
            

        return self.X_wins or self.O_wins or self.tie

    def click(self, event):
        if self.reset_board:
            self.canvas.delete("all")
            self.initialize_board()
            self.initialize_game()
            self.reset_board = False
        else:
            if not self.reset_board:
                grid_position = [event.x, event.y]
                logical_position = self.convert_grid_to_logical_position(grid_position)

                if not self.is_grid_occupied(logical_position):
                    if self.player_X_turns:
                        self.draw_symbol(logical_position, self.symbol_X_color, 'X')
                        self.board_status[logical_position[0], logical_position[1]] = -1
                        self.player_X_turns = not self.player_X_turns
                    else:
                        self.draw_symbol(logical_position, self.symbol_O_color, 'O')
                        self.board_status[logical_position[0], logical_position[1]] = 1
                        self.player_X_turns = not self.player_X_turns

                    if self.is_gameover():
                        self.display_gameover()

if __name__ == "__main__":
    game_instance = TicTacToe()
    game_instance.mainloop()


import random

# File Writing Module
def file_write(string, file_path):
    with open(file_path, 'w') as file:
        file.write(string)

# Game Board Module
class Board:
    def __init__(self, size=15):
        self.size = size
        self.board = [['.' for _ in range(size)] for _ in range(size)]
    
    def display(self):
        for row in self.board:
            print(' '.join(row))
    
    def is_valid_move(self, x, y):
        return 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == '.'
    
    def place_move(self, x, y, player):
        if self.is_valid_move(x, y):
            self.board[x][y] = player
            return True
        return False
    
    def check_win(self, player):
        # Check horizontal, vertical, and two diagonal directions
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == player:
                    for dx, dy in directions:
                        if self.check_direction(x, y, dx, dy, player):
                            return True
        return False
    
    def check_direction(self, x, y, dx, dy, player):
        count = 0
        for _ in range(5):
            if 0 <= x < self.size and 0 <= y < self.size and self.board[x][y] == player:
                count += 1
            else:
                break
            x += dx
            y += dy
        return count == 5

# Player Module
class HumanPlayer:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def get_move(self):
        x, y = map(int, input("Enter your move (row and column): ").split())
        return x, y

class AIPlayer:
    def __init__(self, symbol, difficulty):
        self.symbol = symbol
        self.difficulty = difficulty
    
    def get_move(self, board):
        ai = AI(self.difficulty)
        return ai.get_best_move(board)

# AI Module
class AI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
    
    def get_best_move(self, board):
        if self.difficulty == 'easy':
            return self.random_move(board)
        elif self.difficulty == 'medium':
            return self.minimax_move(board, depth=2)
        elif self.difficulty == 'hard':
            return self.minimax_move(board, depth=4)
    
    def random_move(self, board):
        empty_cells = [(x, y) for x in range(board.size) for y in range(board.size) if board.is_valid_move(x, y)]
        return random.choice(empty_cells)
    
    def minimax_move(self, board, depth):
        # Simplified Minimax for demonstration purposes
        best_score = float('-inf')
        best_move = None
        for x in range(board.size):
            for y in range(board.size):
                if board.is_valid_move(x, y):
                    board.place_move(x, y, 'O')
                    score = self.minimax(board, depth - 1, False)
                    board.place_move(x, y, '.')
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
        return best_move
    
    def minimax(self, board, depth, is_maximizing):
        if board.check_win('O'):
            return 1
        if board.check_win('X'):
            return -1
        if depth == 0:
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for x in range(board.size):
                for y in range(board.size):
                    if board.is_valid_move(x, y):
                        board.place_move(x, y, 'O')
                        score = self.minimax(board, depth - 1, False)
                        board.place_move(x, y, '.')
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for x in range(board.size):
                for y in range(board.size):
                    if board.is_valid_move(x, y):
                        board.place_move(x, y, 'X')
                        score = self.minimax(board, depth - 1, True)
                        board.place_move(x, y, '.')
                        best_score = min(score, best_score)
            return best_score

# Game Controller Module
class GameController:
    def __init__(self):
        self.board = Board()
        self.human = HumanPlayer('X')
        self.ai = AIPlayer('O', 'medium')
    
    def play_game(self):
        current_player = self.human
        while True:
            self.board.display()
            if isinstance(current_player, HumanPlayer):
                x, y = current_player.get_move()
            else:
                x, y = current_player.get_move(self.board)
            
            if self.board.place_move(x, y, current_player.symbol):
                if self.board.check_win(current_player.symbol):
                    self.board.display()
                    print(f"Player {current_player.symbol} wins!")
                    file_write(f"Player {current_player.symbol} wins!", "result.txt")
                    break
                current_player = self.ai if current_player == self.human else self.human
            else:
                print("Invalid move. Try again.")

# Run the game
if __name__ == "__main__":
    game = GameController()
    game.play_game()

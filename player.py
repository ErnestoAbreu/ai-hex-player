from main import Player, HexBoard
from collections import deque

class My_Player(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)
        
    def bfs01(self, board: HexBoard, player_id: int) -> int:
        q = deque()
        
        mark = [[False for _ in range(board.size)] for _ in range(board.size)]
        
        if player_id == 1:
            col = 0
            for row in range(board.size):
                if board.board[row][col] == 1:
                    q.appendleft((row, col, 0))
                else: 
                    q.append((row, col, 1))
        else:
            row = 0
            for col in range(board.size):
                if board.board[row][col] == 2:
                    q.appendleft((row, col, 0))
                else: 
                    q.append((row, col, 1))
                    
        while len(q) != 0:
            row, col, dist = q.popleft()
            
            if (player_id == 1 and col == board.size-1) or (player_id == 2 and row == board.size-1):
                return dist
            
            movr = [0,0,-1,1,-1,1]
            movc = [-1,1,0,0,1,-1]
            for i in range(6):
                new_row = row + movr[i]
                new_col = col + movc[i]
                
                if(0 <= new_row < board.size and 0 <= new_col < board.size and not mark[new_row][new_col]):
                    mark[new_row][new_col] = True
                    if(board.board[new_row][new_col] == player_id):
                        q.appendleft((new_row, new_col, dist))
                    elif(board.board[new_row][new_col] == 0):
                        q.append((new_row, new_col, dist+1))
                        
        
    def eval(self, board: HexBoard) -> float:
        return self.bfs01(board, self.player_id) - self.bfs01(board, 2 if self.player_id == 1 else 1)
        
    def minimax(self, board: HexBoard, depth: int, alpha: float, beta: float, maximizing: bool, player: int, row: int = -1, col: int = -1) -> tuple:
        if row != -1 and col != -1:
            board.place_piece(row, col, player)
        
        if depth == 0 or board.check_connection(1) or board.check_connection(2):
            return (self.eval(board), row, col)
        
        if maximizing:
            max_eval = (float('-inf'), row, col)
            for move in board.get_possible_moves():
                eval, _, _ = self.minimax(board.clone(), depth-1, alpha, beta, False, 2 if player == 1 else 1, move[0], move[1])
                max_eval = max(max_eval, (eval, move[0], move[1]))
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = (float('inf'), row, col)
            for move in board.get_possible_moves():
                eval, _, _ = self.minimax(board.clone(), depth-1, alpha, beta, True, 2 if player == 1 else 1, move[0], move[1])
                min_eval = min(min_eval, (eval, move[0], move[1]))
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
    def play(self, board: HexBoard) -> tuple:
        if self.player_id == 1 and len(board.get_possible_moves()) == board.size**2:
            return (board.size//2, board.size//2)
        
        score, row, col = self.minimax(board.clone(), 2, float('-inf'), float('inf'), True, self.player_id)
        
        return (row, col)
        
        
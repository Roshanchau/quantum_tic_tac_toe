import random

# Function to print the Tic-Tac-Toe board
def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

# Function to check if a player has won
def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

# Function to check if the board is full
def check_draw(board):
    return all(cell != ' ' for row in board for cell in row)

# Function to make the AI's move using minimax algorithm with alpha-beta pruning
def ai_move(board):
    for _ in range(2):  # AI makes two moves
        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, 0, False, float('-inf'), float('inf'))
                    board[i][j] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        board[best_move[0]][best_move[1]] = 'O'

# Minimax algorithm for AI decision making with alpha-beta pruning
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_win(board, 'O'):
        return 1
    elif check_win(board, 'X'):
        return -1
    elif check_draw(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

# Main function to run the game
def play_game():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe! You are X, and the AI is O.")
    print_board(board)

    while True:
        # Player's move
        for _ in range(2):
            while True:
                row = int(input("Enter row (0, 1, or 2): "))
                col = int(input("Enter column (0, 1, or 2): "))
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    break
                else:
                    print("That spot is already taken. Try again.")
            print_board(board)

            if check_win(board, 'X'):
                print("Congratulations! You win!")
                return
            elif check_draw(board):
                print("It's a draw!")
                return

        # AI's move
        print("AI's turn:")
        ai_move(board)
        print_board(board)

        if check_win(board, 'O'):
            print("AI wins! Better luck next time.")
            return
        elif check_draw(board):
            print("It's a draw!")
            return

# Start the game
play_game()

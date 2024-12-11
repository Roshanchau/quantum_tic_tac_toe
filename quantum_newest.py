from termcolor import colored, cprint
import json
from qiskit import *
import qiskit
# from qiskit.tools.monitor import job_monitor
import copy
import pygame
import random
# 0.45.1
# 0.13.2
# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_COLOR = (255, 255, 255)
LINE_WIDTH = 5
GRID_SIZE = 3 

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)

# Set up the display window
screen = pygame.display.set_mode((500, 550))
pygame.display.set_caption("3x3 Grid")

previous_board_coordinates = [[0, 0, 0] for i in range(3)]

previous_board_coordinate = [[0, 0, 0] for i in range(3)]


def draw_grid():
    # Draw vertical lines
    for i in range(1, GRID_SIZE+2):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (i * WIDTH // GRID_SIZE, 100),
            (i * WIDTH // GRID_SIZE, HEIGHT+100),
            LINE_WIDTH,
        )
    
    # Draw horizontal lines
    for i in range(1, GRID_SIZE+2):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (100, i * HEIGHT // GRID_SIZE),
            (WIDTH+100, i * HEIGHT // GRID_SIZE),
            LINE_WIDTH,
        )


def board_coordinates():
    return [[0,0,0] for i in range(3)]

def choose_player():
    global x_turn
    rect = pygame.draw.rect(screen, (160,32,240),(50, HEIGHT + 150, WIDTH+100, 70), border_radius=10)
    font = pygame.font.Font('freesansbold.ttf', 32)
    WHITE = (255, 255, 255)  # Define the color "green"
    text = font.render('Choose X or O:', True, WHITE)
    textRect = text.get_rect()
    textRect.center = (200,480)
    screen.blit(text, textRect)

    x_button = pygame.Rect(330, 460, 40, 40)
    x_text = font.render("X", True, (255, 255, 255))
    x_text_rect = x_text.get_rect(center=x_button.center)
    pygame.draw.rect(screen, (255, 0, 0), x_button)
    screen.blit(x_text, x_text_rect)

    o_button = pygame.Rect(380, 460, 40, 40)
    o_text = font.render("O", True, (255, 255, 255))
    o_text_rect = o_text.get_rect(center=o_button.center)
    pygame.draw.rect(screen, (0, 255, 0), o_button)
    screen.blit(o_text, o_text_rect)

    pygame.display.flip()

    player=True
    while (player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if x_button.collidepoint(mouse_x, mouse_y) or o_button.collidepoint(mouse_x, mouse_y):
                    print("I am here under player choose")
                    print(mouse_x, mouse_y)
                    if 330 <= mouse_x <= 370:
                        print("X clicked")
                        x_turn = True
                        player = False
                    elif 380 <= mouse_x <= 420:
                        print("O clicked")
                        x_turn = False
                        player = False
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 500, 150))
    pygame.display.flip()
    return x_turn  

def display_turn(x_turn):
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 500, 150))
    font = pygame.font.Font('freesansbold.ttf', 32)
    if x_turn:
        text = 'X'
        color= RED
    else:
        text = 'O'
        color= BLUE
    text_turn = font.render('Player Turn: ', True, WHITE)
    text = font.render(text, True, color)
    rect = pygame.draw.rect(screen, (160,32,240),(50, HEIGHT + 150, WIDTH+100, 70), border_radius=10)
    center=rect.center
    text_turn_Rect = text_turn.get_rect()
    text_turn_Rect.center = (center) 
    text_rect = text.get_rect(center=(center[0] + 110, center[1]+3))
    screen.blit(text_turn, text_turn_Rect)
    screen.blit(text, text_rect)
    pygame.display.flip()

def display_winner(winner):
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 500, 150))
    font = pygame.font.Font('freesansbold.ttf', 32)
    if winner == 1:
        text = font.render('Player X Wins', True, WHITE)
        print("Player X Wins")
        
    elif winner == -1:
        text = font.render('Player O Wins', True, WHITE)
        print(" Player O Wins")
    else:
        text = font.render('This is a Draw', True, WHITE)
        print("This is a Draw")
    
    print("888888888888888", winner)
    # display play again button
    rect = pygame.draw.rect(screen, (160,32,240),(50, HEIGHT + 150, WIDTH+100, 70), border_radius=10)
    center=rect.center
    textRect = text.get_rect()
    textRect.center = (center)
    screen.blit(text, textRect)
    restart_button, end_button = finish_game()
    # pygame.display.flip()
    return restart_button, end_button

# This function will add the hamard gate, x gate and cnot gate to the circuit
def quantum_game(circuit, recent_moves):
    """This will return the circuit and draw the circuit diagram"""
    first_move = recent_moves[0]
    second_move = recent_moves[1]
    # hamard gate
    circuit.h(first_move[0] * 3 + first_move[1])

    # x gate
    circuit.x(second_move[0] * 3 + second_move[1])

    # cnot gate
    circuit.cx(first_move[0] * 3 + first_move[1], second_move[0] * 3 + second_move[1])

    print(circuit.draw())
    recent_moves.clear()

    return circuit, recent_moves


def collapse(
    circuit, is_collapse, quantum_moves, x_turn, recent_moves, board_coordinate
):
    
    rect = pygame.draw.rect(screen, (160,32,240),(50, HEIGHT + 150, WIDTH+100, 70), border_radius=10)
    font = pygame.font.Font('freesansbold.ttf', 32)
    WHITE = (255, 255, 255)  # Define the color "green"
    text = font.render('collapsing the board..', True, WHITE)
    center=rect.center
    textRect = text.get_rect()
    textRect.center = (center)
    screen.blit(text, textRect)
    pygame.display.flip()
    pygame.time.delay(1000)


    global ai_turn
    is_collapse = True
    quantum_moves = False
    c1_flag = False
    c3_flag = False
    x_turn = not x_turn if recent_moves else x_turn
    ai_turn = not ai_turn

    if recent_moves:
        circuit.x(recent_moves[0][0] * 3 + recent_moves[0][1])
    # x_turn = not x_turn
    recent_moves.clear()
    circuit.measure([0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 1, 2, 3, 4, 5, 6, 7, 8])
    print(circuit.draw())
    simulator = qiskit.Aer.get_backend("qasm_simulator")
    job = qiskit.execute(circuit, simulator, shots=1)
    result = job.result()
    out = json.dumps(result.get_counts())
    string = out[2:11]
    # reverse the string
    string = string[::-1]
    print("This is string", string)
    # convert string to list
    string = list(string)
    if entanglement_:
        connected = connected_qubits_with_entanglement(
            history_of_moves, entanglement_coordinates
        )
        for c1, c2, c3 in connected:

            c1 = c1[0] * 3 + c1[1]
            c2 = c2[0] * 3 + c2[1]
            c3 = c3[0] * 3 + c3[1]

            print("This is c1, c2, c3", c1, c2, c3)

            # there are the value in 1 and 0
            c_1, c_2, c_3 = entanglement()
            print("This is c_1, c_2, c_3", c_1, c_2, c_3)
            string[c1] = c_1
            string[c2] = c_2
            string[c3] = c_3
            # if c1 == 1 or c3 == 1:
            #     board_coordinate[c1//3][c1%3] = c_1
            #     board_coordinate[c3//3][c3%3] = c_3

            if c_1 == 0:
                board_coordinate[c1 // 3][c1 % 3] = 0
            elif c_2 == 0:
                board_coordinate[c2 // 3][c2 % 3] = 0
            elif c_3 == 0:
                board_coordinate[c3 // 3][c3 % 3] = 0

            if c_1 == "1":
                c1_flag = True
            if c_3 == "1":
                c3_flag = True

            if c_2 == "1":
                print("I am under c_2")
                if c1_flag:
                    print("This is c1_flag", c1_flag)
                    board_coordinate[c2 // 3][c2 % 3] = -board_coordinate[c1 // 3][
                        c1 % 3
                    ]
                elif c3_flag:
                    print("This is c1_flag off", c3_flag)
                    board_coordinate[c2 // 3][c2 % 3] = -board_coordinate[c3 // 3][
                        c3 % 3
                    ]

            c1_flag = False
            c3_flag = False

    # convert list to string
    string = "".join(string)

    print("This is fucking string", string)
    # reset the circuit
    for i in range(9):
        circuit.reset(i)

    for i, val in enumerate(string):
        if val == "0":
            board_coordinate[i // 3][i % 3] = 0

    return is_collapse, quantum_moves, x_turn


def draw_x_or_y(board_coordinates, is_collapse, coordinate_of_moves):
    # print("This is coordinate_of_moves", board_coordinates)
    font = pygame.font.Font("freesansbold.ttf", 60)
    colors = [GREEN, YELLOW, CYAN, MAGENTA, RED, BLUE, WHITE]
    dict_x = {}
    print("This is entanglement_coordinates", entanglement_coordinates)

    print("This is the coordinate_of_moves", coordinate_of_moves)

    for i, coordinate in enumerate(coordinate_of_moves):
        dict_x[tuple(coordinate)] = colors[i//2] 


    for row in range(3):
        for col in range(3):

            if board_coordinates[row][col] == 1:
                if is_collapse:
                    text_color = (255, 0, 0)
                else:
                    text_color = dict_x[(row, col)]

                text = font.render("X", True, text_color)

            elif board_coordinates[row][col] == -1:
                if is_collapse:
                    text_color = (0, 0, 255)
                else:
                    text_color = dict_x[(row, col)]
                text = font.render("O", True, text_color)

            else:
                continue

            text_rect = text.get_rect(
                center=(
                    col * WIDTH // GRID_SIZE + WIDTH // GRID_SIZE // 2+100,
                    row * HEIGHT // GRID_SIZE + HEIGHT // GRID_SIZE // 2+100,
                )
            )
            screen.blit(text, text_rect)
            

    if is_collapse == False:
        for [x, y] in entanglement_coordinates:
            # Here it should remove the X or Y blit for [x,y] coordinates
            print("Here i am")
            # First, blit a rectangle of the background color over the X or Y
            background_color = (0, 0, 0)  # Replace with your background color
            rect = pygame.Rect(
                y * WIDTH // GRID_SIZE + LINE_WIDTH // 2+100,
                x * HEIGHT // GRID_SIZE + LINE_WIDTH // 2+100,
                WIDTH // GRID_SIZE - LINE_WIDTH,
                HEIGHT // GRID_SIZE - LINE_WIDTH,
            )
            pygame.draw.rect(screen, background_color, rect)
            # Then blit the "Q" as before
            text_color = (255, 0, 0)
            text = font.render("Q", True, text_color)
            text_rect = text.get_rect(
                center=(
                    y * WIDTH // GRID_SIZE + WIDTH // GRID_SIZE // 2+100,
                    x * HEIGHT // GRID_SIZE + HEIGHT // GRID_SIZE // 2+100,
                )
            )
            print("This is the text center", text_rect.center)
            screen.blit(text, text_rect)


def check_winner(board_coordinates):
    # print("This si check_winner", board_coordinates)
    # Check rows
    for row in range(3):
        if (
            board_coordinates[row][0]
            == board_coordinates[row][1]
            == board_coordinates[row][2]
            != 0
        ):
            return board_coordinates[row][0]

    # Check columns
    for col in range(3):
        if (
            board_coordinates[0][col]
            == board_coordinates[1][col]
            == board_coordinates[2][col]
            != 0
        ):
            return board_coordinates[0][col]

    # Check diagonals
    if (
        board_coordinates[0][0]
        == board_coordinates[1][1]
        == board_coordinates[2][2]
        != 0
    ):
        return board_coordinates[0][0]
    if (
        board_coordinates[0][2]
        == board_coordinates[1][1]
        == board_coordinates[2][0]
        != 0
    ):
        return board_coordinates[0][2]

    return 0


def before_collapse(board_coordinates, rows, cols, quantum_moves, x_turn, count):
    global ai_turn
    # global previous_board_coordinates
    """It will decide x_turn for the quantum moves or the normal moves"""
    count += 1
    print(count)

    if x_turn:

        board_coordinates[rows][cols] = 1
    else:

        board_coordinates[rows][cols] = -1

    if (quantum_moves and count == 2) or not quantum_moves:
        x_turn = not x_turn
        count = 0
        ai_turn = not ai_turn

    # previous_board_coordinates = copy.deepcopy(board_coordinate)

    return x_turn, count, board_coordinates


def check_complete_fill(board_coordinates):
    # print("This is board_coordinates", board_coordinates)
    for row in range(3):
        for col in range(3):
            if board_coordinates[row][col] == 0:
                return False
    return True


def draw_circuit(board_coordinate):
    global previous_board_coordinates
    for inx, row in enumerate(board_coordinate):
        for j, i in enumerate(row): 
            if i != 0 and previous_board_coordinates[inx][j] == 0:
                circuit.x(inx * 3 + j)

    print(circuit.draw())
    previous_board_coordinates = copy.deepcopy(board_coordinate)
    print("This is previous_board_coordinates", previous_board_coordinates)


def entanglement():
    required_states = ["011", "101", "110"]
    qc = QuantumCircuit(3, 3)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    while True:
        qc.measure([0, 1, 2], [0, 1, 2])
        simulator = qiskit.Aer.get_backend("qasm_simulator")
        job = qiskit.execute(qc, simulator, shots=1)
        result = job.result()
        out = json.dumps(result.get_counts())
        out = out[2:5]
        # reverse the string
        string = out[::-1]
        print(string)
        if string in required_states:
            break
    return string[0], string[1], string[2]


def mark_entanglement(board_coordinate, row, column, previous_board_coordinate):
    global entanglement_
    if board_coordinate[row][column] * previous_board_coordinate[row][column] == -1:
        entanglement_ = True
        entanglement_coordinates.append([row, column])
        print("This is entanglement_position", entanglement_coordinates)


def connected_qubits_with_entanglement(history_of_moves, entanglement_coordinates):
    connected = []
    for i, coordinate in enumerate(history_of_moves):
        if coordinate in entanglement_coordinates:
            index_1 = i // 2
            index_2 = i % 2
            # change index_2 if 0 to 1 and if 1 to 0
            if index_2 == 0:
                index_2 = 1
            else:
                index_2 = 0
            connected.append(history_of_moves[index_1 * 2 + index_2])
            if coordinate not in connected:
                connected.append(coordinate)

    new_connected = [connected[:3], connected[3:6], connected[6:]]
    for i in new_connected:
        if [] in new_connected:
            new_connected.remove([])

    print("This is connected", new_connected)
    return new_connected


def check_draw(board_coordinate):
    for row in board_coordinate:
        if 0 in row:
            return False
    return True



def ai_make_move(board_coordinates, is_collapse ,x_turn):
    print("checking x_turn", x_turn)
    if is_collapse:
        ai_moves = 1
        pygame.time.delay(500)
    else:
        ai_moves = 2
    best_moves = []
    
    for k in range(ai_moves):
        best_score = float("-inf")
        best_move = None
    
        for i in range(3):
            for j in range(3):
                if board_coordinates[i][j] == 0:
                    if x_turn:
                        board_coordinates[i][j] = 1
                    else:
                        board_coordinates[i][j] = -1
                    score = alphabeta_pruning(board_coordinates, 0, False, float("-inf"), float("inf"), x_turn)
                    board_coordinates[i][j] = 0
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move is not None:
            if x_turn:
                board_coordinates[best_move[0]][best_move[1]] = 1
            else:
                board_coordinates[best_move[0]][best_move[1]] = -1
            best_moves.append(best_move)
        else:
            break
        # print("This is the best move", best_move)
        # best_moves.append(best_move)
        # f = open("new.txt", "w")
        # f.write(str(best_moves))
        # f.close()
        print("This is the best_moves", best_moves)
        
    return best_moves, board_coordinates



def alphabeta_pruning(board, depth, is_maximizing, alpha, beta , x_turn):
    if x_turn:
        if check_winner(board) == -1:
            return -1
        elif check_winner(board) == 1:
            return 1
        elif check_complete_fill(board):
            return 0
    else:
        if check_winner(board) == -1:
            return 1
        elif check_winner(board) == 1:
            return -1
        elif check_complete_fill(board):
            return 0

    if is_maximizing:
        best_score = float("-inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = -1
                    score = alphabeta_pruning(board, depth + 1, False, alpha, beta , x_turn)
                    board[i][j] = 0
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break  # Break out of this iteration, not the entire function
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = 1
                    score = alphabeta_pruning(board, depth + 1, True, alpha, beta , x_turn)
                    board[i][j] = 0
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  # Break out of this iteration, not the entire function
        return best_score




# def ai_make_move(board_coordinates):
#     # Check for possible winning moves
#     for row in range(3):
#         for col in range(3):
#             if board_coordinates[row][col] == 0:
#                 board_copy = copy.deepcopy(board_coordinates)
#                 board_copy[row][col] = -1
#                 if check_winner(board_copy) == -1:
#                     return row, col

#     # Check for possible blocking moves
#     for row in range(3):
#         for col in range(3):
#             if board_coordinates[row][col] == 0:
#                 board_copy = copy.deepcopy(board_coordinates)
#                 board_copy[row][col] = 1
#                 if check_winner(board_copy) == 1:
#                     return row, col

#     # Randomly choose a move
#     available_moves = []
#     for row in range(3):
#         for col in range(3):
#             if board_coordinates[row][col] == 0:
#                 available_moves.append((row, col))
#     return random.choice(available_moves)

ai_turn = False


def finish_game():
    
    # make play_again button at the top left corner
    play_again_button = pygame.Rect(30, 30, WIDTH - 100, 50)
    # play_again_button = pygame.Rect(150, 200, WIDTH - 100, 50)
    play_again_text = font.render("Play Again", True, (255, 255, 255))
    play_again_text_rect = play_again_text.get_rect(center=play_again_button.center)
    pygame.draw.rect(screen, (255, 0, 0), play_again_button, border_radius=10)
    screen.blit(play_again_text, play_again_text_rect)
    
    quit_button = pygame.Rect(WIDTH//2+100, 30, WIDTH - 100, 50)
    quit_text = font.render("Quit", True, (255, 255, 255))
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    pygame.draw.rect(screen, (0, 255, 0), quit_button, border_radius=10)
    screen.blit(quit_text, quit_text_rect)
    pygame.display.flip()
    
    return play_again_button, quit_button
    
    
    # reset game state if play again is clicked
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if play_again_button.collidepoint(mouse_x, mouse_y):
                print("*****************")
                reset_game()
                print("--------------------------------------------")
                screen.fill((0,0,0))
                pygame.display.flip()
                
            elif quit_button.collidepoint(mouse_x, mouse_y):
                pygame.quit()
                
    

    
def reset_game():
    print("000000000000000000000000000000000")
    global board_coordinate, circuit, recent_moves, x_turn, count, is_collapse, quantum_moves, history_of_moves, entanglement_coordinates, entanglement_
    global previous_board_coordinate
    board_coordinate = board_coordinates()
    circuit = qiskit.QuantumCircuit(9, 9)
    recent_moves = []
    x_turn = True
    count = 0
    is_collapse = False
    quantum_moves = True
    history_of_moves = []
    entanglement_coordinates = []
    entanglement_ = False
    previous_board_coordinate = [[0, 0, 0] for i in range(3)]
    # screen.fill((0, 0, 0))
    # draw_grid()
    # pygame.display.flip()
    



def play_with_ai():
    global board_coordinate, circuit, recent_moves, x_turn, count, is_collapse, quantum_moves, history_of_moves, entanglement_coordinates, entanglement_
    global previous_board_coordinate
    global ai_turn

    # Reset game state
    board_coordinate = board_coordinates()
    circuit = qiskit.QuantumCircuit(9, 9)
    recent_moves = []
    coordinate_moves = []
    x_turn = True
    count = 0
    is_collapse = False
    quantum_moves = True
    history_of_moves = []
    entanglement_coordinates = []
    entanglement_ = False
    running=True

        
    screen.fill((0, 0, 0))
    draw_grid()
    print(x_turn)
    x_turn=choose_player()
    print(x_turn) 
    pygame.display.flip()

    while running:
        if not ai_turn:
            display_turn(x_turn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ai_turn:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    cols = mouse_x // (WIDTH // GRID_SIZE)-1
                    rows = mouse_y // (HEIGHT // GRID_SIZE)-1

                    if 0 <= rows < GRID_SIZE and 0 <= cols < GRID_SIZE:
                        screen.fill((0, 0, 0))
                        draw_grid()
                        recent_moves.append([rows, cols])
                        history_of_moves.append([rows, cols])
                        if not is_collapse:
                            coordinate_moves.append([rows, cols])

                        x_turn, count, board_coordinate= before_collapse(
                            board_coordinate, rows, cols, quantum_moves, x_turn, count
                        )

                        if len(recent_moves) == 2 and not is_collapse:
                            circuit, recent_moves = quantum_game(circuit, recent_moves)

                        print("This is X_turn", x_turn)

                        if check_complete_fill(board_coordinate) and not is_collapse:
                            draw_x_or_y(board_coordinate, is_collapse, coordinate_moves)
                            pygame.display.flip()

                            print("This is the non final board_coordinates", board_coordinate)

                            pygame.time.delay(1000)

                            screen.fill((0, 0, 0))

                            draw_grid()

                            if not is_collapse:
                                is_collapse, quantum_moves, x_turn = collapse(
                                    circuit,
                                    is_collapse,
                                    quantum_moves,
                                    x_turn,
                                    recent_moves,
                                    board_coordinate,
                                )
                            print("THis is x_turn", x_turn)
                            print("This is the final board_coordinates", board_coordinate)

                            print("Love you", board_coordinate)

                        if is_collapse:
                            draw_circuit(board_coordinate)
                            winner = check_winner(board_coordinate)
                            if winner == 1:
                                print("X wins!")
                                cprint("X wins!", "red")
                                display_winner(1)
                                running=False

                            elif winner == -1:
                                print("O wins!")
                                cprint("O wins!", "blue")
                                display_winner(-1)
                                running=False

                                
                            elif check_complete_fill(board_coordinate):
                                print("This is a Draw!")
                                display_winner(0)
                                running=False

                        print("BOARD COORDINATES", board_coordinate)

                        mark_entanglement(
                            board_coordinate, rows, cols, previous_board_coordinate
                        )
                        
                        previous_board_coordinate = copy.deepcopy(board_coordinate)

                        draw_x_or_y(board_coordinate, is_collapse, coordinate_moves)

                        pygame.display.flip()
            # print("ai_turn", ai_turn) 
                # AI makes a move
            if ai_turn and running:
                print("AI's turn")
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 400, 500, 150))
                rect = pygame.draw.rect(screen, (160,32,240),(50, HEIGHT + 150, WIDTH+100, 70), border_radius=10)
                center=rect.center
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render('AI Turn', True, WHITE)
                textRect = text.get_rect()
                textRect.center = (center)
                screen.blit(text, textRect)
                pygame.display.flip()

                pygame.time.delay(1000)

                
                best_moves, board_coordinate  = ai_make_move(board_coordinate, is_collapse , x_turn )
                print("Fuck", board_coordinate)
                # board_coordinate[row][col] = -1

                recent_moves.extend(best_moves)
                history_of_moves.extend(best_moves)
                if not is_collapse: 
                    coordinate_moves.extend(best_moves)
                x_turn = not x_turn 
                ai_turn=not ai_turn

                if len(recent_moves) == 2 and not is_collapse:
                    print()
                    circuit, recent_moves = quantum_game(circuit, recent_moves)

                if check_complete_fill(board_coordinate) and not is_collapse:
                    draw_x_or_y(board_coordinate, is_collapse, coordinate_moves)
                    pygame.display.flip()

                    pygame.time.delay(1000)

                    screen.fill((0, 0, 0))

                    draw_grid()

                    if not is_collapse:
                        is_collapse, quantum_moves, x_turn = collapse(
                            circuit,
                            is_collapse,
                            quantum_moves,
                            x_turn,
                            recent_moves,
                            board_coordinate,
                        )

                    

                    # mark_entanglement(
                    #     board_coordinate, row, col, previous_board_coordinate
                    # )

                previous_board_coordinate = copy.deepcopy(board_coordinate)
                print("I love Board Coordinates", board_coordinate)

                draw_x_or_y(board_coordinate, is_collapse, coordinate_moves)
                print("This is is_collapse", is_collapse)

                if is_collapse:
                    draw_circuit(board_coordinate)

                    
                    winner=check_winner(board_coordinate)
                    if winner == 1:
                        display_winner(1)
                        print("X wins!")
                        cprint("X wins!", 'red')
                        # running = False
                    elif winner == -1:
                        display_winner(-1)
                        print("O wins!")
                        cprint("O wins!", 'blue')
                        # running = False
                    
                    elif  check_complete_fill(board_coordinate):
                        display_winner(0)
                        print("This is a Draw!")
                        # running = False

                pygame.display.flip()

        # Quit Pygame
reset_button = None

def play_with_players():
    global reset_button
    global board_coordinate, circuit, recent_moves, x_turn, count, is_collapse, quantum_moves, history_of_moves, entanglement_coordinates, entanglement_
    global previous_board_coordinate

    # Reset game state
    board_coordinate = board_coordinates()
    circuit = qiskit.QuantumCircuit(9, 9)
    recent_moves = []
    x_turn = True
    count = 0
    is_collapse = False
    quantum_moves = True
    coordinate_moves = []
    history_of_moves = []
    entanglement_coordinates = []
    entanglement_ = False
    
    screen.fill((0, 0, 0))
    draw_grid()
    print(x_turn)
    x_turn=choose_player()
    print(x_turn) 
    pygame.display.flip()
    running=True


    while running:
        display_turn(x_turn)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                cols = mouse_x // (WIDTH // GRID_SIZE)-1
                rows = mouse_y // (HEIGHT // GRID_SIZE)-1
                print("This is rows and cols", rows, cols)
                

                if 0 <= rows < GRID_SIZE and 0 <= cols < GRID_SIZE:
                    screen.fill((0, 0, 0))
                    draw_grid()
                    # recent moves is the recent moves of X or O
                    # it will contain 1 or max two element
                    recent_moves.append([rows, cols])
                    # it is the total history of moves of X or O
                    history_of_moves.append([rows, cols])
                    if not is_collapse:
                        # coordinate_moves is the moves of X or O before the collapse
                        coordinate_moves.append([rows, cols])

                    x_turn, count, board_coordinate = before_collapse(
                        board_coordinate, rows, cols, quantum_moves, x_turn, count
                    )

                    if len(recent_moves) == 2 and not is_collapse:
                        print()
                        circuit, recent_moves = quantum_game(circuit, recent_moves)

                    if check_complete_fill(board_coordinate) and not is_collapse:
                        draw_x_or_y(board_coordinate, is_collapse, coordinate_moves)
                        pygame.display.flip()

                        pygame.time.delay(1000)

                        screen.fill((0, 0, 0))

                        draw_grid()

                        if not is_collapse:
                            is_collapse, quantum_moves, x_turn = collapse(
                                circuit,
                                is_collapse,
                                quantum_moves,
                                x_turn,
                                recent_moves,
                                board_coordinate,
                            )

                    if is_collapse:
                        draw_circuit(board_coordinate)
                        winner = check_winner(board_coordinate)
                        if winner == 1:
                            print("X wins!")
                            cprint("X wins!", "red")
                            reset_button, end_button = display_winner(1)
                            # running=False
                            
                        elif winner == -1:
                            print("O wins!")
                            cprint("O wins!", "blue")
                            reset_button, end_button = display_winner(-1)
                            # running=False
                        elif check_complete_fill(board_coordinate):
                            reset_button, end_button = display_winner(0)
                            print("This is a Draw!")
                            # running=False


                    
                    mark_entanglement(
                        board_coordinate, rows, cols, previous_board_coordinate
                    )
                    previous_board_coordinate = copy.deepcopy(board_coordinate)

                    draw_x_or_y(board_coordinate, is_collapse, coordinate_moves)
                    print("This is is collapse", is_collapse)

                    pygame.display.flip()
                    
                if reset_button and reset_button.collidepoint(mouse_x, mouse_y):
                    reset_game()
                    screen.fill((0,0,0))
                    pygame.display.flip()
                    running = False
                    
        
            




font = pygame.font.Font("freesansbold.ttf", 16)
def main():
    pygame.init()
    # Main menu loop
    # title_text = font.render("Quantum Tic-Tac-Toe", True, (255, 255, 255))
    # title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    # screen.blit(title_text, title_rect)

    # Draw the buttons
    while True:

        screen.fill((0, 0, 0))
        play_ai_button = pygame.Rect(150, 200, WIDTH - 100, 50)
        play_ai_text = font.render("Play with AI", True, (255, 255, 255))
        play_ai_text_rect = play_ai_text.get_rect(center=play_ai_button.center)
        pygame.draw.rect(screen, (255, 0, 0), play_ai_button, border_radius=10)
        screen.blit(play_ai_text, play_ai_text_rect)

        play_2p_button = pygame.Rect(150, 300, WIDTH - 100, 50)
        play_2p_text = font.render("Play with 2 Players", True, (255, 255, 255))
        play_2p_text_rect = play_2p_text.get_rect(center=play_2p_button.center)
        pygame.draw.rect(screen, (0, 255, 0), play_2p_button , border_radius=10)
        screen.blit(play_2p_text, play_2p_text_rect)

        pygame.display.flip()
        # Draw the title text

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                # break
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if play_ai_button.collidepoint(mouse_x, mouse_y):
                    play_with_ai()
                    print("HEhe")
                elif play_2p_button.collidepoint(mouse_x, mouse_y):
                    print("I am here")
                    play_with_players()

if __name__ == "__main__":
    main()

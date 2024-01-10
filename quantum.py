from termcolor import colored, cprint
import json
from qiskit import *
import qiskit
from qiskit.tools.monitor import job_monitor

import pygame

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_COLOR = (255, 255, 255)
LINE_WIDTH = 5
GRID_SIZE = 3

# Set up the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3x3 Grid")

def draw_grid():
    # Draw vertical lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (i * WIDTH // GRID_SIZE, 0), (i * WIDTH // GRID_SIZE, HEIGHT), LINE_WIDTH)
    
    # Draw horizontal lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, i * HEIGHT // GRID_SIZE), (WIDTH, i * HEIGHT // GRID_SIZE), LINE_WIDTH)

def board_coordinates():
    return [[0,0,0] for i in range(3)]


def quanutum_game(circuit,recent_moves):
    """This will return the circuit and draw the circuit diagram"""
    first_move = recent_moves[0]
    second_move = recent_moves[1]
    # hamard gate
    circuit.h(first_move[0]*3 + first_move[1])

    # x gate
    circuit.x(second_move[0]*3 + second_move[1])

    # cnot gate
    circuit.cx(first_move[0]*3 + first_move[1], second_move[0]*3 + second_move[1])


    print(circuit.draw())
    recent_moves.clear()

    return circuit, recent_moves

    # initialize the hadamard gate hehahah
    # circuit.h()
    # ...

def collapse(circuit):
    circuit.measure([0,1,2,3,4,5,6,7,8],[0,1,2,3,4,5,6,7,8])
    print(circuit.draw())
    simulator = qiskit.Aer.get_backend('qasm_simulator')
    job = qiskit.execute(circuit, simulator, shots=1)
    result = job.result()
    out = json.dumps(result.get_counts())
    string = out[2:11] 

    # reverse the string
    string = string[::-1]
    print(string)

    # reset the circuit
    for i in range(9):  
        circuit.reset(i)
    

    return string

# def after_collapse(circuit, string):



def draw_x_or_y(board_coordinates):
    font = pygame.font.Font('freesansbold.ttf', 60)
    for row in range(3):
        for col in range(3):
            if board_coordinates[row][col] == 1:
                
                # Here True is written to enable smooth edges
                text = font.render("X", True, (255, 0, 0))
                text_rect = text.get_rect(center=(col * WIDTH // GRID_SIZE + WIDTH // GRID_SIZE // 2, row * HEIGHT // GRID_SIZE + HEIGHT // GRID_SIZE // 2))
                screen.blit(text, text_rect)
            elif board_coordinates[row][col] == -1:
                text = font.render("O", True, (0, 0, 255))
                text_rect = text.get_rect(center=(col * WIDTH // GRID_SIZE + WIDTH // GRID_SIZE // 2, row * HEIGHT // GRID_SIZE + HEIGHT // GRID_SIZE // 2))
                screen.blit(text, text_rect)

def check_winner(board_coordinates):
    # Check rows
    for row in range(3):
        if board_coordinates[row][0] == board_coordinates[row][1] == board_coordinates[row][2] != 0:
            return board_coordinates[row][0]

    # Check columns
    for col in range(3):
        if board_coordinates[0][col] == board_coordinates[1][col] == board_coordinates[2][col] != 0:
            return board_coordinates[0][col]

    # Check diagonals
    if board_coordinates[0][0] == board_coordinates[1][1] == board_coordinates[2][2] != 0:
        return board_coordinates[0][0]
    if board_coordinates[0][2] == board_coordinates[1][1] == board_coordinates[2][0] != 0:
        return board_coordinates[0][2]

    return 0

def before_collapse(board_coordinates, rows, cols, quantum_moves, x_turn, count):
    
    count += 1
    print(count)
    if x_turn:
        board_coordinates[rows][cols] = 1
        if quantum_moves and count == 2:
            x_turn = False
            count = 0
        elif not quantum_moves:
            x_turn = False
        
        
    else:       
        board_coordinate[rows][cols] = -1
        if quantum_moves and count == 2:
            x_turn = True
            count = 0
        elif not quantum_moves:
            x_turn = True

    return x_turn, count


def check_complete_fill(board_coordinates):
    for row in range(3):
        for col in range(3):
            if board_coordinates[row][col] == 0:
                return False
    return True
            


        # count += 1
        # if count == 2 and quantum_moves:
            
        #     x_turn = False
        #     count = 0
        
        # elif not quantum_moves:
        #     x_turn = False
        

    # else:
    #     board_coordinate[rows][cols] = -1
    #     count += 1
    #     if count >= 2 and quantum_moves:
            
    #         x_turn = True
    #         count = 0
    #     elif not quantum_moves:
    #         x_turn = True





board_coordinate = board_coordinates()

circuit = qiskit.QuantumCircuit(9,9)

recent_moves = []

# Main loop
running = True
x_turn = True
count = 0
total_count = 0
is_collapse = False
quantum_moves = True

while running:
    for event in pygame.event.get():

        
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cols = mouse_x // (WIDTH // GRID_SIZE)
            rows = mouse_y // (HEIGHT // GRID_SIZE)
            recent_moves.append([rows, cols])
            total_count += 1


            if 0 <= rows < GRID_SIZE and 0 <= cols < GRID_SIZE:
            #     if x_turn:
            #         board_coordinates[rows][cols] = 1
            #         x_turn = False
            #     else:
            #         board_coordinates[rows][cols] = -1
            #         x_turn = True

                        # if 0 <= rows < GRID_SIZE and 0 <= cols < GRID_SIZE:
                print("This is is_collapse", quantum_moves)
                x_turn, count = before_collapse(board_coordinate, rows, cols, quantum_moves, x_turn, count)

                
                if len(recent_moves) == 2:
                    quanutum_game(circuit, recent_moves)
            
                elif total_count == 9:
                    is_collapse = True
                    quantum_moves = False
                    circuit.x(recent_moves[0][0]*3 + recent_moves[0][1])
                    x_turn = False
                    print(circuit.draw())
                    recent_moves.clear()
                    string = collapse(circuit)
                    for i,val in enumerate(string):
                        if val == '0':
                            print("This is i", i)
                            board_coordinate[i//3][i%3] = 0
                        else:
                            total_count += 1
                    winner=check_winner(board_coordinate)
                    if winner == 1:
                        print("X wins!")
                        cprint("X wins!", 'red')
                        # running = False
                    elif winner == -1:
                        print("O wins!")
                        cprint("O wins!", 'blue')


    # Clear the screen
    screen.fill((0, 0, 0))
    draw_grid()


        # running = False






    
    # quanutum_game(board_coordinates, circuit, x_turn)
    draw_x_or_y(board_coordinate)


    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

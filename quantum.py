from termcolor import colored, cprint
import json
from qiskit import *
import qiskit
from qiskit.tools.monitor import job_monitor
import copy
import pygame

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
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3x3 Grid")

previous_board_coordinates = [[0, 0, 0] for i in range(3)]

previous_board_coordinate = [[0, 0, 0] for i in range(3)]



def draw_grid():
    # Draw vertical lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (i * WIDTH // GRID_SIZE, 0),
            (i * WIDTH // GRID_SIZE, HEIGHT),
            LINE_WIDTH,
        )

    # Draw horizontal lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(
            screen,
            LINE_COLOR,
            (0, i * HEIGHT // GRID_SIZE),
            (WIDTH, i * HEIGHT // GRID_SIZE),
            LINE_WIDTH,
        )


def board_coordinates():
    return [[0, 0, 0] for i in range(3)]

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
    is_collapse = True
    quantum_moves = False

    if recent_moves:
        circuit.x(recent_moves[0][0] * 3 + recent_moves[0][1])
    x_turn = False
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
    print(string)
    # convert string to list
    string = list(string)
    if entanglement_:
        connected = connected_qubits_with_entanglement(history_of_moves, entanglement_coordinates)
        
        
        for c1,c2,c3 in connected:
            c1 = c1[0]*3 + c1[1]
            c2 = c2[0]*3 + c2[1]
            c3 = c3[0]*3 + c3[1]
        
            print("This is c1, c2, c3", c1, c2, c3)
        

            c_1, c_2, c_3 = entanglement()

            string[c1] = c_1
            string[c2] = c_2
            string[c3] = c_3

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
    
    for i, coordinate in enumerate(coordinate_of_moves):
        dict_x[tuple(coordinate)] = colors[i // 2]

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
                    col * WIDTH // GRID_SIZE + WIDTH // GRID_SIZE // 2,
                    row * HEIGHT // GRID_SIZE + HEIGHT // GRID_SIZE // 2,
                )
            )
            screen.blit(text, text_rect)
    print("This is dict_x", dict_x)


def check_winner(board_coordinates):
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


# def before_collapse(board_coordinates, rows, cols, quantum_moves, x_turn, count):
#     """It will decide x_turn for the quantum moves or the normal moves"""
#     count += 1
#     print(count)
#     if x_turn:
#         board_coordinates[rows][cols] = 1
#         if quantum_moves and count == 2:
#             x_turn = False
#             count = 0
#         elif not quantum_moves:
#             x_turn = False


#     else:
#         board_coordinates[rows][cols] = -1
#         if quantum_moves and count == 2:
#             x_turn = True
#             count = 0
#         elif not quantum_moves:
#             x_turn = True

#     return x_turn, count, board_coordinates


def before_collapse(board_coordinates, rows, cols, quantum_moves, x_turn, count):
    # global previous_board_coordinates
    """It will decide x_turn for the quantum moves or the normal moves"""
    count += 1
    print(count)

    if x_turn:
        # if board_coordinates[rows][cols] == -1:
        #     circuit.h(rows*3 + cols)

        board_coordinates[rows][cols] = 1
    else:
        # if board_coordinates[rows][cols] == 1:
        #     circuit.h(rows*3 + cols)

        board_coordinates[rows][cols] = -1

    # if previous_board_coordinates[rows][cols] * board_coordinates[rows][cols] == -1:
    #     circuit.cx(rows*3 + cols, rows*3 + cols)

    if (quantum_moves and count == 2) or not quantum_moves:
        x_turn = not x_turn
        count = 0

    # previous_board_coordinates = copy.deepcopy(board_coordinate)

    return x_turn, count, board_coordinates


def check_complete_fill(board_coordinates):
    print("This is board_coordinates", board_coordinates)
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


    # return connected

# class QuantumEntanglement:
#     def __init__(self):
#         self.entanglement_coordinates = []
        
#     def entanglement(self, board_coordinate):
#         required_states = ["011", "101", "110"]
#         qc = QuantumCircuit(3, 3)
#         qc.h(0)
#         qc.h(1)
#         qc.h(2)
#         while True:
#             qc.measure([0, 1, 2], [0, 1, 2])
#             simulator = qiskit.Aer.get_backend("qasm_simulator")
#             job = qiskit.execute(qc, simulator, shots=1)
#             result = job.result()
#             out = json.dumps(result.get_counts())
#             out = out[2:5]
#             # reverse the string
#             string = string[::-1]
#             print(string)
#             if string in required_states:
#                 break
#         return string
    
#     def mark_entanglement(self, board_coordinate, row, column, previous_board_coordinate):
#         if board_coordinate[row][column] * previous_board_coordinate[row][column] == -1:
#             self.entanglement_coordinates.append([row, column])
#             print("This is entanglement_position", self.entanglement_coordinates)
        
#     def connected_qubits_with_entanglement(self, history_of_moves, entanglement_coordinates):
#         connected = []
#         for i, coordinate in enumerate(history_of_moves):
#             if coordinate in entanglement_coordinates:
#                 index_1 = i // 2
#                 index_2 = i % 2
#                 # change index_2 if 0 to 1 and if 1 to 0
#                 if index_2 == 0:
#                     index_2 = 1
#                 else:
#                     index_2 = 0
#                 connected.append(history_of_moves[index_1*2+index_2])
#                 if coordinate not in connected:
#                     connected.append(coordinate)
#                 # connected.append(coordinate)
#         print("This is connected", connected)
#         return connected
    
    

            


            









    
        # circuit.cx(row * 3 + column, row * 3 + column)
    
# def connected_qubits(circuit, qubit):
#     connected = set()
#     for gate in circuit.data:
#         if qubit in gate[1]:
#             for q in gate[1]:
#                 if q != qubit:
#                     connected.add(q.index)

#     return connected

    


    #     for i in range(3):
    #         for j in range(3):
    #             if board_coordinate[i][j] == 1:
    #                 qc.x(i*3 + j)
    #     qc.measure([0,1,2], [0,1,2])
    #     simulator = qiskit.Aer.get_backend('qasm_simulator')
    #     job = qiskit.execute(qc, simulator, shots=1)
    #     result = job.result()
    #     out = json.dumps(result.get_counts())
    #     string = out[2:11]
    #     string = string[::-1]
    #     print(string)
    #     if string in required_states:
    #         break
    #     else:
    #         for i in range(3):
    #             for j in range(3):
    #                 if board_coordinate[i][j] == 1:
    #                     qc.x(i*3 + j)

    # return qc


board_coordinate = board_coordinates()

circuit = qiskit.QuantumCircuit(9, 9)

recent_moves = []


# Main loop
running = True
x_turn = True
count = 0
is_collapse = False
quantum_moves = True
coordinate_moves = []
history_of_moves = []

entanglement_coordinates = []

entanglement_ = False




draw_grid()
pygame.display.flip()




while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cols = mouse_x // (WIDTH // GRID_SIZE)
            rows = mouse_y // (HEIGHT // GRID_SIZE)
            

            if 0 <= rows < GRID_SIZE and 0 <= cols < GRID_SIZE:
                recent_moves.append([rows, cols])
                history_of_moves.append([rows, cols])
                if not is_collapse:
                    coordinate_moves.append([rows, cols])
                #     if x_turn:
                #         board_coordinates[rows][cols] = 1
                #         x_turn = False
                #     else:
                #         board_coordinates[rows][cols] = -1
                #         x_turn = True

                # if 0 <= rows < GRID_SIZE and 0 <= cols < GRID_SIZE:
                x_turn, count, board_coordinate = before_collapse(
                    board_coordinate, rows, cols, quantum_moves, x_turn, count
                )

                if len(recent_moves) == 2 and not is_collapse:
                    print()
                    circuit, recent_moves = quantum_game(circuit, recent_moves)

                if check_complete_fill(board_coordinate):
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
                    # connected = connected_qubits_with_entanglement(history_of_moves, entanglement_coordinates)
                

                    winner = check_winner(board_coordinate)
                    if winner == 1:
                        print("X wins!")
                        cprint("X wins!", "red")
                        # running = False
                    elif winner == -1:
                        print("O wins!")
                        cprint("O wins!", "blue")

                    elif check_complete_fill(board_coordinate):
                        print("This is a Draw!")

                print("BOARD COORDINATES", board_coordinate)
                # print("previous_board_coordinates", previous_board_coordinates)




                # for i, instruction in enumerate(circuit.data):
                #     if hasattr(instruction, 'operation') and hasattr(instruction.operation, 'name') and instruction.operation.name == 'cx':
                #         qubits_connected = instruction.qubits
                #         control_index = qubits_connected[0].index
                #         target_index = qubits_connected[1].index

                                # Clear the screen
                mark_entanglement(board_coordinate, rows, cols, previous_board_coordinate)
                
                screen.fill((0, 0, 0))
                draw_grid()
                previous_board_coordinate = copy.deepcopy(board_coordinate)

                # quanutum_game(board_coordinates, circuit, x_turn)
                draw_x_or_y(board_coordinate, is_collapse, coordinate_moves)

                # Update the display
                pygame.display.flip()
    
                
            
        


# Quit Pygame
pygame.quit()


def play_with_ai():
    global reset_button, winner_found
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
        if not ai_turn and not winner_found:
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
                                reset_button, end_button = display_winner(1)
                                winner_found = True
                                # running=False
                                
                            elif winner == -1:
                                print("O wins!")
                                cprint("O wins!", "blue")
                                reset_button, end_button = display_winner(-1)
                                winner_found = True
                                # running=False
                            elif check_complete_fill(board_coordinate):
                                reset_button, end_button = display_winner(0)
                                print("This is a Draw!")
                                winner_found = True
                                # running=False

                        print("BOARD COORDINATES", board_coordinate)

                        mark_entanglement(
                            board_coordinate, rows, cols, previous_board_coordinate
                        )
                        
                        previous_board_coordinate = copy.deepcopy(board_coordinate)

                        draw_x_or_y(board_coordinate, is_collapse, coordinate_moves)

                        pygame.display.flip()
                        
                                        
                    if reset_button and reset_button.collidepoint(mouse_x, mouse_y):
                        reset_game()
                        winner_found = False
                        screen.fill((0,0,0))
                        pygame.display.flip()
                        running = False
                # print("ai_turn", ai_turn) 
                    # AI makes a move
                if ai_turn and running:
                    print("AI's turn")
                    if not winner_found:
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
                        winner = check_winner(board_coordinate)
                        if winner == 1:
                            print("X wins!")
                            cprint("X wins!", "red")
                            reset_button, end_button = display_winner(1)
                            winner_found = True
                            # running=False
                            
                        elif winner == -1:
                            print("O wins!")
                            cprint("O wins!", "blue")
                            reset_button, end_button = display_winner(-1)
                            winner_found = True
                            # running=False
                        elif check_complete_fill(board_coordinate):
                            reset_button, end_button = display_winner(0)
                            print("This is a Draw!")
                            winner_found = True
                            # running=False
                        
                                
                if reset_button and reset_button.collidepoint(mouse_x, mouse_y):
                    reset_game()
                    winner_found = False
                    screen.fill((0,0,0))
                    pygame.display.flip()
                    running = False

                    # pygame.display.flip()
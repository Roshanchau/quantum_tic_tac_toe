                # AI makes a move
            if not x_turn:
                print("AI's turn")
                
                best_moves, board_coordinate = ai_make_move(board_coordinate, is_collapse)
                # print("Fuck", board_coordinate)
                # board_coordinate[row][col] = -1

                recent_moves.extend(best_moves)
                history_of_moves.extend(best_moves)
                if not is_collapse: 
                    coordinate_moves.extend(best_moves)
                x_turn = not x_turn

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
                        elif winner == -1:
                            print("O wins!")
                            cprint("O wins!", "blue")
                        elif check_complete_fill(board_coordinate):
                            print("This is a Draw!")

                pygame.display.flip()
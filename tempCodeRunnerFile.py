m")
                text_color = (255,0,0)
                text = font.render("Q", True, text_color)
                text_rect = text.get_rect(center=(
                y * WIDTH // GRID_SIZE + WIDTH // GRID_SIZE // 2,
                x * HEIGHT // GRID_SIZE + HEIGHT // GRID_SIZE // 2,))
                screen.blit(text, text_rect)
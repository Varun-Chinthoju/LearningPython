import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()
SCREENWIDTH = 1026
SCREENHEIGHT = 1026
COLOR = (255, 255, 255)
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

# Load images
x_image = pygame.transform.scale(pygame.image.load("images/mark-x.png"), (256, 256))
o_image = pygame.transform.scale(pygame.image.load("images/mark-o.png"), (256, 256))
board_image = pygame.transform.scale(
    pygame.image.load("images/tictactoe.png"), (1026, 1026)
)

# Game variables
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
game_over = False
winner = None


def draw_board():
    screen.fill(COLOR)
    screen.blit(board_image, (0, 0))
    for row in range(3):
        for col in range(3):
            x = col * 256 + (col + 1) * 64
            y = row * 256 + (row + 1) * 64
            if board[row][col] == "X":
                screen.blit(x_image, (x, y))
            elif board[row][col] == "O":
                screen.blit(o_image, (x, y))


def check_win():
    global game_over, winner

    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            winner = row[0]
            game_over = True

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            winner = board[0][col]
            game_over = True

    if (
        board[0][0] == board[1][1] == board[2][2]
        or board[0][2] == board[1][1] == board[2][0]
    ) and board[1][1] != "":
        winner = board[1][1]
        game_over = True

    if all(board[i][j] != "" for i in range(3) for j in range(3)):
        game_over = True
        winner = "Tie"


def handle_mouse_click(pos):
    global current_player

    if not game_over:
        col = pos[0] // 342
        row = pos[1] // 342
        if board[row][col] == "":
            board[row][col] = current_player
            current_player = "O" if current_player == "X" else "X"
            check_win()


def reset_game():
    global board, current_player, game_over, winner
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    winner = None


def main():
    global game_over

    fps = 60
    running = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)

    # Buttons setup
    button_font = pygame.font.Font(None, 36)
    button_width = 150
    button_height = 50
    button_y = SCREENHEIGHT - button_height - 50
    yes_button_rect = pygame.Rect(
        (SCREENWIDTH // 2 - button_width - 25, button_y, button_width, button_height)
    )
    no_button_rect = pygame.Rect(
        (SCREENWIDTH // 2 + 25, button_y, button_width, button_height)
    )

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MOUSEBUTTONDOWN:
                if game_over:
                    if yes_button_rect.collidepoint(event.pos):
                        reset_game()
                    elif no_button_rect.collidepoint(event.pos):
                        running = False
                else:
                    handle_mouse_click(pygame.mouse.get_pos())

        draw_board()

        if game_over:
            font = pygame.font.Font(None, 72)
            if winner == "Tie":
                text = font.render("It's a Tie!", True, (0, 0, 0))
            else:
                text = font.render(f"{winner} Wins!", True, (0, 0, 0))
            text_rect = text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2 - 50))
            screen.blit(text, text_rect)

            # Draw buttons
            pygame.draw.rect(screen, (0, 255, 0), yes_button_rect)  # Green for Yes
            yes_text = button_font.render("Play Again", True, (0, 0, 0))
            yes_text_rect = yes_text.get_rect(center=yes_button_rect.center)
            screen.blit(yes_text, yes_text_rect)

            pygame.draw.rect(screen, (255, 0, 0), no_button_rect)  # Red for No
            no_text = button_font.render("Quit", True, (0, 0, 0))
            no_text_rect = no_text.get_rect(center=no_button_rect.center)
            screen.blit(no_text, no_text_rect)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

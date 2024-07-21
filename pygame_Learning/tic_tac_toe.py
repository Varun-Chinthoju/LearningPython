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


def main():
    fps = 60
    running = True
    clock = pygame.time.Clock()
    board = pygame.transform.scale(
        pygame.image.load("images/tictactoe.png"), (1026, 1026)
    )
    pygame.mouse.set_visible(False)
    while running:
        clock.tick(fps)
        screen.fill(COLOR)
        screen.blit(board, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()

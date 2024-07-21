import pygame
from pygame.locals import *


def main():
    SCREENWIDTH = 800
    SCREENHEIGHT = 600
    COLOR = (255, 255, 255)
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    fps = 60
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(fps)
        screen.fill(COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()

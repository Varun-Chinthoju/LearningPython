import pygame, sys
from pygame.locals import *

pygame.init()
SCREENWIDTH = 800
SCREENHEIGHT = 600
COLOR = (0, 0, 0)
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
player = pygame.Rect((387.5, 287.5, 25, 25))
# Fill the screen first
screen.fill(COLOR)
speed = 1
fps = 500
# Then draw the rectangle
pygame.draw.rect(screen, (255, 0, 0), player)
# Wait until user quits
running = True
clock = pygame.time.Clock()
while running:
    clock.tick(fps)
    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 0, 0), player)

    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True or key[pygame.K_LEFT] == True:
        player.move_ip(-speed, 0)

    elif key[pygame.K_d] == True or key[pygame.K_RIGHT] == True:
        player.move_ip(speed, 0)

    elif key[pygame.K_w] == True or key[pygame.K_UP] == True:
        player.move_ip(0, -speed)

    elif key[pygame.K_s] == True or key[pygame.K_DOWN] == True :
        player.move_ip(0, speed)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()
pygame.quit()

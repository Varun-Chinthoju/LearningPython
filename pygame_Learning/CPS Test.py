import pygame
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

pygame.init()

width = 600
height = 400
screen = pygame.display.set_mode((width, height))

pygame.display.set_caption('CPS Test')

font = pygame.font.SysFont(None, 32)

clicks = 0
test_time = 1  
start_time = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_time == 0:  
                start_time = time.time()
            clicks += 1

    if start_time != 0 and time.time() - start_time >= test_time:
        cps = clicks / test_time
        text = f"Your CPS: {cps:.2f}"
        text_surface = font.render(text, True, RED)
        screen.fill(BLACK)
        screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, height // 2))
        pygame.display.flip()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    exit()

    screen.fill(BLACK)

    if start_time == 0:
        text = "Click as fast as you can!"
    else:
        text = f"Clicks: {clicks}"
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, height // 2))

    pygame.display.flip()

pygame.quit()
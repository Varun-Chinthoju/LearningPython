import pygame
import math
import random
import time
pygame.init()

SCREENWIDTH = 600
SCREENHEIGHT = 800
COLOR = (255, 255, 255)
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

box = pygame.transform.scale(pygame.image.load("images/box.png"), (400, 450))
box_opened = pygame.transform.scale(pygame.image.load("images/box opened.png"), (700, 700))

total_rotation_time = 0.5  
num_frames = 30  
rotation_step = 20 / num_frames 

clock = pygame.time.Clock()

current_image = box
is_clicked = False  
rotation_direction = 1  
total_elapsed_time = 0
rotation_stage = 1  
num_clicks = 0  
running = True
while running:
    dt = clock.tick(60) / 1000 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            box_rect = current_image.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2))
            if box_rect.collidepoint(mouse_pos):
                is_clicked = True
                total_elapsed_time = 0  
                rotation_direction = 1 if random.random() < 0.5 else -1  # Randomly choose initial direction
                num_clicks += 1  

    if is_clicked:
        total_elapsed_time += dt

        rotation_angle = total_elapsed_time / total_rotation_time * rotation_step * rotation_direction

        if rotation_stage == 1:
            current_image = pygame.transform.rotate(box, 20)
            if total_elapsed_time >= total_rotation_time:
                total_elapsed_time = 0 
                rotation_stage = 2  
        elif rotation_stage == 2:
            current_image = pygame.transform.rotate(box, -20)
            if total_elapsed_time >= total_rotation_time:
                total_elapsed_time = 0  
                rotation_stage = 3  
                rotation_direction *= -1  
        else:  
            current_image = pygame.transform.rotate(box, 20)
            if total_elapsed_time >= total_rotation_time:
                is_clicked = False  
                rotation_stage = 1  
        if num_clicks == 3:
            current_image = box_opened  
    screen.fill(COLOR)
    screen.blit(current_image, (SCREENWIDTH / 2 - current_image.get_width() // 2, SCREENHEIGHT / 2 - current_image.get_height() // 2))

    pygame.display.flip()

pygame.quit()

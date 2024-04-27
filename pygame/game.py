import pygame
from pygame.locals import *

pygame.init()
pygame.display.init()
SCREENWIDTH = 800
SCREENHEIGHT = 800
BG_COLOR = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
border = pygame.Rect(SCREENWIDTH // 2 - 5, 0, 10, SCREENHEIGHT)
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
border_color = (0, 0, 0)
# Fill the screen first
screen.fill(BG_COLOR)
speed = 2.5
fps = 120
r1_lives = 3
r2_lives = 3
bullets_vel = 7
max_bullets = 20
rocket_width = 55
rocket_height = 40
lives_height = 50
lives_width = 50
background = pygame.image.load("background.webp")
background_img = pygame.transform.scale(background, (SCREENWIDTH, SCREENHEIGHT))
r2_live1 = pygame.image.load("lives.jpeg")
r2_l1 = pygame.transform.scale(r2_live1, (lives_width, lives_height))

r2_live2 = pygame.image.load("lives.jpeg")
r2_l2 = pygame.transform.scale(r2_live2, (lives_width, lives_height))

r2_live3 = pygame.image.load("lives.jpeg")
r2_l3 = pygame.transform.scale(r2_live3, (lives_width, lives_height))


r1_live1 = pygame.image.load("lives.jpeg")
r1_l1 = pygame.transform.scale(r1_live1, (lives_width, lives_height))

r1_live2 = pygame.image.load("lives.jpeg")
r1_l2 = pygame.transform.scale(r1_live2, (lives_width, lives_height))

r1_live3 = pygame.image.load("lives.jpeg")
r1_l3 = pygame.transform.scale(r1_live3, (lives_width, lives_height))

rocket1_img = pygame.image.load("rocket.png")
rocket1 = pygame.transform.rotate(
    pygame.transform.scale(rocket1_img, (rocket_width, rocket_height)), 270
)
rocket2_img = pygame.image.load("rocket.png")
rocket2 = pygame.transform.rotate(
    pygame.transform.scale(rocket2_img, (rocket_width, rocket_height)), 90
)

pygame.display.set_caption("First game")


def handle_bullets(r1_bullets, r2_bullets, r1, r2):
    global r1_lives
    global r2_lives
    for bullet in r1_bullets:
        bullet.x += bullets_vel
        if r2.colliderect(bullet):
            r1_bullets.remove(bullet)
            r2_lives -= 1

    for bullet in r2_bullets:
        bullet.x -= bullets_vel
        if r1.colliderect(bullet):
            r2_bullets.remove(bullet)
            r1_lives -= 1


def r1_movement(key, r1):
    key = pygame.key.get_pressed()
    if key[pygame.K_a] and r1.x - speed > 0:
        r1.x -= speed + 0.5

    elif key[pygame.K_d] and r1.x + speed + r1.width < border.x:
        r1.x += speed

    elif key[pygame.K_w] and r1.y - speed > 0:
        r1.y -= speed + 0.5

    elif key[pygame.K_s] and r1.y + speed + r1.height < SCREENHEIGHT:
        r1.y += speed


def r2_movement(key, r2):
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and r2.x - speed > border.x + border.width + 15:
        r2.x -= speed + 0.5

    elif key[pygame.K_RIGHT] and r2.x + speed < SCREENWIDTH - r2.width:
        r2.x += speed

    elif key[pygame.K_UP] and r2.y - speed > 0:
        r2.y -= speed + 0.5

    elif key[pygame.K_DOWN] and r2.y + speed + r2.height < SCREENHEIGHT:
        r2.y += speed


def draw_window(r1, r2, r1_bullets, r2_bullets):
    screen.blit(background_img, ((0, 0)))
    pygame.draw.rect(screen, border_color, border)
    screen.blit(rocket1, (r1.x, r1.y))
    screen.blit(rocket2, (r2.x, r2.y))

    if r1_lives == 0:
        print("player 1 wins!!!!")
        pygame.quit()
    if r2_lives == 0:
        print("player 2 wins!!!!")
        pygame.quit()
    if r1_lives >= 1:
        screen.blit(r1_l1, (25, 25))
    if r1_lives >= 2:
        screen.blit(r1_l2, (70, 25))
    if r1_lives == 3:
        screen.blit(r1_l3, (115, 25))
    if r2_lives >= 1:
        screen.blit(r2_l1, (SCREENWIDTH - 75, 25))
    if r2_lives >= 2:
        screen.blit(r2_l2, (SCREENWIDTH - 120, 25))
    if r2_lives == 3:
        screen.blit(r2_l3, (SCREENWIDTH - 165, 25))

    for bullet in r1_bullets:
        pygame.draw.rect(screen, red, bullet)

    for bullet in r2_bullets:
        pygame.draw.rect(screen, red, bullet)

    pygame.display.update()


def main():
    r1 = pygame.Rect(100, 100, rocket_width, rocket_height)
    r2 = pygame.Rect(700, 100, rocket_width, rocket_height)
    r1_bullets = []
    r2_bullets = []
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(r1_bullets) <= max_bullets:
                    bullet = pygame.Rect(
                        r1.x + r1.width, r1.y + r1.height // 2 - 2, 10, 5
                    )
                    r1_bullets.append(bullet)

                if event.key == pygame.K_m and len(r1_bullets) <= max_bullets:
                    bullet = pygame.Rect(r2.x, r2.y + r2.height // 2 - 2, 10, 5)
                    r2_bullets.append(bullet)

        key = pygame.key.get_pressed()
        r1_movement(key, r1)
        r2_movement(key, r2)
        draw_window(r1, r2, r1_bullets, r2_bullets)
        handle_bullets(r1_bullets, r2_bullets, r1, r2)
    pygame.quit()


if __name__ == "__main__":
    main()

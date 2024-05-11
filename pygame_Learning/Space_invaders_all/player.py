import pygame
from lasers import Laser

SCREENWIDTH = 1000
SCREENHEIGHT = 1000


class Player:
    def __init__(self, x, y):
        self.starship_width = 150
        self.starship_height = 75
        self.starship = pygame.transform.rotate(
            pygame.transform.scale(
                pygame.image.load("images/starship.png"),
                (self.starship_width, self.starship_height),
            ),
            90,
        )
        self.rect = self.starship.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.laser_time = 0
        self.laser_cooldown = 200
        self.laser_group = pygame.sprite.Group()
        self.ready = True
        self.sprite = Laser(pygame.mouse.get_pos())
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

    def update(self):
        x, y = pygame.mouse.get_pos()
        self.rect.x = x
        self.rect.y = y
        self.screen.blit(
            self.starship,
            (
                self.rect.x - self.starship_height / 2,
                self.rect.y - self.starship_width / 2,
            ),
        )
        self.recharge()

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.ready:
            self.ready = False
            self.shoot_laser()
            self.laser_time = pygame.time.get_ticks()

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot_laser(self):
        self.sprite.laser.add(Laser(self.rect.center))
        self.sprite.update()

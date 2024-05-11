import pygame

SCREENWIDTH = 1000
SCREENHEIGHT = 1000


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load("images/missile.webp"),
            (5, 10),
        )
        self.rect = self.image.get_rect(center=pos)
        self.laser = pygame.sprite.Group()
        self.speed = 3
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.x, self.y = pygame.mouse.get_pos()


    def destroy(self):
        if self.rect.y <= 0:
            self.kill()

    def update(self):
        self.rect.y = self.y
        self.rect.y += self.speed
        self.draw(self.screen)

    def draw(self, screen):
        self.x, self.y = pygame.mouse.get_pos()
        screen.blit(self.image, (self.x, self.rect.y))

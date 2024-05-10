import pygame, random
from pygame.locals import *

SCREENWIDTH = 1000
SCREENHEIGHT = 1000
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))


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

    def update(self):
        x, y = pygame.mouse.get_pos()
        self.rect.x = x
        self.rect.y = y
        screen.blit(
            self.starship,
            (
                self.rect.x - self.starship_height / 2,
                self.rect.y - self.starship_width / 2,
            ),
        )


player = Player(SCREENWIDTH / 2, SCREENHEIGHT / 5)


class Bullet:
    def __init__(self, x, y):
        self.bullet_width = 5
        self.bullet_height = 10
        self.bullet = pygame.transform.scale(
            pygame.image.load("images/missile.webp"),
            (self.bullet_width, self.bullet_height),
        )
        self.rect = self.bullet.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = pygame.Vector2(random.uniform(-1.0,1.0), -5)  # Move upward (negative y-velocity)

    def update(self):
        self.rect.centerx += self.velocity.x
        self.rect.centery += self.velocity.y


bullet = Bullet(
    player.rect.x - player.starship_height / 2,
    player.rect.y - player.starship_width / 2,
)


class BulletManager:
    def __init__(self):
        self.bullets = []  # Initialize an empty list for bullets

    def create_bullet(self, x, y):
        new_bullet = Bullet(x, y)
        self.bullets.append(new_bullet)  # Add the new bullet to the list

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

    def render_bullets(self, screen):
        for bullet in self.bullets:
            screen.blit(bullet.bullet, (bullet.rect.x, bullet.rect.y))


def main():
    pygame.mouse.set_visible(False)
    Bg = pygame.transform.scale(
        pygame.image.load("images/background.webp"), (SCREENWIDTH, SCREENHEIGHT)
    )
    fps = 60
    running = True
    clock = pygame.time.Clock()
    clock.tick(fps)
    countdown_ms = 100
    ms_100_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(ms_100_timer, countdown_ms)
    bullet_manager = BulletManager()
    while running:
        screen.blit(Bg, (0, 0))
        player.update()
        bullet.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet_manager.create_bullet(player.rect.centerx, player.rect.top)
        bullet_manager.update_bullets()
        bullet_manager.render_bullets(screen)

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()

    # Update bullet positions

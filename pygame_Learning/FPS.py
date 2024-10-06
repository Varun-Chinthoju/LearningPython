import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
FPS = 60

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))


class Player:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 5
        self.direction = None
        self.gun = 1
        self.health = 100
        self.color = RED
        self.kills = 0
        self.round = 1
        self.mines = []
        self.drones = []
        self.walls = []
        self.bullet_streams = []

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < HEIGHT - 20:
            self.y += self.speed
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < WIDTH - 20:
            self.x += self.speed


class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 20)
        self.y = random.randint(0, HEIGHT - 20)
        self.speed = random.uniform(1, 3)
        self.hits = random.randint(1, 5)  # Varying number of hits
        self.color = (255, 0, 0)  # Red color for zombies

    def move(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx /= dist
            dy /= dist
            self.x += dx * self.speed
            self.y += dy * self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, 20, 20))
        # Display hits remaining
        font = pygame.font.Font(None, 24)
        text = font.render(str(self.hits), 1, (255, 255, 255))
        screen.blit(text, (self.x + 5, self.y + 5))


class Bullet:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed


class Mine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 50


class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 500
        self.bullets = []
        self.angle = 0
        self.gun_cooldown = 0
        self.shoot_delay = 1000
        self.last_shot_time = 0

    def move(self, player, enemies, delta_time):
        # Move towards player
        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            dx /= dist
            dy /= dist
            self.x += dx * self.speed * delta_time / 1000
            self.y += dy * self.speed * delta_time / 1000


class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.health = 500


class BulletStream:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []

    def update(self):
        pass


class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = [Enemy() for _ in range(50)]
        self.bullets = []
        self.gun_cooldown = 0
        self.mouse_down = False
        self.last_update_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - self.player.x
                dy = mouse_y - self.player.y
                self.player.direction = math.atan2(dy, dx)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_down = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_down = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.player.gun = 1
                elif event.key == pygame.K_2:
                    self.player.gun = 2
                elif event.key == pygame.K_3:
                    self.player.gun = 3

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx = mouse_x - self.player.x
                dy = mouse_y - self.player.y
                self.player.direction = math.atan2(dy, dx)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.shoot()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.player.gun = 1
                elif event.key == pygame.K_2:
                    self.player.gun = 2
                elif event.key == pygame.K_3:
                    self.player.gun = 3

    def shoot(self):
        if self.gun_cooldown == 0:
            if self.player.gun == 1:  # Pistol
                bullet_speed = 10
                self.bullets.append(
                    Bullet(
                        self.player.x,
                        self.player.y,
                        self.player.direction,
                        bullet_speed,
                    )
                )
            elif self.player.gun == 2:  # Rifle
                bullet_speed = 15
                self.bullets.append(
                    Bullet(
                        self.player.x,
                        self.player.y,
                        self.player.direction,
                        bullet_speed,
                    )
                )
            elif self.player.gun == 3:  # Shotgun
                bullet_speed = 10
                for _ in range(5):
                    angle = self.player.direction + random.uniform(-0.1, 0.1)
                    self.bullets.append(
                        Bullet(self.player.x, self.player.y, angle, bullet_speed)
                    )
            self.gun_cooldown = 10  # cooldown for 10 frames

    def update(self):
        # Update game logic here
        delta_time = pygame.time.get_ticks() - self.last_update_time
        self.last_update_time = pygame.time.get_ticks()

        self.player.move()
        for enemy in self.enemies:
            enemy.move(self.player)

        # Collision detection
        for enemy in self.enemies[:]:
            if (
                enemy.x < self.player.x + 20
                and enemy.x + 20 > self.player.x
                and enemy.y < self.player.y + 20
                and enemy.y + 20 > self.player.y
            ):
                self.player.health -= 1
                self.player.color = BLUE
                self.enemies.remove(enemy)

        # Bullet updates
        # Bullet updates
        for bullet in self.bullets[:]:
            bullet.move()
            for enemy in self.enemies[:]:
                if (
                    bullet.x < enemy.x + 20
                    and bullet.x + 5 > enemy.x
                    and bullet.y < enemy.y + 20
                    and bullet.y + 5 > enemy.y
                ):
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    enemy.hits -= 1  # Reduce hits
                    if enemy.hits <= 0:
                        self.enemies.remove(enemy)
                    self.player.kills += 1
                    break  # Exit inner loop to avoid removing same bullet multiple times

        # Mine updates
        for mine in self.player.mines[:]:
            for enemy in self.enemies[:]:
                if math.hypot(mine.x - enemy.x, mine.y - enemy.y) < mine.radius:
                    self.enemies.remove(enemy)
                    self.player.mines.remove(mine)

        # Drone updates
        for drone in self.player.drones:
            drone.move(self.player, self.enemies, delta_time)
            for drone_bullet in drone.bullets[:]:
                drone_bullet.move()
                for enemy in self.enemies[:]:
                    if (
                        drone_bullet.x < enemy.x + 20
                        and drone_bullet.x + 5 > enemy.x
                        and drone_bullet.y < enemy.y + 20
                        and drone_bullet.y + 5 > enemy.y
                    ):
                        self.enemies.remove(enemy)
                        drone.bullets.remove(drone_bullet)

        # Wall updates
        for wall in self.player.walls[:]:
            for enemy in self.enemies[:]:
                if (
                    wall.x < enemy.x + 20
                    and wall.x + wall.width > enemy.x
                    and wall.y < enemy.y + 20
                    and wall.y + wall.height > enemy.y
                ):
                    self.enemies.remove(enemy)
                    wall.health -= 1
                    if wall.health <= 0:
                        self.player.walls.remove(wall)

        # Bullet stream updates
        for bullet_stream in self.player.bullet_streams:
            bullet_stream.update()
            for bullet in bullet_stream.bullets[:]:
                bullet.move()
                for enemy in self.enemies[:]:
                    if (
                        bullet.x < enemy.x + 20
                        and bullet.x + 5 > enemy.x
                        and bullet.y < enemy.y + 20
                        and bullet.y + 5 > enemy.y
                    ):
                        self.enemies.remove(enemy)
                        bullet_stream.bullets.remove(bullet)

        # Check for game over
        if self.player.health <= 0:
            print("Game Over")
            pygame.quit()
            sys.exit()

        # Check for round completion
        if len(self.enemies) == 0:
            self.player.round += 1
            self.enemies = [Enemy() for _ in range(50 + self.player.round * 20)]

        # Decrease gun cooldown
        self.gun_cooldown -= 1
        if self.gun_cooldown < 0:
            self.gun_cooldown = 0

    def render(self):
        screen.fill(WHITE)
        self.render_player()
        self.render_enemies()
        self.render_bullets()
        self.render_mines()
        self.render_drones()
        self.render_walls()
        self.render_bullet_streams()
        self.render_hud()
        pygame.display.flip()

    def render_player(self):
        pygame.draw.rect(
            screen, self.player.color, (self.player.x, self.player.y, 20, 20)
        )

    def render_enemies(self):
        for enemy in self.enemies:
            pygame.draw.rect(screen, RED, (enemy.x, enemy.y, 20, 20))

    def render_bullets(self):
        for bullet in self.bullets:
            pygame.draw.rect(screen, RED, (bullet.x, bullet.y, 5, 5))

    def render_mines(self):
        for mine in self.player.mines:
            pygame.draw.circle(screen, YELLOW, (mine.x, mine.y), mine.radius)

    def render_drones(self):
        for drone in self.player.drones:
            pygame.draw.rect(screen, GREEN, (drone.x, drone.y, 20, 20))
            for drone_bullet in drone.bullets:
                pygame.draw.rect(screen, RED, (drone_bullet.x, drone_bullet.y, 5, 5))

    def render_walls(self):
        for wall in self.player.walls:
            pygame.draw.rect(screen, GRAY, (wall.x, wall.y, wall.width, wall.height))

    def render_bullet_streams(self):
        for bullet_stream in self.player.bullet_streams:
            for bullet in bullet_stream.bullets:
                pygame.draw.rect(screen, RED, (bullet.x, bullet.y, 5, 5))

    def render_hud(self):
        font = pygame.font.Font(None, 36)

        # Render gun type text
        gun_text = "Gun: "
        if self.player.gun == 1:
            gun_text += "Pistol"
        elif self.player.gun == 2:
            gun_text += "Rifle"
        elif self.player.gun == 3:
            gun_text += "Shotgun"
        text = font.render(gun_text, 1, (0, 0, 0))
        screen.blit(text, (10, 10))

        # Render health text
        health_text = "Health: " + str(self.player.health)
        text = font.render(health_text, 1, (0, 0, 0))
        screen.blit(text, (10, 40))

        # Render kills text
        kills_text = "Kills: " + str(self.player.kills)
        text = font.render(kills_text, 1, (0, 0, 0))
        screen.blit(text, (10, 70))

        # Render round text
        round_text = "Round: " + str(self.player.round)
        text = font.render(round_text, 1, (0, 0, 0))
        screen.blit(text, (10, 100))

        # Render mines text
        mines_text = "Mines: " + str(len(self.player.mines))
        text = font.render(mines_text, 1, (0, 0, 0))
        screen.blit(text, (10, 130))

        # Render drones text
        drones_text = "Drones: " + str(len(self.player.drones))
        text = font.render(drones_text, 1, (0, 0, 0))
        screen.blit(text, (10, 160))

        # Render walls text
        walls_text = "Walls: " + str(len(self.player.walls))
        text = font.render(walls_text, 1, (0, 0, 0))
        screen.blit(text, (10, 190))


def main():
    clock = pygame.time.Clock()
    game = Game()

    while True:
        game.handle_events()
        game.update()
        game.render()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

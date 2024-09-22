import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1000, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

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
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
            if self.y < 0:
                self.y = 0
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
            if self.y > HEIGHT - 20:
                self.y = HEIGHT - 20
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            if self.x > WIDTH - 20:
                self.x = WIDTH - 20

class Enemy:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.randint(1, 3)

    def move(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        angle = math.atan2(dy, dx)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed
    
    def collide(self, player):
        if player.x < self.x + 20 and player.x + 20 > self.x and player.y < self.y + 20 and player.y + 20 > self.y:
            return True
        return False

class Bullet:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def collide(self, enemy):
        if self.x < enemy.x + 20 and self.x + 5 > enemy.x and self.y < enemy.y + 20 and self.y + 5 > enemy.y:
            return True
        return False

class Mine:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 50

    def collide(self, enemy):
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        if distance < self.radius:
            return True
        return False

class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.bullets = []

    def move(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        angle = math.atan2(dy, dx)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed
        for enemy in enemies:
            if math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2) < 100:
                self.bullets.append(Bullet(self.x, self.y, math.atan2(enemy.y - self.y, enemy.x - self.x), 10))

class Wall:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.health = 500

    def collide(self, enemy):
        if enemy.x < self.x + self.width and enemy.x + 20 > self.x and enemy.y < self.y + self.height and enemy.y + 20 > self.y:
            return True
        return False

class BulletStream:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bullets = []

    def update(self):
        for direction in range(10):
            self.bullets.append(Bullet(self.x, self.y, direction * math.pi / 5, 10))

class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = [Enemy() for _ in range(200)]
        self.bullets = []
        self.gun_cooldown = 0
        self.mouse_down = False

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

    def update(self):
        self.player.move()
        for enemy in self.enemies[:]:
            enemy.move(self.player)
            if enemy.collide(self.player):
                self.player.health -= 1
                self.player.color = BLUE
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
            for bullet in self.bullets[:]:
                if bullet.collide(enemy):
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    self.player.kills += 1
                    if self.player.kills % 50 == 0:
                        self.player.health += 10
                    if self.player.kills % 200 == 0:
                        self.player.mines.append(Mine(self.player.x, self.player.y))
                    if self.player.kills % 300 == 0:
                        self.player.drones.append(Drone(self.player.x, self.player.y))
                    if self.player.kills % 500 == 0:
                        self.player.walls.append(Wall(self.player.x - 50, self.player.y - 50))
                        self.player.bullet_streams.append(BulletStream(self.player.x, self.player.y))
            for mine in self.player.mines[:]:
                if mine.collide(enemy):
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    if mine in self.player.mines:
                        self.player.mines.remove(mine)
                    for e in self.enemies[:]:
                        if mine.collide(e):
                            if e in self.enemies:
                                self.enemies.remove(e)
            for drone in self.player.drones:
                drone.move(self.player)
                for drone_bullet in drone.bullets[:]:
                    if drone_bullet.collide(enemy):
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        if drone_bullet in drone.bullets:
                            drone.bullets.remove(drone_bullet)
            for wall in self.player.walls[:]:
                if wall.collide(enemy):
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    wall.health -= 1
                    if wall.health <= 0:
                        if wall in self.player.walls:
                            self.player.walls.remove(wall)
            for bullet_stream in self.player.bullet_streams:
                bullet_stream.update()
                for bullet in bullet_stream.bullets[:]:
                    if bullet.collide(enemy):
                        if enemy in self.enemies:
                            self.enemies.remove(enemy)
                        if bullet in bullet_stream.bullets:
                            bullet_stream.bullets.remove(bullet)
        if len(self.enemies) == 0:
            self.player.round += 1
            self.enemies = [Enemy() for _ in range(200 + self.player.round * 20)]
        for bullet in self.bullets[:]:
            bullet.move()
        for drone in self.player.drones:
            for drone_bullet in drone.bullets[:]:
                drone_bullet.move()
        for bullet_stream in self.player.bullet_streams:
            for bullet in bullet_stream.bullets[:]:
                bullet.move()
        self.gun_cooldown -= 1
        if self.mouse_down and self.gun_cooldown <= 0:
            self.shoot()
        if self.player.health <= 0:
            print("Game Over")
            pygame.quit()
            sys.exit()

    def shoot(self):
        if self.player.gun == 1: # Pistol
            self.bullets.append(Bullet(self.player.x, self.player.y, self.player.direction, 10))
            self.gun_cooldown = 10
        elif self.player.gun == 2: # Rapid Fire
            self.bullets.append(Bullet(self.player.x, self.player.y, self.player.direction, 10))
            self.gun_cooldown = 1
        elif self.player.gun == 3: # Laser
            self.bullets.append(Bullet(self.player.x, self.player.y, self.player.direction, 20))
            self.gun_cooldown = 0

    def render(self):
        screen.fill(WHITE)
        pygame.draw.rect(screen, self.player.color, (self.player.x, self.player.y, 20, 20))
        for enemy in self.enemies:
            pygame.draw.rect(screen, RED, (enemy.x, enemy.y, 20, 20))
        for bullet in self.bullets:
            pygame.draw.rect(screen, RED, (bullet.x, bullet.y, 5, 5))
        for mine in self.player.mines:
            pygame.draw.circle(screen, YELLOW, (mine.x, mine.y), mine.radius)
        for drone in self.player.drones:
            pygame.draw.rect(screen, GREEN, (drone.x, drone.y, 20, 20))
            for drone_bullet in drone.bullets:
                pygame.draw.rect(screen, RED, (drone_bullet.x, drone_bullet.y, 5, 5))
        for wall in self.player.walls:
            pygame.draw.rect(screen, GRAY, (wall.x, wall.y, wall.width, wall.height))
        for bullet_stream in self.player.bullet_streams:
            for bullet in bullet_stream.bullets:
                pygame.draw.rect(screen, RED, (bullet.x, bullet.y, 5, 5))
        font = pygame.font.Font(None, 36)
        text = font.render("Gun: " + str(self.player.gun), 1, (0, 0, 0))
        screen.blit(text, (10, 10))
        text = font.render("Health: " + str(self.player.health), 1, (0, 0, 0))
        screen.blit(text, (10, 40))
        text = font.render("Kills: " + str(self.player.kills), 1, (0, 0, 0))
        screen.blit(text, (10, 70))
        text = font.render("Round: " + str(self.player.round), 1, (0, 0, 0))
        screen.blit(text, (10, 100))
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Game()

    while True:
        game.handle_events()
        game.update()
        game.render()
        clock.tick(60)

if __name__ == "__main__":
    main()
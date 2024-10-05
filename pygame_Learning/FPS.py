import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player properties
PLAYER_SIZE = 20
PLAYER_SPEED = 5

# Enemy properties
ENEMY_SIZE = 20
ENEMY_SPEED = 2

# Gun properties
GUN_FIRE_RATE = 1

class Game:
    def __init__(self):
        self.player = {"x": SCREEN_WIDTH / 2, "y": SCREEN_HEIGHT / 2, "gun": {"name": "Pistol", "unlocks_at": 0, "damage": 1, "fire_rate": 1}, "kills": 0, "walls": [], "health": 100, "level": 1, "xp": 0}
        self.enemies = []
        self.guns = [
            {"name": "Pistol", "unlocks_at": 0, "damage": 1, "fire_rate": 1},
            {"name": "Rifle", "unlocks_at": 100, "damage": 2, "fire_rate": 0.5},
            {"name": "Shotgun", "unlocks_at": 500, "damage": 3, "fire_rate": 0.2},
            {"name": "Sniper", "unlocks_at": 2000, "damage": 5, "fire_rate": 0.1},
            {"name": "Assault Rifle", "unlocks_at": 3000, "damage": 0.5, "fire_rate": 5},
            {"name": "Laser", "unlocks_at": 5000, "damage": 0.2, "fire_rate": 10}
        ]
        self.bullets = []
        self.mines = []
        self.drones = []
        self.power_ups = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.player["gun"] = self.guns[0]
                elif event.key == pygame.K_2 and self.player["kills"] >= self.guns[1]["unlocks_at"]:
                    self.player["gun"] = self.guns[1]
                elif event.key == pygame.K_3 and self.player["kills"] >= self.guns[2]["unlocks_at"]:
                    self.player["gun"] = self.guns[2]
                elif event.key == pygame.K_4 and self.player["kills"] >= self.guns[3]["unlocks_at"]:
                    self.player["gun"] = self.guns[3]
                elif event.key == pygame.K_5 and self.player["kills"] >= self.guns[4]["unlocks_at"]:
                    self.player["gun"] = self.guns[4]
                elif event.key == pygame.K_6 and self.player["kills"] >= self.guns[5]["unlocks_at"]:
                    self.player["gun"] = self.guns[5]
                elif event.key == pygame.K_m:
                    if len(self.player["walls"]) < 5:
                        self.player["walls"].append({"x": self.player["x"], "y": self.player["y"]})

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player["y"] -= PLAYER_SPEED
        if keys[pygame.K_s]:
            self.player["y"] += PLAYER_SPEED
        if keys[pygame.K_a]:
            self.player["x"] -= PLAYER_SPEED
        if keys[pygame.K_d]:
            self.player["x"] += PLAYER_SPEED

        # Spawn enemies
        if random.random() < 0.05:
            self.enemies.append({"x": random.randint(0, SCREEN_WIDTH - ENEMY_SIZE), "y": random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE), "type": random.choice(["basic", "fast", "tank"])})

        # Move enemies
        for enemy in self.enemies:
            dx = self.player["x"] - enemy["x"]
            dy = self.player["y"] - enemy["y"]
            dist = math.hypot(dx, dy)
            if dist > 0:
                dx /= dist
                dy /= dist
                enemy["x"] += dx * ENEMY_SPEED
                enemy["y"] += dy * ENEMY_SPEED * (1 if enemy["type"] != "fast" else 2)

        # Shoot bullets
        if keys[pygame.K_SPACE]:
            if len(self.bullets) < self.player["gun"]["fire_rate"]:
                self.bullets.append({"x": self.player["x"], "y": self.player["y"], "dx": 0, "dy": 0})

        # Move bullets
        for bullet in self.bullets[:]:
            bullet["x"] += bullet["dx"]
            bullet["y"] += bullet["dy"]
            if bullet["x"] < 0 or bullet["x"] > SCREEN_WIDTH or bullet["y"] < 0 or bullet["y"] > SCREEN_HEIGHT:
                self.bullets.remove(bullet)

        # Collision detection
        for enemy in self.enemies[:]:
            for bullet in self.bullets[:]:
                if (bullet["x"] < enemy["x"] + ENEMY_SIZE and
                    bullet["x"] + 5 > enemy["x"] and
                    bullet["y"] < enemy["y"] + ENEMY_SIZE and
                    bullet["y"] + 5 > enemy["y"]):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    self.player["kills"] += 1
                    self.player["xp"] += 10
                    break

        # Update mines
        for mine in self.mines[:]:
            for enemy in self.enemies[:]:
                if math.hypot(mine["x"] - enemy["x"], mine["y"] - enemy["y"]) < 50:
                    self.enemies.remove(enemy)
                    self.mines.remove(mine)
                    break

        # Update drones
        for drone in self.drones[:]:
            drone["x"] += drone["dx"]
            drone["y"] += drone["dy"]
            for enemy in self.enemies[:]:
                if math.hypot(drone["x"] - enemy["x"], drone["y"] - enemy["y"]) < 100:
                    self.enemies.remove(enemy)
                    break

        # Unlock guns
        for gun in self.guns:
            if self.player["kills"] >= gun["unlocks_at"] and self.player["gun"]["name"] != gun["name"]:
                self.player["gun"] = gun
                print(f"Unlocked {gun['name']}")

        # Level up
        if self.player["xp"] >= self.player["level"] * 100:
            self.player["level"] += 1
            self.player["xp"] = 0
            self.player["health"] += 10
            print(f"Leveled up to {self.player['level']}")

        # Spawn power-ups
        if random.random() < 0.01:
            self.power_ups.append({"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(0, SCREEN_HEIGHT), "type": random.choice(["health", "ammo", "speed"])})

        # Apply power-ups
        for power_up in self.power_ups[:]:
            if math.hypot(power_up["x"] - self.player["x"], power_up["y"] - self.player["y"]) < 20:
                if power_up["type"] == "health":
                    self.player["health"] += 20
                elif power_up["type"] == "ammo":
                    self.player["gun"]["fire_rate"] += 1
                elif power_up["type"] == "speed":
                    PLAYER_SPEED += 1
                self.power_ups.remove(power_up)
                break

    def render(self):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, BLUE, (self.player["x"], self.player["y"], PLAYER_SIZE, PLAYER_SIZE))
        for enemy in self.enemies:
            pygame.draw.rect(screen, RED, (enemy["x"], enemy["y"], ENEMY_SIZE, ENEMY_SIZE))
        for bullet in self.bullets:
            pygame.draw.rect(screen, WHITE, (bullet["x"], bullet["y"], 5, 5))
        for mine in self.mines:
            pygame.draw.circle(screen, YELLOW, (mine["x"], mine["y"]), 20)
        for drone in self.drones:
            pygame.draw.rect(screen, GREEN, (drone["x"], drone["y"], 10, 10))
        for wall in self.player["walls"]:
            pygame.draw.rect(screen, WHITE, (wall["x"], wall["y"], 20, 20))
        for power_up in self.power_ups:
            pygame.draw.circle(screen, GREEN, (power_up["x"], power_up["y"]), 10)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Kills: {self.player['kills']}", 1
        
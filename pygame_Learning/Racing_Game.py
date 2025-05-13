import pygame
import math
import time
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (245, 245, 245)  # Light grey background
TRACK_COLOR = (0, 0, 0)  # Track color (dark grey/black)
MUD_COLOR = (139, 69, 19)  # Brown color for mud
WATER_COLOR = (0, 0, 255)  # Blue color for water
MAX_SPEED = 10
FRICTION = 0.98  # How much friction slows the car down
TURN_SMOOTHNESS = 0.05  # Smoothness of turns
DRIFT_TRAIL_DURATION = 1.0
CAR_WIDTH, CAR_HEIGHT = 50, 30
CAR_RADIUS = 25  # Approximate radius for collision detection

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drift Racer")
clock = pygame.time.Clock()

# Define particle for tire smoke
class SmokeParticle:
    def __init__(self, x, y, speed_x, speed_y):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.size = random.randint(2, 6)  # Smaller size range for smaller particles
        self.alpha = 255  # Full opacity
        self.lifetime = random.uniform(0.5, 2.0)  # Lifetime for the smoke particle

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.size *= 0.98  # Gradually shrink the smoke
        self.alpha -= 5  # Fade out over time
        self.lifetime -= 0.02  # Decrease the lifetime
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surface):
        # Draw smoke particle with fading effect
        if self.alpha > 0:
            smoke_color = (180, 180, 180, self.alpha)  # Grey with fading opacity
            pygame.draw.circle(surface, smoke_color, (int(self.x), int(self.y)), int(self.size))

class SplashParticle(SmokeParticle):
    def draw(self, surface):
        if self.alpha > 0:
            splash_color = (0, 100, 255, self.alpha)  # Blue for water splashes
            pygame.draw.circle(surface, splash_color, (int(self.x), int(self.y)), int(self.size))

class MudParticle(SmokeParticle):
    def draw(self, surface):
        if self.alpha > 0:
            mud_color = (139, 69, 19, self.alpha)  # Brown for mud splatters
            pygame.draw.circle(surface, mud_color, (int(self.x), int(self.y)), int(self.size))


# Smoke particles list
smoke_particles = []
drift_tracks = []  # Initialize drift_tracks here

# Load player car images
player1_car = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
player1_car.fill((0, 200, 255))

player2_car = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
player2_car.fill((255, 100, 100))

# Player properties
players = [
    {"pos": [WIDTH // 3, HEIGHT // 2], "angle": 0, "speed": 0, "velocity": [0, 0]},  # Player 1
    {"pos": [2 * WIDTH // 3, HEIGHT // 2], "angle": 0, "speed": 0, "velocity": [0, 0]}  # Player 2
]

# Function to check if player is in mud or water
def check_in_special_zone(player):
    # Mud zone
    mud_rect = pygame.Rect(150, 250, 200, 100)
    if mud_rect.collidepoint(player["pos"][0], player["pos"][1]):
        return 'mud'

    # Water zone
    water_rect = pygame.Rect(600, 500, 200, 100)
    if water_rect.collidepoint(player["pos"][0], player["pos"][1]):
        return 'water'

    return None

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()

    # Reset speed if no buttons are pressed
    for player in players:
        player["speed"] *= 0.9  # Gradually slow down

    # Player 1 (WASD)
    turning1 = False
    if keys[pygame.K_w]:
        players[0]["speed"] = min(players[0]["speed"] + 0.3, MAX_SPEED)
    if keys[pygame.K_s]:
        players[0]["speed"] = max(players[0]["speed"] - 0.3, -MAX_SPEED)
    if keys[pygame.K_a]:
        players[0]["angle"] += 5
        turning1 = True
    if keys[pygame.K_d]:
        players[0]["angle"] -= 5
        turning1 = True

    # Player 2 (Arrow keys)
    turning2 = False
    if keys[pygame.K_UP]:
        players[1]["speed"] = min(players[1]["speed"] + 0.3, MAX_SPEED)
    if keys[pygame.K_DOWN]:
        players[1]["speed"] = max(players[1]["speed"] - 0.3, -MAX_SPEED)
    if keys[pygame.K_LEFT]:
        players[1]["angle"] += 5
        turning2 = True
    if keys[pygame.K_RIGHT]:
        players[1]["angle"] -= 5
        turning2 = True

    # Check for special zones (mud/water)
    for player in players:
        special_zone = check_in_special_zone(player)
        if special_zone == 'mud':
            player["speed"] *= 0.7  # Reduce speed in mud
        elif special_zone == 'water':
            player["speed"] *= 0.5  # Reduce speed in water

    # Handle collisions between the two cars
    p1, p2 = players[0], players[1]
    dx = p2["pos"][0] - p1["pos"][0]
    dy = p2["pos"][1] - p1["pos"][1]
    distance = math.hypot(dx, dy)
    min_distance = 2 * CAR_RADIUS
    
    if distance < min_distance and distance != 0:
        # Calculate overlap amount
        overlap = min_distance - distance
        push_vector = [dx / distance * overlap / 2, dy / distance * overlap / 2]
        
        # Separate the cars to resolve the collision
        p1["pos"][0] -= push_vector[0]
        p1["pos"][1] -= push_vector[1]
        p2["pos"][0] += push_vector[0]
        p2["pos"][1] += push_vector[1]
        
        # Calculate the normal and tangent vectors for the collision
        normal = [dx / distance, dy / distance]
        tangent = [-normal[1], normal[0]]
        
        # Project velocities onto the normal and tangent vectors
        v1n = normal[0] * p1["velocity"][0] + normal[1] * p1["velocity"][1]
        v2n = normal[0] * p2["velocity"][0] + normal[1] * p2["velocity"][1]
        v1t = tangent[0] * p1["velocity"][0] + tangent[1] * p1["velocity"][1]
        v2t = tangent[0] * p2["velocity"][0] + tangent[1] * p2["velocity"][1]
        
        # Swap the normal components (elastic collision)
        v1n_new = v2n * 0.8  # Slightly dampen the collision
        v2n_new = v1n * 0.8
        
        # Update velocities
        p1["velocity"][0] = tangent[0] * v1t + normal[0] * v1n_new
        p1["velocity"][1] = tangent[1] * v1t + normal[1] * v1n_new
        p2["velocity"][0] = tangent[0] * v2t + normal[0] * v2n_new
        p2["velocity"][1] = tangent[1] * v2t + normal[1] * v2n_new
        
        # Add slight rotation effect for realism
        p1["angle"] += random.uniform(-10, 10)
        p2["angle"] += random.uniform(-10, 10)

        # Add splash or mud effects based on zones
        for player in [p1, p2]:
            zone = check_in_special_zone(player)
            if zone == 'mud':
                for _ in range(10):  # Increase for more intense splatter
                    speed_x = random.uniform(-3, 3)
                    speed_y = random.uniform(-3, 3)
                    size = random.randint(3, 7)
                    lifetime = random.uniform(0.5, 1.5)
                    smoke_particles.append(SmokeParticle(player["pos"][0], player["pos"][1], speed_x, speed_y))
            elif zone == 'water':
                for _ in range(15):  # Increase for more dramatic splash
                    speed_x = random.uniform(-5, 5)
                    speed_y = random.uniform(-5, 5)
                    size = random.randint(2, 6)
                    lifetime = random.uniform(0.3, 0.8)
                    smoke_particles.append(SmokeParticle(player["pos"][0], player["pos"][1], speed_x, speed_y))

        # Add drift tracks and smoke for both cars on collision
        for player in [p1, p2]:
            # Add drift tracks
            corners = [
                (player["pos"][0] + 25 * math.cos(rad_angle) - 15 * math.sin(rad_angle),
                 player["pos"][1] - 25 * math.sin(rad_angle) - 15 * math.cos(rad_angle)),
                (player["pos"][0] + 25 * math.cos(rad_angle) + 15 * math.sin(rad_angle),
                 player["pos"][1] - 25 * math.sin(rad_angle) + 15 * math.cos(rad_angle)),
                (player["pos"][0] - 25 * math.cos(rad_angle) + 15 * math.sin(rad_angle),
                 player["pos"][1] + 25 * math.sin(rad_angle) + 15 * math.cos(rad_angle)),
                (player["pos"][0] - 25 * math.cos(rad_angle) - 15 * math.sin(rad_angle),
                 player["pos"][1] + 25 * math.sin(rad_angle) - 15 * math.cos(rad_angle))
            ]

            for corner in corners:
                drift_tracks.append((int(corner[0]), int(corner[1]), time.time()))

            # Add smoke particles
            for _ in range(3):  # Adjust the number of smoke particles
                speed_x = random.uniform(-1, 1) * 2
                speed_y = random.uniform(-1, 1) * 2
                smoke_particles.append(SmokeParticle(player["pos"][0], player["pos"][1], speed_x, speed_y))

    # Update each player's movement and drift
    for player, car_surface, turning in zip(players, [player1_car, player2_car], [turning1, turning2]):
        rad_angle = math.radians(player["angle"])
        forward_vector = [math.cos(rad_angle), -math.sin(rad_angle)]
        player["velocity"][0] += forward_vector[0] * player["speed"] * TURN_SMOOTHNESS
        player["velocity"][1] += forward_vector[1] * player["speed"] * TURN_SMOOTHNESS

        # Apply friction and update position
        player["velocity"][0] *= FRICTION
        player["velocity"][1] *= FRICTION
        player["pos"][0] += player["velocity"][0]
        player["pos"][1] += player["velocity"][1]

        # Keep the player on screen
        player["pos"][0] = max(0, min(WIDTH, player["pos"][0]))
        player["pos"][1] = max(0, min(HEIGHT, player["pos"][1]))

        # Add drift tracks and smoke particles only while turning
        if turning:
            # Add drift tracks
            corners = [
                (player["pos"][0] + 25 * math.cos(rad_angle) - 15 * math.sin(rad_angle),
                 player["pos"][1] - 25 * math.sin(rad_angle) - 15 * math.cos(rad_angle)),
                (player["pos"][0] + 25 * math.cos(rad_angle) + 15 * math.sin(rad_angle),
                 player["pos"][1] - 25 * math.sin(rad_angle) + 15 * math.cos(rad_angle)),
                (player["pos"][0] - 25 * math.cos(rad_angle) + 15 * math.sin(rad_angle),
                 player["pos"][1] + 25 * math.sin(rad_angle) + 15 * math.cos(rad_angle)),
                (player["pos"][0] - 25 * math.cos(rad_angle) - 15 * math.sin(rad_angle),
                 player["pos"][1] + 25 * math.sin(rad_angle) - 15 * math.cos(rad_angle))
            ]
            for corner in corners:
                drift_tracks.append((int(corner[0]), int(corner[1]), time.time()))

            # Add smoke particles
            for _ in range(3):  # Adjust the number of smoke particles
                speed_x = random.uniform(-1, 1) * 2
                speed_y = random.uniform(-1, 1) * 2
                smoke_particles.append(SmokeParticle(player["pos"][0], player["pos"][1], speed_x, speed_y))

    # Remove old drift tracks and smoke particles
    current_time = time.time()
    drift_tracks = [track for track in drift_tracks if current_time - track[2] <= DRIFT_TRAIL_DURATION]
    smoke_particles = [p for p in smoke_particles if p.lifetime > 0]

    # Update and draw particles
    screen.fill(BG_COLOR)
    for track in drift_tracks:
        pygame.draw.circle(screen, TRACK_COLOR, (track[0], track[1]), 4)
    for particle in smoke_particles:
        particle.update()
        particle.draw(screen)

    for player, car_surface in zip(players, [player1_car, player2_car]):
        rotated_car = pygame.transform.rotate(car_surface, player["angle"])
        screen.blit(rotated_car, (player["pos"][0] - rotated_car.get_width() // 2, player["pos"][1] - rotated_car.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

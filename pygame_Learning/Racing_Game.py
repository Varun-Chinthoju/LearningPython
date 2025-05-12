import pygame
import math
import time
import random

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (245, 245, 245)  # Light grey background
GRID_COLOR = (230, 230, 230)
WHITE = (255, 255, 255)
PLAYER1_COLOR = (0, 200, 255)
PLAYER2_COLOR = (255, 100, 100)
TRACK_COLOR = (0, 0, 0)
MAX_SPEED = 6
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

# Smoke particles list
smoke_particles = []
drift_tracks = []  # Initialize drift_tracks here

# Load player car images
player1_car = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
player1_car.fill(PLAYER1_COLOR)

player2_car = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
player2_car.fill(PLAYER2_COLOR)

# Player properties
players = [
    {"pos": [WIDTH // 3, HEIGHT // 2], "angle": 0, "speed": 0, "velocity": [0, 0]},  # Player 1
    {"pos": [2 * WIDTH // 3, HEIGHT // 2], "angle": 0, "speed": 0, "velocity": [0, 0]}  # Player 2
]

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

    # Handle collisions between the two cars
        # Handle collisions between the two cars
    p1, p2 = players[0], players[1]
    dx = p2["pos"][0] - p1["pos"][0]
    dy = p2["pos"][1] - p1["pos"][1]
    distance = math.hypot(dx, dy)
    min_distance = 2 * CAR_RADIUS
# Handle collisions between the two cars
    p1, p2 = players[0], players[1]
    dx = p2["pos"][0] - p1["pos"][0]
    dy = p2["pos"][1] - p1["pos"][1]
    distance = math.hypot(dx, dy)
    min_distance = 2 * CAR_RADIUS

    if distance < min_distance and distance != 0:
        # Calculate the overlap amount
        overlap = min_distance - distance
        # Apply a force to push the cars apart
        push_vector = [dx / distance * overlap / 2, dy / distance * overlap / 2]
        
        # Apply the push to both cars
        p1["pos"][0] -= push_vector[0]
        p1["pos"][1] -= push_vector[1]
        p2["pos"][0] += push_vector[0]
        p2["pos"][1] += push_vector[1]
        
        # Apply rotational force based on collision direction with reduced effect
        p1_angle_change = math.degrees(math.atan2(dy, dx))  # Calculate angle from the collision
        p2_angle_change = math.degrees(math.atan2(-dy, -dx))  # Opposite angle for the second car
        
        # Apply a subtle rotational force to simulate realistic behavior (smaller multiplier)
        p1["angle"] += p1_angle_change * 0.03  # Reduced rotation force for car 1
        p2["angle"] += p2_angle_change * 0.03  # Reduced rotation force for car 2

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

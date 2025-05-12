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
SMOKE_COLOR = (100, 100, 100)
MAX_SPEED = 6
BOOST_SPEED = 10
FRICTION = 0.98  # How much friction slows the car down
TURN_SMOOTHNESS = 0.05  # Smoothness of turns
DRIFT_TRAIL_DURATION = 1.0
CAR_WIDTH, CAR_HEIGHT = 50, 30
CAR_RADIUS = 25  # Approximate radius for collision detection
BOOST_DURATION = 0.8  # How long the boost lasts
BOOST_COOLDOWN = 2.0  # Time between boosts

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drift Racer")
clock = pygame.time.Clock()

drift_tracks = []  # Initialize drift_tracks
smoke_particles = []  # Initialize smoke particles

# Load player car images
player1_car = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
player1_car.fill(PLAYER1_COLOR)

player2_car = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
player2_car.fill(PLAYER2_COLOR)

# Player properties
players = [
    {"pos": [WIDTH // 3, HEIGHT // 2], "angle": 0, "speed": 0, "velocity": [0, 0], "boost_time": 0, "boost_on_cooldown": False},  # Player 1
    {"pos": [2 * WIDTH // 3, HEIGHT // 2], "angle": 0, "speed": 0, "velocity": [0, 0], "boost_time": 0, "boost_on_cooldown": False}  # Player 2
]

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    current_time = time.time()

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
    if keys[pygame.K_LSHIFT] and not players[0]["boost_on_cooldown"]:
        players[0]["speed"] = BOOST_SPEED
        players[0]["boost_time"] = current_time
        players[0]["boost_on_cooldown"] = True

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
    if keys[pygame.K_RSHIFT] and not players[1]["boost_on_cooldown"]:
        players[1]["speed"] = BOOST_SPEED
        players[1]["boost_time"] = current_time
        players[1]["boost_on_cooldown"] = True

    # Handle collisions between the two cars
    p1, p2 = players[0], players[1]
    dx = p2["pos"][0] - p1["pos"][0]
    dy = p2["pos"][1] - p1["pos"][1]
    distance = math.hypot(dx, dy)
    min_distance = 2 * CAR_RADIUS
    if distance < min_distance and distance != 0:
        overlap = min_distance - distance
        push_vector = [dx / distance * overlap / 2, dy / distance * overlap / 2]
        p1["pos"][0] -= push_vector[0]
        p1["pos"][1] -= push_vector[1]
        p2["pos"][0] += push_vector[0]
        p2["pos"][1] += push_vector[1]

    # Update each player's movement and drift
    for player, car_surface, turning in zip(players, [player1_car, player2_car], [turning1, turning2]):
        rad_angle = math.radians(player["angle"])
        forward_vector = [math.cos(rad_angle), -math.sin(rad_angle)]
        player["velocity"][0] += forward_vector[0] * player["speed"] * TURN_SMOOTHNESS
        player["velocity"][1] += forward_vector[1] * player["speed"] * TURN_SMOOTHNESS

        player["velocity"][0] *= FRICTION
        player["velocity"][1] *= FRICTION
        player["pos"][0] += player["velocity"][0]
        player["pos"][1] += player["velocity"][1]

        if turning:
            for _ in range(2):  # Two particles per frame for a denser smoke effect
                smoke_particles.append([player["pos"][0], player["pos"][1], random.randint(10, 15)])

        if player["boost_on_cooldown"] and current_time - player["boost_time"] > BOOST_DURATION:
            player["boost_on_cooldown"] = False

    smoke_particles = [[p[0], p[1], p[2] - 1] for p in smoke_particles if p[2] > 0]

    screen.fill(BG_COLOR)
    for p in smoke_particles:
        pygame.draw.circle(screen, SMOKE_COLOR, (int(p[0]), int(p[1])), p[2])
    for player, car_surface in zip(players, [player1_car, player2_car]):
        rotated_car = pygame.transform.rotate(car_surface, player["angle"])
        screen.blit(rotated_car, (player["pos"][0] - rotated_car.get_width() // 2, player["pos"][1] - rotated_car.get_height() // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 2500, 1500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drift Chase")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)  # Color for drift tracks

# Clock
clock = pygame.time.Clock()

# Car dimensions
car_width, car_height = 200, 100

# Load and scale car images
player_image = pygame.transform.scale(pygame.image.load('images//porche.png'), (car_width, car_height))  # Porsche car for player
police_image = pygame.transform.scale(pygame.image.load('images//police car.png'), (car_width, car_height))  # Police car for cops

# Player car settings
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 0
player_angle = 0
player_turn_angle = 0
acceleration = 0.2
friction = 0.05
rotation_speed = 2
max_turn_angle = 20  # Max turn angle in degrees

# Police car settings
police_speed = 2
police_cars = []
police_turn_angle = 0

# List to store drift tracks
drift_tracks = []

# Spawn police cars at random positions
def spawn_police():
    police_x = random.choice([0, WIDTH - car_width])  # Spawn on the left or right edge
    police_y = random.randint(0, HEIGHT - car_height)  # Random y-coordinate
    police_cars.append([police_x, police_y, 0])  # Add police car with initial angle 0

# Rotate and center image
def rotate_center(image, rect, angle):
    """Rotate an image while keeping its center and size."""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=rect.center)
    return rotated_image, new_rect

# Police car AI: Chase the player
def move_police(police_pos, player_x, player_y):
    police_x, police_y, police_angle = police_pos

    # Calculate direction toward player
    dx, dy = player_x - police_x, player_y - police_y
    distance = math.hypot(dx, dy)
    
    if distance > 0:
        dx, dy = dx / distance, dy / distance  # Normalize direction

    # Move police car toward player
    police_x += dx * police_speed
    police_y += dy * police_speed

    # Update police car angle
    target_angle = math.degrees(math.atan2(-dy, dx))
    police_angle = (police_angle + (target_angle - police_angle) * 0.05) % 360

    # Limit police car turn angle
    police_turn_angle = max(-max_turn_angle, min(max_turn_angle, target_angle - police_angle))

    return [police_x, police_y, police_angle]

# Collision detection between two rectangles
def detect_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get keys for player movement
    keys = pygame.key.get_pressed()

    # Player rotation
    if keys[pygame.K_LEFT] and player_speed > 0:
        player_turn_angle = max(-max_turn_angle, player_turn_angle - rotation_speed)
    if keys[pygame.K_RIGHT] and player_speed > 0:
        player_turn_angle = min(max_turn_angle, player_turn_angle + rotation_speed)

    # Player acceleration/deceleration
    if keys[pygame.K_UP]:
        player_speed += acceleration
    if keys[pygame.K_DOWN]:
        player_speed -= acceleration

    # Apply friction to player
    player_speed *= (1 - friction)

    # Update player angle based on turn angle
    player_angle = (player_angle + player_turn_angle * 0.05) % 360

    # Calculate player movement based on angle
    player_x += player_speed * math.cos(math.radians(player_angle))
    player_y -= player_speed * math.sin(math.radians(player_angle))

    # Keep player within screen bounds
    player_x = max(0, min(player_x, WIDTH - car_width))
    player_y = max(0, min(player_y, HEIGHT - car_height))

    # Record drift track (car's rear position and angle)
    drift_tracks.append((player_x + car_width // 2, player_y + car_height // 2, player_angle))

    # Keep only the last 50 drift marks
    if len(drift_tracks) > 50:
        drift_tracks.pop(0)

    # Draw the drift tracks
    for track in drift_tracks:
        drift_x, drift_y, drift_angle = track
        # Small rectangle to represent the tire marks
        track_rect = pygame.Rect(drift_x, drift_y, 5, 20)
        pygame.draw.rect(screen, GRAY, track_rect)

    # Rotate and draw the player car
    player_rect = pygame.Rect(player_x, player_y, car_width, car_height)
    rotated_player, rotated_player_rect = rotate_center(player_image, player_rect, -player_angle)
    screen.blit(rotated_player, rotated_player_rect.topleft)

    # Spawn police cars periodically
    if random.randint(1, 100) == 1:  # Random chance to spawn a police car
        spawn_police()

    # Move and draw police cars
    for i, police_pos in enumerate(police_cars):
        police_pos[:] = move_police(police_pos, player_x, player_y)

        # Create a rect for collision detection
        police_rect = pygame.Rect(police_pos[0], police_pos[1], car_width, car_height)

        # Draw the police car
        rotated_police, rotated_police_rect = rotate_center(police_image, police_rect, -police_pos[2])
        screen.blit(rotated_police, rotated_police_rect.topleft)

        # Create a smaller rect for collision detection (50% of the original size)
        police_collision_rect = pygame.Rect(police_pos[0] + car_width // 4, police_pos[1] + car_height // 4, car_width // 2, car_height // 2)

        # Create a smaller rect for player collision detection (50% of the original size)
        player_collision_rect = pygame.Rect(player_x + car_width // 4, player_y + car_height // 4, car_width // 2, car_height // 2)

        # Check for collision with the player
        if detect_collision(player_collision_rect, police_collision_rect):
            print("Game Over!")
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
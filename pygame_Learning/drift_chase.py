import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 2000, 1500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drift Chase")

# Colors
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)  # Color for drift tracks
RED = (255, 0, 0)  # Color for explosion

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
turning_radius = 20  # Turning radius in pixels
acceleration = 0.2
friction = 0.05

# Police car settings
police_speed = 2
police_turning_radius = 20  # Turning radius in pixels
police_cars = []

# List to store drift tracks
drift_tracks = []

# Spawn police cars at random positions
def spawn_police():
    police_x = random.choice([0, WIDTH - car_width])  # Spawn on the left or right edge
    police_y = random.randint(0, HEIGHT - car_height)  # Random y-coordinate
    police_angle = random.randint(0, 360)  # Random initial angle
    police_cars.append([police_x, police_y, police_angle, police_speed])  # Add police car with initial angle and speed

# Rotate and center image
def rotate_center(image, rect, angle):
    """Rotate an image while keeping its center and size."""
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=rect.center)
    return rotated_image, new_rect

# Police car AI: Chase the player
def move_police(police_pos, player_x, player_y):
    police_x, police_y, police_angle, police_speed = police_pos

    # Update police car angle
    target_angle = math.degrees(math.atan2(player_y - police_y, player_x - police_x))
    police_angle = (police_angle + (target_angle - police_angle) * 0.1) % 360  # Gradually update angle

    # Move police car
    police_x += -police_speed * math.cos(math.radians(police_angle))
    police_y += -police_speed * math.sin(math.radians(police_angle))

    # Increase police speed
    police_speed += 1
    if police_speed > 10:
        police_speed = 10

    return [police_x, police_y, police_angle, police_speed]

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
    # Draw the drift tracks
    for track in drift_tracks:
        drift_x, drift_y, drift_angle = track
        # Small rectangle to represent the tire marks
        track_rect = pygame.Rect(drift_x, drift_y, 5, 20)
        
    # Player rotation
    if keys[pygame.K_LEFT] and abs(player_speed) > 0:
        player_angle += (player_speed / turning_radius) * (2000 / math.pi) / 60
        pygame.draw.rect(screen, GRAY, track_rect)  # 60 FPS
    if keys[pygame.K_RIGHT] and abs(player_speed) > 0:
        player_angle -= (player_speed / turning_radius) * (2000 / math.pi) / 60
        pygame.draw.rect(screen, GRAY, track_rect)  # 60 FPS

    # Player acceleration/deceleration
    if keys[pygame.K_UP]:
        player_speed -= acceleration
    if keys[pygame.K_DOWN]:
        player_speed += acceleration

    # Apply friction to player
    player_speed *= (1 - friction)

    # Calculate player movement based on angle
    player_x += player_speed * math.sin(math.radians(player_angle))
    player_y -= player_speed * math.cos(math.radians(player_angle))

    # Keep player within screen bounds
    player_x = max(0, min(player_x, WIDTH - car_width))
    player_y = max(0, min(player_y, HEIGHT - car_height))

    # Record drift track (car's rear position and angle)
    drift_tracks.append((player_x + car_width // 2, player_y + car_height // 2, player_angle))

    # Keep only the last 50 drift marks
    if len(drift_tracks) > 50:
        drift_tracks.pop(0)



    # Rotate and draw the player car
    player_rect = pygame.Rect(player_x, player_y, car_width, car_height)
    rotated_player, rotated_player_rect = rotate_center(player_image, player_rect, -player_angle + 90)
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

        # Check for collision with other police cars
        for j, other_police_pos in enumerate(police_cars):
            if i != j:  # Don't check collision with itself
                other_police_collision_rect = pygame.Rect(other_police_pos[0] + car_width // 4, other_police_pos[1] + car_height // 4, car_width // 2, car_height // 2)
                if detect_collision(police_collision_rect, other_police_collision_rect):
                    # Draw explosion effect
                    explosion_rect = pygame.Rect(police_pos[0], police_pos[1], car_width, car_height)
                    pygame.draw.rect(screen, RED, explosion_rect)

                    # Remove police cars that collided
                    police_cars.pop(i)
                    police_cars.pop(j - 1)  # Adjust index since we removed an item

    pygame.display.flip()
    clock.tick(60)
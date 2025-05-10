import pygame
import math
import random
import time
import os

# High score file path



# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 1200, 800  # Make the map larger
BG_COLOR = (245, 245, 245)  # Light grey background
GRID_COLOR = (230, 230, 230)
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 200, 255)
ENEMY_COLOR = (255, 100, 100)
TRACK_COLOR = (0, 0, 0)
MAX_SPEED = 6
DRIFT_FACTOR = .92
ENEMY_SPEED = 3.5 # 3.5
MAX_TURN_RADIUS = 150
MIN_TURN_RADIUS = 30
TURN_RADIUS_DECAY = 0.2
TURN_RADIUS_RESET_TIME = 0.5
EXPLOSION_RADIUS = 100  # Radius in which cars are affected by the explosion
EXPLOSION_PARTICLE_COUNT = 50  # Number of particles in the explosion
HIGH_SCORE_FILE = "high_score.txt"

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drift Chase")
clock = pygame.time.Clock()

# Track data
drift_tracks = []

# Load car images
player_car = pygame.Surface((50, 30), pygame.SRCALPHA)
player_car.fill(PLAYER_COLOR)

# Create multiple enemy cars
num_enemies = 4  # Start with 4 enemy cars for the corners
enemy_cars = []
corners = [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]  # Four corners of the screen
for i in range(num_enemies):
    enemy_car = pygame.Surface((50, 30), pygame.SRCALPHA)
    enemy_car.fill(ENEMY_COLOR)
    enemy_cars.append({
        'car': enemy_car,
        'pos': list(corners[i]),  # Place each car at a corner
        'angle': 0
    })

# Player and enemy properties
player_pos = [WIDTH // 2, HEIGHT // 2]
player_angle = 0
player_speed = 0
player_turning = False
last_turn_time = time.time()  # Initialize the last turn time to the current time
turn_radius = MAX_TURN_RADIUS
turn_amount = 5
score = 0
game_over = False
game_started = False  # Keeps track of whether the game has started
high_score = 0  # Variable to keep track of the high score

# Check for collisions between enemy cars and player car
def check_enemy_collisions():
    global score, game_over
    for i, car1 in enumerate(enemy_cars):
        for j, car2 in enumerate(enemy_cars):
            if i != j:  # Avoid self-collision check
                # Calculate distance between enemy cars
                dist = math.hypot(car1['pos'][0] - car2['pos'][0], car1['pos'][1] - car2['pos'][1])
                if dist < 50:  # Check if the cars collide (or are close enough)
                    # Reset positions of the collided cars
                    update_score()
                    car1['pos'] = get_valid_spawn_position()
                    car2['pos'] = get_valid_spawn_position()
        
        # Check if enemy car hits player
        ex, ey = car1['pos']
        px, py = player_pos
        dist_to_player = math.hypot(px - ex, py - ey)
        if dist_to_player < 50:
            game_over = True  # Game ends when an enemy car hits the player

def get_valid_spawn_position():
    while True:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        # Ensure the spawn position is not within 100 pixels of the player's car
        if math.hypot(player_pos[0] - x, player_pos[1] - y) >= 100:
            return [x, y]

# Increment score based on time or specific actions
def update_score():
    global score
    score+=1
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click events
            if not game_started:  # If the game is not started, click to start
                mouse_pos = pygame.mouse.get_pos()
                play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
                if play_button_rect.collidepoint(mouse_pos):
                    game_started = True  # Start the game when Play button is clicked
                    score = 0  # Reset score for new game
                    game_over = False  # Reset game over flag
                    player_pos = [WIDTH // 2, HEIGHT // 2]  # Reset player position
                    for car in enemy_cars:
                        car['pos'] = list(corners[enemy_cars.index(car)])  # Reset enemy car positions

        # Press any key to restart after game over
        if event.type == pygame.KEYDOWN and game_over:  # Any key to restart after game over
            game_started = True  # Start the game again
            score = 0  # Reset score
            game_over = False  # Reset game over state
            player_pos = [WIDTH // 2, HEIGHT // 2]  # Reset player position
            for car in enemy_cars:
                car['pos'] = list(corners[enemy_cars.index(car)])  # Reset enemy car positions

    if not game_started:  # Display the Home screen before the game starts
        screen.fill(BG_COLOR)
        font = pygame.font.SysFont(None, 60)
        play_text = font.render("Play", True, WHITE)
        high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
        play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
        
        # Draw Play button and High Score
        pygame.draw.rect(screen, (0, 200, 255), play_button_rect)  # Draw the button
        screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2 - play_text.get_height() // 2))
        screen.blit(high_score_text, (10, 10))  # Display high score at top left

        pygame.display.flip()
        clock.tick(60)
        continue

    if game_over:
        if score > high_score:
            high_score = score  # Update the high score if the current score is higher
        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        restart_text = font.render("Press any key to Restart", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))

        pygame.display.flip()
        clock.tick(60)
        continue

    # Update score in the game loop
    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_speed = min(player_speed + 0.5, MAX_SPEED)
    if keys[pygame.K_DOWN]:
        player_speed = max(player_speed - 0.5, -MAX_SPEED)

    # Handle turning and drifting
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        player_turning = True
        if keys[pygame.K_LEFT]:
            player_angle += turn_amount 
        if keys[pygame.K_RIGHT]:
            player_angle -= turn_amount
        drift_tracks.append((int(player_pos[0]), int(player_pos[1]), time.time()))  # Save track positions with timestamps
    else:
        player_turning = False
        turn_amount = 5
    
    if keys[pygame.K_ESCAPE]:
        pygame.quit()



    # Drift effect
    player_speed *= DRIFT_FACTOR
    dx = player_speed * math.cos(math.radians(player_angle))
    dy = -player_speed * math.sin(math.radians(player_angle))
    player_pos[0] += dx
    player_pos[1] += dy

    # Adjust turn radius when turning
    if player_turning:
        # Shrink the turn radius by 20% every 0.1 seconds
        if time.time() - last_turn_time > 0.4:
            turn_amount = turn_amount * 1.1
            if turn_amount>12:
                turn_amount = 12
            last_turn_time = time.time()

    else:
        # Reset turn radius after not turning for a while
        if time.time() - last_turn_time > TURN_RADIUS_RESET_TIME:
            turn_amount = 5

    # Calculate player facing angle based on movement
    if player_speed != 0:
        player_angle = -math.degrees(math.atan2(dy, dx))

    # Keep the player on screen
    player_pos[0] = max(0, min(WIDTH, player_pos[0]))
    player_pos[1] = max(0, min(HEIGHT, player_pos[1]))

    # Remove old drift tracks (older than 1 second)
    drift_tracks = [track for track in drift_tracks if time.time() - track[2] < 1]

    # Move enemy cars
    for enemy_car in enemy_cars:
        ex, ey = enemy_car['pos']
        px, py = player_pos
        angle_to_player = math.atan2(py - ey, px - ex)
        enemy_car['angle'] = -math.degrees(angle_to_player)
        enemy_car['pos'][0] += ENEMY_SPEED * math.cos(angle_to_player)
        enemy_car['pos'][1] += ENEMY_SPEED * math.sin(angle_to_player)

    # Check for enemy car collisions
    check_enemy_collisions()

    # Drawing everything
    screen.fill(BG_COLOR)
    # Draw grid
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)

    # Draw drift tracks
    for track in drift_tracks[-500:]:
        pygame.draw.rect(screen, TRACK_COLOR, (track[0] - 3, track[1] - 3, 6, 6))

    # Draw player car
    rotated_player = pygame.transform.rotate(player_car, player_angle)
    screen.blit(rotated_player, (player_pos[0] - rotated_player.get_width() // 2, player_pos[1] - rotated_player.get_height() // 2))

    # Draw enemy cars
    for enemy_car in enemy_cars:
        rotated_enemy = pygame.transform.rotate(enemy_car['car'], enemy_car['angle'])
        screen.blit(rotated_enemy, (enemy_car['pos'][0] - rotated_enemy.get_width() // 2, enemy_car['pos'][1] - rotated_enemy.get_height() // 2))

    # Display score and high score at top left
    font = pygame.font.SysFont(None, 40)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

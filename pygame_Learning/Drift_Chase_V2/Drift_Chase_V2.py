import pygame
import math
import random
import time

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (245, 245, 245)  # Light grey background
GRID_COLOR = (230, 230, 230)
WHITE = (255, 255, 255)
PLAYER_COLOR = (0, 200, 255)
ENEMY_COLOR = (255, 100, 100)
TRACK_COLOR = (0, 0, 0)
MAX_SPEED = 6
DRIFT_FACTOR = 0.92  # Controls how much drifting reduces speed
ENEMY_SPEED = 5
TURN_RADIUS_DECAY = 0.2
TURN_RADIUS_RESET_TIME = 0.5
FRICTION = 0.98  # How much friction slows the car down
TURN_SMOOTHNESS = 0.05  # Smoothness of turns
drift_tracks = []  # Initialize drift_tracks

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drift Chase")
clock = pygame.time.Clock()

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
velocity = [0, 0]
last_turn_time = time.time()  # Initialize the last turn time to the current time
turn_amount = 5
score = 0
high_score = 0  # Variable to keep track of the high score
game_over = False
game_started = False  # Keeps track of whether the game has started

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
    score += 1

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
        clock.tick(120)
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
        player_speed = min(player_speed + 0.3, MAX_SPEED)
    if keys[pygame.K_DOWN]:
        player_speed = max(player_speed - 0.3, -MAX_SPEED)

    # Handle turning and drifting
    if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
        if keys[pygame.K_LEFT]:
            player_angle += turn_amount
        if keys[pygame.K_RIGHT]:
            player_angle -= turn_amount

        drift_tracks.append((int(player_pos[0]), int(player_pos[1]), time.time(), player_angle))  # Save track positions with timestamps
    # Drift effect
    rad_angle = math.radians(player_angle)
    forward_vector = [math.cos(rad_angle), -math.sin(rad_angle)]
    velocity[0] += forward_vector[0] * player_speed * TURN_SMOOTHNESS
    velocity[1] += forward_vector[1] * player_speed * TURN_SMOOTHNESS

    # Apply friction and update position
    velocity[0] *= FRICTION
    velocity[1] *= FRICTION
    player_pos[0] += velocity[0]
    player_pos[1] += velocity[1]

    # Keep the player on screen
    player_pos[0] = max(0, min(WIDTH, player_pos[0]))
    player_pos[1] = max(0, min(HEIGHT, player_pos[1]))

    # Move enemy cars
    for enemy_car in enemy_cars:
        ex, ey = enemy_car['pos']
        px, py = player_pos
        angle_to_player = math.atan2(py - ey, px - ex)
        enemy_car['angle'] = -math.degrees(angle_to_player)
        enemy_car['pos'][0] += ENEMY_SPEED * math.cos(angle_to_player)
        enemy_car['pos'][1] += ENEMY_SPEED * math.sin(angle_to_player)

    screen.fill(BG_COLOR)
    # Draw grid
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)
    # Check for enemy car collisions
    check_enemy_collisions()
    # Remove old drift tracks
    current_time = time.time()
    drift_tracks = [track for track in drift_tracks if current_time - track[2] <= 1]

    for track in drift_tracks:
        current_player_angle = track[3]  # Use the player angle stored in the drift track
        car_corners = [
            (track[0] + 25 * math.cos(math.radians(current_player_angle)) - 15 * math.sin(math.radians(current_player_angle)),
             track[1] - 25 * math.sin(math.radians(current_player_angle)) - 15 * math.cos(math.radians(current_player_angle))),
            (track[0] + 25 * math.cos(math.radians(current_player_angle)) + 15 * math.sin(math.radians(current_player_angle)),
             track[1] - 25 * math.sin(math.radians(current_player_angle)) + 15 * math.cos(math.radians(current_player_angle))),
            (track[0] - 25 * math.cos(math.radians(current_player_angle)) + 15 * math.sin(math.radians(current_player_angle)),
             track[1] + 25 * math.sin(math.radians(current_player_angle)) + 15 * math.cos(math.radians(current_player_angle))),
            (track[0] - 25 * math.cos(math.radians(current_player_angle)) - 15 * math.sin(math.radians(current_player_angle)),
             track[1] + 25 * math.sin(math.radians(current_player_angle)) - 15 * math.cos(math.radians(current_player_angle)))
        ]
        for corner in car_corners:
            pygame.draw.circle(screen, TRACK_COLOR, (corner[0] - 3, corner[1] - 3), 4)
    # Drawing everything

    
    # Draw player car
    rotated_player = pygame.transform.rotate(player_car, player_angle)
    screen.blit(rotated_player, (player_pos[0] - rotated_player.get_width() // 2, player_pos[1] - rotated_player.get_height() // 2))

    # Draw enemy cars
    for enemy_car in enemy_cars:
        rotated_enemy = pygame.transform.rotate(enemy_car['car'], enemy_car['angle'])
        screen.blit(rotated_enemy, (enemy_car['pos'][0] - rotated_enemy.get_width() // 2, enemy_car['pos'][1] - rotated_enemy.get_height() // 2))

    # Draw score
    font = pygame.font.SysFont(None, 40)
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 30))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()

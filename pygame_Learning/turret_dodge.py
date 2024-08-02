import pygame
import random
import math

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrolling Ground with Jumping, Jetpack, and Turrets")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
sky_blue = (135, 206, 250)

# Player settings
player_x = screen_width // 2
player_y = screen_height - 100
player_size = 20
player_speed = 0
max_speed = 8
acceleration = 0.5
boost_multiplier = 2
boost_amount = 50
boost = boost_amount
boost_regen_rate = 1
friction = 0.2
gravity = 0.8
fall_speed = 12
player_vel_y = 0
is_jumping = False
jump_height = 15
jetpack_fuel = 100
jetpack_consumption_rate = 2
jetpack_power = 1.5
lives = 3
has_shield = False
shield_duration = 5000  # 5 seconds
shield_start_time = 0

# Turret settings
turret_size = 40
turret_color = black
turrets = []
turret_spawn_rate = 3000  # Spawn every 3 seconds
last_turret_spawn = 0
rocket_speed = 5
rockets = []

# Fuel token settings
fuel_token_size = 20
fuel_tokens = []
fuel_token_spawn_rate = 5000  # Spawn every 5 seconds
last_fuel_token_spawn = 0

# Ground settings
ground_height = 80
ground_color = (139, 69, 19)
ground_scroll_speed = 0
ground_x = 0
dent_width = 20
dent_depth = 10
dents = []
obstacle_speed = 5
# Create ground texture
ground_texture = pygame.Surface((40, 40))
ground_texture.fill(ground_color)
for x in range(0, 40, 5):
    for y in range(0, 40, 5):
        pygame.draw.rect(ground_texture, (160, 82, 45), (x, y, 3, 3))
ground_texture = pygame.transform.scale(ground_texture, (ground_texture.get_width() * 2, ground_texture.get_height() * 2))

# Cloud settings
cloud_image = pygame.image.load("images/cloud.png").convert_alpha()
cloud_image = pygame.transform.scale(cloud_image, (cloud_image.get_width() // 2, cloud_image.get_height() // 2))
cloud_speed = 1
clouds = []
for _ in range(5):
    cloud_x = random.randint(0, screen_width)
    cloud_y = random.randint(-cloud_image.get_height(), 0)
    clouds.append([cloud_x, cloud_y])

# Heart image for lives
heart_image = pygame.image.load("images/lives.jpeg").convert_alpha()
heart_image = pygame.transform.scale(heart_image, (heart_image.get_width() // 4, heart_image.get_height() // 4))

# Pause button settings
pause_button_radius = 20
pause_button_color = red
pause_button_x = screen_width - pause_button_radius - 10
pause_button_y = pause_button_radius + 10
is_paused = False

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                player_vel_y = -jump_height
            if event.key == pygame.K_s and not has_shield:  # Activate shield with 's' key
                has_shield = True
                shield_start_time = current_time

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                distance_to_button = (
                    (event.pos[0] - pause_button_x) ** 2 + (event.pos[1] - pause_button_y) ** 2
                ) ** 0.5
                if distance_to_button <= pause_button_radius:
                    is_paused = not is_paused

    if is_paused:
        continue

    # --- Player Movement ---
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        if boost > 0 and keys[pygame.K_LSHIFT]:
            player_speed -= acceleration * boost_multiplier
            boost -= boost_regen_rate * 2
        else:
            player_speed -= acceleration
    elif keys[pygame.K_RIGHT]:
        if boost > 0 and keys[pygame.K_LSHIFT]:
            player_speed += acceleration * boost_multiplier
            boost -= boost_regen_rate * 2
        else:
            player_speed += acceleration
    else:
        if player_speed > 0:
            player_speed -= friction
        elif player_speed < 0:
            player_speed += friction

    boost = min(boost + boost_regen_rate, boost_amount)

    player_speed = max(min(player_speed, max_speed), -max_speed)
    player_x += player_speed

    # --- Jetpack ---
    if keys[pygame.K_j] and jetpack_fuel > 0:
        player_vel_y -= jetpack_power
        jetpack_fuel -= jetpack_consumption_rate

    # --- Gravity ---
    player_vel_y += gravity
    if player_vel_y > fall_speed:
        player_vel_y = fall_speed
    player_y += player_vel_y

    # --- Keep player on top of the ground ---
    if player_y + player_size > screen_height - ground_height:
        player_y = screen_height - ground_height - player_size
        player_vel_y = 0
        is_jumping = False
        dent_x = player_x - ground_x - dent_width // 2
        dents.append(dent_x)

        # Replenish jetpack fuel when on the ground
        jetpack_fuel = min(jetpack_fuel + 5, 100)

    # --- Keep player within the screen bounds ---
    player_x = max(0, min(player_x, screen_width - player_size))

    # --- Turret and rocket movement ---
    for turret in turrets[:]:
        turret[1] += obstacle_speed
        if turret[1] > screen_height:
            turrets.remove(turret)

        # Calculate rocket travel time (1 second)
        target_x = player_x + player_size // 2
        target_y = player_y + player_size // 2
        dx = target_x - (turret[0] + turret_size // 2)
        dy = target_y - (turret[1] + turret_size // 2)
        distance = math.hypot(dx, dy)
        travel_time = distance / rocket_speed
   # Launch a rocket
        rockets.append(
            [
                turret[0] + turret_size // 2,
                turret[1] + turret_size // 2,
                dx / travel_time,
                dy / travel_time,
            ]
        )

    for rocket in rockets[:]:
        rocket[0] += rocket[2]
        rocket[1] += rocket[3]

        # Check for collision with player
        if (
            player_x < rocket[0] < player_x + player_size
            and player_y < rocket[1] < player_y + player_size
        ):
            if has_shield:
                nearest_turret = min(turrets, key=lambda t: math.hypot(player_x - t[0], player_y - t[1])) 
                if nearest_turret in turrets:
                    turrets.remove(nearest_turret)
                has_shield = False
            else:
                lives -= 1
                if lives == 0:
                    running = False
            rockets.remove(rocket)

        if rocket[1] > screen_height:
            rockets.remove(rocket)

    # --- Shield duration ---
    if has_shield and current_time - shield_start_time > shield_duration:
        has_shield = False

    # --- Fuel token spawning and movement ---
    if current_time - last_fuel_token_spawn > fuel_token_spawn_rate:
        fuel_token_x = random.randint(0, screen_width - fuel_token_size)
        fuel_tokens.append([fuel_token_x, -fuel_token_size])
        last_fuel_token_spawn = current_time

    for fuel_token in fuel_tokens[:]:
        fuel_token[1] += obstacle_speed
        if fuel_token[1] > screen_height:
            fuel_tokens.remove(fuel_token)

        if (
            player_x < fuel_token[0] + fuel_token_size
            and player_x + player_size > fuel_token[0]
            and player_y < fuel_token[1] + fuel_token_size
            and player_y + player_size > fuel_token[1]
        ):
            jetpack_fuel = 100
            fuel_tokens.remove(fuel_token)

    # --- Turret spawning ---
    if current_time - last_turret_spawn > turret_spawn_rate:
        turret_x = random.randint(0, screen_width - turret_size)
        turrets.append([turret_x, -turret_size])
        last_turret_spawn = current_time

    # --- Ground Scrolling ---
    ground_scroll_speed = -player_speed
    ground_x += ground_scroll_speed

    if ground_x < -ground_texture.get_width():
        ground_x = 0
    elif ground_x > 0:
        ground_x = -ground_texture.get_width()

    # --- Cloud scrolling ---
    for cloud in clouds:
        cloud[0] -= cloud_speed
        if cloud[0] < -cloud_image.get_width():
            cloud[0] = screen_width
            cloud[1] = random.randint(-cloud_image.get_height(), 0)

    # --- Drawing ---
    screen.fill(sky_blue)

    # Draw clouds
    for cloud in clouds:
        screen.blit(cloud_image, (cloud[0], cloud[1]))

    # Draw the ground (using texture)
    screen.blit(ground_texture, (ground_x, screen_height - ground_texture.get_height()))
    screen.blit(ground_texture, (ground_x + ground_texture.get_width(), screen_height - ground_texture.get_height()))

    # Draw dents (before the grass)
    for dent_x in dents:
        dent_rect = (ground_x + dent_x, screen_height - ground_height + dent_depth,
                     dent_width, ground_height - dent_depth)
        pygame.draw.rect(screen, white, dent_rect)

    # Draw the grass (green rectangle)
    pygame.draw.rect(screen, green, (0, screen_height - ground_height, screen_width, ground_height))

    # Draw fuel tokens
    for fuel_token in fuel_tokens:
        pygame.draw.circle(screen, (255, 255, 0), (fuel_token[0] + fuel_token_size // 2, fuel_token[1] + fuel_token_size // 2),
                           fuel_token_size // 2)

    # Draw turrets
    for turret in turrets:
        pygame.draw.rect(screen, turret_color, (turret[0], turret[1], turret_size, turret_size))

    # Draw rockets
    for rocket in rockets:
        pygame.draw.circle(screen, red, (int(rocket[0]), int(rocket[1])), 5)

    # Draw hearts (lives)
    for i in range(lives):
        screen.blit(heart_image, (10 + i * (heart_image.get_width() + 5), 10))

    # Draw the player
    pygame.draw.rect(screen, blue, (player_x, player_y, player_size, player_size))
    if has_shield:
        pygame.draw.circle(screen, (0, 255, 255), (player_x + player_size // 2, player_y + player_size // 2),
                           player_size, 2)

    # Draw pause button
    pygame.draw.circle(screen, pause_button_color, (pause_button_x, pause_button_y), pause_button_radius)

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

pygame.quit()
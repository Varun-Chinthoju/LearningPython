import pygame
import random
import math

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))  # Initialize display first
pygame.display.set_caption("Turret Dodge")

# --- Image Loading ---  
cloud_image = pygame.image.load("images/cloud.png").convert_alpha()
cloud_image = pygame.transform.scale(cloud_image, (cloud_image.get_width() // 2, cloud_image.get_height() // 2))
heart_image = pygame.image.load("images/lives.jpeg").convert()
heart_image = pygame.transform.scale(heart_image, (heart_image.get_width() // 4, heart_image.get_height() // 4))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
sky_blue = (135, 206, 250)
yellow = (255, 255, 0)  # For fuel bar
cyan = (0, 255, 255)   # For boost bar
magenta = (255, 0, 255) # For shield bar

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
shield_hits = 5  # Shield can take 5 hits
has_shield = False
shield_duration = 5000  # 5 seconds
shield_start_time = 0

# Turret settings
turret_size = 40
turret_color = black
turrets = []
turret_spawn_rate = 2500  # Spawn every 3 seconds
last_turret_spawn = 0
rocket_speed = 5
rockets = []
max_rockets_per_turret = 10  # Turrets can only shoot 10 rockets
rocket_delay = 200  # Delay between rockets in milliseconds
last_rocket_launch = 0
turret_range = 500  # Maximum range for turrets to shoot

# Special turret settings
special_turret_size = 50
special_turret_color = blue
special_turrets = []
special_turret_spawn_rate = 7500  # Spawn every 10 seconds
last_special_turret_spawn = 0
homing_missile_speed = 6
homing_missiles = []
homing_missile_lifetime = 2500  # 2 seconds in milliseconds
special_turret_spawn_chance = 1/10  # 1 in 20 chance of spawning

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

# Obstacle acceleration settings
obstacle_acceleration = 0.05
max_obstacle_speed = 8

# Obstacle settings
obstacle_size = 30
obstacle_speed = 3
obstacles = []
obstacle_spawn_rate = 1500  # Spawn every 1.5 seconds
last_obstacle_spawn = 0

# Extra life (falling heart) settings
extra_life_size = 30
extra_life_speed = 2
extra_lives = []
extra_life_spawn_rate = 10000  # Spawn every 10 seconds
last_extra_life_spawn = 0

# Create ground texture
ground_texture = pygame.Surface((40, 40))
ground_texture.fill(ground_color)
for x in range(0, 40, 5):
    for y in range(0, 40, 5):
        pygame.draw.rect(ground_texture, (160, 82, 45), (x, y, 3, 3))
ground_texture = pygame.transform.scale(ground_texture, (ground_texture.get_width() * 2, ground_texture.get_height() * 2))

# Cloud settings
cloud_speed = 1
clouds = []
for _ in range(5):
    cloud_x = random.randint(0, screen_width)
    cloud_y = random.randint(-cloud_image.get_height(), 0)
    clouds.append([cloud_x, cloud_y])

# Pause button settings
pause_button_radius = 20
pause_button_color = red
pause_button_x = screen_width - pause_button_radius - 10
pause_button_y = pause_button_radius + 10
is_paused = False

# --- Bar settings ---
bar_width = 150
bar_height = 10
bar_margin = 10
jetpack_bar_x = bar_margin
jetpack_bar_y = screen_height - bar_height - bar_margin
boost_bar_x = jetpack_bar_x
boost_bar_y = jetpack_bar_y - bar_height - bar_margin
shield_bar_x = jetpack_bar_x
shield_bar_y = boost_bar_y - bar_height - bar_margin

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
            if event.key == pygame.K_s and not has_shield:
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
        jetpack_fuel = min(jetpack_fuel + 5, 100)

    # --- Keep player within the screen bounds ---
    player_x = max(0, min(player_x, screen_width - player_size))

    # --- Turret and rocket movement ---
    for turret in turrets[:]:
        turret[1] += obstacle_speed
        if turret[1] > screen_height:
            turrets.remove(turret)

        # Only launch rockets if enough time has passed since the last launch
        if current_time - last_rocket_launch > rocket_delay:
            # Only launch rockets if the turret has rockets left and is within range
            if len(rockets) < max_rockets_per_turret * len(turrets) and math.hypot(player_x - turret[0], player_y - turret[1]) <= turret_range:
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
                last_rocket_launch = current_time  # Update last rocket launch time

    for rocket in rockets[:]:
        rocket[0] += rocket[2]
        rocket[1] += rocket[3]

        # Check for collision with player
        if (
            player_x < rocket[0] < player_x + player_size
            and player_y < rocket[1] < player_y + player_size
        ):
            if has_shield:
                shield_hits -= 1
                if shield_hits == 0:
                    has_shield = False
                    shield_hits = 5  # Reset shield hits
                rockets.remove(rocket)  # Remove rocket even if shield is active
                # Find the nearest turret and remove it
                if turrets:  # Check if turrets list is not empty
                    nearest_turret = min(turrets, key=lambda t: math.hypot(player_x - t[0], player_y - t[1]))
                    if nearest_turret in turrets:
                        turrets.remove(nearest_turret)
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
        shield_hits = 5  # Reset shield hits

    # --- Fuel token spawning and movement ---
    if current_time - last_fuel_token_spawn > fuel_token_spawn_rate:
        fuel_token_x = random.randint(0, screen_width - fuel_token_size)
        fuel_tokens.append([fuel_token_x, -fuel_token_size])
        last_fuel_token_spawn = current_time

    for fuel_token in fuel_tokens[:]:
        fuel_token[1] += obstacle_speed  # Fuel tokens move at obstacle speed
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

    # --- Extra life (falling heart) spawning ---
    if current_time - last_extra_life_spawn > extra_life_spawn_rate:
        extra_life_x = random.randint(0, screen_width - extra_life_size)
        extra_lives.append([extra_life_x, -extra_life_size])
        last_extra_life_spawn = current_time

    # --- Extra life movement ---
    for extra_life in extra_lives[:]:
        extra_life[1] += extra_life_speed
        if extra_life[1] > screen_height:
            extra_lives.remove(extra_life)

        # Check for collision with player
        if (
            player_x < extra_life[0] + extra_life_size
            and player_x + player_size > extra_life[0]
            and player_y < extra_life[1] + extra_life_size
            and player_y + player_size > extra_life[1]
        ):
            lives += 1  # Add an extra life
            extra_lives.remove(extra_life)

    # --- Turret spawning ---
    if current_time - last_turret_spawn > turret_spawn_rate:
        turret_x = random.randint(0, screen_width - turret_size)
        turrets.append([turret_x, -turret_size])
        last_turret_spawn = current_time

    # --- Special turret spawning ---
    if current_time - last_special_turret_spawn > special_turret_spawn_rate:
        if random.random() < special_turret_spawn_chance:  # Check for spawn chance
            special_turret_x = random.randint(0, screen_width - special_turret_size)
            special_turrets.append([special_turret_x, -special_turret_size])
            last_special_turret_spawn = current_time

    # --- Special turret and homing missile movement ---
    for special_turret in special_turrets[:]:
        special_turret[1] += obstacle_speed
        if special_turret[1] > screen_height:
            special_turrets.remove(special_turret)

        # Launch a homing missile
        if len(homing_missiles) < len(special_turrets):  # Only one missile per special turret
            target_x = player_x + player_size // 2
            target_y = player_y + player_size // 2
            dx = target_x - (special_turret[0] + special_turret_size // 2)
            dy = target_y - (special_turret[1] + special_turret_size // 2)
            distance = math.hypot(dx, dy)
            travel_time = distance / homing_missile_speed

            homing_missiles.append(
                [
                    special_turret[0] + special_turret_size // 2,
                    special_turret[1] + special_turret_size // 2,
                    dx / travel_time,
                    dy / travel_time,
                    current_time,  # Add launch time to track lifetime
                ]
            )

    for missile in homing_missiles[:]:
        # Update missile velocity to home in on the player
        target_x = player_x + player_size // 2
        target_y = player_y + player_size // 2
        dx = target_x - missile[0]
        dy = target_y - missile[1]
        distance = math.hypot(dx, dy)
        if distance > 0:  # Avoid division by zero
            missile[2] = (dx / distance) * homing_missile_speed
            missile[3] = (dy / distance) * homing_missile_speed

        missile[0] += missile[2]
        missile[1] += missile[3]

        # Check for collision with player
        if (
            player_x < missile[0] < player_x + player_size
            and player_y < missile[1] < player_y + player_size
        ):
            lives -= 2  # Homing missile takes two lives
            if lives <= 0:
                running = False
            homing_missiles.remove(missile)

        # Check for missile lifetime
        if current_time - missile[4] > homing_missile_lifetime:
            homing_missiles.remove(missile)

    # --- Obstacle spawning ---
    if current_time - last_obstacle_spawn > obstacle_spawn_rate:
        obstacle_x = random.randint(0, screen_width - obstacle_size)
        obstacles.append([obstacle_x, -obstacle_size, obstacle_speed])  # Add initial speed
        last_obstacle_spawn = current_time

    # --- Obstacle movement ---
    for obstacle in obstacles[:]:
        obstacle[2] = min(obstacle[2] + obstacle_acceleration, max_obstacle_speed)
        obstacle[1] += obstacle[2]
        if obstacle[1] > screen_height:
            obstacles.remove(obstacle)

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

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, red, (obstacle[0], obstacle[1], obstacle_size, obstacle_size))

    # Draw fuel tokens
    for fuel_token in fuel_tokens:
        pygame.draw.circle(screen, (255, 255, 0), (fuel_token[0] + fuel_token_size // 2, fuel_token[1] + fuel_token_size // 2),
                           fuel_token_size // 2)

    # Draw turrets
    for turret in turrets:
        pygame.draw.rect(screen, turret_color, (turret[0], turret[1], turret_size, turret_size))

    # Draw special turrets
    for special_turret in special_turrets:
        pygame.draw.rect(screen, special_turret_color, (special_turret[0], special_turret[1], special_turret_size, special_turret_size))

    # Draw rockets
    for rocket in rockets:
        pygame.draw.circle(screen, red, (int(rocket[0]), int(rocket[1])), 5)

    # Draw homing missiles
    for missile in homing_missiles:
        pygame.draw.circle(screen, blue, (int(missile[0]), int(missile[1])), 8)  # Larger blue circle for homing missiles

    # Draw extra lives (falling hearts)
    for extra_life in extra_lives:
        screen.blit(heart_image, (extra_life[0], extra_life[1]))

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

    # --- Draw bars ---
    # Jetpack bar
    jetpack_bar_fill = (jetpack_fuel / 100) * bar_width
    pygame.draw.rect(screen, black, (jetpack_bar_x, jetpack_bar_y, bar_width, bar_height))  # Background
    pygame.draw.rect(screen, yellow, (jetpack_bar_x, jetpack_bar_y, jetpack_bar_fill, bar_height))  # Fill

    # Boost bar
    boost_bar_fill = (boost / boost_amount) * bar_width
    pygame.draw.rect(screen, black, (boost_bar_x, boost_bar_y, bar_width, bar_height))  # Background
    pygame.draw.rect(screen, cyan, (boost_bar_x, boost_bar_y, boost_bar_fill, bar_height))  # Fill

    # Shield bar
    shield_bar_fill = (shield_hits / 5) * bar_width
    pygame.draw.rect(screen, black, (shield_bar_x, shield_bar_y, bar_width, bar_height))  # Background
    pygame.draw.rect(screen, magenta, (shield_bar_x, shield_bar_y, shield_bar_fill, bar_height))  # Fill

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

pygame.quit()
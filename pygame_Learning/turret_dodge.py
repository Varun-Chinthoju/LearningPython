import pygame
import random
import math
import time

pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode(
    (screen_width, screen_height)
)  # Initialize display first
pygame.display.set_caption("Turret Dodge")

# --- Image Loading ---
cloud_image = pygame.image.load("images/cloud.png").convert_alpha()
cloud_image = pygame.transform.scale(
    cloud_image, (cloud_image.get_width() // 2, cloud_image.get_height() // 2)
)
heart_image = pygame.image.load("images/lives.jpeg").convert()
heart_image = pygame.transform.scale(
    heart_image, (heart_image.get_width() // 4, heart_image.get_height() // 4)
)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
sky_blue = (135, 206, 250)
yellow = (255, 255, 0)  # For fuel bar
cyan = (0, 255, 255)  # For boost bar
magenta = (255, 0, 255)  # For shield bar
gray = (128, 128, 128)  # For explosion smoke

# --- Game Settings ---
difficulty = "medium"  # Default difficulty
score = 0

# --- Difficulty Settings ---
difficulty_settings = {
    "easy": {
        "turret_spawn_rate": 4000,
        "special_turret_spawn_rate": 15000,
        "obstacle_spawn_rate": 2000,
        "obstacle_acceleration": 0.03,
        "max_obstacle_speed": 6,
        "turret_speed": 4,
        "lives": 7,
    },
    "medium": {
        "turret_spawn_rate": 3000,
        "special_turret_spawn_rate": 10000,
        "obstacle_spawn_rate": 1500,
        "obstacle_acceleration": 0.05,
        "max_obstacle_speed": 8,
        "turret_speed": 3,
        "lives": 5,
    },
    "hard": {
        "turret_spawn_rate": 2000,
        "special_turret_spawn_rate": 7000,
        "obstacle_spawn_rate": 1000,
        "obstacle_acceleration": 0.08,
        "max_obstacle_speed": 10,
        "turret_speed": 2,
        "lives": 3,
    },
    "hardcore": {  # Added hardcore difficulty
        "turret_spawn_rate": 2000,
        "special_turret_spawn_rate": 7000,
        "obstacle_spawn_rate": 1000,
        "obstacle_acceleration": 0.08,
        "max_obstacle_speed": 10,
        "turret_speed": 2,
        "lives": 1,
    },
}

# --- Initialize spawn rates and obstacle settings based on difficulty ---
turret_spawn_rate = difficulty_settings[difficulty]["turret_spawn_rate"]
special_turret_spawn_rate = difficulty_settings[difficulty]["special_turret_spawn_rate"]
obstacle_spawn_rate = difficulty_settings[difficulty]["obstacle_spawn_rate"]
obstacle_acceleration = difficulty_settings[difficulty]["obstacle_acceleration"]
max_obstacle_speed = difficulty_settings[difficulty]["max_obstacle_speed"]
turret_speed = difficulty_settings[difficulty]["turret_speed"]

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
jetpack_fuel = 70
jetpack_consumption_rate = 1
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
last_turret_spawn = 0
rocket_speed = 5
rockets = []
max_rockets_per_turret = 50  # Turrets can only shoot 10 rockets
rocket_delay = 100  # Delay between rockets in milliseconds
last_rocket_launch = 0
turret_range = 500  # Maximum range for turrets to shoot
rocket_lifetime = 2000  # Rocket lasts 2 seconds

# Special turret settings
special_turret_size = 50
special_turret_color = blue
special_turrets = []
last_special_turret_spawn = 0
homing_missile_speed = 6
homing_missiles = []
homing_missile_lifetime = 2500  # 2 seconds in milliseconds
special_turret_spawn_chance = 1 / 10  # 1 in 20 chance of spawning

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

# Obstacle settings
obstacle_size = 30
obstacle_speed = 3
obstacles = []
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
ground_texture = pygame.transform.scale(
    ground_texture, (ground_texture.get_width() * 2, ground_texture.get_height() * 2)
)

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
end_score = 0
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

# --- Menu settings ---
menu_font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 75)
title_text = title_font.render("Turret Dodge", True, black)
title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))

easy_text = menu_font.render("Easy", True, black)
easy_rect = easy_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))

medium_text = menu_font.render("Medium", True, black)
medium_rect = medium_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))

hard_text = menu_font.render("Hard", True, black)
hard_rect = hard_text.get_rect(center=(screen_width // 2, screen_height // 2))

hardcore_text = menu_font.render("Hardcore", True, black)
hardcore_rect = hardcore_text.get_rect(
    center=(screen_width // 2, screen_height // 2 + 50)
)


# --- Functions ---
def reset_game():
    global player_x, player_y, player_speed, player_vel_y, boost, jetpack_fuel, lives, shield_hits, has_shield, turrets, rockets, fuel_tokens, obstacles, extra_lives, last_turret_spawn, last_rocket_launch, last_fuel_token_spawn, last_obstacle_spawn, last_extra_life_spawn, score, turret_spawn_rate, special_turret_spawn_rate, obstacle_spawn_rate, obstacle_acceleration, max_obstacle_speed, turret_speed
    player_x = screen_width // 2
    player_y = screen_height - 100
    player_speed = 0
    player_vel_y = 0
    boost = boost_amount
    jetpack_fuel = 100
    lives = difficulty_settings[difficulty]["lives"]  # Get lives from dictionary
    shield_hits = 5
    has_shield = False
    turrets = []
    rockets = []
    fuel_tokens = []
    obstacles = []
    extra_lives = []
    last_turret_spawn = 0
    last_rocket_launch = 0
    last_fuel_token_spawn = 0
    last_obstacle_spawn = 0
    last_extra_life_spawn = 0
    score = 0
    # Update spawn rates and obstacle settings based on difficulty
    turret_spawn_rate = difficulty_settings[difficulty]["turret_spawn_rate"]
    special_turret_spawn_rate = difficulty_settings[difficulty][
        "special_turret_spawn_rate"
    ]
    obstacle_spawn_rate = difficulty_settings[difficulty]["obstacle_spawn_rate"]
    obstacle_acceleration = difficulty_settings[difficulty]["obstacle_acceleration"]
    max_obstacle_speed = difficulty_settings[difficulty]["max_obstacle_speed"]
    turret_speed = difficulty_settings[difficulty]["turret_speed"]


# --- Particle System ---
class Particle:
    def __init__(self, x, y, color, size, lifetime, x_vel=0, y_vel=0):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.alive = True
        self.x_vel = x_vel
        self.y_vel = y_vel

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.alive = False

        self.x += self.x_vel
        self.y += self.y_vel
        self.y_vel += 0.2  # Gravity effect on particles

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


particles = []
jetpack_particle_colors = [(255, 255, 0), (255, 165, 0)]  # Yellow and orange

# --- Game State ---
game_over = False
player_death_explosion = False

# Game loop
running = True
in_menu = True  # Start in the menu
clock = pygame.time.Clock()

while running:
    current_time = pygame.time.get_ticks()
    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if in_menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if easy_rect.collidepoint(event.pos):
                        difficulty = "easy"
                        reset_game()
                        in_menu = False
                        is_paused = False
                    elif medium_rect.collidepoint(event.pos):
                        difficulty = "medium"
                        reset_game()
                        in_menu = False
                        is_paused = False
                    elif hard_rect.collidepoint(event.pos):
                        difficulty = "hard"
                        reset_game()
                        in_menu = False
                        is_paused = False
                    elif hardcore_rect.collidepoint(
                        event.pos
                    ):  # Add handling for hardcore button click
                        difficulty = "hardcore"
                        reset_game()
                        in_menu = False
                        is_paused = False
        else:
            if not game_over:
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
                            (event.pos[0] - pause_button_x) ** 2
                            + (event.pos[1] - pause_button_y) ** 2
                        ) ** 0.5
                        if distance_to_button <= pause_button_radius:
                            is_paused = not is_paused

    if is_paused:
        continue

    if in_menu:
        # --- Draw menu ---
        screen.fill(sky_blue)

        # Draw clouds

        screen.blit(title_text, title_rect)
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)
        screen.blit(hardcore_text, hardcore_rect)  # Draw the hardcore option

        pygame.display.flip()
        clock.tick(60)
        continue

    # --- Player Movement ---
    keys = pygame.key.get_pressed()
    if not game_over:
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

    if keys[pygame.K_j] and jetpack_fuel > 0 and not game_over:
        player_vel_y -= jetpack_power
        jetpack_fuel -= jetpack_consumption_rate

        # Create jetpack particles
        for _ in range(3):
            particle_x = player_x + player_size // 2 + random.randint(-5, 5)
            particle_y = player_y + player_size
            particle_color = random.choice(jetpack_particle_colors)
            particle_size = random.randint(3, 6)
            particle_lifetime = random.randint(20, 40)
            particles.append(
                Particle(
                    particle_x,
                    particle_y,
                    particle_color,
                    particle_size,
                    particle_lifetime,
                )
            )

    # --- Gravity ---
    # Only apply gravity if player is alive
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

        if game_over and not player_death_explosion:
            # Create explosion particles
            start_time = pygame.time.get_ticks()
            if x == 0:
                end_score = str(score)
            for _ in range(175):
                particle_x = player_x + player_size // 2 + random.randint(-20, 20)
                particle_y = player_y + player_size // 2 + random.randint(-20, 20)
                rand_color = random.randint(1, 3)
                if rand_color == 1:
                    particle_color = gray
                elif rand_color == 2:
                    particle_color = yellow
                elif rand_color == 3:
                    particle_color = red
                particle_size = random.randint(5, 10)
                particle_lifetime = random.randint(30, 50)
                x_vel = random.randint(-10, 10)
                y_vel = random.randint(-10, -2)

                particles.append(
                    Particle(
                        particle_x,
                        particle_y,
                        particle_color,
                        particle_size,
                        particle_lifetime,
                        x_vel,
                        y_vel,
                    )
                )
            player_death_explosion = True
            end_score_text = title_font.render(
                f"Your Final score is: {end_score}", True, black
            )  # Added hardcore mode to the menu
            end_score_rect = end_score_text.get_rect(
                center=(screen_width // 2, screen_height // 2 + 50)
            )

    if player_death_explosion == True:
        if pygame.time.get_ticks() - start_time >= 1000:
            in_menu = True
            player_death_explosion = False
            game_over = False

    # --- Keep player within the screen bounds ---
    player_x = max(0, min(player_x, screen_width - player_size))

    # --- Turret spawning ---
    if current_time - last_turret_spawn > turret_spawn_rate:
        turret_x = random.randint(0, screen_width - turret_size)
        turrets.append([turret_x, -turret_size])
        last_turret_spawn = current_time

    # --- Turret and rocket movement ---
    for turret in turrets[:]:
        turret[1] += turret_speed
        if turret[1] > screen_height:
            turrets.remove(turret)
            score += 1

        # Only launch rockets if enough time has passed since the last launch
        if current_time - last_rocket_launch > rocket_delay:
            # Only launch rockets if the turret has rockets left and is within range
            if (
                len(rockets) < max_rockets_per_turret * len(turrets)
                and math.hypot(player_x - turret[0], player_y - turret[1])
                <= turret_range
            ):
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
                        current_time,  # Track rocket launch time for lifetime
                    ]
                )
                last_rocket_launch = current_time  # Update last rocket launch time

        # --- Score Increment (Moved) ---
        # if 0 <= turret[1] <= screen_height:  # Only give points for on-screen turrets
        #     score += 1

    for rocket in rockets[:]:
        rocket[0] += rocket[2]
        rocket[1] += rocket[3]

        # Check for rocket lifetime
        if current_time - rocket[4] > rocket_lifetime:
            rockets.remove(rocket)
            # Create explosion particles
            for _ in range(30):
                particle_x = rocket[0] + random.randint(-10, 10)
                particle_y = rocket[1] + random.randint(-10, 10)
                particle_color = red
                particle_size = random.randint(3, 6)
                particle_lifetime = random.randint(10, 20)
                x_vel = random.randint(-3, 3)
                y_vel = random.randint(-3, 3)
                particles.append(
                    Particle(
                        particle_x,
                        particle_y,
                        particle_color,
                        particle_size,
                        particle_lifetime,
                        x_vel,
                        y_vel,
                    )
                )
            continue

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
                    nearest_turret = min(
                        turrets,
                        key=lambda t: math.hypot(player_x - t[0], player_y - t[1]),
                    )
                    if nearest_turret in turrets:
                        turrets.remove(nearest_turret)
            else:
                lives -= 1
                if lives == 0:
                    game_over = True  # Trigger game over
                rockets.remove(rocket)

        if rocket[1] > screen_height:
            rockets.remove(rocket)
            # Create explosion particles
            for _ in range(30):
                particle_x = rocket[0] + random.randint(-10, 10)
                particle_y = rocket[1] + random.randint(-10, 10)
                particle_color = red
                particle_size = random.randint(3, 6)
                particle_lifetime = random.randint(10, 20)
                x_vel = random.randint(-3, 3)
                y_vel = random.randint(-3, 3)
                particles.append(
                    Particle(
                        particle_x,
                        particle_y,
                        particle_color,
                        particle_size,
                        particle_lifetime,
                        x_vel,
                        y_vel,
                    )
                )

    # --- Special turret spawning ---
    if current_time - last_special_turret_spawn > special_turret_spawn_rate:
        if random.random() < special_turret_spawn_chance:
            special_turret_x = random.randint(0, screen_width - special_turret_size)
            special_turrets.append([special_turret_x, -special_turret_size])
            last_special_turret_spawn = current_time

    # --- Special turret and homing missile movement ---
    for special_turret in special_turrets[:]:
        special_turret[1] += obstacle_speed
        if special_turret[1] > screen_height:
            special_turrets.remove(special_turret)
            score += 2  # Increment score by 2 for special turrets

        # Launch a homing missile
        if len(homing_missiles) < len(
            special_turrets
        ):  # Only one missile per special turret
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
                game_over = True
            homing_missiles.remove(missile)

        # Check for missile lifetime
        if current_time - missile[4] > homing_missile_lifetime:
            homing_missiles.remove(missile)

    # --- Obstacle spawning ---
    if current_time - last_obstacle_spawn > obstacle_spawn_rate:
        obstacle_x = random.randint(0, screen_width - obstacle_size)
        obstacles.append(
            [obstacle_x, -obstacle_size, obstacle_speed]
        )  # Add initial speed
        last_obstacle_spawn = current_time

    # --- Obstacle movement ---
    for obstacle in obstacles[:]:
        obstacle[2] = min(obstacle[2] + obstacle_acceleration, max_obstacle_speed)
        obstacle[1] += obstacle[2]
        if obstacle[1] > screen_height:
            obstacles.remove(obstacle)

        # Check for collision with player
        if (
            player_x < obstacle[0] + obstacle_size
            and player_x + player_size > obstacle[0]
            and player_y < obstacle[1] + obstacle_size
            and player_y + player_size > obstacle[1]
        ):
            lives -= 1
            obstacles.remove(obstacle)
            if lives == 0:
                game_over = True  # Game over

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

    # --- Shield duration ---
    if has_shield and current_time - shield_start_time > shield_duration:
        has_shield = False
        shield_hits = 5  # Reset shield hits

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
    screen.blit(
        ground_texture,
        (
            ground_x + ground_texture.get_width(),
            screen_height - ground_texture.get_height(),
        ),
    )

    # Draw dents (before the grass)
    for dent_x in dents:
        dent_rect = (
            ground_x + dent_x,
            screen_height - ground_height + dent_depth,
            dent_width,
            ground_height - dent_depth,
        )
        pygame.draw.rect(screen, white, dent_rect)

    # Draw the grass (green rectangle)
    pygame.draw.rect(
        screen, green, (0, screen_height - ground_height, screen_width, ground_height)
    )

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(
            screen, red, (obstacle[0], obstacle[1], obstacle_size, obstacle_size)
        )

    # Draw fuel tokens
    for fuel_token in fuel_tokens:
        pygame.draw.circle(
            screen,
            (255, 255, 0),
            (
                fuel_token[0] + fuel_token_size // 2,
                fuel_token[1] + fuel_token_size // 2,
            ),
            fuel_token_size // 2,
        )

    # Draw turrets
    for turret in turrets:
        pygame.draw.rect(
            screen, turret_color, (turret[0], turret[1], turret_size, turret_size)
        )

    # Draw special turrets
    for special_turret in special_turrets:
        pygame.draw.rect(
            screen,
            special_turret_color,
            (
                special_turret[0],
                special_turret[1],
                special_turret_size,
                special_turret_size,
            ),
        )

    # Draw rockets
    for rocket in rockets:
        pygame.draw.circle(screen, red, (int(rocket[0]), int(rocket[1])), 5)

    # Draw homing missiles
    for missile in homing_missiles:
        pygame.draw.circle(
            screen, blue, (int(missile[0]), int(missile[1])), 8
        )  # Larger blue circle for homing missiles

    # Draw extra lives (falling hearts)
    for extra_life in extra_lives:
        screen.blit(heart_image, (extra_life[0], extra_life[1]))

    # --- Update and Draw Particles ---
    for particle in particles[:]:  # Iterate over a copy of the list
        particle.update()
        if particle.alive:
            particle.draw(screen)
        else:
            particles.remove(particle)

    # Draw hearts (lives)
    for i in range(lives):
        screen.blit(heart_image, (10 + i * (heart_image.get_width() + 5), 10))

    # Draw the player
    if not game_over:
        pygame.draw.rect(
            screen, blue, (player_x, player_y, player_size, player_size)
        )  # Draw the player even after game over
    if has_shield:
        pygame.draw.circle(
            screen,
            (0, 255, 255),
            (player_x + player_size // 2, player_y + player_size // 2),
            player_size,
            2,
        )

    # Draw pause button
    pygame.draw.circle(
        screen,
        pause_button_color,
        (pause_button_x, pause_button_y),
        pause_button_radius,
    )

    # --- Draw bars ---
    # Jetpack bar
    jetpack_bar_fill = (jetpack_fuel / 100) * bar_width
    pygame.draw.rect(
        screen, black, (jetpack_bar_x, jetpack_bar_y, bar_width, bar_height)
    )  # Background
    pygame.draw.rect(
        screen, yellow, (jetpack_bar_x, jetpack_bar_y, jetpack_bar_fill, bar_height)
    )  # Fill

    # Boost bar
    boost_bar_fill = (boost / boost_amount) * bar_width
    pygame.draw.rect(
        screen, black, (boost_bar_x, boost_bar_y, bar_width, bar_height)
    )  # Background
    pygame.draw.rect(
        screen, cyan, (boost_bar_x, boost_bar_y, boost_bar_fill, bar_height)
    )  # Fill

    # Shield bar
    shield_bar_fill = (shield_hits / 5) * bar_width
    pygame.draw.rect(
        screen, black, (shield_bar_x, shield_bar_y, bar_width, bar_height)
    )  # Background
    pygame.draw.rect(
        screen, magenta, (shield_bar_x, shield_bar_y, shield_bar_fill, bar_height)
    )  # Fill

    # Draw score
    score_text = menu_font.render("Score: " + str(score), True, black)
    screen.blit(score_text, (10, 50))  # Display score at top-left

    # Update the display
    pygame.display.flip()

    # Limit frame rate
    clock.tick(60)

pygame.quit()

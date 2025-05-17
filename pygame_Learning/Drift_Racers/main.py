import pygame
import asyncio
import math
import time
import random

# Initialize Pygame
pygame.init()
pygame.font.init() # Initialize font module

# --- Game Settings ---
WIDTH, HEIGHT = 1200, 800
BG_COLOR = (100, 150, 100)  # Grass color
TRACK_COLOR = (50, 50, 50)    # Asphalt color
FINISH_LINE_COLOR = (255, 255, 255)
MUD_COLOR = (139, 69, 19)
WATER_COLOR = (30, 144, 255) # Dodger Blue for water
UI_COLOR = (255, 255, 255)
UI_BG_COLOR = (0, 0, 0, 150) # Semi-transparent black background for UI

# --- Physics & Control (Closer to Original) ---
MAX_SPEED = 5 # Original max speed
FRICTION = 0.98  # Original friction for velocity damping
OFF_TRACK_FRICTION = 0.92 # Friction when off track (Applied to velocity)
TURN_SMOOTHNESS = 0.05 # Original turn smoothness factor (for velocity change)
DRIFT_TRAIL_DURATION = 1.0 # Original duration
CAR_WIDTH, CAR_HEIGHT = 40, 24 # Keep smaller cars for track
CAR_RADIUS = 20

TOTAL_LAPS = 3

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(f"Drift Racer - {TOTAL_LAPS} Laps")
clock = pygame.time.Clock()
UI_FONT = pygame.font.SysFont("monospace", 24, bold=True)
WINNER_FONT = pygame.font.SysFont("impact", 80)
# --- Sound Effects ---
pygame.mixer.init()
drift_sound = pygame.mixer.Sound("car-motor-revving.wav") # Replace "drift.wav" with your sound file
drift_sound.set_volume(0.5)  # Adjust volume as needed
# --- Track and Obstacle Definitions ---
TRACK_MARGIN = 100
TRACK_WIDTH_PX = 200 # Width of the tarmac
TRACK_OUTER_RECT = pygame.Rect(TRACK_MARGIN, TRACK_MARGIN, WIDTH - 2 * TRACK_MARGIN, HEIGHT - 2 * TRACK_MARGIN)
TRACK_INNER_RECT = pygame.Rect(TRACK_MARGIN + TRACK_WIDTH_PX, TRACK_MARGIN + TRACK_WIDTH_PX,
                              WIDTH - 2 * (TRACK_MARGIN + TRACK_WIDTH_PX), HEIGHT - 2 * (TRACK_MARGIN + TRACK_WIDTH_PX))

# Start/Finish Line
START_FINISH_Y = HEIGHT // 2
START_FINISH_LINE = pygame.Rect(WIDTH - TRACK_MARGIN - TRACK_WIDTH_PX - TRACK_WIDTH_PX // 2 + 100, HEIGHT // 2-5, TRACK_WIDTH_PX, 10)

# Checkpoints
CHECKPOINTS = [
    pygame.Rect(WIDTH // 2 - 50, TRACK_MARGIN, 100, TRACK_WIDTH_PX), # Top middle
    pygame.Rect(TRACK_MARGIN, HEIGHT // 2 - 50, TRACK_WIDTH_PX, 100), # Left middle
    pygame.Rect(WIDTH // 2 - 50, HEIGHT - TRACK_MARGIN - TRACK_WIDTH_PX, 100, TRACK_WIDTH_PX), # Bottom middle
]

# Obstacle Zones
MUD_RECT = pygame.Rect(WIDTH * 0.2, TRACK_MARGIN + TRACK_WIDTH_PX // 4, 150, 80)
WATER_RECT = pygame.Rect(WIDTH * 0.65, HEIGHT - TRACK_MARGIN - TRACK_WIDTH_PX + TRACK_WIDTH_PX // 4, 180, 90)

# Surfaces for semi-transparent drawing
mud_surface = pygame.Surface((MUD_RECT.width, MUD_RECT.height), pygame.SRCALPHA)
water_surface = pygame.Surface((WATER_RECT.width, WATER_RECT.height), pygame.SRCALPHA)

# --- Particle Classes ---
# Keep the Particle classes (Smoke, Splash, Mud) exactly as they were in the previous version
# including the __init__, update, and draw methods using SRCALPHA surfaces.
class SmokeParticle:
    def __init__(self, x, y, speed_x, speed_y, start_alpha=200):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.size = random.randint(3, 7)
        self.alpha = start_alpha
        self.lifetime = random.uniform(0.5, 1.5)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.size *= 0.97
        self.alpha -= 6
        self.lifetime -= 1 / 60.0
        if self.alpha < 0: self.alpha = 0
        if self.size < 1: self.lifetime = 0

    def draw(self, surface):
        if self.alpha > 0 and self.size >= 1:
            particle_surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (180, 180, 180, int(self.alpha)), (int(self.size), int(self.size)), int(self.size))
            surface.blit(particle_surf, (int(self.x - self.size), int(self.y - self.size)))

class SplashParticle(SmokeParticle):
    def draw(self, surface):
        if self.alpha > 0 and self.size >= 1:
            particle_surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (100, 180, 255, int(self.alpha)), (int(self.size), int(self.size)), int(self.size))
            surface.blit(particle_surf, (int(self.x - self.size), int(self.y - self.size)))

class MudParticle(SmokeParticle):
    def draw(self, surface):
        if self.alpha > 0 and self.size >= 1:
            particle_surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, (101, 67, 33, int(self.alpha)), (int(self.size), int(self.size)), int(self.size))
            surface.blit(particle_surf, (int(self.x - self.size), int(self.y - self.size)))


# --- Global Lists ---
smoke_particles = []
drift_tracks = []

# --- Load Player Car Images/Surfaces ---
# Keep the car surface loading code as before
player1_car_orig = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
player1_car_orig.fill((0, 200, 255)) # Blue
pygame.draw.rect(player1_car_orig, (255, 255, 0), (CAR_WIDTH * 0.7, 0, CAR_WIDTH * 0.3, CAR_HEIGHT)) # Yellow highlight

player2_car_orig = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)
player2_car_orig.fill((255, 100, 100)) # Red
pygame.draw.rect(player2_car_orig, (255, 255, 0), (CAR_WIDTH * 0.7, 0, CAR_WIDTH * 0.3, CAR_HEIGHT)) # Yellow highlight


# --- Player Properties ---
# Keep the structure, add velocity back from original code
start_pos1 = [START_FINISH_LINE.centerx + 30, START_FINISH_LINE.centery]
start_pos2 = [START_FINISH_LINE.centerx - 30, START_FINISH_LINE.centery]
start_angle = -270 # Pointing left

players = [
    {"pos": list(start_pos1), "angle": start_angle, "speed": 0, "velocity": [0.0, 0.0], "lap": 0, "next_checkpoint": 0, "surface": player1_car_orig, "off_track": False, "finished": False, "finish_time": 0},
    {"pos": list(start_pos2), "angle": start_angle, "speed": 0, "velocity": [0.0, 0.0], "lap": 0, "next_checkpoint": 0, "surface": player2_car_orig, "off_track": False, "finished": False, "finish_time": 0}
]

# --- Helper Functions ---
# Keep is_on_track, check_in_special_zone, spawn_particles,
# draw_track, draw_special_zones, draw_ui as they were.
# We don't need add_drift_effects anymore.

def is_on_track(player_pos):
    """Checks if a point is within the track boundaries."""
    x, y = player_pos
    if not TRACK_OUTER_RECT.collidepoint(x, y): return False
    rx_outer, ry_outer = TRACK_OUTER_RECT.width / 2, TRACK_OUTER_RECT.height / 2
    cx_outer, cy_outer = TRACK_OUTER_RECT.center
    if ((x - cx_outer)**2 / rx_outer**2 + (y - cy_outer)**2 / ry_outer**2) > 1:
        return False
    if TRACK_INNER_RECT.width > 0 and TRACK_INNER_RECT.height > 0:
       rx_inner, ry_inner = TRACK_INNER_RECT.width / 2, TRACK_INNER_RECT.height / 2
       cx_inner, cy_inner = TRACK_INNER_RECT.center
       if ((x - cx_inner)**2 / rx_inner**2 + (y - cy_inner)**2 / ry_inner**2) < 1:
           return False
    return True

def check_in_special_zone(player):
    """Checks if player is in mud or water using car radius."""
    player_center = pygame.Vector2(player["pos"])
    if MUD_RECT.collidepoint(player_center): return 'mud'
    if WATER_RECT.collidepoint(player_center): return 'water'
    # Could add more refined check (e.g., rect collision) if needed
    # player_rect = pygame.Rect(player["pos"][0] - CAR_RADIUS, player["pos"][1] - CAR_RADIUS, CAR_RADIUS * 2, CAR_RADIUS * 2)
    # if player_rect.colliderect(MUD_RECT): return 'mud'
    # if player_rect.colliderect(WATER_RECT): return 'water'
    return None

def spawn_particles(player_pos, zone_type, num_particles, base_speed_range=(-1, 1), speed_multiplier=2, start_alpha=200):
    """Spawns appropriate particles based on zone."""
    particles_to_add = []
    particle_class = SmokeParticle
    if zone_type == 'mud':
        particle_class = MudParticle
    elif zone_type == 'water':
        particle_class = SplashParticle

    # Base particle spawn on player's current velocity slightly
    base_vx = players[0]["velocity"][0] if len(players) > 0 else 0 # Handle potential empty list early
    base_vy = players[0]["velocity"][1] if len(players) > 0 else 0
    # Find the player index if possible to get correct velocity - less efficient
    # player_index = -1
    # for idx, p in enumerate(players):
    #     if p["pos"] == list(player_pos): # This comparison might fail due to float precision
    #          player_index = idx
    #          break
    # if player_index != -1:
    #      base_vx = players[player_index]["velocity"][0]
    #      base_vy = players[player_index]["velocity"][1]


    for _ in range(num_particles):
        # Give particles some velocity opposite to car's movement + random spread
        speed_x = (random.uniform(base_speed_range[0], base_speed_range[1]) - base_vx * 0.1) * speed_multiplier
        speed_y = (random.uniform(base_speed_range[0], base_speed_range[1]) - base_vy * 0.1) * speed_multiplier
        particles_to_add.append(particle_class(player_pos[0], player_pos[1], speed_x, speed_y, start_alpha))
    return particles_to_add

def draw_track():
    """Draws the track background, tarmac, and lines."""
    screen.fill(BG_COLOR) # Grass
    pygame.draw.ellipse(screen, TRACK_COLOR, TRACK_OUTER_RECT)
    if TRACK_INNER_RECT.width > 0 and TRACK_INNER_RECT.height > 0:
         pygame.draw.ellipse(screen, BG_COLOR, TRACK_INNER_RECT)
    pygame.draw.rect(screen, FINISH_LINE_COLOR, START_FINISH_LINE)
    check_size = 10
    for y in range(START_FINISH_LINE.top, START_FINISH_LINE.bottom, check_size):
         for x in range(START_FINISH_LINE.left, START_FINISH_LINE.right, check_size):
              if ((x // check_size) % 2 == (y // check_size) % 2):
                  pygame.draw.rect(screen, (100, 100, 100), (x, y, check_size, check_size))

def draw_special_zones(current_time):
    """Draws and animates the mud and water zones."""
    mud_alpha = 100 + math.sin(current_time * 3) * 30
    mud_surface.fill((MUD_COLOR[0], MUD_COLOR[1], MUD_COLOR[2], int(mud_alpha)))
    screen.blit(mud_surface, MUD_RECT.topleft)

    water_alpha = 120 + math.sin(current_time * 2.5 + 1) * 40
    water_surface.fill((*WATER_COLOR, int(water_alpha)))
    ripple_offset1 = math.sin(current_time * 4) * 3
    ripple_offset2 = math.cos(current_time * 3.5) * 2
    # Need to create rects relative to the water_surface, not the screen
    base_rect = pygame.Rect(0, 0, WATER_RECT.width, WATER_RECT.height)
    ripple_rect1 = base_rect.inflate(ripple_offset1, ripple_offset1 * 0.5)
    ripple_rect2 = base_rect.inflate(ripple_offset2 * 0.8, ripple_offset2)
    pygame.draw.ellipse(water_surface, (*WATER_COLOR, int(water_alpha * 0.7)), ripple_rect1, width=2)
    pygame.draw.ellipse(water_surface, (*WATER_COLOR, int(water_alpha * 0.6)), ripple_rect2, width=2)
    screen.blit(water_surface, WATER_RECT.topleft)


def draw_ui(players, game_state, winner_text):
    """Draws lap counts and winner message."""
    ui_box = pygame.Surface((WIDTH, 50), pygame.SRCALPHA)
    ui_box.fill(UI_BG_COLOR)
    screen.blit(ui_box, (0, 0))
    lap_text_p1 = UI_FONT.render(f"P1 Laps: {players[0]['lap']}/{TOTAL_LAPS}", 1, (0, 200, 255))
    screen.blit(lap_text_p1, (10, 10))
    lap_text_p2 = UI_FONT.render(f"P2 Laps: {players[1]['lap']}/{TOTAL_LAPS}", 1, (255, 100, 100))
    screen.blit(lap_text_p2, (WIDTH - lap_text_p2.get_width() - 10, 10))
    if game_state == "FINISHED":
        winner_surf = WINNER_FONT.render(winner_text, 1, (255, 215, 0))
        winner_rect = winner_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        pygame.draw.rect(screen, (0,0,0, 200), winner_rect.inflate(20, 20))
        screen.blit(winner_surf, winner_rect)

# --- Game State ---
game_state = "RACING"
winner_message = ""
race_start_time = time.time()

# --- Game Loop ---
running = True
async def main():
    while running:
        current_time = time.time()
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        keys = pygame.key.get_pressed()

        # --- Update Players ---
        if game_state == "RACING":
            # Player 1 Controls (WASD) - Original Style Speed Adjust
            turning1 = False
            if keys[pygame.K_w]:
                drift_sound.play()
                players[0]["speed"] = min(players[0]["speed"] + 0.3, MAX_SPEED)
            if keys[pygame.K_s]:
                drift_sound.play()
                players[0]["speed"] = max(players[0]["speed"] - 0.3, -MAX_SPEED / 1.5) # Allow reverse
            if keys[pygame.K_a]:
                players[0]["angle"] += 5 # Original fixed turn rate
                turning1 = True
            if keys[pygame.K_d]:
                players[0]["angle"] -= 5
                turning1 = True

            # Player 2 Controls (Arrow Keys) - Original Style Speed Adjust
            turning2 = False
            if keys[pygame.K_UP]:
                drift_sound.play()
                players[1]["speed"] = min(players[1]["speed"] + 0.3, MAX_SPEED)
            if keys[pygame.K_DOWN]:
                drift_sound.play()
                players[1]["speed"] = max(players[1]["speed"] - 0.3, -MAX_SPEED / 1.5) # Allow reverse
            if keys[pygame.K_LEFT]:
                players[1]["angle"] += 5
                turning2 = True
            if keys[pygame.K_RIGHT]:
                players[1]["angle"] -= 5
                turning2 = True

            player_turn_flags = [turning1, turning2]

            if (not(keys[pygame.K_DOWN] or keys[pygame.K_UP]) and not(keys[pygame.K_w] or keys[pygame.K_s])) and game_state == "FINISHED":
                drift_sound.stop()

            # Update movement, physics, laps for each player
            for i, player in enumerate(players):
                if player["finished"]: continue

                # Original gradual slowdown if no acceleration buttons pressed
                no_input = (i == 0 and not (keys[pygame.K_w] or keys[pygame.K_s])) or \
                        (i == 1 and not (keys[pygame.K_UP] or keys[pygame.K_DOWN]))
                if no_input:
                    player["speed"] *= 0.96 # Gentle coasting slowdown

                # --- Original Physics Update ---
                rad_angle = math.radians(player["angle"])
                forward_vector = [math.cos(rad_angle), -math.sin(rad_angle)]

                # Update velocity based on speed, angle, and smoothness (Core of original drift)
                player["velocity"][0] += forward_vector[0] * player["speed"] * TURN_SMOOTHNESS
                player["velocity"][1] += forward_vector[1] * player["speed"] * TURN_SMOOTHNESS

                # Check track status & Get appropriate friction
                player["off_track"] = not is_on_track(player["pos"])
                current_friction = OFF_TRACK_FRICTION if player["off_track"] else FRICTION

                # Apply friction to velocity
                player["velocity"][0] *= current_friction
                player["velocity"][1] *= current_friction

                # Check special zones
                special_zone = check_in_special_zone(player) if not player["off_track"] else None
                zone_speed_multiplier = 1.0
                # Apply zone slowdown *directly* to velocity in this model
                if special_zone == 'mud':
                    player["velocity"][0] *= 0.85 # Slow down velocity significantly in mud
                    player["velocity"][1] *= 0.85
                    player["speed"] *= 0.9 # Also reduce the base speed buildup slightly
                elif special_zone == 'water':
                    player["velocity"][0] *= 0.92 # Slow down velocity less in water
                    player["velocity"][1] *= 0.92
                    player["speed"] *= 0.95 # Reduce base speed buildup less


                # Update position using the (frictioned and zone-modified) velocity
                player["pos"][0] += player["velocity"][0]
                player["pos"][1] += player["velocity"][1]
                # --- End Original Physics Update ---


                # --- Checkpoint and Lap Logic (Keep as is) ---
                player_rect = pygame.Rect(player["pos"][0] - 5, player["pos"][1] - 5, 10, 10)
                next_cp_index = player["next_checkpoint"]
                if next_cp_index < len(CHECKPOINTS):
                    if player_rect.colliderect(CHECKPOINTS[next_cp_index]):
                        player["next_checkpoint"] += 1
                elif player_rect.colliderect(START_FINISH_LINE):
                    player["lap"] += 1
                    player["next_checkpoint"] = 0
                    if player["lap"] >= TOTAL_LAPS:
                        player["finished"] = True
                        player["finish_time"] = current_time - race_start_time


                # --- Original Drift Effects Generation (Activated by Turning Flags) ---
                if player_turn_flags[i] and not player["off_track"] and abs(player["speed"]) > 1.0: # Only make effects if moving & turning
                    # Add drift tracks (Simplified: one point behind)
                    track_pos_x = player["pos"][0] - forward_vector[0] * CAR_HEIGHT * 0.7
                    track_pos_y = player["pos"][1] - forward_vector[1] * CAR_HEIGHT * 0.7
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

                    # Add smoke/mud/water particles using helper
                    zone = check_in_special_zone(player) # Check zone for particle type
                    num_particles = 3 # Original number
                    # Spawn slightly behind the car
                    particle_spawn_pos = (player["pos"][0] - forward_vector[0] * CAR_HEIGHT * 0.5,
                                        player["pos"][1] - forward_vector[1] * CAR_HEIGHT * 0.5)
                    smoke_particles.extend(spawn_particles(particle_spawn_pos, zone, num_particles, base_speed_range=(-1, 1), speed_multiplier=1.5))


            # --- Handle Car Collisions (Keep improved collision physics) ---
            p1, p2 = players[0], players[1]
            if not p1["finished"] and not p2["finished"]:
                dx = p2["pos"][0] - p1["pos"][0]
                dy = p2["pos"][1] - p1["pos"][1]
                distance_sq = dx*dx + dy*dy
                min_distance_sq = (CAR_RADIUS * 2)**2

                if 0 < distance_sq < min_distance_sq:
                    distance = math.sqrt(distance_sq)
                    overlap = (CAR_RADIUS * 2) - distance
                    nx, ny = dx / distance, dy / distance

                    # Separate cars
                    push_amount = overlap / 2
                    # Prevent position update if it pushes off track? Optional.
                    p1["pos"][0] -= nx * push_amount
                    p1["pos"][1] -= ny * push_amount
                    p2["pos"][0] += nx * push_amount
                    p2["pos"][1] += ny * push_amount

                    # Collision response using velocity vectors (more robust than just speed)
                    # Relative velocity
                    rvx = p1["velocity"][0] - p2["velocity"][0]
                    rvy = p1["velocity"][1] - p2["velocity"][1]
                    vel_along_normal = rvx * nx + rvy * ny

                    if vel_along_normal <= 0: # Only resolve if moving towards each other
                        elasticity = 0.6 # Slightly less bouncy maybe
                        impulse_scalar = -(1 + elasticity) * vel_along_normal
                        impulse_scalar /= 2 # Assume equal mass

                        impulse_x = impulse_scalar * nx
                        impulse_y = impulse_scalar * ny

                        # Apply impulse to velocities
                        p1["velocity"][0] += impulse_x
                        p1["velocity"][1] += impulse_y
                        p2["velocity"][0] -= impulse_x
                        p2["velocity"][1] -= impulse_y

                        # IMPORTANT: In the original physics model, 'speed' is separate from 'velocity'.
                        # A collision affects velocity directly. We might want to slightly adjust 'speed' too,
                        # or let the next frame's friction/acceleration handle it. Let's just modify velocity for now.
                        # Optional: Dampen speed slightly on impact
                        # p1["speed"] *= 0.95
                        # p2["speed"] *= 0.95

                        # Spawn impact particles
                        impact_pos = ((p1["pos"][0] + p2["pos"][0]) / 2, (p1["pos"][1] + p2["pos"][1]) / 2)
                        zone = check_in_special_zone({"pos": impact_pos})
                        num_impact_particles = 8; impact_speed = 2.5
                        if zone == 'mud': num_impact_particles=12; impact_speed=1.5
                        if zone == 'water': num_impact_particles=15; impact_speed=3.0
                        smoke_particles.extend(spawn_particles(impact_pos, zone, num_impact_particles, (-1, 1), impact_speed, start_alpha=255))


            # --- Check for Race Finish (Keep as is) ---
            if all(p["finished"] for p in players):
                game_state = "FINISHED"
                if players[0]["finish_time"] < players[1]["finish_time"]: winner_message = "Player 1 Wins!"
                elif players[1]["finish_time"] < players[0]["finish_time"]: winner_message = "Player 2 Wins!"
                else: winner_message = "It's a Tie!"
            elif any(p["finished"] for p in players) and game_state == "RACING":
                if players[0]["finished"] and not players[1]["finished"]:
                    game_state = "FINISHED"; winner_message = "Player 1 Wins!"
                elif players[1]["finished"] and not players[0]["finished"]:
                    game_state = "FINISHED"; winner_message = "Player 2 Wins!"


        # --- Update Particles and Tracks ---
        # Keep this section as is (using lifetimes and durations)
        drift_tracks = [track for track in drift_tracks if current_time - track[2] <= DRIFT_TRAIL_DURATION]
        smoke_particles = [p for p in smoke_particles if p.lifetime > 0]
        for particle in smoke_particles:
            particle.update()

        # --- Drawing ---
        # Keep this section as is (draw track, zones, tracks, particles, cars, UI)
        draw_track()
        draw_special_zones(current_time)

        for track in drift_tracks:
            age = current_time - track[2]
            alpha = max(0, 255 * (1 - age / DRIFT_TRAIL_DURATION))
            track_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(track_surf, (0, 0, 0, int(alpha * 0.5)), (4, 4), 4)
            screen.blit(track_surf, (track[0] - 4, track[1] - 4))

        for particle in smoke_particles:
            particle.draw(screen)

        for player in players:
            rotated_car = pygame.transform.rotate(player["surface"], player["angle"])
            car_rect = rotated_car.get_rect(center=player["pos"])
            screen.blit(rotated_car, car_rect.topleft)

        draw_ui(players, game_state, winner_message)

        # --- Display Update ---
        pygame.display.flip()

    # --- End Game ---
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())

import pygame, random
from pygame.locals import *

pygame.init()
# game variables:

screen_width = 800
screen_height = 800
bg_color = (100, 200, 255)
fps = 30
cloud_velocity = 5
sun_height, sun_width, cloud_height, cloud_width = 100, 100, 75, 150
tile_size = screen_width / 20
speed = 5
dy = 0
dx = 0

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

# load images
sun_img = pygame.image.load("images/sun.png")
sun_resized = pygame.transform.scale(sun_img, (sun_width, sun_height))
r1 = pygame.Rect(0, 25, cloud_width, cloud_height)
r2 = pygame.Rect(0, 25, cloud_width, cloud_height)
cloud1_img = pygame.image.load("images/cloud1.png")
cloud2_img = pygame.image.load("images/cloud.png")
cloud1_resized = pygame.transform.scale(cloud1_img, (cloud_width, cloud_height))
cloud2_resized = pygame.transform.scale(cloud2_img, (cloud_width, cloud_height))


class World:
    def __init__(self, data):
        self.tile_list = []
        grass_block_img = pygame.image.load("images/grass_block.jpeg")
        stone_wall_img = pygame.image.load("images/stone wall.png")
        lava_img = pygame.image.load("images/Minecraft-Lava.jpg")
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 2:
                    img = pygame.transform.scale(
                        grass_block_img, ((tile_size, tile_size))
                    )
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 1:
                    img = pygame.transform.scale(
                        stone_wall_img, ((tile_size, tile_size))
                    )
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                elif tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size)
                    # blob_group.add(blob)
                elif tile == 6:
                    img = pygame.transform.scale(lava_img, ((tile_size, tile_size)))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 1)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.image.load("images/slime.jpeg"), ((tile_size, tile_size))
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > 50:
            self.move_direction *= -1
            self.move_counter = 0


class Player:
    def __init__(self, x, y):
        player = pygame.image.load("images/steve.webp")
        self.image = pygame.transform.scale(player, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width
        self.height = self.image.get_height
        self.vel_y = 0
        self.jumped = False
        self.rect.bottom = screen_height
        self.rect = self.image.get_rect()

    def update(self):
        dx = 0
        dy = 0
        # keypresses
        # print(key[pygame.K_SPACE])
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
            self.vel_y = -15
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= 5
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += 5
            self.counter += 1
            self.direction = 1
        if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
            self.counter = 0
            self.index = 0
        # add gravity
        self.vel_y += 1
        if self.vel_y > 15:
            self.vel_y = 10
        dy += self.vel_y
        # check for collision

        self.in_air = True
        for tile in world.tile_list:
            # check for collision in x direction
            if tile[1].colliderect(
                int(self.rect.x + dx), int(self.rect.y), self.width(), self.height()
            ):
                dx = 0
            # check for collision in y direction
            if tile[1].colliderect(
                int(self.rect.x), int(self.rect.y + dy), self.width(), self.height()
            ):
                # check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                # check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        # update player coordinates

        print(f"dx: {dx}, dy: {dy}")
        print(f"before: x: {self.rect.x}, y: {self.rect.y}, bottom: {self.rect.bottom}")
        self.rect.x += dx
        self.rect.y += dy
        # self.rect.move(self.rect.x + 10, self.rect.y + 10)
        # self.rect.bottom = 0  # screen_height
        if self.rect.bottom > 1000:
            self.rect.bottom = screen_height
            dy = 0
        print(f"after: x: {self.rect.x}, y: {self.rect.y}, bottom: {self.rect.bottom}")

        screen.blit(self.image, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1)


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 4, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


player = Player(100, screen_height - 130)
world = World(world_data)
# blob_group = pygame.sprite.Group()


def main():
    clock = pygame.time.Clock()
    running = True
    screen.fill(bg_color)
    screen.blit(sun_resized, ((25, 25)))
    countdown_ms = 17  # milliseconds
    ms_100_timer = pygame.USEREVENT + 1
    player.rect.x = 100
    player.rect.y = screen_height - tile_size
    pygame.time.set_timer(ms_100_timer, countdown_ms)
    i = random.randint(1, 700)
    x = random.randint(1, 700)
    y = random.randint(1, 700)
    z = random.randint(1, 700)

    player.update()
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == ms_100_timer:
                screen.fill(bg_color)
                i += 2.5
                x += 2.2
                y += 1.5
                z += 1.35
                if i >= (screen_width) + cloud_width / 2:
                    i = 1.0
                if x >= (screen_width) + cloud_width / 2:
                    x = 1.0
                if y >= (screen_width) + cloud_width / 2:
                    y = 1.0
                if z >= (screen_width) + cloud_width / 2:
                    z = 1.0
                screen.blit(cloud1_resized, ((-cloud_width + int(i), 70)))
                screen.blit(cloud2_resized, ((-cloud_width + int(x), 25)))
                screen.blit(cloud1_resized, ((-cloud_width + int(y), 50)))
                screen.blit(cloud2_resized, ((-cloud_width + int(z), 100)))
                screen.blit(sun_resized, ((50, 50)))
                world.draw()
                player.update()

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()

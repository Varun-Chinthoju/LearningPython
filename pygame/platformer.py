import pygame, random
from pygame.locals import *

pygame.init()
# game variables:

screen_width = 1000
screen_height = 1000
bg_color = (100, 200, 255)
fps = 100
cloud_velocity = 5
sun_height, sun_width, cloud_height, cloud_width = 100, 100, 75, 150
tile_size = 50


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")

# load images
sun_img = pygame.image.load("sun.png")
sun_resized = pygame.transform.scale(sun_img, (sun_width, sun_height))
r1 = pygame.Rect(0, 25, cloud_width, cloud_height)
r2 = pygame.Rect(0, 25, cloud_width, cloud_height)
cloud1_img = pygame.image.load("cloud1.png")
cloud2_img = pygame.image.load("cloud.png")
cloud1_resized = pygame.transform.scale(cloud1_img, (cloud_width, cloud_height))
cloud2_resized = pygame.transform.scale(cloud2_img, (cloud_width, cloud_height))


class World:
    def __init__(self, data):
        self.tile_list = []
        grass_block_img = pygame.image.load("grass_block.jpeg")
        stone_wall_img = pygame.image.load("stone wall.png")
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
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class player:
    def __init__(self, x, y):
        player = pygame.image.load("Untitled drawing.png")
        self.image = pygame.transform.scale(player, ())
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        screen.blit(self.image, self.rect)


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


player = player(100, screen_height - 130)


def main():
    clock = pygame.time.Clock()
    running = True
    screen.fill(bg_color)
    screen.blit(sun_resized, ((25, 25)))
    countdown_ms = 17  # milliseconds
    ms_100_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(ms_100_timer, countdown_ms)
    i = random.randint(1, 700)
    x = random.randint(1, 700)
    y = random.randint(1, 700)
    z = random.randint(1, 700)
    world = World(world_data)

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

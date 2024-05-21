import pygame, random, time
from pygame.locals import *
from pygame import mixer

mixer.init()
pygame.init()
SCREENWIDTH = 800
SCREENHEIGHT = 800
BGCOLOR = (50, 200, 255)
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
font = pygame.font.SysFont("impact", 60)
pygame.display.set_caption("Flappy Bird")
mixer.music.set_volume(0.7)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Player:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(
            pygame.image.load("images/fb.png"), (100, 100)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.collision = "False"
        self.fall_speed = 7
        self.gravity_rate = 1
        self.pressed = 0
        self.proportional_speed = 7

    def update(self, pipes):
        dy = 0
        # keypresses
        key = pygame.key.get_pressed()
        if self.pressed == 0:
            self.rect.y = SCREENHEIGHT / 2
        if key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]:
            mixer.music.load("images/flap.mp3")
            mixer.music.play()
            self.vel_y = -self.proportional_speed
            self.pressed += 1

        # add gravity
        self.vel_y += self.gravity_rate
        if self.vel_y > self.fall_speed:
            self.vel_y = self.fall_speed
        dy += self.vel_y
        self.rect.y += dy
        # Check for collision with pipes
        if pipes.collide(self.rect):
            print(f"You got {pipes.points} points!!")
            print("thanks for playing!!")
            exit()
            # Handle collision (e.g., end game, reduce life, etc.)
        # Prevent player from moving outside the screen
        if self.rect.y >= SCREENHEIGHT - 70:
            self.rect.y = SCREENHEIGHT - 70
        elif self.rect.y <= 0:
            self.rect.y = 0

        screen.blit(self.image, (self.rect.x, self.rect.y))


class Pipes:
    def __init__(self, x, y, gap, pipe_height):
        self.pipe_width = 150
        self.pipe_vel = 5
        self.gap = gap
        self.points = 0
        self.up_pipe_img = pygame.image.load("images/up pipe.png")
        self.down_pipe_img = pygame.image.load("images/down pipe.png")
        self.up_pipe_resized = pygame.transform.scale(
            self.up_pipe_img, (self.pipe_width, pipe_height)
        )
        self.down_pipe_resized = pygame.transform.scale(
            self.down_pipe_img, (self.pipe_width, pipe_height)
        )
        self.up_rect = self.up_pipe_resized.get_rect(x=x, y=y)
        self.down_rect = self.down_pipe_resized.get_rect(
            x=x, y=y + pipe_height + self.gap
        )

    def update(self, player):
        self.up_rect.x -= self.pipe_vel
        self.down_rect.x -= self.pipe_vel
        # Reset pipe position if off-screen
        if self.up_rect.x + self.pipe_width < 0:
            self.reset_pipes()
        screen.blit(self.up_pipe_resized, (self.up_rect.x, self.up_rect.y))
        screen.blit(self.down_pipe_resized, (self.down_rect.x, self.down_rect.y))

        # Increase pipe velocity based on points
        self.pipe_vel = 7 + self.points / 4
        player.proportional_speed = 10 + self.points / 10
        player.gravity_rate = 1 + int(self.points / 10)
        player.fall_speed = int(self.pipe_vel * 1.5)

    def collide(self, player_rect):
        return self.up_rect.colliderect(player_rect) or self.down_rect.colliderect(
            player_rect
        )

    def reset_pipes(self):
        self.up_rect.x = SCREENWIDTH
        self.down_rect.x = SCREENWIDTH
        self.up_rect.y = random.randint(
            int(-pipe_height + (4 / 10) * SCREENHEIGHT), int(-gap * 0.5)
        )
        self.down_rect.y = self.up_rect.y + pipe_height + self.gap
        if self.up_rect.x > 100 + self.pipe_width:
            self.points += 1


# Example usage:
gap = 250
pipe_height = SCREENHEIGHT  # Height of each pipe image
pipes = Pipes(
    SCREENWIDTH + 150,
    random.randint(-pipe_height - gap + 30, int(-gap * 0.5)),
    gap,
    pipe_height,
)

player = Player(100, SCREENHEIGHT / 2)


def main():
    FPS = 60
    running = True
    clock = pygame.time.Clock()
    countdown_ms = 17
    ms_100_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(ms_100_timer, countdown_ms)
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit()
            if event.type == ms_100_timer:
                screen.fill(BGCOLOR)
                pipes.update(player)
                player.update(pipes)
                draw_text(
                    str(pipes.points), font, (255, 255, 255), int(SCREENWIDTH / 2), 30
                )

        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()

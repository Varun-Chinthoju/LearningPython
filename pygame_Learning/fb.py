import pygame
import random

# Game constants
screen_width = 800
screen_height = 600
gravity = 0.3  # Adjust gravity for game feel
bird_jump_velocity = -8  # Adjust jump strength

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

def draw_text(text, font_size, x, y, color):
  """Draws text on the screen."""
  font = pygame.font.Font(None, font_size)
  text_surface = font.render(text, True, color)
  screen.blit(text_surface, (x, y))

def create_pipe(gap_size):
  """Creates a top and bottom pipe pair with a random gap."""
  pipe_height = random.randint(100, screen_height - gap_size - 100)
  top_pipe = pygame.Rect(screen_width, 0, 50, pipe_height)
  bottom_pipe = pygame.Rect(screen_width, pipe_height + gap_size, 50, screen_height)
  return top_pipe, bottom_pipe

class Bird(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image = pygame.image.load("images/fb.png")
    self.rect = self.image.get_rect()
    self.rect.center = (screen_width // 2, screen_height // 2)
    self.velocity_y = 0

  def update(self):
    self.velocity_y += gravity
    self.rect.y += self.velocity_y

    # Prevent going off-screen
    if self.rect.top <= 0:
      self.rect.top = 0
      self.velocity_y = 0
    if self.rect.bottom >= screen_height:
      self.rect.bottom = screen_height
      self.velocity_y = 0

  def jump(self):
    self.velocity_y = bird_jump_velocity

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Load assets
bird = Bird()
bird_group = pygame.sprite.Group()
bird_group.add(bird)

clock = pygame.time.Clock()
gap_size = 150  # Adjust gap size for difficulty
pipes = []
score = 0
font = pygame.font.Font(None, 32)
passed_pipes = []  # Track passed pipes for scoring

# Game loop
running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_SPACE:
        bird.jump()

  # Update game objects
  bird.update()

  # Create new pipes

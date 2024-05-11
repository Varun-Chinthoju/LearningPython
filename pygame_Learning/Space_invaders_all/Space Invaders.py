import pygame, random
from pygame.locals import *
from pygame.sprite import Group
from player import Player
from lasers import Laser


class Game:
    def __init__(self):
        self.SCREENWIDTH = 1000
        self.SCREENHEIGHT = 1000
        self.screen = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        self.player = Player(
            self.SCREENWIDTH / 2, self.SCREENHEIGHT - (self.SCREENHEIGHT / 5)
        )
        self.laser = Laser(pygame.mouse.get_pos())
        pygame.mouse.set_visible(False)
        self.Bg = pygame.transform.scale(
            pygame.image.load("images/background.webp"),
            (self.SCREENWIDTH, self.SCREENHEIGHT),
        )
        fps = 60
        clock = pygame.time.Clock()
        clock.tick(fps)
        countdown_ms = 100
        ms_100_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(ms_100_timer, countdown_ms)

    def run(self):
        self.screen.blit(self.Bg, (0, 0))
        self.player.update()
        self.player.get_input()
        for laser in self.player.sprite:
            self.player.sprite.update()
            self.player.sprite.draw(self.screen)

    def main(self):
        running = True
        while running:
            self.run()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.update()
        pygame.quit()


game = Game()

if __name__ == "__main__":
    game.main()

    # Update bullet positions

import pygame


LETTERS_DIST = 30
LETTER_WIDTH = 60
VEX_HEIGHT = 110
VEX_WIDTH = 198
LETTER_HEIGHT = 75
SCREENWIDTH = 800
SCREENHEIGHT = 600
COLOR = (255, 255, 255)
STARTING_PLACE = 25


def key_press(key, screen, keypress_counters, images):
    key = pygame.key.get_pressed()
    if key[pygame.K_y]:
        keypress_counters["Y"] = 1
        if keypress_counters["Y"] == 1:
            screen.blit(images.y2, (STARTING_PLACE, (1 / 4) * SCREENHEIGHT))
            screen.blit(
                images.y1,
                (
                    STARTING_PLACE + (2 * (LETTERS_DIST)) + LETTER_WIDTH,
                    (1 / 4) * SCREENHEIGHT,
                ),
            )

    if key[pygame.K_a]:
        keypress_counters["A"] = 1
        if keypress_counters["A"] == 1:
            screen.blit(
                images.A,
                (
                    STARTING_PLACE + LETTERS_DIST + LETTER_WIDTH / 2,
                    (1 / 4) * SCREENHEIGHT,
                ),
            )

    if key[pygame.K_i]:
        keypress_counters["I"] = 1
        if keypress_counters["I"] == 1:
            screen.blit(
                images.I,
                (
                    STARTING_PLACE + (2 * LETTERS_DIST) + (2.5 * LETTER_WIDTH),
                    (1 / 4) * SCREENHEIGHT,
                ),
            )
            screen.blit(
                images.I,
                (
                    STARTING_PLACE + (8 * LETTERS_DIST) + (4.5 * LETTER_WIDTH),
                    (1 / 4) * SCREENHEIGHT,
                ),
            )

    if key[pygame.K_g]:
        keypress_counters["G"] = 1
        if keypress_counters["G"] == 1:
            screen.blit(
                images.G,
                (
                    STARTING_PLACE + (3 * LETTERS_DIST) + (3.5 * LETTER_WIDTH),
                    (1 / 4) * SCREENHEIGHT,
                ),
            )

    if key[pygame.K_o]:
        keypress_counters["O"] = 1
        if keypress_counters["O"] == 1:
            screen.blit(
                images.O,
                (
                    STARTING_PLACE + (5 * LETTERS_DIST) + (3.5 * LETTER_WIDTH),
                    (1 / 4) * SCREENHEIGHT,
                ),
            )
            screen.blit(
                images.O,
                (
                    STARTING_PLACE + (14 * LETTERS_DIST) + (4.5 * LETTER_WIDTH),
                    (1 / 4) * SCREENHEIGHT,
                ),
            )
    if key[pygame.K_t]:
        keypress_counters["T"] = 1
        if keypress_counters["T"] == 1:
            screen.blit(
                images.T,
                (
                    STARTING_PLACE + (7 * LETTERS_DIST) + (3.5 * LETTER_WIDTH),
                    (1 / 4) * SCREENHEIGHT,
                ),
            )
            screen.blit(
                images.T,
                (
                    STARTING_PLACE + (12 * LETTERS_DIST) + (4.5 * LETTER_WIDTH),
                    (1 / 4) * SCREENHEIGHT,
                ),
            )

    if key[pygame.K_n]:
        keypress_counters["N"] = 1
        if keypress_counters["N"] == 1:
            screen.blit(
                images.N,
                (
                    STARTING_PLACE + (10 * LETTERS_DIST) + (4.5 * LETTER_WIDTH),
                    (1 / 4) * SCREENHEIGHT,
                ),
            )

    if key[pygame.K_v] or key[pygame.K_e] or key[pygame.K_x]:
        keypress_counters["VEX"] = 1
        if keypress_counters["VEX"] == 1:
            screen.blit(
                images.VEX, ((SCREENWIDTH - VEX_WIDTH) / 2, (2 / 5) * SCREENHEIGHT)
            )


class Images:

    def load(self):
        self.y1 = pygame.transform.scale(
            pygame.image.load("images/Y.png"), (LETTER_WIDTH, LETTER_HEIGHT)
        )
        self.y2 = pygame.transform.scale(
            pygame.image.load("images/Y.png"),
            (LETTER_WIDTH, LETTER_HEIGHT),
        )

        self.A = pygame.transform.scale(
            pygame.image.load("images/A.webp"), (LETTER_WIDTH, LETTER_HEIGHT)
        )

        self.I = pygame.transform.scale(
            pygame.image.load("images/I.png"), (LETTER_WIDTH, LETTER_HEIGHT)
        )

        self.G = pygame.transform.scale(
            pygame.image.load("images/G.png"), (LETTER_WIDTH, LETTER_HEIGHT)
        )

        self.O = pygame.transform.scale(
            pygame.image.load("images/OOO.png"), (LETTER_WIDTH, LETTER_HEIGHT)
        )

        self.T = pygame.transform.scale(
            pygame.image.load("images/T.png"), (LETTER_WIDTH, LETTER_HEIGHT)
        )

        self.I1 = pygame.transform.scale(
            pygame.image.load("images/I.png"), (LETTER_WIDTH, LETTER_HEIGHT)
        )

        self.N = pygame.transform.scale(
            pygame.image.load("images/N.png"), (LETTER_WIDTH, LETTER_HEIGHT)
        )

        self.T1 = pygame.transform.scale(
            pygame.image.load("images/T.png"), (LETTER_WIDTH, LETTER_HEIGHT)
        )

        self.O1 = pygame.transform.scale(
            pygame.image.load("images/o.png"), (LETTER_WIDTH, LETTER_HEIGHT)
        )

        self.VEX = pygame.transform.scale(
            pygame.image.load("images/VEX.png"), (VEX_WIDTH, VEX_HEIGHT)
        )


def main():
    pygame.init()
    pygame.display.init()

    # variables
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    fps = 60
    pygame.display.set_caption("YAY I GOT INTO VEX!!")
    keypress_counters = {
        "Y": 0,
        "A": 0,
        "I": 0,
        "G": 0,
        "O": 0,
        "T": 0,
        "N": 0,
        "VEX": 0,
    }

    images = Images()
    images.load()

    # images
    running = True
    clock = pygame.time.Clock()
    key = pygame.key.get_pressed()

    clock.tick(fps)
    screen.fill(COLOR)

    while running:
        key_press(key, screen, keypress_counters, images)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

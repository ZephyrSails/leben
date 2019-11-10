from pflanze import Pflanze
from leben import Leben
from vision import Vision
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    VISION_HEIGHT = 140

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,
                                      SCREEN_HEIGHT + VISION_HEIGHT))
    game_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    vision_screen = pygame.Surface((SCREEN_WIDTH, VISION_HEIGHT))

    running = True

    pflanzen = pygame.sprite.Group()

    leben = Leben(game_screen, vision_screen, pflanzen)
    leben_group = pygame.sprite.Group()
    leben_group.add(leben)

    def add_pflanze(pflanzen):
        pflanze = Pflanze(SCREEN_WIDTH, SCREEN_HEIGHT)
        pflanzen.add(pflanze)

    for _ in range(32):
        add_pflanze(pflanzen)

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()

        game_screen.fill((0, 0, 0))
        leben.update(pressed_keys)

        game_screen.blit(leben.surf, leben.rect)

        for pflanze in pflanzen:
            game_screen.blit(pflanze.surf, pflanze.rect)

        collide_group = pygame.sprite.groupcollide(leben_group, pflanzen,
                                                   False, True)
        for _ in range(len(collide_group)):
            add_pflanze(pflanzen)

        screen.blit(game_screen, (0, 0))
        screen.blit(vision_screen, (0, SCREEN_HEIGHT))

        pygame.display.flip()


if __name__ == "__main__":
    main()

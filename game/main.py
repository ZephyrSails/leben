from flight import Flight
from pflanze import Pflanze
from panel import Panel
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True

    leben = Leben()
    leben_group = pygame.sprite.Group()
    leben_group.add(leben)
    pflanzen = pygame.sprite.Group()

    def add_pflanze(pflanzen):
        pflanze = Pflanze(SCREEN_WIDTH, SCREEN_HEIGHT)
        pflanzen.add(pflanze)

    for _ in range(28):
        add_pflanze(pflanzen)

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()
        leben.update(pressed_keys)

        screen.fill((0, 0, 0))

        screen.blit(leben.surf, leben.rect)

        for pflanze in pflanzen:
            screen.blit(pflanze.surf, pflanze.rect)

        collide_group = pygame.sprite.groupcollide(leben_group, pflanzen,
                                                   False, True)
        for _ in range(len(collide_group)):
            add_pflanze(pflanzen)

        pygame.display.flip()


if __name__ == "__main__":
    main()

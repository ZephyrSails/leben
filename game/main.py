from pflanze import Pflanze
from leben import Leben
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PANEL_HEIGHT = 140

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,
                                      SCREEN_HEIGHT + PANEL_HEIGHT))
    game_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    panel_screen = pygame.Surface((SCREEN_WIDTH, PANEL_HEIGHT))

    running = True

    leben = Leben(game_screen)
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

        pygame.display.flip()


if __name__ == "__main__":
    main()

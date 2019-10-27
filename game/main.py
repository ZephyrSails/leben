from leben import Leben

import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
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

        screen.blit(leben.surf, leben.circle)

        pygame.display.flip()


if __name__ == "__main__":
    main()

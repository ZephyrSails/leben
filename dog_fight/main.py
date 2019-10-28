from flight import Flight
from bullet import Bullet

import pygame
from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT, K_RSHIFT)


def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True

    flight = Flight(SCREEN_WIDTH, SCREEN_HEIGHT)

    bullets = pygame.sprite.Group()

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()
        flight.update(pressed_keys)

        bullets.update()

        if pressed_keys[K_RSHIFT]:
            bullets.add(
                Bullet(flight.x, flight.y, flight.dir_radians, SCREEN_WIDTH,
                       SCREEN_HEIGHT))
            print("fire:", len(bullets))

        screen.fill((0, 0, 0))

        screen.blit(flight.surf, flight.rect)
        for bullet in bullets:
            screen.blit(bullet.surf, bullet.rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()

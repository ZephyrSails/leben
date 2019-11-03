from flight import Flight
from bullet import Bullet

import pygame
from pygame.locals import (K_ESCAPE, KEYDOWN, QUIT, K_UP, K_RSHIFT, K_LEFT,
                           K_RIGHT, K_w, K_a, K_d, K_LSHIFT, K_LCTRL, K_RCTRL)
import random

KEY_SETS = [[K_UP, K_RSHIFT, K_LEFT, K_RIGHT, K_RCTRL],
            [K_w, K_LSHIFT, K_a, K_d, K_LCTRL]]

COLOR_SETS = [(200, 25, 50), (25, 200, 50)]


def main():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True

    flights = pygame.sprite.Group()

    scores = []
    for idx in range(2):
        flights.add(
            Flight(idx, screen, KEY_SETS[idx], COLOR_SETS[idx], flights))
        scores.append(0)

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        pressed_keys = pygame.key.get_pressed()

        screen.fill((0, 0, 0))

        # for flight in flights:
        flights.update(pressed_keys)

        for idx, flight in enumerate(flights):
            hostile_bullets = pygame.sprite.Group()
            for hostile_idx, hostile_flight in enumerate(flights):
                if hostile_idx != idx:
                    hostile_bullets.add(*hostile_flight.bullets)
            flight_group = pygame.sprite.Group([flight])
            collide_group = pygame.sprite.groupcollide(
                flight_group, hostile_bullets, False, True)
            scores[idx] -= len(collide_group)
        print('\r{}'.format(scores), end="")

        pygame.display.flip()


if __name__ == "__main__":
    main()

import pygame
import math
import random


class Panel(pygame.sprite.Sprite):
    def __init__(self, flight):
        super(Panel, self).__init__()
        # identity
        self.flight = flight

        self.width = 80
        self.height = 100
        self.dist = 10 + self.width
        self.surf = pygame.Surface((self.width, self.height))

        self.rect = self.surf.get_rect(
            center=(
                int(self.flight.id * self.dist + self.width // 2),
                int(self.height // 2),
            ))

        pygame.draw.rect(self.surf, self.flight.color,
                         (0, 0, self.width, self.height), 3)

    def update(self):
        pass

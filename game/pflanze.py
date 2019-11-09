import pygame
import random


class Pflanze(pygame.sprite.Sprite):
    def __init__(self, X, Y):
        super(Pflanze, self).__init__()
        self.x = random.randint(0, X)
        self.y = random.randint(0, Y)

        self.radius = random.randint(5, 10)
        self.color = (50, 250, 25)
        self.bg_color = (0, 0, 0)

        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.surf.set_colorkey(self.bg_color)
        self.rect = self.surf.get_rect(center=(
            self.x,
            self.y,
        ))

        pygame.draw.circle(self.surf, self.color, (self.radius, self.radius),
                           self.radius)

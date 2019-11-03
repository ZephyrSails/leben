import pygame
import math


class Contrail(pygame.sprite.Sprite):
    def __init__(self, parent):
        super(Contrail, self).__init__()
        # identity
        self.id = parent.id

        # environment
        self.SCREEN_WIDTH = parent.SCREEN_WIDTH
        self.SCREEN_HEIGHT = parent.SCREEN_HEIGHT

        # pisition
        self.x = parent.x
        self.y = parent.y

        # attribute
        self.init_radius = parent.radius
        self.radius = self.init_radius
        self.bg_color = parent.bg_color
        self.color = pygame.Color(*parent.color)
        self.alpha = self.color.a // 4

        # life span
        self.init_life_tick = parent.contrail_tick
        self.curr_life_tick = self.init_life_tick

        # decays
        self.radius_decay = self.init_radius / self.init_life_tick
        self.alpha_decay = self.alpha / self.init_life_tick

        # pygame
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.surf.set_colorkey(self.bg_color)
        self.rect = self.surf.get_rect(center=(
            int(self.x),
            int(self.y),
        ))

        # draw
        self.draw()

    def draw(self):
        pygame.draw.circle(self.surf, self.color,
                           (self.init_radius, self.init_radius),
                           int(self.radius))

    def update(self):
        self.curr_life_tick -= 1
        if self.curr_life_tick == 0:
            self.kill()

        self.radius -= self.radius_decay
        self.alpha -= self.alpha_decay
        self.surf.set_alpha(int(self.alpha))

        self.surf = pygame.transform.scale(
            self.surf, (int(self.radius * 2), int(self.radius * 2)))
        self.rect = self.surf.get_rect(center=(
            int(self.x),
            int(self.y),
        ))

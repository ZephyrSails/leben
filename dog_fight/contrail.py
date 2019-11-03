import pygame
import math


class Contrail(pygame.sprite.Sprite):
    def __init__(self, flight):
        super(Contrail, self).__init__()
        # identity
        self.id = flight.id

        # environment
        self.SCREEN_WIDTH = flight.SCREEN_WIDTH
        self.SCREEN_HEIGHT = flight.SCREEN_HEIGHT

        # pisition
        self.x = flight.x
        self.y = flight.y

        # attribute
        self.init_radius = flight.radius
        self.radius = self.init_radius
        self.bg_color = flight.bg_color
        self.color = pygame.Color(*flight.color)
        self.alpha = self.color.a // 2

        # life span
        self.init_life_tick = 50
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

    def redraw(self):
        pygame.draw.circle(self.surf, self.bg_color,
                           (self.init_radius, self.init_radius),
                           self.init_radius)
        pygame.draw.circle(self.surf, self.color,
                           (self.init_radius, self.init_radius),
                           int(self.radius))

    def update(self):
        self.curr_life_tick -= 1
        if self.curr_life_tick == 0:
            self.kill()
        self.redraw()
        ratio = self.curr_life_tick / self.init_life_tick

        self.radius -= self.radius_decay
        self.alpha -= self.alpha_decay
        self.surf.set_alpha(int(self.alpha))

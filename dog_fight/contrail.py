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
        self.init_alpha = self.color.a

        # life span
        self.init_life_tick = 20
        self.curr_life_tick = self.init_life_tick

        # pygame
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.rect = self.surf.get_rect(center=(
            int(self.x),
            int(self.y),
        ))

    def redraw(self):
        pygame.draw.circle(self.surf, self.color, (self.radius, self.radius),
                           self.radius)

    def update(self):
        self.curr_life_tick -= 1
        if self.curr_life_tick == 0:
            self.kill()
        self.redraw()
        #
        # ratio = self.curr_life_tick / self.init_life_tick
        #
        # self.color.a = int(self.init_alpha * ratio)
        # self.radius = int(self.init_radius * ratio)
        # print(ratio, self.color, self.radius)

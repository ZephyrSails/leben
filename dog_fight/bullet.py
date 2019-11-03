import pygame
import math
import random


class Bullet(pygame.sprite.Sprite):
    def __init__(self, flight):
        super(Bullet, self).__init__()
        # identity
        self.id = flight.id

        # environment
        self.SCREEN_WIDTH = flight.SCREEN_WIDTH
        self.SCREEN_HEIGHT = flight.SCREEN_HEIGHT

        # motion
        self.speed = 10
        self.radians = math.radians(flight.dir_degree + random.randint(-2, 2))
        self.x_speed = math.cos(self.radians) * self.speed
        self.y_speed = math.sin(self.radians) * self.speed

        # attribute
        self.radius = 2
        self.bg_color = flight.bg_color
        self.color = flight.color
        self.explosion_radius = 5
        self.bound_radius = max(self.explosion_radius, self.radius)

        # pisition
        self.x = flight.x
        self.y = flight.y

        self.surf = pygame.Surface((self.bound_radius * 2,
                                    self.bound_radius * 2))
        self.surf.set_colorkey(self.bg_color)
        self.draw()
        self.rect = self.surf.get_rect(center=(
            int(self.x),
            int(self.y),
        ))

        # life span
        self.life_tick = 200

        # explosion visual
        self.to_be_killed_in_n_turn = -1

    def draw(self):
        pygame.draw.circle(self.surf, self.color,
                           (self.bound_radius, self.bound_radius), self.radius)
        # pygame.draw.circle(self.surf, self.bg_color,
        #                    (self.bound_radius, self.bound_radius), self.radius)
        # pygame.draw.line(
        #     self.surf, self.color,
        #     (int(self.bound_radius - self.radius * math.cos(self.radians)),
        #      int(self.bound_radius - self.radius * math.sin(self.radians))),
        #     (int(self.bound_radius + self.radius * math.cos(self.radians)),
        #      int(self.bound_radius + self.radius * math.sin(self.radians))), 1)

    def update(self):
        if self.to_be_killed_in_n_turn != -1:
            if self.to_be_killed_in_n_turn == 0:
                super(Bullet, self).kill()
                return
            pygame.draw.circle(self.surf, self.color,
                               (self.bound_radius, self.bound_radius),
                               self.explosion_radius)
            self.to_be_killed_in_n_turn -= 1
        else:
            dx = int(self.x + self.x_speed) - int(self.x)
            dy = int(self.y + self.y_speed) - int(self.y)
            self.x += self.x_speed
            self.y += self.y_speed
            self.rect.move_ip(dx, dy)

            if self.rect.left < 0:
                self.x_speed = -self.x_speed
                # self.rect.move_ip(self.SCREEN_WIDTH, 0)
            if self.rect.left > self.SCREEN_WIDTH:
                self.x_speed = -self.x_speed
                # self.rect.move_ip(-self.SCREEN_WIDTH, 0)
            if self.rect.top <= 0:
                self.y_speed = -self.y_speed
                # self.rect.move_ip(0, self.SCREEN_HEIGHT)
            if self.rect.top >= self.SCREEN_HEIGHT:
                self.y_speed = -self.y_speed
                # self.rect.move_ip(0, -self.SCREEN_HEIGHT)

        self.life_tick -= 1
        if self.life_tick == 0:
            super(Bullet, self).kill()

    def blit(self, screen):
        screen.blit(self.surf, self.rect)

    def kill(self):
        self.to_be_killed_in_n_turn = 1

import pygame
import math
from enum import Enum
from pygame.locals import (
    K_ESCAPE,
    K_RSHIFT,
    KEYDOWN,
    QUIT,
)
import random
from bullet import Bullet
from contrail import Contrail


class Flight(pygame.sprite.Sprite):
    def __init__(self, id, screen, keySet, color):
        super(Flight, self).__init__()
        # identity
        self.id = id

        # environment
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()

        # control
        self.kWarp, self.kFire, self.kLeft, self.kRight = keySet

        # motion
        self.speed = 2
        self.warp_speed = self.speed * 3
        self.turn_speed = 3

        # status
        self.hp_cap = 100
        self.hp = 80

        # attribute
        self.color = color
        self.bg_color = (0, 0, 0)
        self.line_color = (1, 1, 1)
        self.radius = 10  # pixel
        self.view_angle = 90  # degree
        self.mouth_degree = 45

        # pisition
        self.x = random.randint(0, self.SCREEN_WIDTH)
        self.y = random.randint(0, self.SCREEN_HEIGHT)

        # pygame
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.surf.set_colorkey(self.bg_color)

        self.rect = self.surf.get_rect(center=(
            int(self.x),
            int(self.y),
        ))
        self.set_direction(0)

        # projectile
        self.bullet_limit = 100
        self.bullet_list = []
        self.bullets = pygame.sprite.Group()

        # decorator
        self.contrails = pygame.sprite.Group()

    def draw_line(self, radians):
        pygame.draw.line(
            self.surf, self.line_color, (int(self.radius), int(self.radius)),
            (int(self.radius + self.radius * math.cos(radians)),
             int(self.radius + self.radius * math.sin(radians))), 2)

    def draw_mouth(self):
        pygame.draw.circle(self.surf, self.color, (self.radius, self.radius),
                           self.radius)
        self.draw_line(self.dir_radians)
        self.draw_line(self.dir_l_radians)
        self.draw_line(self.dir_r_radians)

    def set_direction(self, degree):
        self.dir_degree = degree % 360  # degree, 0~360, 0 is right, 90 is up
        self.dir_radians = math.radians(self.dir_degree)
        self.dir_l_radians = math.radians(degree - self.mouth_degree % 360)
        self.dir_r_radians = math.radians(degree + self.mouth_degree % 360)
        cos = math.cos(self.dir_radians)
        sin = math.sin(self.dir_radians)
        self.x_speed = self.speed * cos
        self.y_speed = self.speed * sin
        self.x_warp_speed = self.warp_speed * cos
        self.y_warp_speed = self.warp_speed * sin
        self.draw_mouth()

    def update(self, pressed_keys):
        # flight motion
        if pressed_keys[self.kWarp]:
            dx = int(self.x + self.x_warp_speed) - int(self.x)
            dy = int(self.y + self.y_warp_speed) - int(self.y)
            self.x += self.x_warp_speed
            self.y += self.y_warp_speed
            self.rect.move_ip(dx, dy)
        if pressed_keys[self.kLeft]:
            self.set_direction(self.dir_degree - self.turn_speed)
        if pressed_keys[self.kRight]:
            self.set_direction(self.dir_degree + self.turn_speed)

        dx = int(self.x + self.x_speed) - int(self.x)
        dy = int(self.y + self.y_speed) - int(self.y)
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.move_ip(dx, dy)

        if self.x < 0:
            self.rect.move_ip(self.SCREEN_WIDTH, 0)
            self.x = self.rect.left + self.radius
        if self.x > self.SCREEN_WIDTH:
            self.rect.move_ip(-self.SCREEN_WIDTH, 0)
            self.x = self.rect.left + self.radius
        if self.y <= 0:
            self.rect.move_ip(0, self.SCREEN_HEIGHT)
            self.y = self.rect.top + self.radius
        if self.y >= self.SCREEN_HEIGHT:
            self.rect.move_ip(0, -self.SCREEN_HEIGHT)
            self.y = self.rect.top + self.radius

        # fire
        if pressed_keys[self.kFire]:
            self.bullet_list.append(Bullet(self))
            self.bullets.add(self.bullet_list[-1])
            if len(self.bullets) > self.bullet_limit:
                oldest_bullet = self.bullet_list.pop(0)
                oldest_bullet.kill()

        self.bullets.update()
        for bullet in self.bullets:
            self.screen.blit(bullet.surf, bullet.rect)

        # contrails
        self.contrails.add(Contrail(self))
        self.contrails.update()
        for contrail in self.contrails:
            self.screen.blit(contrail.surf, contrail.rect)

        self.screen.blit(self.surf, self.rect)

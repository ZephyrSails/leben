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


class Move(Enum):
    W = 0  # warp forward
    F = 1  # fire
    L = 2  # turn left
    R = 3  # turn right


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
        self.radius = 10  # pixel
        self.view_angle = 90  # degree
        self.mouth_degree = 45

        # pisition
        self.x = random.randint(0, self.SCREEN_WIDTH)
        self.y = random.randint(0, self.SCREEN_HEIGHT)
        self.set_direction(0)

        # pygame
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))

        pygame.draw.circle(self.surf, self.color, (self.x, self.y),
                           self.radius)
        self.draw_mouth()

        self.rect = self.surf.get_rect(center=(
            self.x,
            self.y,
        ))

        # projectile
        self.bullet_limit = 100
        self.bullet_list = []
        self.bullets = pygame.sprite.Group()

        # decorator
        self.contrails = pygame.sprite.Group()

    def draw_line(self, radians):
        pygame.draw.line(
            self.surf, self.bg_color, (int(self.radius), int(self.radius)),
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

    def move(self, move):
        if move == Move.W:
            dx = int(self.x + self.x_warp_speed) - int(self.x)
            dy = int(self.y + self.y_warp_speed) - int(self.y)
            self.x += self.x_warp_speed
            self.y += self.y_warp_speed
            self.rect.move_ip(dx, dy)
        if move == Move.L:
            self.set_direction(self.dir_degree - self.turn_speed)
            self.draw_mouth()
        if move == Move.R:
            self.set_direction(self.dir_degree + self.turn_speed)
            self.draw_mouth()
        if move == None:
            dx = int(self.x + self.x_speed) - int(self.x)
            dy = int(self.y + self.y_speed) - int(self.y)
            self.x += self.x_speed
            self.y += self.y_speed
            self.rect.move_ip(dx, dy)

        if self.rect.left < 0:
            self.rect.left += self.SCREEN_WIDTH
        if self.rect.right > self.SCREEN_WIDTH:
            self.rect.right -= self.SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top += self.SCREEN_HEIGHT
        if self.rect.bottom >= self.SCREEN_HEIGHT:
            self.rect.bottom -= self.SCREEN_HEIGHT

    def print(self):
        print("[{:.2f}, {:.2f}, {:.2f}]".format(self.x, self.y,
                                                self.dir_degree))

    def update(self, pressed_keys):
        if pressed_keys[self.kWarp]:
            self.move(Move.W)
        if pressed_keys[self.kFire]:
            self.move(Move.F)
        if pressed_keys[self.kLeft]:
            self.move(Move.L)
        if pressed_keys[self.kRight]:
            self.move(Move.R)
        self.move(None)

        if pressed_keys[self.kFire]:
            self.bullet_list.append(Bullet(self))
            self.bullets.add(self.bullet_list[-1])
            if len(self.bullets) > self.bullet_limit:
                oldest_bullet = self.bullet_list.pop(0)
                oldest_bullet.kill()

        self.bullets.update()
        for bullet in self.bullets:
            self.screen.blit(bullet.surf, bullet.rect)

        self.contrails.add(Contrail(self))
        self.contrails.update()
        for contrail in self.contrails:
            self.screen.blit(contrail.surf, contrail.rect)

        self.screen.blit(self.surf, self.rect)

        # self.print()

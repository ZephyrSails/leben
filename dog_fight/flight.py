import pygame
import math
from enum import Enum
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RSHIFT,
    KEYDOWN,
    QUIT,
)


class Move(Enum):
    W = 0  # warp forward
    F = 1  # fire
    L = 2  # turn left
    R = 3  # turn right


class Flight(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(Flight, self).__init__()
        # environment
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        # motion
        self.speed = 2
        self.warp_speed = self.speed * 3
        self.turn_speed = 3

        # status
        self.hp_cap = 100
        self.hp = 80

        # attribute
        self.radius = 10  # pixel
        self.view_angle = 90  # degree
        self.mouth_degree = 45

        # pisition
        self.x = self.radius
        self.y = self.radius
        self.set_direction(0)

        # pygame
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))

        pygame.draw.circle(self.surf, (255, 255, 255), (self.x, self.y),
                           self.radius)
        self.draw_mouth()

        self.rect = self.surf.get_rect()

    def draw_line(self, radians):
        pygame.draw.line(
            self.surf, (0, 0, 0), (int(self.radius), int(self.radius)),
            (int(self.radius + self.radius * math.cos(radians)),
             int(self.radius + self.radius * math.sin(radians))), 2)

    def draw_mouth(self):
        pygame.draw.circle(self.surf, (255, 255, 255),
                           (self.radius, self.radius), self.radius)
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
        if move == Move.F:
            print('fire')
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
        if pressed_keys[K_UP]:
            self.move(Move.W)
            self.print()
        if pressed_keys[K_RSHIFT]:
            self.move(Move.F)
            self.print()
        if pressed_keys[K_LEFT]:
            self.move(Move.L)
            self.print()
        if pressed_keys[K_RIGHT]:
            self.move(Move.R)
            self.print()
        self.move(None)
        self.print()

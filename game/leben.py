import pygame
import math
from enum import Enum
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Move(Enum):
    F = 0  # move forward
    B = 1  # move backward
    L = 2  # turn left
    R = 3  # turn right


class Leben(pygame.sprite.Sprite):
    def __init__(self):
        super(Leben, self).__init__()
        # motion
        self.speed = 1
        self.turn_speed = 1

        # status
        self.hp_cap = 100
        self.hp = 80

        # attribute
        self.radius = 20  # pixel
        self.view_angle = 90  # degree

        # pisition
        self.x = 0
        self.y = 0
        self.set_dir(0)

        # pygame
        self.surf = pygame.Surface((25, 25))
        self.surf.fill((255, 255, 255))
        self.circle = self.surf.get_rect()
        # self.circle = pygame.draw.circle(self.surf, (255, 255, 255),
        #                                  (self.x, self.y), self.radius)

    def set_dir(self, degree):
        self.dir_degree = degree % 360  # degree, 0~360, 0 is right, 90 is up
        self.dir_radians = math.radians(self.dir_degree)
        self.x_speed = self.speed * math.cos(self.dir_radians)
        self.y_speed = self.speed * math.sin(self.dir_radians)

    def move(self, move):
        if move == Move.F:
            dx = int(self.x + self.x_speed) - int(self.x)
            dy = int(self.y + self.y_speed) - int(self.y)
            self.x += self.x_speed
            self.y += self.y_speed
            self.circle.move_ip(dx, dy)
        if move == Move.B:
            dx = int(self.x - self.x_speed) - int(self.x)
            dy = int(self.y - self.y_speed) - int(self.y)
            self.x -= self.x_speed
            self.y -= self.y_speed
            self.circle.move_ip(dx, dy)
        if move == Move.L:
            self.set_dir(self.dir_degree - self.turn_speed)
        if move == Move.R:
            self.set_dir(self.dir_degree + self.turn_speed)

    def print(self):
        print("[{:.2f}, {:.2f}, {:.2f}]".format(self.x, self.y,
                                                   self.dir_degree))

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.move(Move.F)
            self.print()
        if pressed_keys[K_DOWN]:
            self.move(Move.B)
            self.print()
        if pressed_keys[K_LEFT]:
            self.move(Move.L)
            self.print()
        if pressed_keys[K_RIGHT]:
            self.move(Move.R)
            self.print()

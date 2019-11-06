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
    def __init__(self, screen):
        super(Leben, self).__init__()
        # environment
        self.screen = screen

        # motion
        self.speed = 7
        self.turn_speed = 5

        # status
        self.hp_cap = 100
        self.hp = 80

        # attribute
        self.radius = 20  # pixel
        self.view_angle = 90  # degree
        self.mouth_degree = 45
        self.color = (255, 255, 255)
        self.vision_color = (255, 255, 0)
        self.bg_color = (0, 0, 0)
        self.vision_len = 1000

        # pisition
        self.x_init = self.radius
        self.y_init = self.radius
        self.x = self.x_init
        self.y = self.y_init
        self.set_direction(0)

        # pygame
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.surf.set_colorkey(self.bg_color)
        # self.surf.fill((255, 255, 255))

        pygame.draw.circle(self.surf, self.color, (self.x, self.y),
                           self.radius)
        self.draw_mouth()

        self.rect = self.surf.get_rect()

    def set_direction(self, degree):
        self.dir_degree = degree % 360  # degree, 0~360, 0 is right, 90 is up
        self.dir_radians = math.radians(self.dir_degree)
        self.dir_l_radians = math.radians(degree - self.mouth_degree % 360)
        self.dir_r_radians = math.radians(degree + self.mouth_degree % 360)
        self.x_speed = self.speed * math.cos(self.dir_radians)
        self.y_speed = self.speed * math.sin(self.dir_radians)

    def move(self, move):
        if move == Move.F:
            dx = int(self.x + self.x_speed) - int(self.x)
            dy = int(self.y + self.y_speed) - int(self.y)
            self.x += self.x_speed
            self.y += self.y_speed
            self.rect.move_ip(dx, dy)
        if move == Move.B:
            dx = int(self.x - self.x_speed) - int(self.x)
            dy = int(self.y - self.y_speed) - int(self.y)
            self.x -= self.x_speed
            self.y -= self.y_speed
            self.rect.move_ip(dx, dy)
        if move == Move.L:
            self.set_direction(self.dir_degree - self.turn_speed)
        if move == Move.R:
            self.set_direction(self.dir_degree + self.turn_speed)

    def draw_mouth_line(self, radians):
        pygame.draw.line(
            self.surf, self.bg_color, (int(self.x_init), int(self.y_init)),
            (int(self.x_init + self.radius * math.cos(radians)),
             int(self.y_init + self.radius * math.sin(radians))), 2)

    def draw_mouth(self):
        pygame.draw.circle(self.surf, self.color, (self.x_init, self.y_init),
                           self.radius)
        self.draw_mouth_line(self.dir_radians)
        self.draw_mouth_line(self.dir_l_radians)
        self.draw_mouth_line(self.dir_r_radians)

    def draw_vision(self):
        pygame.draw.line(
            self.screen, self.vision_color, (int(self.x), int(self.y)),
            (int(self.x + self.vision_len * math.cos(self.dir_l_radians)),
             int(self.y + self.vision_len * math.sin(self.dir_l_radians))), 2)
        pygame.draw.line(
            self.screen, self.vision_color, (int(self.x), int(self.y)),
            (int(self.x + self.vision_len * math.cos(self.dir_r_radians)),
             int(self.y + self.vision_len * math.sin(self.dir_r_radians))), 2)

    def print(self):
        print("[{:.2f}, {:.2f}, {:.2f}]".format(self.x, self.y,
                                                self.dir_degree))

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.move(Move.F)
        if pressed_keys[K_DOWN]:
            self.move(Move.B)
        if pressed_keys[K_LEFT]:
            self.move(Move.L)
        if pressed_keys[K_RIGHT]:
            self.move(Move.R)
        self.draw_vision()
        self.draw_mouth()

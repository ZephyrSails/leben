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


def get_periphery_radians(x, y, a, b, r):
    """
    base: (x, y)
    target: (a, b), r
    """
    if x == a and b == y:
        return None, None
    R = math.sqrt((b - y)**2 + (a - x)**2)
    tan = r / R
    radians_delta = math.atan(tan)

    center_radians = math.pi * 1.5 if (a == x) else math.atan(
        (b - y) / (a - x))
    return (center_radians - radians_delta), (center_radians + radians_delta)


def regulate_radians(radians):
    return radians % (2 * math.pi)


def radians_between(radians, left, right):
    left = regulate_radians(left)
    right = regulate_radians(right)
    if right < left:
        right += 2 * math.pi
    radians = regulate_radians(radians)
    radians2 = radians - 2 * math.pi
    radians3 = radians + 2 * math.pi
    assert right > left
    print(left, radians, right)
    return radians < right and radians > left or radians2 < right and radians2 > left or radians3 < right and radians3 > left


class Move(Enum):
    F = 0  # move forward
    B = 1  # move backward
    L = 2  # turn left
    R = 3  # turn right


class Leben(pygame.sprite.Sprite):
    def __init__(self, screen, environment_group):
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

        # environment
        self.environment_group = environment_group

    def set_direction(self, degree):
        self.dir_degree = degree  # degree, 0~360, 0 is right, 90 is up
        self.dir_radians = math.radians(self.dir_degree)
        self.dir_l_radians = math.radians(degree - self.mouth_degree)
        self.dir_r_radians = math.radians(degree + self.mouth_degree)

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
        # while radians < 0:
        #     radians += math.pi
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
        self.draw_vison_line_from_center(self.dir_l_radians)
        self.draw_vison_line_from_center(self.dir_r_radians)

        count = 0
        for obj in self.environment_group:
            l_radians, r_radians = get_periphery_radians(
                self.x, self.y, obj.x, obj.y, obj.radius)
            if l_radians == None:
                continue

            for radians in l_radians, r_radians:
                if radians_between(radians, self.dir_l_radians,
                                   self.dir_r_radians):
                    count += 1
                    self.draw_vison_line_from_center(radians)
        print(count)

    def draw_vison_line_from_center(self, radians):
        pygame.draw.line(
            self.screen, self.vision_color, (int(self.x), int(self.y)),
            (int(self.x + self.vision_len * math.cos(radians)),
             int(self.y + self.vision_len * math.sin(radians))), 2)

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

        self.draw_mouth()
        self.draw_vision()

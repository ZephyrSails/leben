import pygame
import math


class Move(Enum):
    F = 0  # move forward
    B = 1  # move backward
    L = 2  # turn left
    R = 3  # turn right


class Leben(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
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
        pygame.draw.circle(surface, color, center, radius)

    def set_dir(self, degree):
        self.dir_degree = degree % 360  # degree, 0~360, 0 is right, 90 is up
        self.dir_radians = math.radians(self.dir_degree)
        self.x_speed = self.speed * math.cos(angle)
        self.y_speed = self.speed * math.sin(angle)

    def move(self, move):
        if move == Move.F:
            self.x += self.x_speed
            self.y += self.y_speed
        if move == Move.B:
            self.x -= self.x_speed
            self.y -= self.y_speed
        if move == Move.L:
            self.set_dir(self.dir - self.turn_speed)
        if move == Move.R:
            self.set_dir(self.dir + self.turn_speed)

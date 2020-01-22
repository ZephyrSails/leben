import pygame
import math
import random
from enum import Enum
from .helpers.radians_helper import (
    get_periphery_radians,
    regulate_radians,
    radians_between,
)


class Action(Enum):
    F = 0  # move forward
    B = 1  # move backward
    L = 2  # turn left
    R = 3  # turn right


class Leben(pygame.sprite.Sprite):
    def __init__(self, game_screen, vision_screen, environment_group):
        super(Leben, self).__init__()
        # environment
        self.game_screen = game_screen
        self.vision_screen = vision_screen
        self.environment_group = environment_group
        self.objs_in_view = []
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.game_screen.get_size()

        # motion
        self.speed = 7
        self.turn_speed = 2

        # status
        self.id = 0
        self.max_hp = 100
        self.hp = 80
        self.curr_delta = 0  # hp delta, a.k.a reward

        # attribute
        self.radius = 20  # pixel
        self.mouth_degree = 50
        self.view_degree = self.mouth_degree * 2
        self.color = (255, 255, 255)
        self.vision_color = (255, 255, 0)
        self.bg_color = (0, 0, 0)
        self.vision_len = 1000

        # position
        self.x_init = self.radius
        self.y_init = self.radius
        self.x = random.randint(0, self.SCREEN_WIDTH)
        self.y = random.randint(0, self.SCREEN_HEIGHT)
        self.set_direction(random.randint(0, 360))

        # pygame
        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.surf.set_colorkey(self.bg_color)

        pygame.draw.circle(self.surf, self.color, (self.x, self.y),
                           self.radius)
        self.draw_mouth()

        self.rect = self.surf.get_rect(center=(
            int(self.x),
            int(self.y),
        ))

    def set_direction(self, degree):
        self.dir_degree = degree  # degree, 0~360, 0 is right, 90 is up
        self.dir_radians = math.radians(self.dir_degree)
        self.dir_l_radians = math.radians(degree - self.mouth_degree)
        self.dir_r_radians = math.radians(degree + self.mouth_degree)

        self.x_speed = self.speed * math.cos(self.dir_radians)
        self.y_speed = self.speed * math.sin(self.dir_radians)

    def draw_mouth_line(self, radians):
        pygame.draw.line(self.surf, self.bg_color,
                         (int(self.x_init), int(self.y_init)),
                         (int(self.x_init + self.radius * math.cos(radians)),
                          int(self.y_init + self.radius * math.sin(radians))),
                         2)

    def draw_mouth(self):
        pygame.draw.circle(self.surf, self.color, (self.x_init, self.y_init),
                           self.radius)
        self.draw_mouth_line(self.dir_radians)
        self.draw_mouth_line(self.dir_l_radians)
        self.draw_mouth_line(self.dir_r_radians)

    def get_dot_from_center(self, R, radians):
        return (int(self.x + R * math.cos(radians)),
                int(self.y + R * math.sin(radians)))

    def draw_vision(self):
        self.draw_semicircle_from_center(self.vision_len, self.dir_l_radians,
                                         self.dir_r_radians)

        for l_radians, r_radians, _, R in self.objs_in_view:
            self.draw_blind_area_from_center(R, l_radians, r_radians)

    def draw_line_from_center(self, radians):
        pygame.draw.line(self.game_screen, self.vision_color,
                         (int(self.x), int(self.y)),
                         self.get_dot_from_center(self.vision_len, radians), 2)

    def draw_triangle_from_center(self, R, l_radians, r_radians):
        pygame.draw.polygon(self.game_screen, self.vision_color,
                            [(int(self.x), int(self.y)),
                             self.get_dot_from_center(R, l_radians),
                             self.get_dot_from_center(R, r_radians)])

    def draw_semicircle_from_center(self, R, l_radians, r_radians):
        points = [(self.x, self.y)]
        assert (l_radians < r_radians)
        radians = l_radians
        while radians < r_radians:
            points.append(self.get_dot_from_center(R, radians))
            radians += 0.2
        points.append(self.get_dot_from_center(R, r_radians))

        pygame.draw.polygon(self.game_screen, self.vision_color, points)

    def draw_blind_area_from_center(self, R, l_radians, r_radians):
        if l_radians > r_radians:
            r_radians += 2 * math.pi

        assert l_radians < r_radians
        points = [
            self.get_dot_from_center(R, r_radians),
            self.get_dot_from_center(R, l_radians),
        ]
        radians = l_radians

        while radians < r_radians:
            points.append(self.get_dot_from_center(self.vision_len, radians))
            radians += 0.2
        points.append(self.get_dot_from_center(self.vision_len, r_radians))

        pygame.draw.polygon(self.game_screen, self.bg_color, points)

    def print(self):
        print("[{:.2f}, {:.2f}, {:.2f}]".format(self.x, self.y,
                                                self.dir_degree))

    def update_vision(self):
        self.objs_in_view = []
        for obj in self.environment_group:
            l_radians, r_radians, R = get_periphery_radians(
                self.x, self.y, obj.x, obj.y, obj.radius)
            if l_radians == None or r_radians == None:
                continue
            self.dir_l_radians = regulate_radians(self.dir_l_radians)
            self.dir_r_radians = regulate_radians(self.dir_r_radians)
            l_radians = regulate_radians(l_radians)
            r_radians = regulate_radians(r_radians)
            if self.dir_l_radians > self.dir_r_radians:
                if l_radians < self.dir_r_radians or r_radians < self.dir_r_radians:
                    l_radians += 2 * math.pi
                    r_radians += 2 * math.pi
                self.dir_r_radians += 2 * math.pi

            obj_in_vision = False

            for radians in [l_radians, r_radians]:
                if radians_between(radians, self.dir_l_radians,
                                   self.dir_r_radians):
                    obj_in_vision = True
            if obj_in_vision:
                self.objs_in_view.append((l_radians, r_radians, obj.color, R))

            self.objs_in_view.sort(key=lambda p: -p[3])

    def get_1d_vision(self, width):
        radians_width = self.dir_r_radians - self.dir_l_radians

        vision = [self.bg_color] * width

        for l_radians, r_radians, color, R in self.objs_in_view:
            left_idx = 0 if l_radians < self.dir_l_radians else int(
                ((l_radians - self.dir_l_radians) / radians_width) * width)
            right_idx = width if r_radians > self.dir_r_radians else int(
                ((r_radians - self.dir_l_radians) / radians_width) * width)
            vision[left_idx:right_idx] = [color] * (right_idx - left_idx)
        return vision

    def get_1d_vision_binary(self, width):
        vision = self.get_1d_vision(width)
        return [0 if color == (0, 0, 0) else 1 for color in vision]

    def draw_1d_vision(self):
        width, height = self.vision_screen.get_size()
        color_table = self.get_1d_vision(width)
        for idx, color in enumerate(color_table):
            pygame.draw.line(self.vision_screen, color, (idx, 0),
                             (idx, height), 1)

    def update(self, actions):
        x_next = self.x
        y_next = self.y
        if Action.F in actions:
            x_next += self.x_speed
            y_next += self.y_speed
        if Action.B in actions:
            x_next -= self.x_speed
            y_next -= self.y_speed
        x_next = max(0, min(self.SCREEN_WIDTH, x_next))
        y_next = max(0, min(self.SCREEN_HEIGHT, y_next))

        dx = int(x_next) - int(self.x)
        dy = int(y_next) - int(self.y)
        self.x = x_next
        self.y = y_next
        self.rect.move_ip(dx, dy)
        if Action.L in actions:
            self.set_direction(self.dir_degree - self.turn_speed)
        if Action.R in actions:
            self.set_direction(self.dir_degree + self.turn_speed)

        self.update_vision()

        self.draw_mouth()
        self.draw_vision()

        self.draw_1d_vision()

    def update_reward(self, actions, collide_group):
        hp = self.hp - 0.01
        for key in collide_group:
            for pflanze in collide_group[key]:
                hp += pflanze.value
        if len(actions) > 0:
            hp -= 0.1

        hp = min(hp, self.max_hp)

        self.curr_delta = hp - self.hp
        self.hp = hp

    def get_state(self):
        return self.hp, self.curr_delta

    def get_status_str(self):
        return "[{:0.2f}, {:0.2f}] dir: {:0.2f}, hp: {:0.2f}".format(
            self.x, self.y, self.dir_degree, self.hp)

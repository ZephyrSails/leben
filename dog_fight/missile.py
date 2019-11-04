import pygame
import math
from enum import Enum
from contrail import Contrail


class MissileStatus(Enum):
    Tracking = 1,
    Detonated = 2,


class Missile(pygame.sprite.Sprite):
    def __init__(self, flight, degree_delta, targets):
        """
        Input:
            flight: Flight
            degree_delta: Int, direction to shoot out missile
            targets: pygame.sprite.Group
        """
        super(Missile, self).__init__()
        self.flight = flight

        # identity
        self.id = self.flight.id

        # environment
        self.SCREEN_WIDTH = self.flight.SCREEN_WIDTH
        self.SCREEN_HEIGHT = self.flight.SCREEN_HEIGHT

        # motion
        self.max_a = 0.2
        self.curr_a = 0
        self.inc_a = 0.002
        self.max_speed = 5
        self.x_a = 0
        self.y_a = 0
        self.radians = math.radians(self.flight.dir_degree + degree_delta)

        self.x_speed = math.cos(
            self.radians) * self.max_speed / self.flight.speed
        self.y_speed = math.sin(
            self.radians) * self.max_speed / self.flight.speed
        print(self.radians, self.flight.dir_degree)

        # attribute
        self.life_tick = 500
        self.radius = 3
        self.explosion_radius = 7
        self.bound_radius = max(self.explosion_radius, self.radius)
        self.bg_color = self.flight.bg_color
        self.color = self.flight.color

        # position
        self.x = self.flight.x
        self.y = self.flight.y

        self.surf = pygame.Surface((self.bound_radius * 2,
                                    self.bound_radius * 2))
        self.surf.set_colorkey(self.bg_color)
        self.draw()
        self.rect = self.surf.get_rect(center=(
            self.x,
            self.y,
        ))

        # target
        self.targets = targets

        # timing
        self.status = MissileStatus.Tracking
        self.life_tick = 500
        self.detonation_tick = 50

        # decorator
        self.contrail_tick = self.detonation_tick
        self.contrails = pygame.sprite.Group()

    def draw(self):
        pygame.draw.circle(self.surf, self.color,
                           (self.bound_radius, self.bound_radius), self.radius)

    def updateAcceleration(self):

        hostile_targets = filter(lambda target: target.id != self.id,
                                 self.targets)

        min_dist_square = float('inf')
        min_dist_target_direction = None
        min_dist_target = None

        for hostile_target in hostile_targets:
            d_x = hostile_target.x - self.x
            d_y = hostile_target.y - self.y

            curr_dist_square = (d_x)**2 + (d_y)**2
            if curr_dist_square < min_dist_square:
                min_dist_square = curr_dist_square
                min_dist_target_direction = (d_x, d_y)
                min_dist_target = hostile_target

        if hostile_target == None:
            return None

        min_dist = math.sqrt(min_dist_square)
        d_x, d_y = min_dist_target_direction

        if self.curr_a < self.max_a:
            self.curr_a += self.inc_a

        self.x_a = d_x * self.curr_a / min_dist
        self.y_a = d_y * self.curr_a / min_dist
        return min_dist_target

    def detonate(self):
        self.status = MissileStatus.Detonated
        pygame.draw.circle(self.surf, self.color,
                           (self.bound_radius, self.bound_radius),
                           self.explosion_radius)

    def update(self):
        if self.status == MissileStatus.Tracking:
            min_dist_target = self.updateAcceleration()
            if min_dist_target == None:
                return
            self.x_speed += self.x_a
            self.y_speed += self.y_a

            mag_speed = math.sqrt(((self.x_speed)**2 + (self.y_speed)**2))
            if mag_speed > self.max_speed:
                self.x_speed *= self.max_speed / mag_speed
                self.y_speed *= self.max_speed / mag_speed

            dx = int(self.x + self.x_speed) - int(self.x)
            dy = int(self.y + self.y_speed) - int(self.y)

            self.x += self.x_speed
            self.y += self.y_speed
            self.rect.move_ip(dx, dy)

            self.life_tick -= 1
            if self.life_tick == 0 or pygame.sprite.collide_circle(
                    self, min_dist_target):
                self.detonate()

            # contrails
            self.contrails.add(Contrail(self))
            self.flight.update_and_blits(self.contrails)
        if self.status == MissileStatus.Detonated:
            self.detonation_tick -= 1
            if self.detonation_tick == 0:
                self.kill()

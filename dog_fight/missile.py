import pygame
import math


class Missile(pygame.sprite.Sprite):
    def __init__(self, flight, degree_delta, targets):
        """
        Input:
            flight: Flight
            degree_delta: Int, direction to shoot out missile
            targets: pygame.sprite.Group
        """
        super(Missile, self).__init__()
        # identity
        self.id = flight.id

        # environment
        self.SCREEN_WIDTH = flight.SCREEN_WIDTH
        self.SCREEN_HEIGHT = flight.SCREEN_HEIGHT

        # motion
        self.max_a = 0.1
        self.curr_a = 0
        self.inc_a = 0.0001
        self.max_speed = 4
        self.x_a = 0
        self.y_a = 0
        self.radians = math.radians(flight.dir_degree + degree_delta)
        self.x_speed = math.cos(
            self.radians) * flight.x_speed * self.max_speed / flight.speed
        self.y_speed = math.sin(
            self.radians) * flight.y_speed * self.max_speed / flight.speed

        # attribute
        self.life_tick = 500
        self.radius = 3
        self.bg_color = flight.bg_color
        self.color = flight.color

        # position
        self.x = flight.x
        self.y = flight.y

        self.surf = pygame.Surface((self.radius * 2, self.radius * 2))
        self.redraw()
        self.rect = self.surf.get_rect(center=(
            self.x,
            self.y,
        ))

        # target
        self.targets = targets

        # timing
        self.life_tick = 500

    def redraw(self):
        pygame.draw.circle(self.surf, self.color, (self.radius, self.radius),
                           self.radius)

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

    def update(self):
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

import pygame
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, radians, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(Bullet, self).__init__()
        # environment
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        # motion
        self.speed_multiplier = 4
        self.radians = radians
        self.x_speed = math.cos(radians) * self.speed_multiplier
        self.y_speed = math.sin(radians) * self.speed_multiplier

        # attribute
        self.len = 2
        self.bg_color = (255, 255, 255)
        self.color = (0, 0, 0)

        # pisition
        self.x = x
        self.y = y

        self.surf = pygame.Surface((self.len * 2, self.len * 2))
        self.redraw()
        self.rect = self.surf.get_rect(center=(
            self.x,
            self.y,
        ))

    def redraw(self):
        pygame.draw.circle(self.surf, self.bg_color, (self.len, self.len),
                           self.len)
        pygame.draw.line(self.surf, self.color,
                         (int(self.len - self.len * math.cos(self.radians)),
                          int(self.len - self.len * math.sin(self.radians))),
                         (int(self.len + self.len * math.cos(self.radians)),
                          int(self.len + self.len * math.sin(self.radians))),
                         1)

    def update(self):
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
        # self.redraw()

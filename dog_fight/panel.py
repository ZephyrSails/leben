import pygame
import math
import random


class Panel(pygame.sprite.Sprite):
    def __init__(self, flight, height):
        super(Panel, self).__init__()
        # identity
        self.flight = flight

        self.width = 200
        self.height = height
        self.dist = 10 + self.width
        self.surf = pygame.Surface((self.width, self.height))

        self.rect = self.surf.get_rect(
            center=(
                int(self.flight.id * self.dist + self.width // 2),
                int(self.height // 2),
            ))

        self.line_width = 2
        pygame.draw.rect(self.surf, self.flight.color,
                         (0, 0, self.width, self.height), self.line_width)

        # panel title
        font = pygame.font.Font('freesansbold.ttf', 20)
        text_surf = font.render('Player {}'.format(self.flight.id), True,
                                self.flight.bg_color, self.flight.color)
        text_rect = text_surf.get_rect()
        text_rect.move_ip(self.line_width, self.line_width)
        self.surf.blit(text_surf, text_rect)

        self.titel_height = text_rect.height + self.line_width * 2
        self.bar_height = 26

        self.text_width = 0

        texts = ["HP", "BL", "MS"]
        for idx, text in enumerate(texts):
            text_surf = font.render(text, True, self.flight.color,
                                    self.flight.bg_color)
            text_rect = text_surf.get_rect()
            text_rect.move_ip(self.line_width,
                              self.titel_height + idx * self.bar_height)
            self.text_width = max(self.text_width,
                                  text_rect.width + self.line_width * 4)
            self.surf.blit(text_surf, text_rect)

        self.bar_width = self.width - self.text_width - self.line_width

    def update(self):
        for idx, (curr_val, max_val) in enumerate(
            [[self.flight.hp, self.flight.max_hp],
             [
                 self.flight.bullet_limit - len(self.flight.bullets),
                 self.flight.bullet_limit
             ],
             [
                 len(self.flight.missiles_range) - len(self.flight.missiles),
                 len(self.flight.missiles_range)
             ]]):

            bar_width = int(self.bar_width * curr_val / max_val)

            pygame.draw.rect(
                self.surf, self.flight.bg_color,
                (self.text_width, self.titel_height + idx * self.bar_height,
                 self.bar_width, self.bar_height))

            pygame.draw.rect(
                self.surf, self.flight.color,
                (self.text_width, self.titel_height + idx * self.bar_height,
                 self.bar_width, self.bar_height), self.line_width)

            pygame.draw.rect(
                self.surf, self.flight.color,
                (self.text_width, self.titel_height + idx * self.bar_height,
                 bar_width, self.bar_height))

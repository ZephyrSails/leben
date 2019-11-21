import pygame
import math
import random


class Panel(pygame.sprite.Sprite):
    def __init__(self, leben, height):
        super(Panel, self).__init__()
        # identity
        self.leben = leben

        self.width = 200
        self.height = height
        self.dist = 10 + self.width
        self.surf = pygame.Surface((self.width, self.height))

        self.rect = self.surf.get_rect(
            center=(
                int(self.leben.id * self.dist + self.width // 2),
                int(self.height // 2),
            ))

        self.line_width = 2
        pygame.draw.rect(self.surf, self.leben.color,
                         (0, 0, self.width, self.height), self.line_width)

        # panel title
        font = pygame.font.Font('freesansbold.ttf', 20)
        text_surf = font.render('Player {}'.format(self.leben.id), True,
                                self.leben.bg_color, self.leben.color)
        text_rect = text_surf.get_rect()
        text_rect.move_ip(self.line_width, self.line_width)
        self.surf.blit(text_surf, text_rect)

        self.titel_height = text_rect.height + self.line_width * 2
        self.bar_height = 26

        self.text_width = 0

        texts = ["HP"]
        for idx, text in enumerate(texts):
            text_surf = font.render(text, True, self.leben.color,
                                    self.leben.bg_color)
            text_rect = text_surf.get_rect()
            text_rect.move_ip(self.line_width,
                              self.titel_height + idx * self.bar_height)
            self.text_width = max(self.text_width,
                                  text_rect.width + self.line_width * 4)
            self.surf.blit(text_surf, text_rect)

        self.bar_width = self.width - self.text_width - self.line_width

    def update(self):
        for idx, (curr_val,
                  max_val) in enumerate([[self.leben.hp, self.leben.max_hp]]):

            bar_width = int(self.bar_width * curr_val / max_val)

            pygame.draw.rect(
                self.surf, self.leben.bg_color,
                (self.text_width, self.titel_height + idx * self.bar_height,
                 self.bar_width, self.bar_height))

            pygame.draw.rect(
                self.surf, self.leben.color,
                (self.text_width, self.titel_height + idx * self.bar_height,
                 self.bar_width, self.bar_height), self.line_width)

            pygame.draw.rect(
                self.surf, self.leben.color,
                (self.text_width, self.titel_height + idx * self.bar_height,
                 bar_width, self.bar_height))

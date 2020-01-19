from .pflanze import Pflanze
from .panel import Panel
from .leben import Leben, Action
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Game:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.VISION_HEIGHT = 140
        self.PANEL_HEIGHT = 140

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH,
             self.SCREEN_HEIGHT + self.VISION_HEIGHT + self.PANEL_HEIGHT))
        self.game_screen = pygame.Surface((self.SCREEN_WIDTH,
                                           self.SCREEN_HEIGHT))
        self.vision_screen = pygame.Surface((self.SCREEN_WIDTH,
                                             self.VISION_HEIGHT))
        self.panel_screen = pygame.Surface((self.SCREEN_WIDTH,
                                            self.PANEL_HEIGHT))
        self.running = True

        self.pflanzen = pygame.sprite.Group()
        self.panels = pygame.sprite.Group()
        self.leben_group = pygame.sprite.Group()

        self.leben = Leben(self.game_screen, self.vision_screen, self.pflanzen)
        self.leben_group.add(self.leben)

        self.bg_color = (0, 0, 0)

        self.panels.add(Panel(self.leben, self.PANEL_HEIGHT))

        for _ in range(32):
            self._add_pflanze()

    def _add_pflanze(self):
        self.pflanzen.add(Pflanze(self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def update(self, actions):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        self.game_screen.fill(self.bg_color)
        self.panel_screen.fill(self.bg_color)
        self.leben.update(actions)

        self.game_screen.blit(self.leben.surf, self.leben.rect)

        for pflanze in self.pflanzen:
            self.game_screen.blit(pflanze.surf, pflanze.rect)

        collide_group = pygame.sprite.groupcollide(self.leben_group,
                                                   self.pflanzen, False, True)
        self.leben.update_reward(actions, collide_group)
        for _ in range(len(collide_group)):
            self._add_pflanze()

        self.panels.update()
        for panel in self.panels:
            self.panel_screen.blit(panel.surf, panel.rect)

        self.screen.blit(self.game_screen, (0, 0))
        self.screen.blit(self.vision_screen, (0, self.SCREEN_HEIGHT))
        self.screen.blit(self.panel_screen,
                         (0, self.SCREEN_HEIGHT + self.VISION_HEIGHT))

        pygame.display.flip()

    def get_1d_vision_binary(self, width):
        return self.leben.get_1d_vision_binary(width)

    def get_1d_vision(self, width):
        return self.leben.get_1d_vision(width)

    def get_state(self):
        return self.leben.get_state()

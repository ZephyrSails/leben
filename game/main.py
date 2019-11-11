from pflanze import Pflanze
from leben import Leben, Action
from vision import Vision
import pygame
from pygame.locals import (
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class Game:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.VISION_HEIGHT = 140

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT + self.VISION_HEIGHT))
        self.game_screen = pygame.Surface((self.SCREEN_WIDTH,
                                           self.SCREEN_HEIGHT))
        self.vision_screen = pygame.Surface((self.SCREEN_WIDTH,
                                             self.VISION_HEIGHT))
        self.running = True

        self.pflanzen = pygame.sprite.Group()

        self.leben = Leben(self.game_screen, self.vision_screen, self.pflanzen)
        self.leben_group = pygame.sprite.Group()
        self.leben_group.add(self.leben)

        for _ in range(32):
            self.add_pflanze()

    def add_pflanze(self):
        self.pflanzen.add(Pflanze(self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def update(self, actions):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False

        self.game_screen.fill((0, 0, 0))
        self.leben.update(actions)

        self.game_screen.blit(self.leben.surf, self.leben.rect)

        for pflanze in self.pflanzen:
            self.game_screen.blit(pflanze.surf, pflanze.rect)

        collide_group = pygame.sprite.groupcollide(self.leben_group,
                                                   self.pflanzen, False, True)
        for _ in range(len(collide_group)):
            self.add_pflanze()

        self.screen.blit(self.game_screen, (0, 0))
        self.screen.blit(self.vision_screen, (0, self.SCREEN_HEIGHT))

        pygame.display.flip()


def pressed_keys_to_actions():
    moves = set([])
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[K_UP]:
        moves.add(Action.F)
    if pressed_keys[K_DOWN]:
        moves.add(Action.B)
    if pressed_keys[K_LEFT]:
        moves.add(Action.L)
    if pressed_keys[K_RIGHT]:
        moves.add(Action.R)
    return moves


def main():
    game = Game()
    while game.running:
        game.update(pressed_keys_to_actions())


if __name__ == "__main__":
    main()

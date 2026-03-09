import pygame
from assets import Assets

class Entity:
    def __init__(self, game, width, height):
        self.game = game
        self.rect = pygame.Rect(game.level.startPosition[0], game.level.startPosition[1], width, height)
        self.frames = []
        self.frame = 0
        self.animTimer = 0
        self.animNext = ""
        self.dead = False
    
    @property
    def x(self):
        return self.rect.centerx

    @property
    def y(self):
        return self.rect.bottom

    def update(self):
        pass

    def draw(self):
        pass

    def set_animation(self, name, next=""):
        self.frames = Assets.animations[f"lemming_{name}"]
        self.animNext = next
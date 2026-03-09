import pygame
from assets import Assets

class Entity:
    def __init__(self, game, width, height):
        self.game = game
        self.rect = pygame.Rect(game.level.start_position[0], game.level.start_position[1], width, height)
        self.frames = []
        self.frame = 0
        self.anim_timer = 0
        self.anim_next = ""
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
        self.anim_next = next
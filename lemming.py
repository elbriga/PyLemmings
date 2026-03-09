import pygame
from assets import Assets
from entity import Entity
from lemmingState import Walker

class Lemming(Entity):
    def __init__(self, game, **kwargs):
        Entity.__init__(self, game, 40, 80)
        self.x = game.level.start_position[0]
        self.y = game.level.start_position[1]
        self.state = Walker(self)
        self.direction = 1
        self.climbheight = 4
        self.falling = 0
        self.selected = False

    def draw(self):
        frame = self.frames[self.frame % len(self.frames)]
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        self.game.screen.blit(frame, (self.x - self.width / 2, self.y - self.height))
        pygame.draw.circle(self.game.screen, (255, 0, 0), (int(self.x), int(self.y)), 5)

    def update(self):
        self.state.update()

    def isNear(self, pos, range):
        return self.x > pos[0] - range and self.x < pos[0] + range and self.y > pos[1] - range and self.y < pos[1] + range

    def setAnimation(self, name):
        self.frames = Assets.animations[f"lemming_{name}"]
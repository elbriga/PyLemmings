import pygame
from entity import Entity
from lemmingState import LemmingState

class Lemming(Entity):
    def __init__(self, game, **kwargs):
        Entity.__init__(self, game, 40, 80)
        self.stateName = ""
        self.direction = 1
        self.climbheight = 4
        self.falling = 0
        self.hasUmbrella = False
        self.set_state("Andando")

    def draw(self):
        frame = self.frames[self.frame % len(self.frames)]
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        self.game.screen.blit(frame, self.rect)
        if self.hasUmbrella and self.stateName == "Andando":
            pygame.draw.circle(self.game.screen, (255, 255, 0), (self.x, self.y), 5)
        if self.game.debug:
            pygame.draw.circle(self.game.screen, (255, 0, 0), (self.rect.right, self.rect.bottom + 1), 5)
            pygame.draw.circle(self.game.screen, (255, 255, 0), (self.rect.left, self.rect.bottom + 1), 5)

    def update(self):
        self.state.update()

    def is_near(self, pos, distance):
        area = pygame.Rect(pos[0] - distance, pos[1] - distance, distance * 2, distance * 2)
        return self.rect.colliderect(area)
    
    def is_on_floor(self):
        bottomleft = self.game.level.ground_at_position((self.rect.left, self.rect.bottom + 1))
        if not bottomleft:
            bottomright = self.game.level.ground_at_position((self.rect.right, self.rect.bottom + 1))
            if not bottomright:
                return False
        return True
    
    def floor_height_in_front(self):
        height = 0
        # find the height of the ground in front of a lemming up to the maximum height a lemming can climb
        while height <= self.climbheight:
            # the pixel 'in front' of a lemming will depend on the direction it's traveling
            if self.direction == 1:
                positioninfront = (self.rect.right, self.rect.bottom - height)
            else:
                positioninfront = (self.rect.left, self.rect.bottom - height)
            if not self.game.level.ground_at_position(positioninfront):
                break

            height += 1

        return height

    def set_state(self, stateName):
        self.stateName = stateName
        self.state = LemmingState.states[stateName](self)
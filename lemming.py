import pygame
from assets import Assets
from entity import Entity

class Lemming(Entity):
    def __init__(self, game, **kwargs):
        Entity.__init__(self, game, 40, 80)
        self.frames = Assets.animations["lemming_walk"]
        self.x = game.level.start_position[0]
        self.y = game.level.start_position[1]
        self.selected = False
        self.direction = 1
        self.climbheight = 4
        self.falling = 0

    def isNear(self, pos, range):
        return self.x > pos[0] - range and self.x < pos[0] + range and self.y > pos[1] - range and self.y < pos[1] + range
    
    def draw(self):
        frame = self.frames[self.frame % len(self.frames)]
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        self.game.screen.blit(frame, (self.x - self.width / 2, self.y - self.height))
        #pygame.draw.circle(screen.surface, (255, 0, 0), (int(self.x), int(self.y)), 5)

    # update a lemming's position in the level
    def update(self):
        # if there's no ground below a lemming (check both corners), it is falling
        bottomleft = self.game.level.groundatposition((self.x - self.width / 2, self.y + 1))
        bottomright = self.game.level.groundatposition((self.x + self.width / 2, self.y + 1))
        if not bottomleft and not bottomright:
            self.falling += 1
            if self.falling > 3:
                self.frames = Assets.animations["lemming_fall"]
            self.y += 1
        # if not falling, a lemming is walking
        else:
            if self.falling > 200:
                # Die!
                if not self.dead:
                    self.frames = Assets.animations["lemming_die"]
                    self.frame = 0
                    self.dead = True
            else:
                self.frames = Assets.animations["lemming_walk"]
                self.falling = 0
                height = 0
                found = False
                # find the height of the ground in front of a lemming
                # up to the maximum height a lemming can climb
                while (found == False) and (height <= self.climbheight):
                    # the pixel 'in front' of a lemming will depend on
                    # the direction it's traveling
                    if self.direction == 1:
                        positioninfront = (self.x + self.width / 2, self.y - height)
                    else:
                        positioninfront = (self.x - self.width / 2, self.y - height)
                    if not self.game.level.groundatposition(positioninfront):
                        self.x += self.direction
                        # rise up to new ground level
                        self.y -= height
                        found = True

                    height += 1
                # turn the lemming around if the ground in front
                # is too high to climb
                if not found:
                    self.direction *= -1
                
                if self.isNear(self.game.level.end_position, 15):
                    self.game.lemmings.remove(self)
                    self.game.points += 1
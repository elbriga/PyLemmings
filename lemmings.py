#!/usr/bin/env python3
import pygame
from time import sleep
from PIL import Image

from assets import Assets
from entity import Entity

# screen size
HEIGHT=800
WIDTH=800

class Level:
    def __init__(self, image):
        self.max_lemmings = 10
        self.start_position = (100,100)
        self.end_position = (580,710)
        self.background_colour = (114,114,201,255)
        self.surface = pygame.image.load(f'images/{image}.png').convert()
        self.surface.set_colorkey(self.background_colour)
        self.ground_mask = pygame.mask.from_surface(self.surface)
        
    # returns 'True' if the pixel specified is 'ground'
    # (i.e. anything except BACKGROUND_COLOUR)
    def groundatposition(self, pos):
        try:
            return self.ground_mask.get_at((int(pos[0]), int(pos[1])))
        except IndexError:
            return False

class Game:
    def __init__(self, level):
        self.entities = []
        self.points = 0
        self.add_timer = 0
        self.add_interval = 10
        self.add_done = False
        self.level = level
        Assets.load()
    
    def update(self):
        if not self.add_done:
            if len(self.entities) < self.level.max_lemmings:
                # increment the timer and create a new
                # lemming if the interval has passed
                self.add_timer += 0.1
                if self.add_timer > self.add_interval:
                    self.add_timer = 0
                    self.entities.append(Lemming(self))
            else:
                self.add_done = True

        # update each entity's in the level
        for e in self.entities[:]:
            e.update()
            e.anim_timer += 1
            if e.anim_timer > 3:
                e.anim_timer = 0
                e.frame = (e.frame + 1) % len(e.frames)
                if e.dead and e.frame == 0:
                    self.entities.remove(e)

    def draw(self):
        # draw the level
        screen.blit(self.level.surface,(0,0))
        # draw entities
        for e in self.entities:
            e.draw()
        # draw score
        font = pygame.font.SysFont(None, 40)
        text = font.render(f"Pontos: {self.points} / {len(self.entities)}", True, (255,255,255))
        screen.blit(text, (10,10))

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
        screen.blit(frame, (self.x - self.width / 2, self.y - self.height))
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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyLemmings")

jogo = Game(Level('level'))

clock = pygame.time.Clock()

jogo = Game(Level('level'))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    jogo.update()

    screen.fill((0,0,0))
    jogo.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


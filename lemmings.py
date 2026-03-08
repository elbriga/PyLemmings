#!/usr/bin/env python3
import pgzrun
import pygame
from time import sleep
from PIL import Image

from assets import Assets

# screen size
HEIGHT=800
WIDTH=800

class Level:
    def __init__(self, image):
        self.max_lemmings = 10
        self.image = image
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
        self.lemmings = []
        self.points = 0
        self.add_timer = 0
        self.add_interval = 10
        self.add_done = False
        self.level = level
        Assets.load()
    
    def update(self):
        if not self.add_done:
            if len(self.lemmings) < self.level.max_lemmings:
                # increment the timer and create a new
                # lemming if the interval has passed
                self.add_timer += 0.1
                if self.add_timer > self.add_interval:
                    self.add_timer = 0
                    self.lemmings.append(Lemming(self))
            else:
                self.add_done = True
        # update each lemming's position in the level
        for lem in self.lemmings[:]:
            lem.update()

    def draw(self):
        screen.clear()
        # draw the level
        screen.blit(self.level.image,(0,0))
        # draw lemmings
        for lem in self.lemmings:
            lem.draw()
        # draw score
        screen.draw.text(f"Points: {self.points}", (10, 10), color="white", fontsize=40)

class Lemming():
    def __init__(self, game, **kwargs):
        self.game = game
        self.x = game.level.start_position[0]
        self.y = game.level.start_position[1]
        self.direction = 1
        self.climbheight = 4
        self.width = 20
        self.height = 40
        self.frames = Assets.animations["lemming_walk"]
        self.frame = 0
        self.anim_timer = 0

    def isNear(self, pos, range):
        return self.x > pos[0] - range and self.x < pos[0] + range and self.y > pos[1] - range and self.y < pos[1] + range
    
    def draw(self):
        frame = self.frames[self.frame]
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, (self.x, self.y))

    # update a lemming's position in the level
    def update(self):
        self.anim_timer += 1
        if self.anim_timer > 3:
            self.anim_timer = 0
            self.frame = (self.frame + 1) % len(self.frames)
        
        # if there's no ground below a lemming (check both corners), it is falling
        bottomleft = self.game.level.groundatposition((self.x, self.y + self.height))
        bottomright = self.game.level.groundatposition((self.x + (self.width - 1), self.y + self.height))
        if not bottomleft and not bottomright:
            self.y += 1
        # if not falling, a lemming is walking
        else:
            height = 0
            found = False
            # find the height of the ground in front of a lemming
            # up to the maximum height a lemming can climb
            while (found == False) and (height <= self.climbheight):
                # the pixel 'in front' of a lemming will depend on
                # the direction it's traveling
                if self.direction == 1:
                    positioninfront = (self.x + self.width, self.y + (self.height - 1) - height)
                else:
                    positioninfront = (self.x - 1, self.y + (self.height - 1) - height)
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

jogo = Game(Level('level'))
def update():
    jogo.update()
def draw():
    jogo.draw()
pgzrun.go()

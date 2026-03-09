import pygame
from assets import Assets
from lemming import Lemming

class Game:
    def __init__(self, screen, level):
        self.screen = screen
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
            if not e.dead:
                e.update()

            e.anim_timer += 1
            if e.anim_timer > 3:
                e.anim_timer = 0
                e.frame = (e.frame + 1) % len(e.frames)
                if e.dead and e.frame == 0:
                    self.entities.remove(e)

    def draw(self):
        # draw the level
        self.screen.blit(self.level.surface,(0,0))
        # draw entities
        for e in self.entities:
            e.draw()
        # draw score
        font = pygame.font.SysFont(None, 40)
        text = font.render(f"Pontos: {self.points} / {len(self.entities)}", True, (255,255,255))
        self.screen.blit(text, (10,10))
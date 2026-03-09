import pygame
from assets import Assets
from lemming import Lemming

class Game:
    def __init__(self, screen, level):
        self.screen = screen
        self.entities = []
        self.level = level
        self.points = 0
        self.totLemmings = 0
        self.addTimer = 0
        self.addInterval = 10
        self.paused = False
        self.hovered = None
        self.debug = True
        Assets.load()
    
    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.hovered = self.get_lemming_near((mx, my))

        if self.paused:
            return
        
        if self.totLemmings < self.level.numLemmings:
            # increment the timer and create a new
            # lemming if the interval has passed
            self.addTimer += 0.1
            if self.addTimer > self.addInterval:
                self.addTimer = 0
                self.totLemmings += 1
                self.entities.append(Lemming(self))

        # update each entity's in the level
        for e in self.entities[:]:
            if not e.dead:
                e.update()
                # Checar pela saida
                if isinstance(e, Lemming):
                    if e.is_near(self.level.endPosition, 15):
                        self.points += 1
                        e.dead = True
                        e.frame = -1 # Remover agora

            e.animTimer += 1
            if e.animTimer > 3:
                e.animTimer = 0
                e.frame = (e.frame + 1) % len(e.frames)
                if e.frame == 0:
                    if e.dead:
                        self.entities.remove(e)
                    elif e.animNext != "":
                        e.set_animation(e.animNext)
                        e.animNext = ""

    def draw(self):
        # draw the level
        self.screen.blit(self.level.surface,(0,0))
        # draw entities
        for e in self.entities:
            e.draw()
        # desenhar o selecionado
        if self.hovered:
            pygame.draw.circle(self.screen, (0,255,0), (self.hovered.x, self.hovered.y - self.hovered.rect.height // 4), 25, 3)
        # draw score
        font = pygame.font.SysFont(None, 40)
        text = font.render(f"Pontos: {self.points} / {self.level.numLemmings}", True, (255,255,255))
        self.screen.blit(text, (10,10))
    
    def get_lemming_near(self, pos, radius=80):
        best = None
        mx, my = pos
        best_dist = radius * radius

        for lem in self.entities:
            if not isinstance(lem, Lemming):
                continue
            if lem.dead:
                continue

            dx = lem.x - mx
            dy = lem.y - my

            dist = dx * dx + dy * dy
            if dist < best_dist:
                best = lem
                best_dist = dist

        return best

    def get_blocker(self, rect):
        for e in self.entities:
            if isinstance(e, Lemming) and e.stateName == "Parado":
                block_area = e.rect.inflate(20, 10)

                if rect.colliderect(block_area):
                    return e

        return None
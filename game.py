import pygame
from assets import Assets
from lemming import Lemming
from level import Level
class Game:
    def __init__(self, screen, levelName):
        self.screen = screen
        self.entities = []
        self.level = Level(levelName)
        self.points = 0
        self.totLemmings = 0
        self.minHeightToDie = 200
        self.addTimer = 0
        self.addInterval = 10
        self.paused = False
        self.hovered = None
        self.debug = True
        self.scoreFont = pygame.font.SysFont(None, 40)
        self.blockerShape = pygame.mask.Mask((40, 44), True)
        Assets.load()
    
    @property
    def lemmings(self):
        return (e for e in self.entities if isinstance(e, Lemming) and not e.dead)
    
    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.hovered = self.get_lemming_near((mx, my))

        if self.paused:
            return
        
        if self.totLemmings < self.level.numLemmings:
            self.addTimer += 0.1
            # Add lemming se o intervalo passou
            if self.addTimer > self.addInterval:
                self.addTimer = 0
                self.totLemmings += 1
                self.entities.append(Lemming(self))

        # Atualizar as entidades
        for e in self.entities[:]:
            if not e.dead:
                e.update()
                # Checar pela saida
                if isinstance(e, Lemming):
                    if e.is_near(self.level.endPosition, 15):
                        self.points += 1
                        e.dead = True
                        e.frame = -1 # Remover agora

            # Animacao
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
        # Desenhar o level
        self.screen.blit(self.level.surface,(0,0))
        # Desenhar as entidades
        for e in self.entities:
            e.draw()
        # Desenhar o selecionado
        if self.hovered:
            pygame.draw.circle(self.screen, (0,255,0), (self.hovered.x, self.hovered.y - self.hovered.rect.height // 4), 25, 3)
        # Desenhar o score
        text = self.scoreFont.render(f"Pontos: {self.points} / {self.level.numLemmingsToSave}", True, (255,255,255))
        self.screen.blit(text, (10,10))
    
    def get_lemming_near(self, pos, radius=80):
        best = None
        mx, my = pos
        best_dist = radius * radius
        for lem in self.lemmings:
            dx = lem.x - mx
            dy = lem.y - my
            dist = dx * dx + dy * dy
            if dist < best_dist:
                best = lem
                best_dist = dist
        return best
    
    def buildBlockerMask(self):
        self.level.blockerMask.clear()
        for lem in self.lemmings:
            if lem.stateName == "Parado":
                self.level.blockerMask.draw(self.blockerShape, (lem.rect.x, lem.rect.centery))
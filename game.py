import pygame
from assets import Assets
from lemming import Lemming
from level import Level

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True  # Controla o loop principal
        self.quitting = False
        self.entities = []
        self.level = Level(1)
        self.points = 0
        self.totLemmings = 0
        self.selectedSkill = ""
        self.minHeightToDie = 200
        self.addTimer = 0
        self.paused = False
        self.showMask = False
        self.hovered = None
        self.debug = False
        self.scoreFont = pygame.font.SysFont(None, 40)
        self.skillsFont = pygame.font.SysFont(None, 30)
        Assets.load()
    
    @property
    def lemmings(self):
        return (e for e in self.entities if isinstance(e, Lemming) and not e.dead)

    def quit(self):
        self.armaggedon(True)

    def armaggedon(self, quit=False):
        if quit:
            self.quitting = True
        for l in self.lemmings:
            l.set_state("Exploder")
    
    def update(self):
        mx, my = pygame.mouse.get_pos()
        self.hovered = self.get_lemming_near((mx, my))

        if self.paused:
            return
        
        if self.totLemmings < self.level.config.numLemmings and not self.quitting:
            self.addTimer += 0.1
            # Add lemming se o intervalo passou
            if self.addTimer > self.level.config.releaseRate:
                self.addTimer = 0
                self.totLemmings += 1
                self.entities.append(Lemming(self))

        # Atualizar as entidades
        for e in self.entities[:]:
            if not e.dead:
                e.update()
                # Checar pela saida
                if isinstance(e, Lemming):
                    if e.is_near(self.level.config.endPosition, 15):
                        self.points += 1
                        e.die("gone")

            # Animacao
            e.animTimer += 1
            if e.animTimer > 3:
                e.animTimer = 0
                e.frame = (e.frame + 1) % len(e.frames)
                if e.frame == 0 and isinstance(e, Lemming):
                    e.on_cycle_anim()
                    if e.animNext != "":
                        e.on_change_anim()
                        e.set_animation(e.animNext)
                    elif e.dead:
                        self.entities.remove(e)
                        if self.quitting and len(self.lemmings) == 0:
                            self.running = False # Quebra o loop principal

    def draw(self):
        # Desenhar o level
        if not self.showMask:            
            self.screen.blit(self.level.terrain, (0, 0))
        else:
            mask_surface = self.level.terrainMask.to_surface(
                setcolor=(255, 255, 255, 255),
                unsetcolor=(0, 0, 0, 0)
            )
            self.screen.blit(mask_surface, (0, 0))
            mask_surface = self.level.blockerMask.to_surface(
                setcolor=(255, 0, 0, 255),
                unsetcolor=(0, 0, 0, 0)
            )
            self.screen.blit(mask_surface, (0, 0))
        # Desenhar as entidades
        for e in self.entities:
            e.draw()
        # Desenhar o selecionado
        if self.hovered:
            pygame.draw.circle(self.screen, (0, 255, 0), (self.hovered.x, self.hovered.y - self.hovered.rect.height // 4), 25, 3)
        # Desenhar o score
        text = self.scoreFont.render(f"Pontos: {self.points} / {self.level.config.numLemmingsToSave}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        # Desenhar as Skills
        i = 0
        for key, val in self.level.config.skills.items():
            if val <= 0:
                continue
            colour = (0, 255, 255) if key == self.selectedSkill else (255, 255, 255)
            text = self.skillsFont.render(f"{key}: {val}", True, colour)
            self.screen.blit(text, (300, 10 + i * 20))
            i += 1
    
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

    def toggle_paused(self):
        self.paused = not self.paused

    def toggle_show_mask(self):
        self.showMask = not self.showMask
    
    def select_skill(self, skillName):
        if skillName in self.level.config.skills:
            self.selectedSkill = skillName
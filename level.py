import pygame
import json

class Level:
    def __init__(self, number):
        self.config = LevelConfig(number)
        self.terrain = pygame.image.load(f'levels/level{number}.png').convert()
        self.terrain.set_colorkey(self.config.backgroundColour)
        self.terrainMask = pygame.mask.from_surface(self.terrain)
        self.terrain.set_colorkey(None)
        w, h = self.terrainMask.get_size()
        self.blockerMask = pygame.mask.Mask((w, h), False)
        self.blockerShape = pygame.mask.Mask((40, 44), True)
        self.digWidth = 44
        self.digHeight = 10
        self.digShape = pygame.mask.Mask((self.digWidth, self.digHeight), True) # TODO : meio-circulo
        # criar máscara circular
        self.explosionRadius = 40
        surf = pygame.Surface((self.explosionRadius*2, self.explosionRadius*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255,255,255), (self.explosionRadius, self.explosionRadius), self.explosionRadius)
        self.explosionShape = pygame.mask.from_surface(surf)
        # Degraus
        self.stepWidth = 16
        self.stepHeight = 4
        self.stepShape = pygame.mask.Mask((self.stepWidth, self.stepHeight + 2), True)
        
    # Verifica se um pixel eh solido no mapa ou nos Blocker's
    def is_solid(self, pos):
        posInt = (int(pos[0]), int(pos[1]))
        try:
            return (
                self.terrainMask.get_at(posInt) or
                self.blockerMask.get_at(posInt)
            )
        except IndexError:
            return False
    
    # Reconstroi a mascara dos lemmings Blockers
    def build_blocker_mask(self, lemmings):
        self.blockerMask.clear()
        for lem in lemmings:
            if lem.stateName == "Parado" and not lem.dead:
                self.blockerMask.draw(self.blockerShape, (lem.rect.x, lem.rect.centery))
    
    # Corta um pedaco do terreno
    def dig(self, pos):
        posInt = (int(pos[0]), int(pos[1]))
        digRect = pygame.Rect(int(pos[0]), int(pos[1]), self.digWidth, self.digHeight)
        pygame.draw.rect(self.terrain, self.config.backgroundColour, digRect)
        self.terrainMask.erase(self.digShape, posInt)
    
    def dig_hole(self, pos):
        x = int(pos[0])
        y = int(pos[1])
        # apagar visualmente no terreno
        pygame.draw.circle(self.terrain, self.config.backgroundColour, (x, y), self.explosionRadius)
        # remover da máscara do terreno
        self.terrainMask.erase(self.explosionShape, (x - self.explosionRadius, y - self.explosionRadius))
        
    
    def add_step(self, pos, direction):
        x = int(pos[0]) + (4 * direction)
        y = int(pos[1]) - self.stepHeight
        if direction == -1:
            x -= self.stepWidth
        # criar visualmente no terreno
        pygame.draw.rect(self.terrain, self.config.stepColour, (x, y, self.stepWidth, self.stepHeight))
        # criar na máscara do terreno
        self.terrainMask.draw(self.stepShape, (x, y))

class LevelConfig:
    def __init__(self, number):
        # Defaults
        self.number = number
        self.skills = {}
        self.numLemmings = 10
        self.numLemmingsToSave = 8
        self.startPosition = (100, 100)
        self.endPosition = (580, 710)
        self.backgroundColour = (114, 114, 201, 255)
        self.releaseRate = 10
        self.timeLimit = 300
        self.stepColour = (99, 0, 19, 255)
        self.load(number)

    def load(self, number):
        # Carregar os dados do nivel do JSON
        with open(f"levels/level{number}.json") as f:
            conf = json.load(f)
            for key, value in conf.items():
                if key == "objects":
                    for o in conf["objects"]:
                        if o['type'] == 'entrance':
                            self.startPosition = (o['x'], o['y'])
                        if o['type'] == 'exit':
                            self.endPosition = (o['x'], o['y'])
                elif key == "backgroundColour":
                    self.backgroundColour = (value[0], value[1], value[2], 255)
                elif hasattr(self, key):
                    setattr(self, key, value)
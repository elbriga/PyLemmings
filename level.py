import pygame

class Level:
    def __init__(self, image):
        self.numLemmings = 10
        self.startPosition = (100,100)
        self.endPosition = (580,710)
        self.backgroundColour = (114,114,201,255)
        self.surface = pygame.image.load(f'images/{image}.png').convert()
        self.surface.set_colorkey(self.backgroundColour)
        self.groundMask = pygame.mask.from_surface(self.surface)
        
    # Verifica se um pixel eh solido no mapa ou nos Blocker's
    def is_solid(self, pos):
        try:
            return self.groundMask.get_at((int(pos[0]), int(pos[1])))
        except IndexError:
            return False
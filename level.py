import pygame

class Level:
    def __init__(self, image):
        self.max_lemmings = 10
        self.max_height_to_die = 200
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
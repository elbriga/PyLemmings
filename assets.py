import pygame

class Assets:
    animations = {}

    @staticmethod
    def slice_sprites(sheet, total, xi, yi, step, width, height):
        sprites = []
        for i in range(0, total):
            x = xi + i * step
            sprite = pygame.Surface((width, height), pygame.SRCALPHA)
            sprite.blit(sheet, (0, 0), (x, yi, width, height))
            sprites.append(sprite.convert_alpha())
        return sprites

    @classmethod
    def load(cls):
        sheet = pygame.image.load("images/lemming_sheet.png").convert_alpha()

        cls.animations["lemming_walk"] = cls.slice_sprites(sheet, 8, 18, 0, 16, 10, 10)
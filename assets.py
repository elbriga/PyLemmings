import pygame

class Assets:
    animations = {}
    final_width = 10  # x4
    final_height = 20 # x4

    @staticmethod
    def slice_sprites(sheet, total, xi, yi, step, width, height):
        sprites = []
        for i in range(0, total):
            x = xi + i * step
            sprite = pygame.Surface((Assets.final_width, Assets.final_height), pygame.SRCALPHA)
            sprite.blit(sheet, (0, Assets.final_height - height), (x, yi, width, height))
            sprite.set_colorkey((0, 0, 0))
            sprite = pygame.transform.scale2x(sprite)
            sprite = pygame.transform.scale2x(sprite)
            sprites.append(sprite.convert_alpha())
        return sprites

    @classmethod
    def load(cls):
        sheet = pygame.image.load("images/lemming_sheet.png").convert_alpha()

        cls.animations["lemming_walk"] = cls.slice_sprites(sheet, 8, 18, 0, 16, 10, 10)
        cls.animations["lemming_fall"] = cls.slice_sprites(sheet, 4, 14, 20, 16, 10, 10)
        # Die from falling
        cls.animations["lemming_splat"] = cls.slice_sprites(sheet, 16, 19, 138, 16, 10, 10)
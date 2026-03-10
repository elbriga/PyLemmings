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
        # https://www.spriters-resource.com/amiga_amiga_cd32/lemmings/asset/37732/
        sheet = pygame.image.load("images/lemming_sheet.png").convert_alpha()

        cls.animations["lemming_walk"] = cls.slice_sprites(sheet, 8, 18, 0, 16, 10, 10)
        cls.animations["lemming_fall"] = cls.slice_sprites(sheet, 4, 14, 20, 16, 10, 10)
        cls.animations["lemming_open"] = cls.slice_sprites(sheet, 4, 19, 96, 16, 10, 16)
        cls.animations["lemming_float"] = cls.slice_sprites(sheet, 4, 83, 96, 16, 10, 16)
        # Die from falling
        cls.animations["lemming_splat"] = cls.slice_sprites(sheet, 16, 19, 138, 16, 10, 10)
        cls.animations["lemming_stop"] = cls.slice_sprites(sheet, 16, 20, 148, 16, 10, 10)
        cls.animations["lemming_boom"] = cls.slice_sprites(sheet, 16, 19, 169, 16, 10, 12)
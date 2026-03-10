import pygame
from entity import Entity
from lemmingState import LemmingState

class Lemming(Entity):
    def __init__(self, game, **kwargs):
        Entity.__init__(self, game, 40, 80)
        self.stateName = ""
        self.direction = 1
        self.climbHeight = 4
        self.falling = 0
        self.hasUmbrella = False
        self.set_state("Andando")

    def draw(self):
        screen = self.game.screen
        frame = self.frames[self.frame % len(self.frames)]
        if self.direction == -1:
            frame = pygame.transform.flip(frame, True, False)
        screen.blit(frame, self.rect)
        if self.hasUmbrella and self.stateName == "Andando":
            pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 5)
        if self.game.debug:
            pygame.draw.circle(screen, (255, 0, 0), (self.rect.right, self.rect.bottom + 1), 5)
            pygame.draw.circle(screen, (255, 255, 0), (self.rect.left, self.rect.bottom + 1), 5)
            if self.stateName == "Parado":
                blockArea = pygame.Rect(self.rect.x, self.rect.centery, 40, 44)
                pygame.draw.rect(screen, (255,0,0), blockArea, 1)

    def update(self):
        self.state.update()

    def is_near(self, pos, distance):
        area = pygame.Rect(pos[0] - distance, pos[1] - distance, distance * 2, distance * 2)
        return self.rect.colliderect(area)
    
    def is_on_floor(self):
        return (
            self.game.level.is_solid((self.rect.left, self.rect.bottom + 1)) or
            self.game.level.is_solid((self.rect.right, self.rect.bottom + 1))
        )

    def floor_height_in_front(self):
        height = 0
        # Achar a altura do chao na frente do lemming, ate a altura que ele consegue subir
        while height <= self.climbHeight:
            # O pixel 'na frente' do lemming depende da direcao dele
            positionInFront = (self.rect.right if self.direction == 1 else self.rect.left, self.rect.bottom - height)
            if not self.game.level.is_solid(positionInFront):
                break

            height += 1

        return height

    def set_state(self, stateName):
        self.stateName = stateName
        self.state = LemmingState.states[stateName](self)
    
    def toggleBlock(self):
        block = (self.stateName == "Andando")
        if block:
            self.set_state("Parado")
            self.set_animation("stop")
        else:
            self.set_state("Andando")
        self.game.buildBlockerMask()

    def explode(self):
        self.set_state("Parado")
        self.set_animation("boom")
        self.frame = 0
        self.dead = True
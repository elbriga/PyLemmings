import pygame
from lemmingState import Stoper

class Events:
    @staticmethod
    def exec(game, event):
        #print(event)
        if event.type == pygame.QUIT:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                return False
            if event.key == pygame.K_p:
                game.paused = not game.paused
            
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # botao esquerdo
                lem = game.hovered
                if lem and lem.nomeEstado == "Andando":
                    lem.set_state("Parado")
                    lem.setAnimation("stop")
        
        return True
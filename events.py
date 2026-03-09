import pygame

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
                lem = game.get_lemming_near(event.pos)
                if lem:
                    game.set_selected(lem)
        
        return True
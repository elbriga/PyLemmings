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
            if game.hovered:
                lem = game.hovered
                if event.button == 1:  # botao esquerdo
                    lem.hasUmbrella = True

                if event.button == 2:  # botao meio
                    lem.toggleBlock()

                if event.button == 3:  # botao direito
                    lem.dig()
        
        return True
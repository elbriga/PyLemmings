#!/usr/bin/env python3
import pygame
from game import Game
from level import Level

# screen size
HEIGHT=800
WIDTH=800

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyLemmings")

jogo = Game(screen, Level('level'))

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    jogo.update()

    screen.fill((0,0,0))
    jogo.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()


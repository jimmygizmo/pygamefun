#! /usr/bin/env -vS python

import pygame


# Display surface, event loop

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# SCREEN_TITLE = "PyArcade Game One"
GAME_TITLE = 'Space Blasto'

surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

running = True
BGCOLOR = 'blue4'

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    surface.fill(BGCOLOR)

    pygame.display.update()  # update entire surface or use  .flip() which will update only part of the surface.


pygame.quit()


##
#


# DOCS:
# https://pyga.me/docs/

# PyGame vs Arcade:
# https://aircada.com/pygame-vs-arcade/

# Named Colors:
# https://pyga.me/docs/ref/color_list.html


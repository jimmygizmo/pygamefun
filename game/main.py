#! /usr/bin/env -vS python

import pygame


# Display surface, event loop

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GAME_TITLE = 'Space Blasto'
BGCOLOR = 'tan4'
ONECOLOR = 'aqua'
ONESIZE = (20, 20)  # Using a tuple for x, y in this case.

display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# NOTE: Two different things: a "Surface" v.s. a "display surface". First we used a "display surface".
# Next we use a "Surface". (They are very similar. "display surface" is the main surface we draw on. The ONE we see.
# We can attach multiple "Surface" objects to the one official "display surface".

one_surf = pygame.Surface(ONESIZE)
one_surf.fill(ONECOLOR)

one_x = 100
one_y = 150
one_vel_x = 0.3
one_vel_y = 0.2

running = True

while running:
    # #### ####   EVENT LOOP    #### ####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #display_surface.fill(BGCOLOR)  # Vid28:46 Interesting: If we don't do this, moving things leave a trail.

    display_surface.blit(one_surf, (one_x, one_y))

    pygame.display.update()  # update entire surface or use  .flip() which will update only part of the surface.

    # Bounce off wall in X Axis - If either limit is hit, reverse the speed/velocity
    if one_x < 0 or one_x > 1260:
        one_vel_x = one_vel_x * -1

    # Bounce off wall in Y Axis - If either limit is hit, reverse the speed/velocity
    if one_y < 0 or one_y > 700:
        one_vel_y = one_vel_y * -1

    # Technically a speed is an absolute value, but a velocity (in one dimension, as we are currently dealing with it)
    # is just a speed with a positive or negative sign. (A speed with direction indicated.)
    # A velocity is both a speed and a direction, and direction has dimensions, one, two or three, usually.

    one_x += one_vel_x
    one_y += one_vel_y



pygame.quit()


##
#


# TUTORIAL VIDEO  (Notice some comments have a Video Timing Marker: Vid28:46)
# This video is over 11 hours long and covers about 5 different games and a lot of PyGame details.
# https://www.youtube.com/watch?v=8OMghdHP-zs

# DOCS:
# https://pyga.me/docs/

# PyGame vs Arcade:
# https://aircada.com/pygame-vs-arcade/

# Named Colors:
# https://pyga.me/docs/ref/color_list.html


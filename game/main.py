#! /usr/bin/env -vS python

import pygame


pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GAME_TITLE = 'Space Blasto'
BGCOLOR = 'tan4'
ONECOLOR = 'aqua'
ONESIZE = (20, 20)  # Using a tuple for x, y in this case.
MONSTER_ONE = 'assets/grumpy-cat-sm.png'
MONSTER_TWO = 'assets/gold-retriever-sm.png'


# MONSTER DATA
monsters = []
monster = {'name': 'grumpy',
           'img':  'assets/grumpy-cat-sm.png',
           'w': 200,
           'h': 200,
           'color': 'blue',
           'x': 150,
           'y': 150,
           'xv': 0.2,
           'yv': 0.04,
           }
monsters.append(monster)
monster = {'name': 'goldie',
           'img':  'assets/gold-retriever-sm.png',
           'w': 200,
           'h': 200,
           'color': 'red',
           'x': 150,
           'y': 150,
           'xv': 0.23,
           'yv': -0.43,
           }
monsters.append(monster)


# DISPLAY SURFACE
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# NOTE: Two different things: a "Surface" v.s. a "display surface". First we used a "display surface".
# Next we use a "Surface". (They are very similar. "display surface" is the main surface we draw on. The ONE we see.
# We can attach multiple "Surface" objects to the one official "display surface".

# INITIALIZE MONSTERS
for monster in monsters:
    # monster['surface'] = pygame.Surface((monster['w'], monster['h']))
    # monster['surface'].fill(monster['color'])
    monster['surface'] = pygame.image.load(monster['img']).convert_alpha()
    # TODO: For performance, pre-calculate/populate values like half-width, half-height, etc. etc. etc.
    # Don't do this if we find built in methods for FRect. This is probably well-covered by FRect/PyGame.

# Refactoring to use monsters array/list
# one_surf = pygame.Surface(ONESIZE)
# one_surf.fill(ONECOLOR)
# one_x = -1100
# one_y = -100
# one_vel_x = 0.2
# one_vel_y = 0.04
# monster_surf_one = pygame.image.load(MONSTER_THREE).convert_alpha()


running = True
while running:
    # #### ####   EVENT LOOP    #### ####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #display_surface.fill(BGCOLOR)  # Vid28:46 Interesting: If we don't always re-draw BG, moving things leave a trail.
    display_surface.fill(BGCOLOR)  # Normally we always re-draw the BG.

    #display_surface.blit(one_surf, (one_x, one_y))
    for monster in monsters:
        display_surface.blit(monster['surface'], (monster['x'], monster['y']))

    pygame.display.update()  # update entire surface or use  .flip() which will update only part of the surface.
    #pygame.display.flip()  # Similar to update but not entire screen. TODO: Clarify

    # CALCULATIONS FOR NEW POSITIONS FOR THE NEXT LOOP:
    for monster in monsters:
        # Really, to calculate limits like this for an object requires using half the object width etc.
        # It also requires images with no buffer/margin of transparency in the image. TODO: Fix this in our images.

        # Bounce off wall in X Axis - If either limit is hit, reverse the speed/velocity
        if monster['x'] < 0 or monster['x'] > 1170:
            monster['xv'] = monster['xv'] * -1

        # Bounce off wall in Y Axis - If either limit is hit, reverse the speed/velocity
        if monster['y'] < 0 or monster['y'] > 600:
            monster['yv'] = monster['yv'] * -1

        # Technically a speed is an absolute value, but a velocity (in one dimension, as we are currently dealing with it)
        # is just a speed with a positive or negative sign. (A speed with direction indicated.)
        # A velocity is both a speed and a direction, and direction has dimensions, one, two or three, usually.

        monster['x'] += monster['xv']
        monster['y'] += monster['yv']


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


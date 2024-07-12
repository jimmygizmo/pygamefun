#! /usr/bin/env -vS python

import pygame
import os.path


pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GAME_TITLE = 'Space Blasto'
BGCOLOR = 'olivedrab'
ASSET_PATH = 'assets'  # Relative path with no trailing slash.


# MONSTER DATA
monsters = []
monster = {'name': 'goldie',
           'img':  'gold-retriever-160x142.png',
           'w': 160,
           'h': 142,
           'color': 'red',
           'x': 0,
           'y': 0,
           'xv': 0.042,
           'yv': -0.03,
           }
monsters.append(monster)
monster = {'name': 'grumpy',
           'img':  'grumpy-cat-110x120.png',
           'w': 110,
           'h': 120,
           'color': 'blue',
           'x': 55,
           'y': 60,
           'xv': 0.11,
           'yv': 0.04,
           }
monsters.append(monster)


# DISPLAY SURFACE
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# INITIALIZE MONSTERS
for monster in monsters:
    # monster['surface'] = pygame.Surface((monster['w'], monster['h']))
    # monster['surface'].fill(monster['color'])
    imgpath = os.path.join(ASSET_PATH, monster['img'])
    monster['surface'] = pygame.image.load(imgpath).convert_alpha()
    # TODO: For performance, pre-calculate/populate values like half-width, half-height, etc. etc. etc.
    # Don't do this if we find built in methods for FRect. This is probably well-covered by FRect/PyGame.
    monster['Hw'] = monster['w'] / 2
    monster['Hh'] = monster['h'] / 2


running = True
while running:
    # #### ####   EVENT LOOP    #### ####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # CALCULATIONS FOR NEW POSITIONS, BOUNCING
    for monster in monsters:
        # Really, to calculate limits like this for an object requires using half the object width etc.
        # It also requires images with no buffer/margin of transparency in the image. TODO: Fix this in our images.

        monster['x'] += monster['xv']
        monster['y'] += monster['yv']

        # Bounce off LEFT wall in X Axis
        if monster['x'] < 0:
            monster['x'] = 0  # Stop at the LEFT edge instead of passing it.
            monster['xv'] = monster['xv'] * -1
        # Bounce off RIGHT wall in X Axis
        if monster['x'] > (SCREEN_WIDTH - monster['h']):
            monster['x'] = (SCREEN_WIDTH - monster['h'])  # Stop at the RIGHT edge instead of passing it.
            monster['xv'] = monster['xv'] * -1

        # Bounce off TOP wall in Y Axis
        if monster['y'] < 0:
            monster['yv'] = monster['yv'] * -1
        # Bounce off BOTTOM wall in Y Axis
        if monster['y'] > (SCREEN_HEIGHT - monster['h']):
            monster['y'] = (SCREEN_HEIGHT - monster['h'])  # Stop at the BOTTOM edge instead of passing it.
            monster['yv'] = monster['yv'] * -1


    #display_surface.fill(BGCOLOR)  # Vid28:46 Interesting: If we don't always re-draw BG, moving things leave a trail.
    display_surface.fill(BGCOLOR)  # Normally we always re-draw the BG.

    #display_surface.blit(one_surf, (one_x, one_y))
    for monster in monsters:
        display_surface.blit(monster['surface'], (monster['x'], monster['y']))

    pygame.display.update()  # update entire surface or use  .flip() which will update only part of the surface.
    #pygame.display.flip()  # Similar to update but not entire screen. TODO: Clarify


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

# GENERAL NOTES:

# "Surface" v.s. a "display surface". They are very similar. "display surface" is the main surface we draw on.
# The ONE we see. We can attach multiple "Surface" objects to the one official "display surface".

# Technically a speed is an absolute value, but a velocity (in one dimension, as we are currently dealing with it)
# is just a speed with a positive or negative sign. (A speed with direction indicated.)
# A velocity is both a speed and a direction, and direction has dimensions, one, two or three, usually.


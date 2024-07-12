#! /usr/bin/env -vS python

import pygame
import os.path
import random


pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
GAME_TITLE = 'Space Blasto'
BGCOLOR = 'olivedrab'
BGIMG = 'lawn-bg-dark-2560x1440.jpg'  # 'grass-field-med-1920x1249.jpg'  # 'lawn-bg-dark-2560x1440.jpg'
ASSET_PATH = 'assets'  # Relative path with no trailing slash.
DEBUG = False
PROP_SPRAY_COUNT = 40
PROP_SPRAY_RADIUS = 400


# MONSTER DATA
monsters = []
monster = {'name': 'red-flower-floaty',
           'img':  'red-flower-66x64.png',
           'w': 66,
           'h': 64,
           'color': 'red1',
           'x': 240,
           'y': 300,
           'xv': -0.03,
           'yv': 0.01,
           }
monsters.append(monster)
monster = {'name': 'red-flower-drifty',
           'img':  'red-flower-66x64.png',
           'w': 66,
           'h': 64,
           'color': 'orangered',
           'x': 240,
           'y': 300,
           'xv': 0.032,
           'yv': -0.033,
           }
monsters.append(monster)
monster = {'name': 'goldie',
           'img':  'gold-retriever-160x142.png',
           'w': 160,
           'h': 142,
           'color': 'gold',
           'x': 500,
           'y': 300,
           'xv': 0.042,
           'yv': -0.03,
           }
monsters.append(monster)
monster = {'name': 'fishy',
           'img':  'goldfish-280x220.png',
           'w': 280,
           'h': 220,
           'color': 'darkgoldenrod1',
           'x': 840,
           'y': 300,
           'xv': -0.07,
           'yv': -0.15,
           }
monsters.append(monster)
monster = {'name': 'grumpy',
           'img':  'grumpy-cat-110x120.png',
           'w': 110,
           'h': 120,
           'color': 'blanchedalmond',
           'x': 780,
           'y': 300,
           'xv': 0.11,
           'yv': 0.04,
           }
monsters.append(monster)


# PROP DATA
prop_templates = []
prop_template = {'name': 'red-flower',
           'img':  'red-flower-66x64.png',
           'w': 66,
           'h': 64,
           'color': 'purple',
           'x': 640,
           'y': 360,
           'spray_count': 40,
           'spray_radius': 600,
           }
prop_templates.append(prop_template)


# DISPLAY SURFACE
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# INITIALIZE MONSTERS
for monster in monsters:
    if DEBUG:
        monster['surface'] = pygame.Surface((monster['w'], monster['h']))
        monster['surface'].fill(monster['color'])
    else:
        imgpath = os.path.join(ASSET_PATH, monster['img'])
        print(f"MONSTER: {imgpath}")  # ----DEBUG----
        monster['surface'] = pygame.image.load(imgpath).convert_alpha()

    # FRect/PyGame probably have facilities making such pre-calculations unnecessary, but the concept is very
    # general and there are always many kinds of pre-calculation/caching performance-boost options one can
    # apply in performance-critical areas. Leaving this here to show the concept. Monsters can carry some of their
    # pre-calculated custom values they will use often (like for collision-detection). The trade-off is the speed
    # to retrieve those values vs. calculate them each time. Such things need to be profiled appropriately to
    # understand if you gain anything and how much.
    monster['Hw'] = monster['w'] / 2  # Not using yet. May not need. (Good pre-calculation performance strategy.)
    monster['Hh'] = monster['h'] / 2  # Not using yet. May not need. (Good pre-calculation performance strategy.)


# INITIALIZE PROPS - 'SPRAY' REPLICATED PROPS (randomly within specified radius)
props = []
for prop_t in prop_templates:
    for index in range(prop_t['spray_count']):  # We will use the index for a unique prop name. Not critical.
        # We must create a NEW prop dictionary object each time, otherwise they would all be the same reference.
        prop = {'img': prop_t['img'],  # Copy the unchanging attributes from the template before we customize any.
                'w': prop_t['w'],
                'h': prop_t['h'],
                'color': prop_t['color'],
                }
        # As we iterate (spray), we will customize only some of the attributes.

        diameter = 2 * prop_t['spray_radius']  # This variable makes if easier to read/understand. Remove for perf.
        prop['name'] = prop_t['name'] + "-" + str(index)
        print(f"SPRAYED PROP: {prop['name']}")  # ----DEBUG----
        x_offset = random.randint(0, diameter) - prop_t['spray_radius']
        y_offset = random.randint(0, diameter) - prop_t['spray_radius']
        print(x_offset)  # ----DEBUG----
        print(y_offset)  # ----DEBUG----
        prop['x'] = prop_t['x'] + x_offset
        prop['y'] = prop_t['y'] + y_offset

        if DEBUG:
            prop['surface'] = pygame.Surface((prop['w'], prop['h']))
            prop['surface'].fill(prop['color'])
        else:
            imgpath = os.path.join(ASSET_PATH, prop['img'])
            print(f"PROP: {imgpath}")
            prop['surface'] = pygame.image.load(imgpath).convert_alpha()

        props.append(prop)


print(props)

# ###############################################    MAIN EXECUTION    #################################################

bgpath = os.path.join(ASSET_PATH, BGIMG)
bg_surface = pygame.image.load(bgpath)

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
        if monster['x'] > (SCREEN_WIDTH - monster['w']):
            monster['x'] = (SCREEN_WIDTH - monster['w'])  # Stop at the RIGHT edge instead of passing it.
            monster['xv'] = monster['xv'] * -1

        # Bounce off TOP wall in Y Axis
        if monster['y'] < 0:
            monster['yv'] = monster['yv'] * -1
        # Bounce off BOTTOM wall in Y Axis
        if monster['y'] > (SCREEN_HEIGHT - monster['h']):
            monster['y'] = (SCREEN_HEIGHT - monster['h'])  # Stop at the BOTTOM edge instead of passing it.
            monster['yv'] = monster['yv'] * -1


    #display_surface.fill(BGCOLOR)  # Vid28:46 Interesting: If we don't always re-draw BG, moving things leave a trail.
    #display_surface.fill(BGCOLOR)  # Normally we always re-draw the BG.

    # Paint the BG image every time. Paint the bg_surface (blit it) onto the main display_surface at coords (0, 0)
    display_surface.blit(bg_surface, (0, 0))

    # DRAW PROPS
    for prop in props:
        display_surface.blit(prop['surface'], (prop['x'], prop['y']))

    # DRAW MONSTERS
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


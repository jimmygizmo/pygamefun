#! /usr/bin/env -vS python

import pygame
import os.path
import random


pygame.init()

SCREEN_WIDTH = 1280.0
SCREEN_HEIGHT = 720.0
GAME_TITLE = 'Space Blasto'
BGCOLOR = 'olivedrab'
BGIMG = 'lawn-bg-dark-2560x1440.jpg'  # 'grass-field-med-1920x1249.jpg'  # 'lawn-bg-dark-2560x1440.jpg'
ASSET_PATH = 'assets'  # Relative path with no trailing slash.
DEBUG = False


# MONSTER DATA
monsters = []
monster = {'name': 'red-flower-floaty',
           'img':  'red-flower-66x64.png',
           'w': 66.0,
           'h': 64.0,
           'color': 'red1',
           'x': 240.0,
           'y': 300.0,
           'xv': -0.03,
           'yv': 0.01,
           }
monsters.append(monster)
monster = {'name': 'red-flower-drifty',
           'img':  'red-flower-66x64.png',
           'w': 66.0,
           'h': 64.0,
           'color': 'orangered',
           'x': 240.0,
           'y': 300.0,
           'xv': 0.032,
           'yv': -0.033,
           }
monsters.append(monster)
monster = {'name': 'goldie',
           'img':  'gold-retriever-160x142.png',
           'w': 160.0,
           'h': 142.0,
           'color': 'gold',
           'x': 500.0,
           'y': 300.0,
           'xv': 0.042,
           'yv': -0.03,
           }
monsters.append(monster)
monster = {'name': 'fishy',
           'img':  'goldfish-280x220.png',
           'w': 280.0,
           'h': 220.0,
           'color': 'darkgoldenrod1',
           'x': 840.0,
           'y': 300.0,
           'xv': -0.07,
           'yv': -0.15,
           }
monsters.append(monster)
monster = {'name': 'grumpy',
           'img':  'grumpy-cat-110x120.png',
           'w': 110.0,
           'h': 120.0,
           'color': 'blanchedalmond',
           'x': 780.0,
           'y': 300.0,
           'xv': 0.11,
           'yv': 0.04,
           }
monsters.append(monster)


# PROP DATA
prop_templates = []
prop_template = {'name': 'red-flower',
           'img':  'red-flower-66x64.png',
           'w': 66.0,
           'h': 64.0,
           'color': 'purple',
           'x': 640.0,
           'y': 360.0,
           'spray_count': 40,
           'spray_radius': 600.0,
           }
prop_templates.append(prop_template)


# DISPLAY SURFACE
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# INITIALIZE MONSTERS
for monster in monsters:
    if DEBUG:
        monster['surface'] = pygame.Surface(monster['w'], monster['h'])
        monster['surface'].fill(monster['color'])
    else:
        imgpath = os.path.join(ASSET_PATH, monster['img'])
        monster['surface'] = pygame.image.load(imgpath).convert_alpha()

    monster['rect'] = monster['surface'].get_rect(center=(monster['x'], monster['y']))


# INITIALIZE PROPS - 'SPRAY' REPLICATED PROPS (randomly within specified radius)
props = []
for prop_t in prop_templates:
    for index in range(prop_t['spray_count']):  # We will use the index for a unique prop name. Not critical.
        # We must create a NEW prop dictionary object each time, otherwise they would all be the same reference.
        prop = {'img': prop_t['img'],  # Copy the unchanging attributes from the template before handling dynamic ones.
                'w': prop_t['w'],
                'h': prop_t['h'],
                'color': prop_t['color'],
                }

        diameter = 2.0 * prop_t['spray_radius']  # This variable makes it easier to read/understand. Inline for perf.
        prop['name'] = prop_t['name'] + "-" + str(index)
        x_offset = random.uniform(0.0, diameter) - prop_t['spray_radius']  # uniform() gives a random float value
        y_offset = random.uniform(0.0, diameter) - prop_t['spray_radius']  # uniform() includes the limits
        prop['x'] = prop_t['x'] + x_offset
        prop['y'] = prop_t['y'] + y_offset

        if DEBUG:
            prop['surface'] = pygame.Surface((prop['w'], prop['h']))
            prop['surface'].fill(prop['color'])
        else:
            imgpath = os.path.join(ASSET_PATH, prop['img'])
            prop['surface'] = pygame.image.load(imgpath).convert_alpha()

        prop['rect'] = prop['surface'].get_rect(center=(prop['x'], prop['y']))

        props.append(prop)


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

        # **************************************************************************************************************
        # * IDEA: For position updates, we might be able to do this to ANY of the named corners or sides.
        # The rect is designed to update all the related values and then the surface uses the updated rect
        # however it needs to when it is time to blit. It would be irrelevant as to what particular point
        # was used to update the position of the entire rect. SO, while we will still look closely at Vectors,
        # this may take us closer to what we want, regarding the stuff I am trying below.
        # I am trying to update the position of the rect and was looking for a .centerx and a .centery or
        # or something similar, but since I can update and reference at the same time ( or even more accurately,
        # reference and update at the same time), I SHOULD be able to do this:
        # monster['rect'].left += monster['xv']
        # monster['rect'].top += monster['yv']
        # **************************************************************************************************************

        # TODO: We might want to change this logic. Currently we move before collision detect etc. and treat
        # it like prep for the next iteration. Just doesn't feel right and some of our bounces show it happening
        # too far from the edge. This might be why we never fully hit the edge sometimes. Regardsless of the bounce
        # issue, this just does not feel like the right order of things. But we still need to strategically figure
        # out our major processing steps and their order, so this is working great for an early pass.

        # ***** RE-ENABLE AFTER ***** TEST. This may still be needed if we cannot use .left += and .right +=
        monster['x'] += monster['xv']  # Probably deprecate this action later
        monster['y'] += monster['yv']  # Probably deprecate this action later

        # newx = monster['rect'].centerx + monster['xv']  # Lets try something else
        # newy = monster['rect'].centery + monster['yv']  # Lets try something else

        # New test. See ******** above:
        # monster['rect'].left += monster['xv']
        # monster['rect'].top += monster['yv']
        # FAILED. MONSTERS STAY IN INITIAL POS.
        # THIS WAS ANOTHER ATTEMPT AT -UPDATE-IN-PLACE-. So far the only thing working is a copying of values and
        # then re-assignment of the rect.center using a tuple. This issue probably has something to do with ref
        # vs. copy. WE NEED TO LOOK AT VERCTORS ANYHOW. AND OUR WORKING SOLUTION IS FINE. BUT THE DOCS AND DESIGN
        # SEEM TO IMPLY WE CAN REF AND UPDATE AT THE SAME TIME, BUT MANY VARIATIONS OF THIS HAVE SO FAR FAILED.

        newx = monster['x'] + monster['xv']  # This FIXED it, but I really want to use something like centerx/centery
        newy = monster['y'] + monster['yv']  # This FIXED it, but I really want to use something like centerx/centery
        # TUTORIAL COMES DIRECTLY TO THIS ISSUE. SAME CHALLENGE. THE SOLUTION IS SAID TO BE: VECTORS
        # WHAT WE HAVE HERE WORKS, BUT AS AI NOTED ABOVE, IS NOT THE CLEAN WAY I WAS LOOKING FOR.
        # ***** FOR ***** TEST DONT NEED THIS:
        monster['rect'].center = (newx, newy)

        # These calculations are based off using the topleft of the rect. TODO: Change to using center of the rect.

        # # Bounce off LEFT wall in X Axis
        # if monster['x'] < 0:
        #     monster['x'] = 0  # Stop at the LEFT edge instead of passing it.
        #     monster['xv'] = monster['xv'] * -1
        # # Bounce off RIGHT wall in X Axis
        # if monster['x'] > (SCREEN_WIDTH - monster['w']):
        #     monster['x'] = (SCREEN_WIDTH - monster['w'])  # Stop at the RIGHT edge instead of passing it.
        #     monster['xv'] = monster['xv'] * -1
        #
        # # Bounce off TOP wall in Y Axis
        # if monster['y'] < 0:
        #     monster['yv'] = monster['yv'] * -1
        # # Bounce off BOTTOM wall in Y Axis
        # if monster['y'] > (SCREEN_HEIGHT - monster['h']):
        #     monster['y'] = (SCREEN_HEIGHT - monster['h'])  # Stop at the BOTTOM edge instead of passing it.
        #     monster['yv'] = monster['yv'] * -1

        # Bounce off LEFT wall in X Axis
        if monster['rect'].left < 0:
            monster['rect'].left = 0  # Stop at the LEFT edge instead of passing it.
            monster['xv'] = monster['xv'] * -1  # Reverse X-Axis speed/velocity
        # Bounce off RIGHT wall in X Axis
        if monster['rect'].right > SCREEN_WIDTH:
            monster['rect'].right = SCREEN_WIDTH  # Stop at the RIGHT edge instead of passing it.
            monster['xv'] = monster['xv'] * -1  # Reverse X-Axis speed/velocity

        # Bounce off TOP wall in Y Axis
        if monster['rect'].top < 0:
            monster['rect'].top = 0  # Stop at the TOP edge instead of passing it.
            monster['yv'] = monster['yv'] * -1  # Reverse Y-Axis speed/velocity
        # Bounce off BOTTOM wall in Y Axis
        if monster['rect'].bottom > SCREEN_HEIGHT:
            monster['rect'].bottom = SCREEN_HEIGHT  # Stop at the BOTTOM edge instead of passing it.
            monster['yv'] = monster['yv'] * -1  # Reverse Y-Axis speed/velocity

        # Should not need this now.
        # monster['rect'] = monster['surface'].get_rect(topleft=(monster['x'], monster['y']))


    #display_surface.fill(BGCOLOR)  # Normally we always re-draw the BG.

    # Paint the BG image every time. Paint the bg_surface (blit it) onto the main display_surface at coords (0, 0)
    display_surface.blit(bg_surface, (0, 0))

    # ##################################################    DRAW    ####################################################

    # DRAW PROPS
    for prop in props:
        prop['rect'] = prop['surface'].get_rect(topleft=(prop['x'], prop['y']))  # TODO: Refactor to center
        display_surface.blit(prop['surface'], prop['rect'])

    # DRAW MONSTERS
    for monster in monsters:
        display_surface.blit(monster['surface'], monster['rect'])

    # pygame.display.update()  # update entire surface or use  .flip() which will update only part of the surface.
    pygame.display.flip()  # Similar to update but not entire screen. TODO: Clarify


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

# ----------------------------------------------------------------------------------------------------------------------

# Rectangles (FRects)  (rectangles with a size and position)

# CORNERS  (assign a tuple of coordinates):
# topleft              midtop              topright
# midleft                 center             midright
# bottomleft             midbottom          bottomright

# SIDES  (assign a single axis value):
#                        top
# left                                        right
#                       bottom

# CREATE standalone OR CREATE from SURFACE
# pygame.FRect(pos, size)  # standalone
# surface.get_frect(point=pos)

# GITHUB EXPERIMENT: Changing email and username to match those previously used. Trying to solve issue with
# contribution tracking. This comment will be pushed to test the fix. FIXED. The contribution was immediately
# recognized. See the GitHub info page on how contributions tracked. Email/username MUST be correct. See the specs.
# This issue has been fixed and this comment will soon be removed.


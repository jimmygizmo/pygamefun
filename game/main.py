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
prop_template = {'name': 'blue-flower',
           'img':  'blue-flower-160x158.png',
           'w': 160.0,
           'h': 158.0,
           'color': 'purple',
           'x': 190.0,
           'y': 160.0,
           'spray_count': 10,
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


    # ################################################    PHYSICS    ###################################################
    # Calculations for new object positions, collisions, velocity changes and update of related object state.
    # CALCULATIONS FOR NEW POSITIONS, BOUNCING

    for monster in monsters:

        # RECENT TAKEAWAYS IN THIS AREA:
        # 1. Rect values are INT only so they are approximations. Do not propagate back to FLOAT source of truth.
        # 2. Source of truth is FLOAT and maintained in global, local or some other application memory.
        # 3. Rects are only intended for positioning Surfaces on screen.
        # 4. You CANNOT reference AND update one of the named sides like this: monster['rect'].left += monster['xv']
        # 5. Maintain a FLOAT source of truth and keep doing this kind of thing: monster['x'] += monster['xv']
        # 6. Probably continue updating position AS FIRST MAIN LOOP STEP as done in 5. Then recalc other physics next.
        # 7. Rect is used at the time of blit, to position the Surface on the screen.
        # 8. A sensible perspective is that at START OF LOOP, we FIRST take care of MOTION which has JUST BEEN
        #    occurring during the time the previous frame was statically displayed for its duration. This means
        #    we never actually see the original default object positions displayed, unless we add a separate
        #    initialization step for that. It is a design pattern. Handle motion/physics at start of loop before draw.


        # MOVE TRUE POSITION PER VELOCITY - Maintain the source of truth as FLOAT values in the primary data structure.
        monster['x'] += monster['xv']
        monster['y'] += monster['yv']
        # We must copy the float values and compose a new tuple to use to assign to rect.center
        newx = monster['x']
        newy = monster['y']
        # ASSUMED: When this assignment occurs, this is when all rect values ARE APPROXIMATED AS INT.
        monster['rect'].center = (newx, newy)
        # The following DEBUG output will show that the source of truth uses accurate FLOAT values, while the
        # rect INT values are approximations, which work perfectly to handle Surface positioning, but not truth values.
        # print(f"TRUTH: x, y        {monster['x']}, {monster['y']}")  # ----  DEBUG  ----
        # print(f"RECT: centerx, centery   {monster['rect'].centerx}, {monster['rect'].centery}")  # ----  DEBUG  ----
        # The above also shows that STANDARD ROUNDING occurs for the conversion of FLOAT to INT when rect is populated.

        # SUBTLETIES BELOW: We bound the displaying surface at the edge, BUT we let the TRUTH VALUE possibly EXCEED
        # the boundary and stay that way, we simply reverse/bounce possibly a little bit BEYOND the screen edge.
        # This is never seen. It seems possible this could lead to a 1 frame pause (approx) of an object staying
        # just slightly stuck against the wall for a slightly sticky bounce as compared to much more typical bounces.
        # It's not a big effect, but since we want to both preserve true float values AND efficiently "bounce"
        # with respect to what can be perceived on the screen by most people in most cases, then it is important to
        # note here some of the tiny compromises we make. Bottom line is that our TRUTH values are not corrupted by
        # including appeoximated rect values, BUT in a way we are corrupting the "simulation" in a sense, because we
        # are sometimes bouncing of a virtual wall which is slightly displaced from the wall that the user sees.
        # It's interesting how much subtlty has already arizen. We were promised FLOAT support in rects and some of
        # the challenge here I am discussing is realted to the fact that we don't have support for float values in
        # rects. They could still appoximate using ints to match screen pixels, BUT they would work better if one
        # could assign and retreive FLOAT values for ALL named coordinates. The Surface/blit can perform the FLOAT
        # to INT approximations to match pixels on the screen, but the rect could work very well handling all of
        # its values as floats. I'm surprised to find a great tutorial referring to frects, but my PyGame does
        # not appear to have FRects, only Rects and no floating point support in rects. I'm still ing trying to
        # figure out if I am missing something or if this was a feature that was removed.

        # Bounce off LEFT wall in X Axis
        if monster['rect'].left <= 0:
            monster['rect'].left = 0  # Great! We don't touch the TRUTH VALUE. We do bound the Surface on screen.
            monster['xv'] = monster['xv'] * -1
        # Bounce off RIGHT wall in X Axis
        if monster['rect'].right >= SCREEN_WIDTH:
            monster['rect'].right = SCREEN_WIDTH  # Great! We don't touch the TRUTH VALUE. We do bound the Surface.
            monster['xv'] = monster['xv'] * -1

        # Bounce off TOP wall in Y Axis
        if monster['rect'].top <= 0:
            monster['rect'].top = 0  # Great! We don't touch the TRUTH VALUE. We do bound the Surace on screen.
            monster['yv'] = monster['yv'] * -1
        # Bounce off BOTTOM wall in Y Axis
        if monster['rect'].bottom >= SCREEN_HEIGHT:
            monster['rect'].bottom = SCREEN_HEIGHT  # Great! We don't touch the TRUTH VALUE. We do bound the Surface.
            monster['yv'] = monster['yv'] * -1


    #display_surface.fill(BGCOLOR)  # Normally we always re-draw the BG.

    # Paint the BG image every time. Paint the bg_surface (blit it) onto the main display_surface at coords (0, 0)
    display_surface.blit(bg_surface, (0, 0))

    # ##################################################    DRAW    ####################################################

    # DRAW PROPS
    for prop in props:
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


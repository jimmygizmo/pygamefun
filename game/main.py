#! /usr/bin/env -vS python

import pygame
import os.path
import random


# ###############################################    CONFIGURATION    ##################################################

SCREEN_WIDTH = 1280.0
SCREEN_HEIGHT = 720.0
GAME_TITLE = 'Space Blasto'
BGCOLOR = 'olivedrab'
BGIMG = 'lawn-bg-dark-2560x1440.jpg'  # 'grass-field-med-1920x1249.jpg'  # 'lawn-bg-dark-2560x1440.jpg'
ASSET_PATH = 'assets'  # Relative path with no trailing slash.
DEBUG = True


# MONSTER DATA
monsters = []
monster = {'name': 'red-flower-floaty',
           'img':  'red-flower-66x64.png',
           'w': 66,
           'h': 64,
           'color': 'red1',
           'x': 240.0,
           'y': 300.0,
           'xv': -0.03,
           'yv': 0.01,
           }
monsters.append(monster)
monster = {'name': 'red-flower-drifty',
           'img':  'red-flower-66x64.png',
           'w': 66,
           'h': 64,
           'color': 'orangered',
           'x': 240.0,
           'y': 300.0,
           'xv': 0.032,
           'yv': -0.033,
           }
monsters.append(monster)
monster = {'name': 'goldie',
           'img':  'gold-retriever-160x142.png',
           'w': 160,
           'h': 142,
           'color': 'gold',
           'x': 500.0,
           'y': 300.0,
           'xv': 0.042,
           'yv': -0.03,
           }
monsters.append(monster)
monster = {'name': 'fishy',
           'img':  'goldfish-280x220.png',
           'w': 280,
           'h': 220,
           'color': 'darkgoldenrod1',
           'x': 840.0,
           'y': 300.0,
           'xv': -0.07,
           'yv': -0.15,
           }
monsters.append(monster)
monster = {'name': 'grumpy',
           'img':  'grumpy-cat-110x120.png',
           'w': 110,
           'h': 120,
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
           'w': 66,
           'h': 64,
           'color': 'purple',
           'x': 640.0,
           'y': 360.0,
           'spray_count': 40,
           'spray_radius': 600.0,
           }
prop_templates.append(prop_template)
prop_template = {'name': 'blue-flower',
           'img':  'blue-flower-160x158.png',
           'w': 160,
           'h': 158,
           'color': 'purple',
           'x': 510.0,
           'y': 160.0,
           'spray_count': 10,
           'spray_radius': 480.0,
           }
prop_templates.append(prop_template)


# ###############################################    INITIALIZATION    #################################################


print(f"Pygame component versions:")
print(f"ver - Version number as a string: {pygame.version.ver}")
print(f"vernum - Version numbers as a tuple of three ints: {pygame.version.vernum}")
print(f"rev - Repo revision of the build: {pygame.version.rev}")
print(f"SDL library version as tuple of ints: {pygame.version.SDL}")
# Note the above print as string, probably by design. To use the tuples I probabl need to refer to them as such and
# it will just work. This is owing to special internal __double_under__ methods. TEST:
(v1, v2, v3) = pygame.version.SDL
print(f"SDL main version number. version.SDL was referenced as a tuple and not as a string: {v1}")
# TEST RESULT: Confirmed. Theory proven. v1 does return the SDL main version number.


pygame.init()

# INITIALIZE THE MAIN DISPLAY SURFACE (SCREEN / WINDOW)
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# INITIALIZE MONSTERS
for monster in monsters:
    if DEBUG:
        print(f"{monster['w']}, {monster['h']}")
        monster['surface'] = pygame.Surface((monster['w'], monster['h']))
        monster['surface'].fill(monster['color'])
    else:
        imgpath = os.path.join(ASSET_PATH, monster['img'])
        monster['surface'] = pygame.image.load(imgpath).convert_alpha()

    monster['rect'] = monster['surface'].get_frect(center=(monster['x'], monster['y']))


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

        prop['rect'] = prop['surface'].get_frect(center=(prop['x'], prop['y']))

        props.append(prop)


# TEST:
generic_frect = pygame.FRect(0, 0, 10, 10)  # CONFIRMED! PyGame-CE has FRect. (PyGame does not.)


# ###############################################    MAIN EXECUTION    #################################################

bgpath = os.path.join(ASSET_PATH, BGIMG)
bg_surface = pygame.image.load(bgpath)

running = True
while running:
    # #### ####   EVENT LOOP    #### ####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # ##################################################    DRAW    ####################################################

    #display_surface.fill(BGCOLOR)  # Normally we always re-draw the BG. This is for solid fill. An image is better:
    # Paint the BG image every time. Paint the bg_surface (blit it) onto the main display_surface at coords (0, 0)
    display_surface.blit(bg_surface, (0, 0))

    # DRAW PROPS
    for prop in props:
        display_surface.blit(prop['surface'], prop['rect'])

    # DRAW MONSTERS
    for monster in monsters:
        display_surface.blit(monster['surface'], monster['rect'])

    # pygame.display.update()  # update entire surface or use  .flip() which will update only part of the surface.
    pygame.display.flip()  # Similar to update but not entire screen. TODO: Clarify


    # ################################################    PHYSICS    ###################################################
    # Calculations for new object positions, collisions, velocity changes and update of related object state.
    # CALCULATIONS FOR NEW POSITIONS, BOUNCING

    for monster in monsters:

        # RECENT TAKEAWAYS IN THIS AREA:
        # 1. FRects slightly change truth values. Don't propagate those back to your truth. Maintain truth as such.
        # 2. Source of truth is FLOAT and maintained in global, local or some other application memory.
        # 3. Rects/FRects are only intended for positioning Surfaces on screen.
        # TODO: Further test #4 assertion, I'm surprised I cannot. I tested it quite a bit. Test it more anyhow.
        # 4. You CANNOT reference AND update one of the named sides like this: monster['rect'].left += monster['xv']
        # 5. Maintain a FLOAT source of truth and keep doing this kind of thing: monster['x'] += monster['xv']
        # 6. Probably continue updating position AS FIRST MAIN LOOP STEP as done in 5. Then recalc other physics next.
        # 7. Rect/FRect is used at the time of blit, to position the Surface on the screen.


        # MOVE TRUE POSITION PER VELOCITY - Maintain the source of truth as FLOAT values in the primary data structure.
        monster['x'] += monster['xv']
        monster['y'] += monster['yv']
        # We must copy the float values and compose a new tuple to use to assign to rect.center
        newx = monster['x']
        newy = monster['y']
        # Rect or FRect both change the truth values. Rect can change them a lot when it does standard rounding when
        # converting from FLOAT to INT, but even FRect also slightly changes FLOAT values when populating the FRect.
        monster['rect'].center = (newx, newy)
        # The following debug is useful. It can show that FRects do slightly change float values.
        # If you use PyGame, you will have to use Rects which only support INTs. PyGame-CE FRects support FLOATs.
        # print(f"TRUTH: x, y        {monster['x']}, {monster['y']}")  # ----  DEBUG  ----
        # print(f"RECT: centerx, centery   {monster['rect'].centerx}, {monster['rect'].centery}")  # ----  DEBUG  ----
        # The above also shows that STANDARD ROUNDING occurs for the conversion of FLOAT to INT when rect is populated.
        # And when using FRects (get_frect), this debug shows that FRects change the truth value slightly (+- .00001 ?)
        # Two examples of how when FRect populates values, it slightly changes them:
        # TRUTH: x, y                   932.4600000000189, 355.44000000002836
        # RECT: centerx, centery        932.4600219726562, 355.44000244140625    + 0.000022
        # TRUTH: x, y                   198.38999999999842, 313.8699999999874
        # RECT: centerx, centery        198.38999938964844, 313.8699951171875    - 0.00000061
        # Differences are pretty small but if they infect truth values in loops somehow then this will cause problems.
        # There is no problem, however, if one simply follow PyGame-CE Best Practices and stored truth elsewhere as
        # full float values. To re-state it, don't use FRect/Rect values for truth and don't do any calculations which
        # use the Rect/FRect values to modify your TRUTH values, not my addition or multiplication etc. They could be
        # used for collision detection and limiting, which is their real value in some ways .. and this can still
        # affect truth, most certainly, but less directly. So be wise and avoid the most direct influences on truth
        # values by any kind of approximated value, as much as you possibly can. In our current case, we DO use
        # FRect values like left, right, top, bottom for bouncing and this does skew/currupt truth very slightly
        # becuse it affects the timing of bounce and the timing of velocity change and this affects distances traveled.
        # The point here is that you need to understand how all this works. If you do have a solid overall understanding
        # and awareness of the different interactions and effects, then when you encounter unexpected things, like
        # errors or strange behavior in edge cases (like slightly early bouncing) then you can quickly and fully
        # understand precisely what is happening and thus you can most efficiently address the issue correctly or
        # perhaps you can decide that what you are facing is all by design, well-understood and totally acceptible,
        # so no action is needed and you can move on with this complete understanding and not some problematic
        # partial understanding. Partial and mis-understandings of how your code is actually working can lead to huge
        # losses of time and bag bugs surfacing at inopportune times (in production, after a big release/promotion etc.)
        # These are words for the wise. Understand your code, fully. Debug/print statements will reveal all truth.
        # Occasionally you might need some enhanced visualization, but the bits and bytes don't lie if you shine
        # sufficient light on them.

        # BOUNCE SUBTLETIES: We bound the displaying surface at the edge, BUT we let the TRUTH VALUE possibly EXCEED
        # the boundary and stay that way, we simply reverse/bounce possibly a little bit BEYOND the screen edge.

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


pygame.quit()


##
#


# ###################################################    NOTES    ######################################################

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
# topleft              midtop               topright
# midleft      [centerx center centery]     midright
# bottomleft           midbottom            bottomright

# SIDES  (assign a single axis value):
#                        top
# left         [centerx center centery]     right
#                       bottom

# OVERALL:
# size, width, height
# w, h

# CREATE standalone OR CREATE from SURFACE
# pygame.FRect(pos, size)  # standalone
# surface.get_frect(point=pos)

# GITHUB EXPERIMENT: Changing email and username to match those previously used. Trying to solve issue with
# contribution tracking. This comment will be pushed to test the fix. FIXED. The contribution was immediately
# recognized. See the GitHub info page on how contributions tracked. Email/username MUST be correct. See the specs.
# This issue has been fixed and this comment will soon be removed.


##
#

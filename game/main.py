#! /usr/bin/env -vS python
import math

import pygame
from typing import TypedDict
import os.path
import random
import collections


# ###############################################    CONFIGURATION    ##################################################

SCREEN_WIDTH = 1280.0
SCREEN_HEIGHT = 720.0
TICKRATE = 60  # (frame rate)
GAME_TITLE = 'Space Blasto'
BGCOLOR = 'olivedrab'
BGIMG = 'lawn-bg-dark-2560x1440.jpg'  # 'grass-field-med-1920x1249.jpg'  # 'lawn-bg-dark-2560x1440.jpg'
ASSET_PATH = 'assets'  # Relative path with no trailing slash.
DEBUG = False
# List of tuples of the phase name and the phase duration in phase units (currently 1 second) TODO: Fix. FRAMES!!!!!
ENVIRO_PHASES = collections.deque(  # More efficient at popping from the left side of a list.
    [('peace', 2000), ('rogue', 400), ('chaos', 500), ('rogue', 200), ('frozen', 300)]
)  # p, r, c, f


# Using a TypedDict to satisfy MyPy recommendations for type-hinting/strong-typing.
# TypeDict for MONSTER
Monster = TypedDict('Monster', {
        'name': str,  # Monster short name
        'img': str,  # Filename of PNG (with transparency)
        'w': int,  # PNG pixel width
        'h': int,  # PNG pixel height
        'color': str,  # Debug mode color of rectangle
        'x': float,  # Initial position X value (SOON WILL NOT BE MAINTAINED. RECT WILL BECOME POSITION TRUTH)
        'y': float,  # Initial position Y value (SOON WILL NOT BE MAINTAINED. RECT WILL BECOME POSITION TRUTH)
        'v': pygame.math.Vector2,  # Velocity
        'd': pygame.math.Vector2,  # Direction
        's': float,  # Initial/default speed
        'p': float,  # Enviro: Peace (speed)
        'r': float,  # Enviro: Rogue (speed)
        'c': float,  # Enviro: Chaos (speed)
        'f': float,  # Enviro: Frozen (speed)
        'xv': float,  # Velocity X value (SOON MAY NOT BE MAINTAINED. 'd' and 's' MAY REPLACE)
        'yv': float,  # Velocity Y value (SOON MAY NOT BE MAINTAINED. 'd' and 's' MAY REPLACE)
        'surface': pygame.Surface,  # The PyGame-CE Surface object - Displays the image and more
        'rect': pygame.FRect,  # The PyGame-CE FRect object - Positions the Surface and more
        })

# MONSTER DATA - Initial state for a handful of entities that move, experience physics and interact. W/initial motion.
monsters = []
monster: Monster = {'name': 'red-flower-floaty',
           'img':  'red-flower-66x64.png',
           'w': 66,
           'h': 64,
           'color': 'red1',
           'x': 240.0,
           'y': 300.0,
           'v': None,
           'd': None,
           's': 1.0,
           'p': 1.0,
           'r': 1.0,
           'c': 3.5,
           'f': 0.002,
           'xv': -0.624,
           'yv': 0.782,
           'surface': None,
           'rect': None,
           }
monsters.append(monster)
monster: Monster = {'name': 'red-flower-drifty',
           'img':  'red-flower-66x64.png',
           'w': 66,
           'h': 64,
           'color': 'orangered',
           'x': 240.0,
           'y': 300.0,
           'v': None,
           'd': None,
           's': 1.0,
           'p': 1.0,
           'r': 1.0,
           'c': 4.2,
           'f': 0.003,
           'xv': 0.137,
           'yv': -0.991,
           'surface': None,
           'rect': None,
           }
monsters.append(monster)
monster: Monster = {'name': 'goldie',
           'img': 'gold-retriever-160x142.png',
           'w': 160,
           'h': 142,
           'color': 'gold',
           'x': 500.0,
           'y': 300.0,
           'v': None,
           'd': None,
           's': 1.41,
           'p': 1.6,
           'r': 8.8,
           'c': 12.9,
           'f': 0.008,
           'xv': 1.0,
           'yv': 1.0,
           'surface': None,
           'rect': None,
           }
monsters.append(monster)
monster: Monster = {'name': 'fishy',
           'img':  'goldfish-280x220.png',
           'w': 280,
           'h': 220,
           'color': 'darkgoldenrod1',
           'x': 840.0,
           'y': 300.0,
           'v': None,
           'd': None,
           's': 1.0,
           'p': 0.9,
           'r': 1.0,
           'c': 5.0,
           'f': 0.001,
           'xv': -0.114,
           'yv': -0.994,
           'surface': None,
           'rect': None,
           }
monsters.append(monster)
monster: Monster = {'name': 'grumpy',
           'img':  'grumpy-cat-110x120.png',
           'w': 110,
           'h': 120,
           'color': 'blanchedalmond',
           'x': 780.0,
           'y': 300.0,
           'v': None,
           'd': None,
           's': 1.0,
           'p': 0.8,
           'r': 0.05,
           'c': 7.7,
           'f': 0.0,
           'xv': 0.261,
           'yv': 0.966,
           'surface': None,
           'rect': None,
           }
monsters.append(monster)


# TypedDict for PROP_TEMPLATE
PropTemplate = TypedDict('PropTemplate', {
        'name': str,
        'img': str,
        'w': int,
        'h': int,
        'color': str,
        'x': float,
        'y': float,
        'spray_count': int,
        'spray_radius': float,
        'surface': pygame.Surface,
        'rect': pygame.FRect,
        })

# PROP DATA - Initial state for a handful of non-moving props. Includes specs for random instantiation (spraying).
prop_templates = []
prop_template: PropTemplate = {'name': 'red-flower',
           'img':  'red-flower-66x64.png',
           'w': 66,
           'h': 64,
           'color': 'crimson',
           'x': 640.0,
           'y': 360.0,
           'spray_count': 40,
           'spray_radius': 600.0,
           'surface': None,
           'rect': None,
           }
prop_templates.append(prop_template)
prop_template: PropTemplate = {'name': 'blue-flower',
           'img':  'blue-flower-160x158.png',
           'w': 160,
           'h': 158,
           'color': 'darkturquoise',
           'x': 510.0,
           'y': 160.0,
           'spray_count': 10,
           'spray_radius': 480.0,
           'surface': None,
           'rect': None,
           }
prop_templates.append(prop_template)

# TypedDict for PROP. Props are generated dynamically, when we "spray" props from their template.
Prop = TypedDict('Prop', {
        'name': str,
        'img': str,
        'w': int,
        'h': int,
        'color': str,
        'x': float,
        'y': float,
        'surface': pygame.Surface,
        'rect': pygame.FRect,
        })


# ###############################################    INITIALIZATION    #################################################

pygame.init()

# INITIALIZE THE MAIN DISPLAY SURFACE (SCREEN / WINDOW)
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# INITIALIZE MONSTERS
for monster in monsters:
    if DEBUG:
        monster['surface'] = pygame.Surface((monster['w'], monster['h']))
        monster['surface'].fill(monster['color'])
        # Instantiate the velocity vector with the TRUTH xv and yv values. This initial stub may soon change.
        monster['v'] = pygame.math.Vector2(monster['xv'], monster['yv'])
        monster['d'] = pygame.math.Vector2(monster['xv'], monster['yv'])  # Direction. New feature. Evolving rapidly.
        monster['s'] = math.sqrt((monster['xv']**2 + monster['yv']**2))  # Speed. New feature. Evolving rapidly.
    else:
        imgpath = os.path.join(ASSET_PATH, monster['img'])
        monster['surface'] = pygame.image.load(imgpath).convert_alpha()
        # Instantiate the velocity vector with the TRUTH xv and yv values. This initial stub may soon change.
        monster['v'] = pygame.math.Vector2(monster['xv'], monster['yv'])
        monster['d'] = pygame.math.Vector2(monster['xv'], monster['yv'])  # Direction. New feature. Evolving rapidly.
        monster['s'] = math.sqrt((monster['xv']**2 + monster['yv']**2))  # Speed. New feature. Evolving rapidly.

    monster['rect'] = monster['surface'].get_frect(center=(monster['x'], monster['y']))
    # print(f"Monster speed: {monster['s']}")  # ----  DEBUG  ----


# INITIALIZE PROPS - 'SPRAY' REPLICATED PROPS (randomly within specified radius, to specified count)
props = []
for prop_t in prop_templates:
    for index in range(prop_t['spray_count']):  # We will use the index for a unique prop name. Not critical.
        # We must create a NEW prop dictionary object each time, otherwise they would all be the same reference.
        prop: Prop = {'img': prop_t['img'],  # Copy the unchanging attributes from the template before handling dynamic ones.
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


# ###############################################    MAIN EXECUTION    #################################################

bgpath = os.path.join(ASSET_PATH, BGIMG)

if DEBUG:
    bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_surface.fill(BGCOLOR)
else:
    bg_surface = pygame.image.load(bgpath)

running = True
ephase = None
ephase_name = None
ephase_count = 0  # 0, not None since we will likly first/always do an arithmetic check on it, not an existence check.
clock = pygame.time.Clock()

while running:
    clock.tick(TICKRATE)
    # #### ####   EVENT LOOP    #### ####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ENVIRONMENT PHASE PROCESSING - Rotate enviro sequence. Modify monster behavior per their enviro-reaction profiles.
    if ephase is None:
        ephase = ENVIRO_PHASES[0]
        print(f"LOADING ENVIRO PHASE: {ephase}")
        ephase_name = ephase[0]
        ephase_count = ephase[1]
        print(f"EPHASE name: {ephase_name}    EPHASE name: {ephase_count}")
        cut_ephase = ENVIRO_PHASES.popleft()
        # TODO: Is it correct to say "move the top of the stack to the bottom" .. figure it out and make it correct.
        ENVIRO_PHASES.append(cut_ephase)  # Move the top of stack to the bottom. Phases endlessly repeat.
        print(f"ENVIRO_PHASES: {ENVIRO_PHASES}")
    else:
        # APPLY THE EFFECTS HERE - MONSTERS CHANGE THEIR SPEEDS
        for monster in monsters:
            if ephase_name == 'peace':
                monster['s'] = monster['p']
            elif ephase_name == 'rogue':
                monster['s'] = monster['r']
            elif ephase_name == 'chaos':
                monster['s'] = monster['c']
            elif ephase_name == 'frozen':
                monster['s'] = monster['f']
            else:
                monster['s'] = 10.0  # Extremely fast, for debugging. A bad ephase name, causes extreme monster speed.

        ephase_count -= 1  # Decrement the counter. TODO: SECONDS?? FRAMES??
        if ephase_count % 100 == 0:
            print(ephase_count)
        # NOW CHECK IF ephase_count is 0 - IF 0: Make ephase = None, so we trigger loading of the next phase
        if ephase_count < 1:
            ephase = None


    # ##################################################    DRAW    ####################################################

    # REDRAW THE BG
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


        # MOVE TRUE POSITION PER VELOCITY - Maintain the source of truth as FLOAT values in the primary data structure.
        # monster['x'] += monster['xv']
        # monster['y'] += monster['yv']
        # newx = monster['x']
        # newy = monster['y']
        # monster['rect'].center = (newx, newy)

        # NEW WAY USING VECTORS - While moving experimentally towards using the FRect for a less-accurate truth:

        # We still need to maintain the truth values .. but, with FRect accuracy to 4 or 5 decimal places (float does
        # remain much more accurat than that .. but 4 or 5 in FRect may be sufficient) .. then with that AND also
        # the convenience of vectors, the plan is to EXPLORE the use of the rect to maintain truth. This will
        # relegate x, y, xv, yv attributes to being initial state only and then after that the objects rect will be
        # the source of truth. THIS WILL BE AN EXPERIMENT AT FIRST. We can always go back to maintaining truth in
        # the fully-float-capable object data structures. Do we need accuracies on the scale of one-ten-thousandth of
        # a pixel and greater? In some applications, absolutely! But in games? Maybe most of the time we do not need
        # that accuracy and the many types of convenience of FRect/Rect in PyGame-CE will lead to the decision to
        # use the FRect as source of truth (in most cases.) I can see things going that way, at least initially. I may
        # leave concisely-commented stubs in place where one can easily go back to maintaining a much more accurate
        # source of truth (on position and velocity, mostly, we are talking about here.)
        monster['x'] += monster['xv']
        monster['y'] += monster['yv']
        # Then we can very simply update position and don't necessarily need the above step to maintain the orig. truth.
        # print(monster['v'])  # ----  DEBUG  ----
        monster['rect'].center += monster['v']

        # EXPERIMENT - USE DIRECTION VECTOR AND SPEED.
        # NOTE: Our direction vectors have not been minimized and our use and calculation of speed was a quick take
        # based on basic mathematics (pythagorean theorem: a**2 + b**2 = c**2  (a^2 + b^2 = c^2 in other notation)
        # So the above becomes:
        monster['rect'].center += (monster['d'] * monster['s'])
        # This makes sense as the direction should be a set of velocities on x and y which amount to a speed of
        # travel forward of 1 unit. This is the case where the velocity components have been minimized. And then
        # one 'scales' the direction vector by the scalar float value for speed.
        # Based on this, I think my calculation for speed is correct.
        # Now, for following commits, I suspect Vector2 offers a method for the pythagorean calculation I did.
        # We will use the built-in method equivalents for this next and then do some cleanup now since this full
        # adoption of vectors is falling in to place. As mentioned, I will leave most of the full float truth
        # stuff maintained and in the data structures for now.


        # Bounce off LEFT wall in X Axis
        if monster['rect'].left <= 0:
            monster['rect'].left = 0  # Great! We don't touch the TRUTH VALUE. We do bound the Surface on screen.
            monster['xv'] = monster['xv'] * -1
            # Experimental transition to using vectors: We need to update the vector here too:
            # IMPORTANT: Can/should we update using methods rather than instantiate a new/replacement object?
            # monster['v'] = pygame.math.Vector2(monster['xv'], monster['yv'])
            # Now lets try simply updating the Vector2 instance by calling its update() method:
            monster['v'].update(monster['xv'], monster['yv'])
            monster['d'].update(monster['xv'], monster['yv'])  # Update direction vector too. Experimental.
            monster['s'] = math.sqrt((monster['xv'] ** 2 + monster['yv'] ** 2))  # Update Speed. New feature/Experimtl.

        # Bounce off RIGHT wall in X Axis
        if monster['rect'].right >= SCREEN_WIDTH:
            monster['rect'].right = SCREEN_WIDTH  # Great! We don't touch the TRUTH VALUE. We do bound the Surface.
            monster['xv'] = monster['xv'] * -1
            # Experimental transition to using vectors: We need to update the vector here too:
            # IMPORTANT: Can/should we update using methods rather than instantiate a new/replacement object?
            # monster['v'] = pygame.math.Vector2(monster['xv'], monster['yv'])
            # Now lets try simply updating the Vector2 instance by calling its update() method:
            monster['v'].update(monster['xv'], monster['yv'])
            monster['d'].update(monster['xv'], monster['yv'])  # Update direction vector too. Experimental.
            monster['s'] = math.sqrt((monster['xv'] ** 2 + monster['yv'] ** 2))  # Update Speed. New feature/Experimtl.

        # Bounce off TOP wall in Y Axis
        if monster['rect'].top <= 0:
            monster['rect'].top = 0  # Great! We don't touch the TRUTH VALUE. We do bound the Surace on screen.
            monster['yv'] = monster['yv'] * -1
            # Experimental transition to using vectors: We need to update the vector here too:
            # IMPORTANT: Can/should we update using methods rather than instantiate a new/replacement object?
            # monster['v'] = pygame.math.Vector2(monster['xv'], monster['yv'])
            # Now lets try simply updating the Vector2 instance by calling its update() method:
            monster['v'].update(monster['xv'], monster['yv'])
            monster['d'].update(monster['xv'], monster['yv'])  # Update direction vector too. Experimental.
            monster['s'] = math.sqrt((monster['xv'] ** 2 + monster['yv'] ** 2))  # Update Speed. New feature/Experimtl.
        # Bounce off BOTTOM wall in Y Axis
        if monster['rect'].bottom >= SCREEN_HEIGHT:
            monster['rect'].bottom = SCREEN_HEIGHT  # Great! We don't touch the TRUTH VALUE. We do bound the Surface.
            monster['yv'] = monster['yv'] * -1
            # Experimental transition to using vectors: We need to update the vector here too:
            # IMPORTANT: Can/should we update using methods rather than instantiate a new/replacement object?
            # monster['v'] = pygame.math.Vector2(monster['xv'], monster['yv'])
            # Now lets try simply updating the Vector2 instance by calling its update() method:
            monster['v'].update(monster['xv'], monster['yv'])
            monster['d'].update(monster['xv'], monster['yv'])  # Update direction vector too. Experimental.
            monster['s'] = math.sqrt((monster['xv'] ** 2 + monster['yv'] ** 2))  # Update Speed. New feature/Experimtl.


pygame.quit()


##
#


# ###################################################    NOTES    ######################################################




##
#

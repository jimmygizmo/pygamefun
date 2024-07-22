#! /usr/bin/env -vS python
import math

import pygame
from typing import TypedDict
import os.path
import random
import collections
# import sys  # Temproarily not used, but I'm sure it will be. Was used for sys.exit(1) but now we raise Exception.


# ###############################################    CONFIGURATION    ##################################################

SCREEN_WIDTH = 1280.0
SCREEN_HEIGHT = 720.0
TICKRATE = 60  # (frame rate) - 0/None gives maximum/unlimited. Depends on code but recently saw 500-1000 FPS.
GAME_TITLE = 'Space Blasto'
BGCOLOR = 'olivedrab'
BGIMG = 'lawn-bg-dark-2560x1440.jpg'  # 'grass-field-med-1920x1249.jpg'  # 'lawn-bg-dark-2560x1440.jpg'
ASSET_PATH = 'assets'  # Relative path with no trailing slash.
DEBUG = False
# List of tuples of the phase name and the phase duration in phase units (currently 1 second) TODO: Fix. FRAMES!!!!!
ENVIRO_PHASES = collections.deque(  # More efficient at popping from the left side of a list.
    [('peace', 800), ('rogue', 160), ('chaos', 400), ('frozen', 60), ('rogue', 50), ('frozen', 110)]
)  # p, r, c, f
# ANOTHER PERSPECTIVE: ephases are sort of motion-modification macros on a timer schedule that repeats (currently.)
ACID_MODE = False  # Suppress background re-painting. This makes objects leave psychedelic trails for a fun effect.


# Using a TypedDict to satisfy MyPy recommendations for type-hinting/strong-typing.
# TypeDict for MONSTER
Monster = TypedDict('Monster', {
        'name': str,  # Monster short name
        'img': str,  # Filename of PNG (with transparency)
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
        'w': int,  # PNG pixel width
        'h': int,  # PNG pixel height
        'color': str,  # Debug mode color of rectangle
        'x': float,  # Initial position X value
        'y': float,  # Initial position Y value
        'd': pygame.math.Vector2,  # Direction
        's': float,  # Initial/default speed
        'p': float,  # Enviro: Peace (speed)
        'r': float,  # Enviro: Rogue (speed)
        'c': float,  # Enviro: Chaos (speed)
        'f': float,  # Enviro: Frozen (speed)
        'surface': pygame.Surface,  # The PyGame-CE Surface object - Displays the image and more
        'surface_r': pygame.Surface,  # The PyGame-CE Surface object - Displays the image and more  (RIGHT direction)
        'rect': pygame.FRect,  # The PyGame-CE FRect object - Positions the Surface and more
        })

# MONSTER DATA - Initial state for a handful of entities that move, experience physics and interact. W/initial motion.
monsters = []

monster1: Monster = {'name': 'red-flower-floaty',
           'img':  'red-flower-66x64.png',
           'flip': False,
           'w': 66,
           'h': 64,
           'color': 'red1',
           'x': 240.0,
           'y': 300.0,
           'd': pygame.math.Vector2((-0.624, 0.782)),  # placeholder instance (mypy)
           's': 100.0,
           'p': 100.0,
           'r': 100.0,
           'c': 350.0,
           'f': 2.0,
           'surface': pygame.Surface((0, 0)),  # placeholder instance (mypy)  -  Default/LEFT-facing
           'surface_r': pygame.Surface((0, 0)),  # placeholder instance (mypy)  -  RIGHT-facing (generated)
           'rect': pygame.FRect(),  # placeholder instance (mypy)
           }
monsters.append(monster1)
monster2: Monster = {'name': 'red-flower-drifty',
           'img':  'red-flower-66x64.png',
           'flip': True,
           'w': 66,
           'h': 64,
           'color': 'orangered',
           'x': 240.0,
           'y': 300.0,
           'd': pygame.math.Vector2((0.137, -0.991)),  # placeholder instance (mypy)
           's': 100.0,
           'p': 100.0,
           'r': 100.0,
           'c': 420.0,
           'f': 3.0,
           'surface': pygame.Surface((0, 0)),  # placeholder instance (mypy)  -  Default/LEFT-facing
           'surface_r': pygame.Surface((0, 0)),  # placeholder instance (mypy)  -  RIGHT-facing (generated)
           'rect': pygame.FRect(),  # placeholder instance (mypy)
           }
monsters.append(monster2)
monster3: Monster = {'name': 'goldie',
           'img': 'gold-retriever-160x142.png',
           'flip': True,
           'w': 160,
           'h': 142,
           'color': 'gold',
           'x': 500.0,
           'y': 300.0,
           'd': pygame.math.Vector2((1.0, 1.0)),  # placeholder instance (mypy)
           's': 141.0,
           'p': 160.0,
           'r': 880.0,
           'c': 1290.0,
           'f': 10.0,
           'surface': pygame.Surface((0, 0)),  # placeholder instance (mypy)  -  Default/LEFT-facing
           'surface_r': pygame.Surface((0, 0)),  # placeholder instance (mypy)  -  RIGHT-facing (generated)
           'rect': pygame.FRect(),  # placeholder instance (mypy)
           }
monsters.append(monster3)
monster4: Monster = {'name': 'fishy',
           'img':  'goldfish-280x220.png',
           'flip': False,
           'w': 280,
           'h': 220,
           'color': 'darkgoldenrod1',
           'x': 840.0,
           'y': 300.0,
           'd': pygame.math.Vector2((-0.994, -0.114)),  # placeholder instance (mypy)
           's': 80.0,
           'p': 90.0,
           'r': 100.0,
           'c': 700.0,
           'f': 2850.0,
           'surface': pygame.Surface((0, 0)),  # placeholder instance (mypy)  -  Default/LEFT-facing
           'surface_r': pygame.Surface((0, 0)),  # placeholder instance (mypy)  -  RIGHT-facing (generated)
           'rect': pygame.FRect(),  # placeholder instance (mypy)
           }
monsters.append(monster4)
monster5: Monster = {'name': 'grumpy',
           'img':  'grumpy-cat-110x120.png',
           'flip': True,
           'w': 110,
           'h': 120,
           'color': 'blanchedalmond',
           'x': 780.0,
           'y': 300.0,
           'd': pygame.math.Vector2((0.261, 0.966)),  # placeholder instance (mypy)
           's': 90.0,
           'p': 80.0,
           'r': 50.0,
           'c': 2170.0,
           'f': 40.0,
           'surface': pygame.Surface((0, 0)),  # placeholder instance (mypy)  -  Default/LEFT-facing
           'surface_r': pygame.Surface((0, 0)),  # placeholder instance (mypy)  -  RIGHT-facing (generated)
           'rect': pygame.FRect(),  # placeholder instance (mypy)
           }
monsters.append(monster5)


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
prop_template1: PropTemplate = {'name': 'red-flower',
           'img':  'red-flower-66x64.png',
           'w': 66,
           'h': 64,
           'color': 'crimson',
           'x': 640.0,
           'y': 360.0,
           'spray_count': 40,
           'spray_radius': 600.0,
           'surface': pygame.Surface((0, 0)),  # placeholder instance (mypy)
           'rect': pygame.FRect(),  # placeholder instance (mypy)
           }
prop_templates.append(prop_template1)
prop_template2: PropTemplate = {'name': 'blue-flower',
           'img':  'blue-flower-160x158.png',
           'w': 160,
           'h': 158,
           'color': 'darkturquoise',
           'x': 510.0,
           'y': 160.0,
           'spray_count': 10,
           'spray_radius': 480.0,
           'surface': pygame.Surface((0, 0)),  # placeholder instance (mypy)
           'rect': pygame.FRect(),  # placeholder instance (mypy)
           }
prop_templates.append(prop_template2)

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
    else:
        imgpath = os.path.join(ASSET_PATH, monster['img'])
        monster['surface'] = pygame.image.load(imgpath).convert_alpha()
        if monster['flip']:
            monster['surface'] = pygame.transform.flip(monster['surface'], True, False)
        # Generate the RIGHT-facing surface
        monster['surface_r'] = pygame.transform.flip(monster['surface'], True, False)

    monster['rect'] = monster['surface'].get_frect(center=(monster['x'], monster['y']))


# INITIALIZE PROPS - 'SPRAY' REPLICATED PROPS (randomly within specified radius, to specified count)
props = []
for prop_t in prop_templates:
    for index in range(prop_t['spray_count']):  # We will use the index for a unique prop name. Not critical.
        prop: Prop = {'name': '',  # placeholder (mpypy)
                'img': prop_t['img'],  # Copy the unchanging attributes from the template before handling dynamic ones.
                'w': prop_t['w'],
                'h': prop_t['h'],
                'color': prop_t['color'],
                'x': 0.0,  # placeholder (mpypy)
                'y': 0.0,  # placeholder (mpypy)
                'surface': pygame.Surface((0, 0)),  # placeholder instance (mypy)
                'rect': pygame.FRect(),  # placeholder instance (mypy)
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
keys = []  # Why declared here? For some rare edge-cases it MIGHT be needed for and, before loop is a common place.
ephase_count = 0  # 0, not None since we will likly first/always do an arithmetic check on it, not an existence check.
clock = pygame.time.Clock()

#   * * * * * * * * * * * * * * * * * * * *
#   * * * * * *    MAIN LOOP    * * * * * *
#   * * * * * * * * * * * * * * * * * * * *
while running:
    delta_time = clock.tick(TICKRATE) / 1000  # Seconds elapsed for a single frame (e.g. - 60 Frm/sec = 0.017 sec/Frm)
    # print(f"delta_time - duration of one frame - (seconds): {delta_time}")  # ----  DEBUG  ----


    # ##################################################    INPUT    ###################################################
    # pygame.key    pygame.mouse


    # #### ####   EVENT LOOP    #### ####
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN:
        #     print(f"A key was depressed. Unknown if released or how long pressed.    KEY #: {event.key}    KEY unicode character: {event.unicode}")
        # if event.type == pygame.MOUSEMOTION:
        #     print(f"Mouse is moving.    Position: {event.pos}")
        #     (monsters[3]['rect'].centerx, monsters[3]['rect'].centery) = event.pos  # Just stick the fish at the mouse pos, for now.

        # Just stick the fish at the mouse pos, for now.      Now using pygame.mouse.get_pos()      (and not events)
        # (monsters[3]['rect'].centerx, monsters[3]['rect'].centery) = pygame.mouse.get_pos()  # Crude but works great.

        # print(f"Mouse buttons pressed: {pygame.mouse.get_pressed()}")  # Returns (bool, bool, bool) for the 3 buttons.

        # print(f"Mouse relative speed: {pygame.mouse.get_rel()}")

        # It's important to use the following list properly.
        keys = pygame.key.get_pressed()
        last_direction_x = monsters[3]['d'].x


        # print(f"Returns a HUGE list of all keys, bool values: pygame.key.get_pressed: {keys}")
        # This is how you are supposed to use this list, via the K_ constants (which hold the int index position of the key in this list)
        # if keys[pygame.K_ESCAPE]:
        #     print(f"ESCAPE key pressed. Exiting game. Buh bye!")
        #     running = False
        # if keys[pygame.K_LEFT] and monsters[3]['d'].x > 0:
        #     monsters[3]['d'].x = -1
        #     monsters[3]['surface'] = pygame.transform.flip(monsters[3]['surface'], True, False)
        # if keys[pygame.K_RIGHT] and monsters[3]['d'].x < 0:
        #     monsters[3]['d'].x = 1
        #     monsters[3]['surface'] = pygame.transform.flip(monsters[3]['surface'], True, False)
        # if keys[pygame.K_UP]:
        #     monsters[3]['d'].y = -1
        # if keys[pygame.K_DOWN]:
        #     monsters[3]['d'].y = 1

        # Another interesting alternate control method:
        monsters[3]['d'].x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        # To understand this, note that int(True) = 1 and int(False) = 0 and keys[] are bools. 1-0 = 1, 0-1 = -1. Bingo!
        # Now for the vertical direction
        monsters[3]['d'].y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        # To illustrate the diagonal speed-differential we will fix next:
        # print(f"Velocity magnitude = Linear speed forward: {(monsters[3]['d'] * monsters[3]['s']).magnitude()}")
        # NOTE: Just referencing Vector2.magnitude will not work. It is a method. Do: mag = Vector2.magnitude()

        # We must NORMALIZE the direction vector
        # TODO: The IF logic may not be correct for our code. Confirm with video tutorial at 1:49:41 approx.
        #     The if-else here stems from the idea that you cannot call normalize() when (x, y) = (0, 0).
        #     TODO: Confirm that initial premise, then look closer at the if-else logic. The way I chose to initialize
        #     direction may be different from the video and therefore might require different logic here for edge case.
        # UPDATE: Maybe better to say "cannot normalize a vector of length 0".
        # IN PYGAME: Only a Vector2(0, 0) can be FALSE. ALL OTHER Vector 2 values other than (0, 0) are TRUE.
        monsters[3]['d'] = monsters[3]['d'].normalize() if monsters[3]['d'] else monsters[3]['d']
        # That all pretty much confirms and clarifys how this works. We just need to confirm our initialization.
        # It is looking like the if-else will stay as is.

        # print(f"FIXED: Linear speed forward: {(monsters[3]['d'] * monsters[3]['s']).magnitude()}")
        # You can see it is fixed. The 40% speed boost when going diagonally no longer occurs. Cool.

        # Now we can FLIP the SPRITE - IF THE SIGN OF THE X DIRECTION HAS CHANGED FROM BEFORE THE INPUT.
        # TODO: This solution seems imperfect. I'm almost sure there is are some bouncing/other edge-cases this
        #     does not handle in the current design, but this is a start:
        multiplied_directions = monsters[3]['d'].x * last_direction_x
        print(f"multiplied: {multiplied_directions}    dir: {monsters[3]['d'].x}    last_dir: {last_direction_x}")  # ----  DEBUG  ----
        # if multiplied_directions < 0:  # Then they have different signs and X direction has changed, so FLIP.
        #     monsters[3]['surface'] = pygame.transform.flip(monsters[3]['surface'], True, False)
        # UPDATE: Hardly works.
        #     It flips --occasionally--. So this is a very buggy implementation and needs work.
        # POSSIBLE PROBLEM, -0.0 is not detected. So we will modify the if. Example:
        # multiplied: -0.0    dir: 0.0    last_dir: -1.0
        # Trying to fix this by just flipping the logic of the if because then we don't even consider 0.0 OR -0.0.
        # Like this (as opposed to above, commented out):
        if not (multiplied_directions > 0):  # Then they have different signs and X direction has changed, so FLIP.
            monsters[3]['surface'] = pygame.transform.flip(monsters[3]['surface'], True, False)
        # Lol, this is a funny series of bugs centering around the needed logic here. NOW, it flips a lot BUT
        # only gets the direction right about 1 out of 3 or 4 times. It flips frantically and rarely ends up in the
        # correct directions, SO clearly we are on the WRONG path with how we are multiplying to detect changed in
        # direction. Now it is time to step back a little from that quick first attempt and think more about a good
        # solution.
        # Perhaps, our original if-else input processing was in-fact better.
        # One reason we are in this situation with flipping is because we are using the "cute/efficient" input
        # processing   int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]).
        # Maybe we should not use that and go back to the more traditional if-else.
        # The performance impacts need to be considerd. These are most certainly performance-critical areas inside
        # a tight real-time loop in a performance-critical app. There is a reason we are experimenting and fully
        # exploring different strategies and considering all aspects, including future performance concerns.

        # THE NEXT DAY. I stepped back from the flipping problem above and I think it is something that needs to
        # occur during the draw phase. We could say this: First we determine motion and physics and the new state of it,
        # partially based on input, and then we have all the data we need to draw. So, the flipped status of the sprite,
        # which is the direction it is pointing (currently only considering the horizontal) is a matter of drawing
        # correctly. So bottom line is we handle it in the drawing phase. Let's move all that there and see if we can
        # also come up with a better way of detecting direction change or even better .. simply prepare the two needed
        # sprites and then based on the current direction, simply paint the correct surface. This is almost certainly
        # much more efficient than repeatedly performing the flipping operation.
        # TODO: 1. Move flipping to draw phase. 2. Pre-prepare the flipped surface so you have both. 3 Improve logic
        #    and/or simply paint the correct surface rather than flipping a single one.  4. To allow initial sprites
        #    to face either left or right, but to require the standard that the initial loaded sprite face LEFT,
        #    provide a flag to trigger flipping of the sprite upon initial image load. When used, the new flipped
        #    (flipped again) image for the RIGHT direction will then be correct. This saves the need to use an image
        #    editing program to do this, although one is likely being used anyhow in order to get good custom sprites.
        #    Nonethless this is a good feature and this overall design pattern is looking excellent, prior to
        #    implementation.


    # ENVIRONMENT PHASE PROCESSING - Rotate enviro sequence. Modify monster behavior per their enviro-reaction profiles.
    if ephase is None:
        ephase = ENVIRO_PHASES[0]
        ephase_name = ephase[0]
        ephase_count = ephase[1]
        cut_ephase = ENVIRO_PHASES.popleft()
        ENVIRO_PHASES.append(cut_ephase)
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
                raise ValueError(f"FATAL: Invalid ephase_name \"{ephase_name}\". "
                        "Check values in ENVIRO_PHASES config.")
            # TODO: This could -almost- be raised as a KeyError. Later, if we implement OrderedDict, it literally would
            #     be a KeyError exception in the kind of processing I am envisioning.
            #     (Currently we use a custom list-of-tuples strategy, but OrderedDict would make sense. The processing
            #     code would be quite different of course and using a built-in KeyError, via a dict get() method
            #     would be central to that different processing.
            #
            # NOTE: Another good option for the type of exception here could be ValueError. It means the type is correct
            #     but the value is invalid. I have used these a lot in the past and they make sense, especially if you
            #     need to distinguish from some other cases you may be lumping together under the generic Exception().

        ephase_count -= 1  # Decrement the counter for the current phase.
        if ephase_count < 1:
            ephase = None


    # ##################################################    DRAW    ####################################################

    # REDRAW THE BG
    if ACID_MODE is False:
        display_surface.blit(bg_surface, (0, 0))

    # DRAW PROPS
    for prop in props:
        display_surface.blit(prop['surface'], prop['rect'])

    # DRAW MONSTERS
    for monster in monsters:
        if monster['d'].x <= 0:
            display_surface.blit(monster['surface'], monster['rect'])  # LEFT-facing
        else:
            display_surface.blit(monster['surface_r'], monster['rect'])  # RIGHT-facing


    # pygame.display.update()  # update entire surface or use  .flip() which will update only part of the surface.
    pygame.display.flip()  # Similar to update but not entire screen. TODO: Clarify


    # ################################################    PHYSICS    ###################################################

    for monster in monsters:
        # ***************************
        # WORKING ON THIS MYPY ERROR:
        # delta_vector = pygame.Vector2(monster['d'] * monster['s'])  # SEEN AS A tuple[float, float] - SAME
        delta_vector = monster['d'] * monster['s'] * delta_time
        # MYPY ERROR HERE - TRICKY ONE:
        # main.py:365: error: Incompatible types in assignment (expression has type "Vector2",
        #     variable has type "tuple[float, float]")  [assignment]
        monster['rect'].center += delta_vector
        # ***************************

        # Bounce off LEFT wall in X Axis
        if monster['rect'].left <= 0:
            monster['rect'].left = 0
            monster['d'].x *= -1
            # Now the drawing phase automatically handles the direction to fact, LEFT vs. RIGHT.
            # This is no-longer needed:
            # monster['surface'] = pygame.transform.flip(monster['surface'], True, False)

        # Bounce off RIGHT wall in X Axis
        if monster['rect'].right >= SCREEN_WIDTH:
            monster['rect'].right = SCREEN_WIDTH
            monster['d'].x *= -1
            # Now the drawing phase automatically handles the direction to fact, LEFT vs. RIGHT.
            # This is no-longer needed:
            # monster['surface'] = pygame.transform.flip(monster['surface'], True, False)

        # Bounce off TOP wall in Y Axis
        if monster['rect'].top <= 0:
            monster['rect'].top = 0
            monster['d'].y *= -1

        # Bounce off BOTTOM wall in Y Axis
        if monster['rect'].bottom >= SCREEN_HEIGHT:
            monster['rect'].bottom = SCREEN_HEIGHT
            monster['d'].y *= -1


pygame.quit()


##
#


# ###################################################    NOTES    ######################################################

# GREAT page on Python Exceptions:
# https://docs.python.org/3/library/exceptions.html

# For those developing Python on Windows. Now with WSL/Ubuntu live all the time on my Windows 10/11 dev machines,
# I am now just as happy as when using a Mac. Almost no difference. By the way, I heavily use IntelliJ IDEs like PyCharm.
# So, on your Windows, you will want to install WSL:
# https://learn.microsoft.com/en-us/windows/wsl/install

# I'll add much more info on setting up the ultimate Windows Python/Full-Stack/Open-Source Developers Workstation.
# I'll provide the same for Mac. Docker will be involved for some use-cases. There will be MUCH more info than just
# the WSL link above. I work hard on fine-tuning the ultimate development environments, so you will want to check this
# topic area out independently of this PyGame-CE project.


# Interesting input handling - found via stackexchange:
# https://github.com/rik-cross/pygamepal/blob/main/src/pygamepal/input.py


##
#

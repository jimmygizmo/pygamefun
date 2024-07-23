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


# #############################################    CLASS DEFINITIONS    ################################################

# Now we start to make this program Object-Oriented and start using classes. In PyGame, this means using "Sprites".

class Player(pygame.sprite.Sprite):
    def __init__(self, player_spec: Monster):
        super().__init__()
        self.player_spec: Monster = player_spec
        self.image: pygame.Surface = pygame.Surface((0, 0))
        self.image_r: pygame.Surface = pygame.Surface((0, 0))  # POSSIBLY, this might be a separate instance of Player. Not clear yet.
        self.rect: pygame.FRect = pygame.FRect()

        if DEBUG:
            self.image = pygame.Surface((self.player_spec['w'], self.player_spec['h']))
            self.image.fill(self.player_spec['color'])
        else:
            self.imgpath: str = os.path.join(ASSET_PATH, self.player_spec['img'])  # Var added for clarity. Don't need.
            self.image = pygame.image.load(self.imgpath).convert_alpha()
            if self.player_spec['flip']:
                self.image = pygame.transform.flip(self.image, True, False)
        # Generate the RIGHT-facing surface
        self.image_r = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_frect(center=(self.player_spec['x'], self.player_spec['y']))










# ###############################################    INITIALIZATION    #################################################

pygame.init()

# INITIALIZE THE MAIN DISPLAY SURFACE (SCREEN / WINDOW)
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# Test class usage
test_instance_of_player_class = Player(monsters[3])


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

keys: pygame.key.ScancodeWrapper = pygame.key.ScancodeWrapper()  # All this required to satisfy strict typing of MyPy.
# Originally the above was simply keys = [], which we dont even necessarily need here, but this var MIGHT be good to be available at this scope or at the start of the loop before being freshly re-populated. (Last-keys analysis of change etc.)

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

        keys = pygame.key.get_pressed()  # For now, until we re-architect movement control, get_pressed() works best.
        # keys = pygame.key.get_just_pressed()  # Still not perfect, when trying to limit repeated key presses.?
        # TODO: We will use timers to make the single-press capture work. We'll do this later.
        #     Currently get_just_pressed() is giving us TWO key presses each time, maybe three. Not what we want.
        # UPDATE - PROBLEM: Introduced a problem where we often miss double key-presses where I go diagonal, LEFT+UP for
        #     example. This makes sense. It is not a perfect mechanism. Getting 2 missiles fired and messing up our
        #     use of simultaneous key controls for diagonal etc. SO, Handling key presses NEEDS WORK!

        # Primary (somewhat "cute") input control method. Prior to this I used an if-else cascade which is also good.
        monsters[3]['d'].x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        # To understand this, note that int(True) = 1 and int(False) = 0 and keys[] are bools. 1-0 = 1, 0-1 = -1. Bingo!
        # Now for the vertical direction
        monsters[3]['d'].y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        # We must NORMALIZE the direction vector and cannot do this when it has a length of 0, hence the truth check.
        # Only one Vector2 can be Falsy and that is (0, 0) with all else being Truthy.
        monsters[3]['d'] = monsters[3]['d'].normalize() if monsters[3]['d'] else monsters[3]['d']
        # I do like one-line if-else structures like this. Very nice for situations like this, especially when the true
        # case predominates and occurs much more frequently than the false case. Then the context matches how you
        # encounter it and read it very nicely. And hey, it's nice and compact as well as elegant.
        # In some special cases it can read/look weird and I would say that it does not work as well when the action
        # in the first part is more of a rare occurance. For rare occurances, I think it might be better to use multi-
        # lines. It all depends. If you had a a LOT of these, then regardless of the frequency, it might work very very
        # nicely to have to many checks done on one line in one place. It's a clear & tidy pattern for many situations.

        if keys[pygame.K_SPACE]:
            # print('fire laser')
            pass


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

        # Bounce off RIGHT wall in X Axis
        if monster['rect'].right >= SCREEN_WIDTH:
            monster['rect'].right = SCREEN_WIDTH
            monster['d'].x *= -1

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

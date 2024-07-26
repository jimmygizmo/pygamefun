#! /usr/bin/env -vS python
import math

import pygame
from typing import TypedDict
import os.path
import random
import collections
from typing import Union


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

LEGACY_MODE = True  # To be used during transition to using Classes/Sprites. Can be removed after transition.


PlayerSpec = TypedDict('PlayerSpec', {
        'name': str,  # Player short name
        'instance_id' : int,  # 0-based Int serial number unique to each instance of Player created. -1 means no instance created for this spec yet. (Jumping through MyPy hoops. Can't use None.) We are transitioning to OOP. This will all change.
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


NpcSpec = TypedDict('NpcSpec', {
        'name': str,  # NPC short name
        'instance_id' : int,  # 0-based Int serial number unique to each instance of Entity created. -1 means no instance created for this spec yet. (Jumping through MyPy hoops. Can't use None.) We are transitioning to OOP. This will all change.
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

# NPC DATA - Initial state for a handful of NPCs that move, experience physics and interact. W/initial motion.
npc_specs = []

npc1: NpcSpec = {
           'name': 'red-flower-floaty',
           'instance_id': -1,
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
npc_specs.append(npc1)
npc2: NpcSpec = {
           'name': 'red-flower-drifty',
           'instance_id': -1,
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
npc_specs.append(npc2)
npc3: NpcSpec = {
           'name': 'goldie',
           'instance_id': -1,
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
npc_specs.append(npc3)
npc4: NpcSpec = {
           'name': 'fishy',
           'instance_id': -1,
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
npc_specs.append(npc4)
npc5: NpcSpec = {
           'name': 'grumpy',
           'instance_id': -1,
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
npc_specs.append(npc5)


# TypedDict for PROP_TEMPLATE
PropTemplate = TypedDict('PropTemplate', {
        'name': str,
        'img': str,
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
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
prop_template1: PropTemplate = {
           'name': 'red-flower',
           'img':  'red-flower-66x64.png',
           'flip': False,
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
prop_template2: PropTemplate = {
           'name': 'blue-flower',
           'img':  'blue-flower-160x158.png',
           'flip': False,
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
PropSpec = TypedDict('PropSpec',{
        'name': str,
        'instance_id' : int,  # 0-based Int serial number unique to each instance of Entity created. -1 means no instance created for this spec yet. (Jumping through MyPy hoops. Can't use None.) We are transitioning to OOP. This will all change.
        'img': str,
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
        'w': int,
        'h': int,
        'color': str,
        'x': float,
        'y': float,
        'surface': pygame.Surface,
        'rect': pygame.FRect,
        })

# TODO: Add a tumble weed prop and a wind force for those. Each responds at differnet speeds possibly based on size.
#     This shows why Prop class also inherits from Entity. Props are like monsters that might often sit still but the
#     don't need all the monster features. They need physics features. Props are sort of just one step up from Entity.
#     Entity is currently not intended to be instantiated and only sub-classed. It's about code organization and how
#     that code gets used and to what degree it gets customized etc. etc. Right now I don't see Entity ever being
#     instantiated as it is just a repository of common code for anything that moves and reacts to physics and
#     environmental influences on the screen.
# NOTE: Another term for "sub-class" is to "extend" a class. There exists other equivalent terminology. I will update
# notes in this project with more info on terminology like this used in the context of different programming languages.
# There is always some flexibility nowadays as so many developers do many different langauges and learn terminology
# from so many different educational sources. I will distill things down to the "best" terminology as I have been a
# part of the evolution of the industry and used so many languages for so many decades. (Coding for most of 44 years
# as I started quite young with BASIC, Pascal and Foretran and have used nearly all languages projessionally with
# a lot of Python, Javascript, Perl, C Sharp, C, C++, Java, Visual Basic, and many frameworks, protocols and more.)
# This puts me in a good position to distill down what I can say is a "Best Practice" usage of terminology and in
# what contexts for what audiences.


# #############################################    CLASS DEFINITIONS    ################################################

# Now we start to make this program Object-Oriented and start using classes. In PyGame, this means using "Sprites".

# TODO: Entity is a base concept, below Monster. We need to rename EntitySpec to MonsterSpec etc. PropSpec is OK.
#     We'll be adding other Specs too I think like maybe a PlayerSpec. THIS IS NOW BEING DONE IN --THIS-- COMMIT

class Entity(pygame.sprite.Sprite):  # TODO: Add PlayerSpec soon.
    def __init__(self, groups, spec: NpcSpec | PropSpec):
        # TODO: We could append prop group the groups list here since each class will always assign at least their own group.
        super().__init__(groups)
        # self.spec: PlayerSpec | NpcSpec | PropSpec = spec  # PlayerSpec coming soon.
        self.spec: NpcSpec | PropSpec = spec
        self.image: pygame.Surface = pygame.Surface((0, 0))
        self.image_r: pygame.Surface = pygame.Surface((0, 0))  # POSSIBLY, this might be a separate instance of Player. Not clear yet.
        self.rect: pygame.FRect = pygame.FRect()
        self.keys: list[int] = [0]  # Placeholder. MyPy gymnastics. Do we really have to do this all the time now for MyPy? I like None much better for pre-initialization.

        if DEBUG:
            self.image = pygame.Surface((self.spec['w'], self.spec['h']))
            self.image.fill(self.spec['color'])
        else:
            self.imgpath: str = os.path.join(ASSET_PATH, self.spec['img'])  # Var added for clarity. Don't need.
            self.image = pygame.image.load(self.imgpath).convert_alpha()
            if self.spec['flip']:
                self.image = pygame.transform.flip(self.image, True, False)
        # Generate the RIGHT-facing surface
        self.image_r = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_frect(center=(self.spec['x'], self.spec['y']))

    def update(self):
        pass
        self.keys = pygame.key.get_pressed()  # TODO: Maybe self.keys? It won't shadow with the outer scope keys goes away later.

        # As an interim technique, I'll maintain truth inside the spec object we put in the instance.
        self.spec['d'].x = int(self.keys[pygame.K_RIGHT]) - int(self.keys[pygame.K_LEFT])
        self.spec['d'].y = int(self.keys[pygame.K_DOWN]) - int(self.keys[pygame.K_UP])

        self.spec['d'] = self.spec['d'].normalize() if self.spec['d'] else self.spec['d']

        if keys[pygame.K_SPACE]:
            # print('fire laser')
            pass



# The plan is to have an Entity base class and then sub-class for Monster, Prop, Player. BUT since I have not finalized
# how to separate out the attributes and or have any that stay unused in the base class for some time .. to get started,
# I will simply copy the Entity class and then let the divergence of those and formation of Entity base class just
# happen naturally. We are about to start adding methods.




class Npc(Entity):
    def __init__(self, groups, spec: NpcSpec):
        # TODO: We could append prop group the groups list here since each class will always assign at least their own group.
        super().__init__(groups, spec)
        self.spec: PropSpec = spec
        self.image: pygame.Surface = pygame.Surface((0, 0))
        # self.image_r: pygame.Surface = pygame.Surface((0, 0))  *** REMOVED from cloned Entity code. *** - This is a prop.
        self.rect: pygame.FRect = pygame.FRect()

        # TODO: Since this is a prop, we probably do not need to generate the right-facing surface, but the flip feature is good.

        if DEBUG:
            self.image = pygame.Surface((self.spec['w'], self.spec['h']))
            self.image.fill(self.spec['color'])
        else:
            self.imgpath: str = os.path.join(ASSET_PATH, self.spec['img'])  # Var added for clarity. Don't need.
            self.image = pygame.image.load(self.imgpath).convert_alpha()
            if self.spec['flip']:
                self.image = pygame.transform.flip(self.image, True, False)
        # Generate the RIGHT-facing surface - *** REMOVED from cloned Entity code. *** - This is a prop.

        self.rect = self.image.get_frect(center=(self.spec['x'], self.spec['y']))

    def update(self):
        print(f"NPC/prop {self.spec['name']} is being updated")





class Prop(Entity):
    def __init__(self, groups, spec: PropSpec):
        # TODO: We could append prop group the groups list here since each class will always assign at least their own group.
        super().__init__(groups, spec)
        self.spec: PropSpec = spec
        self.image: pygame.Surface = pygame.Surface((0, 0))
        # self.image_r: pygame.Surface = pygame.Surface((0, 0))  *** REMOVED from cloned Entity code. *** - This is a prop.
        self.rect: pygame.FRect = pygame.FRect()

        # TODO: Since this is a prop, we probably do not need to generate the right-facing surface, but the flip feature is good.

        if DEBUG:
            self.image = pygame.Surface((self.spec['w'], self.spec['h']))
            self.image.fill(self.spec['color'])
        else:
            self.imgpath: str = os.path.join(ASSET_PATH, self.spec['img'])  # Var added for clarity. Don't need.
            self.image = pygame.image.load(self.imgpath).convert_alpha()
            if self.spec['flip']:
                self.image = pygame.transform.flip(self.image, True, False)
        # Generate the RIGHT-facing surface - *** REMOVED from cloned Entity code. *** - This is a prop.

        self.rect = self.image.get_frect(center=(self.spec['x'], self.spec['y']))

    def update(self):
        print(f"NPC/prop {self.spec['name']} is being updated")






# ###############################################    INITIALIZATION    #################################################

pygame.init()

# INITIALIZE THE MAIN DISPLAY SURFACE (SCREEN / WINDOW)
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

# The prefix "all_" works well to identify these as sprite groups by convention in this app. Especially during our transition.
# At least for now, I want to use 'monsters' or 'props' etc as objects/lists to hold either the spec objects or the instances.
# eventually I think such lists will go away (or maybe not .. but probably since we can leverage sprite classes in custom ways
# .. for the totality of iteration needs, we will remain to be seen..)
all_sprites: pygame.sprite.Group = pygame.sprite.Group()
all_monsters: pygame.sprite.Group = pygame.sprite.Group()
all_props: pygame.sprite.Group = pygame.sprite.Group()
all_players: pygame.sprite.Group = pygame.sprite.Group()


# INITIALIZE NPCs - LEGACY (not OOP)
for npc_spec in npc_specs:
    if DEBUG:
        npc_spec['surface'] = pygame.Surface((npc_spec['w'], npc_spec['h']))
        npc_spec['surface'].fill(npc_spec['color'])
    else:
        imgpath = os.path.join(ASSET_PATH, npc_spec['img'])
        npc_spec['surface'] = pygame.image.load(imgpath).convert_alpha()
        if npc_spec['flip']:
            npc_spec['surface'] = pygame.transform.flip(npc_spec['surface'], True, False)
    # Generate the RIGHT-facing surface
    npc_spec['surface_r'] = pygame.transform.flip(npc_spec['surface'], True, False)

    npc_spec['rect'] = npc_spec['surface'].get_frect(center=(npc_spec['x'], npc_spec['y']))

# INITIALIZE PROPS - 'SPRAY' REPLICATED PROPS (randomly within specified radius, to specified count)
prop_specs = []
for prop_t in prop_templates:
    for index in range(prop_t['spray_count']):  # We will use the index for a unique prop name. Not critical.
        prop_spec: PropSpec = {
                'name': prop_t['name'] + str(index),  # Unique name of generated (sprayed) prop_spec. (Compared to npc_spec which are hardcoded.)
                'instance_id': -1,  # -1 means instance not instantiated yet.
                'img': prop_t['img'],  # Copy the unchanging attributes from the template before handling dynamic ones.
                'flip': False,
                'w': prop_t['w'],
                'h': prop_t['h'],
                'color': prop_t['color'],
                'x': 0.0,  # placeholder (mpypy)
                'y': 0.0,  # placeholder (mpypy)
                'surface': pygame.Surface((0, 0)),  # placeholder instance (mypy)
                'rect': pygame.FRect(),  # placeholder instance (mypy)
                }

        diameter = 2.0 * prop_t['spray_radius']  # This variable makes it easier to read/understand. Inline for perf.
        prop_spec['name'] = prop_t['name'] + "-" + str(index)
        x_offset = random.uniform(0.0, diameter) - prop_t['spray_radius']  # uniform() gives a random float value
        y_offset = random.uniform(0.0, diameter) - prop_t['spray_radius']  # uniform() includes the limits
        prop_spec['x'] = prop_t['x'] + x_offset
        prop_spec['y'] = prop_t['y'] + y_offset

        if DEBUG:
            prop_spec['surface'] = pygame.Surface((prop_spec['w'], prop_spec['h']))
            prop_spec['surface'].fill(prop_spec['color'])
        else:
            imgpath = os.path.join(ASSET_PATH, prop_spec['img'])
            prop_spec['surface'] = pygame.image.load(imgpath).convert_alpha()

        prop_spec['rect'] = prop_spec['surface'].get_frect(center=(prop_spec['x'], prop_spec['y']))

        prop_specs.append(prop_spec)

        # print(prop_spec)  # ----  DEBUG  ----


# ################################################    INSTANTIATION    #################################################

# INSTANTIATE NPCs - OOP - Classes/PyGame Sprites    (Leaving out the DEBUG features for now.)

# We dynamically generate (spray) prop_specs from prop_templates, but we are moving towards phasing out prop_spec
# objects and using only sprite groups and sprite class instances. So, can look at moving some of the prop_spec
# generation code (for spraying etc) down here to 'instantiate props'. The goal would be to do it all here and
# eliminate the need for prop_spec objects. (Similarly we are moving towards eliminating the need for npc_spec
# objects too.

# INSTANITATE PROPS
props: list[Prop] = []
for i, prop_spec in enumerate(prop_specs):
    prop_spec['instance_id'] = i
    imgpath = os.path.join(ASSET_PATH, prop_spec['img'])
    prop: Prop = Prop([all_sprites, all_props], prop_spec)  # PyCharm FALSE WARNING HERE (AbstractGroup)
    props.append(prop)  # Although considered for removal in lieu of sprite groups, I see reasons to keep such lists.

# INSTANITATE MONSTERS
monsters: list[Entity] = []
for i, npc_spec in enumerate(npc_specs):
    npc_spec['instance_id'] = i
    imgpath = os.path.join(ASSET_PATH, npc_spec['img'])
    monster: Entity = Entity([all_sprites, all_monsters], npc_spec)  # PyCharm FALSE WARNING HERE (AbstractGroup)
    monsters.append(monster)  # Although considered for removal in lieu of sprite groups, I see reasons to keep such lists.



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

    # Check all new events since the last main loop iteration
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # BUG FIX NOTE: When I added this LEGACY_MODE if-switch, I also moved this OUT of the event loop.
    # This was a non-obvious indentation bug. All my code comments actually made it hard to see, hence why I
    # frequently clean up my code comments and move them in to notes files for possible use in documentation later.
    # This never should have been inside the event loop. It was not a horrible bug and only caused some weird
    # edge-case behavior with bouncing while holding down keys etc. Anyhow, fixing it did change behavior when
    # input-controlled player hits a wall. No big deal. Code is more correct now and all this will be changing soon.
    if LEGACY_MODE:
        keys = pygame.key.get_pressed()

        npc_specs[3]['d'].x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        npc_specs[3]['d'].y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        npc_specs[3]['d'] = npc_specs[3]['d'].normalize() if npc_specs[3]['d'] else npc_specs[3]['d']

        if keys[pygame.K_SPACE]:
            # print('fire laser')
            pass


    # ENVIRONMENT PHASE PROCESSING - Rotate enviro sequence. Modify npc_spec behavior per their enviro-reaction profiles.
    if ephase is None:
        ephase = ENVIRO_PHASES[0]
        ephase_name = ephase[0]
        ephase_count = ephase[1]
        cut_ephase = ENVIRO_PHASES.popleft()
        ENVIRO_PHASES.append(cut_ephase)
    else:
        # APPLY THE EFFECTS HERE - NPCs CHANGE THEIR SPEEDS
        for npc_spec in npc_specs:
            if ephase_name == 'peace':
                npc_spec['s'] = npc_spec['p']
            elif ephase_name == 'rogue':
                npc_spec['s'] = npc_spec['r']
            elif ephase_name == 'chaos':
                npc_spec['s'] = npc_spec['c']
            elif ephase_name == 'frozen':
                npc_spec['s'] = npc_spec['f']
            else:
                raise ValueError(f"FATAL: Invalid ephase_name '{ephase_name}'. "
                        "Check values in ENVIRO_PHASES config.")

        ephase_count -= 1  # Decrement the counter for the current phase.
        if ephase_count < 1:
            ephase = None


    # ##################################################    DRAW    ####################################################

    # NEW for OOP:
    all_sprites.update()

    if LEGACY_MODE:
        # REDRAW THE BG
        if ACID_MODE is False:
            display_surface.blit(bg_surface, (0, 0))

        # DRAW PROPS
        for prop_spec in prop_specs:
            display_surface.blit(prop_spec['surface'], prop_spec['rect'])

        # DRAW NPCs
        for npc_spec in npc_specs:
            if npc_spec['d'].x <= 0:
                display_surface.blit(npc_spec['surface'], npc_spec['rect'])  # LEFT-facing
            else:
                display_surface.blit(npc_spec['surface_r'], npc_spec['rect'])  # RIGHT-facing

    # NEW for OOP:
    all_sprites.draw(display_surface)


    # pygame.display.update()  # update entire surface or use  .flip() which will update only part of the surface.
    pygame.display.flip()  # Similar to update but not entire screen. TODO: Clarify


    # ################################################    PHYSICS    ###################################################

    for npc_spec in npc_specs:
        # ***************************
        # WORKING ON THIS MYPY ERROR:
        # delta_vector = pygame.Vector2(npc_spec['d'] * npc_spec['s'])  # SEEN AS A tuple[float, float] - SAME
        delta_vector = npc_spec['d'] * npc_spec['s'] * delta_time
        # MYPY ERROR HERE - TRICKY ONE:
        # main.py:365: error: Incompatible types in assignment (expression has type "Vector2",
        #     variable has type "tuple[float, float]")  [assignment]
        npc_spec['rect'].center += delta_vector
        # ***************************

        # Bounce off LEFT wall in X Axis
        if npc_spec['rect'].left <= 0:
            npc_spec['rect'].left = 0
            npc_spec['d'].x *= -1

        # Bounce off RIGHT wall in X Axis
        if npc_spec['rect'].right >= SCREEN_WIDTH:
            npc_spec['rect'].right = SCREEN_WIDTH
            npc_spec['d'].x *= -1

        # Bounce off TOP wall in Y Axis
        if npc_spec['rect'].top <= 0:
            npc_spec['rect'].top = 0
            npc_spec['d'].y *= -1

        # Bounce off BOTTOM wall in Y Axis
        if npc_spec['rect'].bottom >= SCREEN_HEIGHT:
            npc_spec['rect'].bottom = SCREEN_HEIGHT
            npc_spec['d'].y *= -1


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

# IMPORTANT!
# Union type in type hinting solves the problem of allowing None pre-initialization vales and also of allowing
# multiple/different similar types as passed arguments. I will solve both these problems using this.
# There is a compact syntax now we can use which is extremely intuitive. I love it! Go Python! Go MyPy! Go strong typing!
# https://medium.com/@apps.merkurev/union-type-expression-in-python-50a1b7d012cd

# NOW WE CAN:
# def f(lst: list[int | str], param: int | None) -> float | str:
#     return ''
#
# f([1, 'abc'], None)


##
#

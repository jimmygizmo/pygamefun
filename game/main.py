#! /usr/bin/env -vS python

import pygame
from typing import TypedDict
import os.path
import random
import collections


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

# PLAYER DATA - Initial state for a single player (usually) or possibly multiple players.
player_specs = []

player1: PlayerSpec = {
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
player_specs.append(player1)


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
npc_specs.append(npc4)


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
        })


# #############################################    CLASS DEFINITIONS    ################################################


class Entity(pygame.sprite.Sprite):  # TODO: Add PlayerSpec soon.
    def __init__(self,
                 groups,
                 spec: PlayerSpec | NpcSpec | PropSpec,
                 x: float,
                 y: float,
                 direction: pygame.math.Vector2,
                 speed: float,
                 ):
        # self.spec: PlayerSpec | NpcSpec | PropSpec = spec  # PlayerSpec coming soon.
        self.spec: PlayerSpec | NpcSpec | PropSpec = spec  # Phasing out most/all of this. Separately, Spec dicts are being simplified.
        self.x: float = x
        self.y: float = y
        self.dir: pygame.math.Vector2 = direction  # Direction
        self.speed: float = speed  # Speed
        self.image: pygame.Surface = pygame.Surface((0, 0))  # Active image (depending on direction of motion)
        self.image_l: pygame.Surface = pygame.Surface((0, 0))  # Left-facing copy of the image for motion. DEFAULT.
        self.image_r: pygame.Surface = pygame.Surface((0, 0))  # Right-facing copy of the image for motion. Generated.
        self.rect: pygame.FRect = pygame.FRect()
        super().__init__(groups)  # super.update() could be done first before setting all the self.* but for now I have them last.

        if DEBUG:
            self.image_l = pygame.Surface((self.spec['w'], self.spec['h']))
            self.image_l.fill(self.spec['color'])
        else:
            self.imgpath: str = os.path.join(ASSET_PATH, self.spec['img'])  # Var added for clarity. Don't need.
            self.image_l = pygame.image.load(self.imgpath).convert_alpha()
            if self.spec['flip']:
                self.image_l = pygame.transform.flip(self.image_l, True, False)  # Happens once at init.
            # The loaded image should be facing left and if not, use the 'flip' option. The right-facing version is
            # generated after the image is loaded and optionally flipped. Don't use flip on images already facing left.

        # Props TODO: For efficiency, since we could have MANY props, detect PropSpec type and then don't generate this:
        self.image_r = pygame.transform.flip(self.image_l, True, False)  # Generate right-facing surface.

        # CONCERN: I think this is where I will fix a bug where the rect appears to have not been initialized.
        # It would not have been, so I know it is a good fix. ** BUT ** my concern is about the fix and the actual
        # FRext it references. I will watch and see if we have a problem in only one direction.
        # If we DO have a problem (and that is an IF) then the fix might be we have to set the rect every time we
        # set the image based on direction. (so we get the reference to the SAME FRect). Updates to the FRect for
        # motion are the concern. Is the FRect we get good with all the updates? Is it the same FRect reference or at
        # some step did it become a new object and thus did not get all position, speed or direction updates.
        # Easily enough detected and fixed if this is the case.
        #self.rect = self.image.get_frect(center=(self.x, self.y))  # THIS WAS A BUG
        self.rect = self.image_l.get_frect(center=(self.x, self.y))  # Hopefully the above concerns don't apply here.
        # Initial tests show this appears to be working fine. We could log the address of the objects to be sure.

    def update(self, delta_time: float, ephase_name: str):
        # TODO: Articulate the reason we have to make the update signatures match. NOTE: ephase_name ARG had to be added
        #     to places it is not actually used. (* PyCharm static analysis warning *)

        delta_vector = self.dir * self.speed * delta_time
        # MYPY ERROR HERE - TRICKY ONE:
        # main.py:365: error: Incompatible types in assignment (expression has type "Vector2",
        #     variable has type "tuple[float, float]")  [assignment]
        self.rect.center += delta_vector
        # ***************************

        # Bounce off LEFT wall in X Axis
        if self.rect.left <= 0:
            self.rect.left = 0
            self.dir.x *= -1

        # Bounce off RIGHT wall in X Axis
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.dir.x *= -1

        # Bounce off TOP wall in Y Axis
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dir.y *= -1

        # Bounce off BOTTOM wall in Y Axis
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.dir.y *= -1

        # Activate the correctly-facing image, based on X direction.
        if self.dir.x < 0:
            self.image = self.image_l
        else:
            self.image = self.image_r


class Player(Entity):
    def __init__(self,
                 groups,
                 spec: PlayerSpec,
                 x: float,
                 y: float,
                 direction: pygame.math.Vector2,
                 speed: float,
                 ):
        # self.keys: list[int] = [0]  # Placeholder. MyPy gymnastics. Do we really have to do this all the time now for MyPy? I like None much better for pre-initialization.
        self.keys: pygame.key.ScancodeWrapper = pygame.key.ScancodeWrapper()  # BETTER than the above?
        super().__init__(groups, spec, x, y, direction, speed)  # super.update() could be done first before setting all the self.* but for now I have them last.

    def update(self, delta_time: float, ephase_name: str):
        enviro_influence(self, ephase_name)

        self.keys = pygame.key.get_pressed()  # *** MyPy ERROR suggests that self.keys maybe should be ScancodeWrapper ???
        self.dir.x = int(self.keys[pygame.K_RIGHT]) - int(self.keys[pygame.K_LEFT])
        self.dir.y = int(self.keys[pygame.K_DOWN]) - int(self.keys[pygame.K_UP])

        self.dir = self.dir.normalize() if self.dir  else self.dir

        if self.keys[pygame.K_SPACE]:
            print('fire laser')

        # NOTE: WE UPDATE BASED ON INPUT --BEFORE-- WE CHECK FOR WALL COLLISION/BOUNCING (in super/Entity).
        # TODO: Is this the order of processing we want? Is it the same as legacy? I think yes and yes, but CONFIRM!
        super().update(delta_time, ephase_name)


class Npc(Entity):
    def __init__(self,
                 groups,
                 spec: NpcSpec,
                 x: float,
                 y: float,
                 direction: pygame.math.Vector2,
                 speed: float,
                 ):
        super().__init__(groups, spec, x, y, direction, speed)  # super.update() can be done before or after setting any self.* but think about how it might matter! Maybe not at all.

    def update(self, delta_time: float, ephase_name: str):
        enviro_influence(self, ephase_name)
        super().update(delta_time, ephase_name)


class Prop(Entity):
    def __init__(self,
                 groups,
                 spec: PropSpec,
                 x: float,
                 y: float,
                 ):
        prop_zero_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)  # Props special case direction, to init Entity.
        prop_zero_speed: float = 0.0  # Props special case speed, to init Entity.
        super().__init__(groups, spec, x, y, prop_zero_direction, prop_zero_speed)  # super.update() can be done before or after setting any self.* but think about how it might matter! Maybe not at all.

    def update(self, delta_time: float, ephase_name: str):
        super().update(delta_time, ephase_name)


# #############################################    FUNCTION DEFINITIONS    #############################################

# *** MyPy ERROR about PropSpec dict has no keys for p,r,c,f - BUT PropSpec WILL **NEVER** BE PASSED HERE !!! ???
def enviro_influence(xself: Player | Npc, ephase_name: str) -> None:
    # ENVIRO PHASES - APPLICATION OF INFLUENCE OF CURRENT PHASE
    if ephase_name == 'peace':
        xself.speed = xself.spec['p']  # Use of Spec dicts is being minimized, but this maybe remain as a good one.
    elif ephase_name == 'rogue':
        xself.speed = xself.spec['r']  # Use of Spec dicts is being minimized, but this maybe remain as a good one.
    elif ephase_name == 'chaos':
        xself.speed = xself.spec['c']  # Use of Spec dicts is being minimized, but this maybe remain as a good one.
    elif ephase_name == 'frozen':
        xself.speed = xself.spec['f']  # Use of Spec dicts is being minimized, but this maybe remain as a good one.
    else:
        raise ValueError(f"FATAL: Invalid ephase_name '{ephase_name}'. "
                         "Check values in ENVIRO_PHASES config.")


# ###############################################    INITIALIZATION    #################################################

pygame.init()

# INITIALIZE THE MAIN DISPLAY SURFACE (SCREEN / WINDOW)
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_TITLE)

all_sprites: pygame.sprite.Group = pygame.sprite.Group()
all_players: pygame.sprite.Group = pygame.sprite.Group()
all_npcs: pygame.sprite.Group = pygame.sprite.Group()
all_props: pygame.sprite.Group = pygame.sprite.Group()

# GENERATE PROP SPECS - 'SPRAY' REPLICATED PROPS (randomly within specified radius, to specified count)
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
                }

        diameter = 2.0 * prop_t['spray_radius']  # This variable makes it easier to read/understand. Inline for perf.
        prop_spec['name'] = prop_t['name'] + "-" + str(index)
        x_offset = random.uniform(0.0, diameter) - prop_t['spray_radius']  # uniform() gives a random float value
        y_offset = random.uniform(0.0, diameter) - prop_t['spray_radius']  # uniform() includes the limits
        prop_spec['x'] = prop_t['x'] + x_offset
        prop_spec['y'] = prop_t['y'] + y_offset

        # print(prop_spec)  # ----  DEBUG  ----
        prop_specs.append(prop_spec)


# ################################################    INSTANTIATION    #################################################

# INSTANTIATE ALL THE TYPES OF ENTITIES - OOP - Classes/PyGame Sprites    (Leaving out the DEBUG features for now.)

# TODO: See if we can move the prop spec (spraying/generation) code inside of prop instantiation. Probably can/should.

# INSTANITATE PLAYER(S)
players: list[Player] = []
for i, player_spec in enumerate(player_specs):
    player_spec['instance_id'] = i
    imgpath = os.path.join(ASSET_PATH, player_spec['img'])
    player: Player = Player( groups=[all_sprites, all_players],
                             spec=player_spec,
                             x=player_spec['x'],
                             y=player_spec['y'],
                             direction=player_spec['d'],
                             speed=player_spec['s'],
                             )  # PyCharm FALSE WARNING HERE (AbstractGroup)
    players.append(player)  # Although considered for removal in lieu of sprite groups, I see reasons to keep such lists.

# INSTANITATE NPCs
npcs: list[Npc] = []
for i, npc_spec in enumerate(npc_specs):
    npc_spec['instance_id'] = i
    imgpath = os.path.join(ASSET_PATH, npc_spec['img'])
    npc: Npc = Npc( groups=[all_sprites, all_npcs],
                    spec=npc_spec,
                    x=npc_spec['x'],
                    y=npc_spec['y'],
                    direction=npc_spec['d'],
                    speed=npc_spec['s'],
                    )  # PyCharm FALSE WARNING HERE (AbstractGroup)
    npcs.append(npc)

# INSTANITATE PROPS
props: list[Prop] = []
for i, prop_spec in enumerate(prop_specs):
    prop_spec['instance_id'] = i
    imgpath = os.path.join(ASSET_PATH, prop_spec['img'])
    prop: Prop = Prop( groups=[all_sprites, all_props],
                       spec=prop_spec,
                       x=prop_spec['x'],
                       y=prop_spec['y'],
                       )  # PyCharm FALSE WARNING HERE (AbstractGroup)
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
g_ephase_name = None

ephase_count = 0  # 0, not None since we will likly first/always do an arithmetic check on it, not an existence check.
clock = pygame.time.Clock()


#   * * * * * *    MAIN LOOP    * * * * * *
while running:
    g_delta_time = clock.tick(TICKRATE) / 1000  # Seconds elapsed for a single frame (e.g. - 60 Frm/sec = 0.017 sec/Frm)


    # ##################################################    INPUT    ###################################################

    for event in pygame.event.get():  # Check all new events since the last main loop iteration
        if event.type == pygame.QUIT:
            running = False


    # #######################################    ENVIRONMENT PHASE PROCESSING    #######################################

    # ENVIRO_PHASES is a collections.deque instance and we popleft() the first/current 'phase'.
    #     Then we add the phase we removed from the left/start of the (deque) to the end (right side/last position).
    if ephase is None:
        ephase = ENVIRO_PHASES[0]
        g_ephase_name = ephase[0]
        ephase_count = ephase[1]
        cut_ephase = ENVIRO_PHASES.popleft()
        ENVIRO_PHASES.append(cut_ephase)
    else:
        ephase_count -= 1  # Decrement the counter for the current phase.
        if ephase_count < 1:
            ephase = None


    # ##################################################    DRAW    ####################################################


    #   ^ ^ ^ ^ ^ ^    MAIN UPDATE ACTIONS    ^ ^ ^ ^ ^ ^
    all_props.update(g_delta_time, g_ephase_name)
    all_npcs.update(g_delta_time, g_ephase_name)
    all_players.update(g_delta_time, g_ephase_name)

    # REDRAW THE BG
    if ACID_MODE is False:
        display_surface.blit(bg_surface, (0, 0))

    #   | | | | | |    MAIN DRAWING ACTIONS    | | | | | |
    all_props.draw(display_surface)
    all_npcs.draw(display_surface)
    all_players.draw(display_surface)

    pygame.display.flip()  # Similar to update but not entire screen. TODO: Clarify


    # ################################################    PHYSICS    ###################################################

    # All physics/motion code now in Entity update() and/or Player or Npc update(). This section marker may go away.


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

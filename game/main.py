#! /usr/bin/env -vS python

import pygame
from typing import TypedDict
import os.path
import random
import collections


# ###############################################    CONFIGURATION    ##################################################

SCREEN_WIDTH = 1640.0
SCREEN_HEIGHT = 860.0
TICKRATE = 60  # (frame rate) - 0/None gives maximum/unlimited. Depends on code but recently saw 500-1000 FPS.
GAME_TITLE = 'Space Blasto'
BGCOLOR = 'olivedrab'
BGIMG = 'lawn-bg-dark-2560x1440.jpg'  # 'grass-field-med-1920x1249.jpg'  # 'lawn-bg-dark-2560x1440.jpg'
ASSET_PATH = 'assets'  # Relative path with no trailing slash.
DEBUG = False
ACID_MODE = False  # Suppress background re-painting. This makes objects leave psychedelic trails for a fun effect.
LASER_COOLDOWN_DURATION = 100  # Milliseconds - minimum time between laser firing

# List of tuples of the phase name and the phase duration in frames/iterations. collections.deque.popleft() is said
# to be efficient at popping from the left side of a list. I'm just giving it a try. There are many ways to rotate a list.
ENVIRO_PHASES = collections.deque([
     ('peace', 800),
     ('rogue', 160),
     ('chaos', 400),
     ('frozen', 60),
     ('rogue', 50),
     ('frozen', 110),
     ]
)  # The equivalent Spec keys for these phases are simply the first letters of the phase names: p, r, c, f


PlayerSpec = TypedDict('PlayerSpec',
    {
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
    }
)  # PlayerSpec

# PLAYER DATA - Initial state for a single player (usually) or possibly multiple players.
player_specs: list[PlayerSpec] = [
    {
        'name': 'buck',
        'instance_id': -1,
        'img':  'rocket-200x252.png',
        'flip': False,
        'w': 200,
        'h': 252,
        'color': 'aqua',
        'x': 890.0,
        'y': 540.0,
        'd': pygame.math.Vector2((-0.994, -0.114)),  # placeholder instance (mypy)
        's': 80.0,
        'p': 90.0,
        'r': 100.0,
        'c': 700.0,
        'f': 1650.0,
    },
]  # player_specs: list[PlayerSpec]


WeaponSpec = TypedDict('WeaponSpec',
    {
        'name': str,  # Weapon/projectile short name
        'instance_id' : int,  # 0-based Int serial number unique to each instance of Weapon created. -1 means no instance created for this spec yet. (Jumping through MyPy hoops. Can't use None.) We are transitioning to OOP. This will all change.
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
    }
)  # WeaponSpec

# WEAPON/PROJECTILE DATA - Initial state for a weapon/projectile
weapon_specs: list[WeaponSpec] = [
    {
        'name': 'orb',
        'instance_id': -1,
        'img':  'green-ball-140x140.png',
        'flip': False,
        'w': 140,
        'h': 140,
        'color': 'green3',
        'x': 890.0,
        'y': 260.0,
        'd': pygame.math.Vector2((0.0, -1.0)),  # placeholder instance (mypy)
        's': 134.0,
        'p': 98.0,
        'r': 122.0,
        'c': 840.0,
        'f': 2350.0,
    },
]  # weapon_specs: list[WeaponSpec]


NpcSpec = TypedDict('NpcSpec',
    {
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
    }
)  # NpcSpec

# NPC DATA - Initial state for a handful of NPCs that move, experience physics and interact. W/initial motion.
npc_specs: list[NpcSpec] = [
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
    {
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
    },
]  # npc_specs: list[NpcSpec]


# TypedDict for PROP_TEMPLATE
PropTemplate = TypedDict('PropTemplate',
    {
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
    }
)  # PropTemplate

# PROP DATA - Initial state for a handful of non-moving props. Includes specs for random instantiation (spraying).
prop_templates: list[PropTemplate] = [
    {
       'name': 'red-flower',
       'img':  'red-flower-66x64.png',
       'flip': False,
       'w': 66,
       'h': 64,
       'color': 'crimson',
       'x': 804.0,
       'y': 440.0,
       'spray_count': 60,
       'spray_radius': 780.0,
    },
    {
       'name': 'blue-flower',
       'img':  'blue-flower-160x158.png',
       'flip': False,
       'w': 160,
       'h': 158,
       'color': 'darkturquoise',
       'x': 880.0,
       'y': 360.0,
       'spray_count': 18,
       'spray_radius': 680.0,
    },
]  # prop_templates: list[PropTemplate]

# TypedDict for PROP. Props are generated dynamically, when we "spray" props from their template.
PropSpec = TypedDict('PropSpec',
    {
        'name': str,
        'instance_id' : int,  # 0-based Int serial number unique to each instance of Entity created. -1 means no instance created for this spec yet. (Jumping through MyPy hoops. Can't use None.) We are transitioning to OOP. This will all change.
        'img': str,
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
        'w': int,
        'h': int,
        'color': str,
        'x': float,
        'y': float,
    }
)  # PropSpec


# #############################################    CLASS DEFINITIONS    ################################################


class Entity(pygame.sprite.Sprite):
    def __init__(self,
                 groups,
                 spec: PlayerSpec | WeaponSpec | NpcSpec | PropSpec,
                 x: float,
                 y: float,
                 direction: pygame.math.Vector2,
                 speed: float,
                 ):
        print(f"-*-*-*-*-*-  NEW ENTITY INIT  -*-*-*-*-*- groups: {groups}")
        # print(spec)
        # print(x)
        # print(y)
        # print(direction)
        # print(speed)
        self.spec: PlayerSpec | WeaponSpec | NpcSpec | PropSpec = spec
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

        self.rect = self.image_l.get_frect(center=(self.x, self.y))

    def update(self, delta_time: float, ephase_name: str):
        # TODO: Articulate the reason we have to make the update signatures match. NOTE: ephase_name ARG had to be added
        #     to places it is not actually used. (* PyCharm static analysis warning *)

        delta_vector = self.dir * self.speed * delta_time
        # MYPY ERROR HERE - TRICKY ONE:
        # main.py:365: error: Incompatible types in assignment (expression has type "Vector2",
        #     variable has type "tuple[float, float]")  [assignment]
        self.rect.center += delta_vector
        # ***************************

        self.physics_outer_walls()  # Handle bouncing off walls. NOTE: Props override this and pass. Props ignore walls.

        # Activate the correctly-facing image, based on X direction.
        if self.dir.x < 0:
            self.image = self.image_l
        else:
            self.image = self.image_r

    def physics_outer_walls(self):
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


class Player(Entity):
    def __init__(self,
                 groups,
                 spec: PlayerSpec,
                 weapon_spec: WeaponSpec,
                 all_weapons_group_ref: pygame.sprite.Group,
                 x: float,
                 y: float,
                 direction: pygame.math.Vector2,
                 speed: float,
                 ):
        self.weapon_spec = weapon_spec
        self.all_weapons_group_ref = all_weapons_group_ref
        print(f"# # # # # # # # Player got special weapon attrs (group ref):{self.all_weapons_group_ref}")
        self.can_shoot: bool = True
        self.laser_shoot_time: int = 0
        self.cooldown_duration: int = LASER_COOLDOWN_DURATION  # milliseconds
        super().__init__(groups, spec, x, y, direction, speed)  # super.update() could be done first before setting all the self.* but for now I have them last.

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()  # Milliseconds since pygame.init() was called.
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, delta_time: float, ephase_name: str):
        enviro_influence(self, ephase_name)

        keys = pygame.key.get_pressed()
        recent_keys = pygame.key.get_just_pressed()

        self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.dir.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])

        self.dir = self.dir.normalize() if self.dir else self.dir

        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            print('fire laser')
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            projectile: Weapon = Weapon(groups=[all_sprites, self.all_weapons_group_ref],
                                         spec=self.weapon_spec,
                                         x=self.rect.midtop[0],
                                         y=self.rect.midtop[1],
                                         direction=self.weapon_spec['d'],
                                         speed=self.weapon_spec['s'],
                   )  # PyCharm FALSE WARNING HERE (AbstractGroup)
        # self.all_weapons_group_ref.add(projectile)  # FIX? Adding when instantiating not seeming to work. NOPE. DELETE.
        self.laser_timer()


        #   **   TROUBLE HERE - CANNOT GET Weapon ADDED TO THE all_weapons GROUP   **


        # NOTE: WE UPDATE BASED ON INPUT --BEFORE-- WE CHECK FOR WALL COLLISION/BOUNCING (in super/Entity).
        super().update(delta_time, ephase_name)


class Weapon(Entity):
    def __init__(self,
                 groups,
                 spec: WeaponSpec,
                 x: float,
                 y: float,
                 direction: pygame.math.Vector2,
                 speed: float,
                 ):
        # self.can_shoot: bool = True
        # self.laser_shoot_time: int = 0
        # self.cooldown_duration: int = LASER_COOLDOWN_DURATION  # milliseconds
        print(f"* * * * * * Will now call Weapon.super.init: groups:{groups}")
        super().__init__(groups, spec, x, y, direction, speed)  # super.update() could be done first before setting all the self.* but for now I have them last.

    # TODO: WEAPON/PROJECTILE BEHAVIORS TBD
    # def weapon_timer(self):
    #     if not self.can_shoot:
    #         current_time = pygame.time.get_ticks()  # Milliseconds since pygame.init() was called.
    #         if current_time - self.laser_shoot_time >= self.cooldown_duration:
    #             self.can_shoot = True



#=======================================================================================================================
# ISSUE - WE ARE NEVER COMPLETING THE INIT. ERRROR COMPLAINS OF A SURFACE MISSING WHEN TRYING TO DRAW .. BUT
    # WE SHOULD NOT BE DRAWING JUST YET IT SEEMS.

    # /home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/bin/python /home/bilbo/repos/pygamefun/game/main.py
    # pygame-ce 2.5.0 (SDL 2.30.3, Python 3.12.4)
    # # # # # # # # # Player got special weapon attrs (group ref):<Group(0 sprites)>
    # fire laser
    # * * * * * * Will now call Weapon.super.init: groups:[<Group(84 sprites)>, <Group(0 sprites)>]
    # Traceback (most recent call last):
    #   File "/home/bilbo/repos/pygamefun/game/main.py", line 704, in <module>
    #     all_weapons.draw(display_surface)
    #   File "/home/bilbo/.pyenv/versions/3.12.4/envs/ve.pygamefun/lib/python3.12/site-packages/pygame/sprite.py", line 567, in draw
    #     zip(sprites, surface.blits((spr.image, spr.rect) for spr in sprites))
    #                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # TypeError: Source objects must be a surface

    # Process finished with exit code 1

#=======================================================================================================================



    def update(self, delta_time: float, ephase_name: str):
        print(f" === === === === NOW IN Weapon.update() === === === ===")
        enviro_influence(self, ephase_name)

        # TODO: WEAPON/PROJECTILE BEHAVIORS TBD
        # keys = pygame.key.get_pressed()
        # recent_keys = pygame.key.get_just_pressed()
        #
        # self.dir.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        # self.dir.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        #
        # self.dir = self.dir.normalize() if self.dir else self.dir
        #
        # if recent_keys[pygame.K_SPACE] and self.can_shoot:
        #     print('fire laser')
        #     self.can_shoot = False
        #     self.laser_shoot_time = pygame.time.get_ticks()
        #
        # self.laser_timer()

        super().update(delta_time, ephase_name)
        print(f"+ + + + + + + + + + + After Weapon+Entity updates, Surfaces - (main) self.image: {self.image}")
        print(f"self.image_l: {self.image_l}")
        print(f"self.image_r: {self.image_r}")
        # Suspect these might be missing (based on error during Weapon instantiation, but at this point we SHOULD have them.


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

    def physics_outer_walls(self):  # Overrides Entity.physics_outer_walls, so we can disable that for Props.
        pass


# #############################################    FUNCTION DEFINITIONS    #############################################

# *** MyPy ERROR about PropSpec dict has no keys for p,r,c,f - BUT PropSpec WILL **NEVER** BE PASSED HERE !!! ???
def enviro_influence(xself: Player | Weapon | Npc, ephase_name: str) -> None:
    # ENVIRO PHASES - APPLICATION OF INFLUENCE OF CURRENT PHASE
    if ephase_name == 'peace':
        xself.speed = xself.spec['p']
    elif ephase_name == 'rogue':
        xself.speed = xself.spec['r']
    elif ephase_name == 'chaos':
        xself.speed = xself.spec['c']
    elif ephase_name == 'frozen':
        xself.speed = xself.spec['f']
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
all_weapons: pygame.sprite.Group = pygame.sprite.Group()
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

        prop_specs.append(prop_spec)


# ################################################    INSTANTIATION    #################################################

# TODO: See if we can move the prop spec (spraying/generation) code inside of prop instantiation. Probably can/should.

# INSTANITATE PLAYER(S)
players: list[Player] = []
for i, player_spec in enumerate(player_specs):
    player_spec['instance_id'] = i
    imgpath = os.path.join(ASSET_PATH, player_spec['img'])
    player: Player = Player( groups=[all_sprites, all_players],
                             spec=player_spec,
                             weapon_spec=weapon_specs[0],  # THIS IS A HACK. Temporary.
                             all_weapons_group_ref=all_weapons,  # THIS IS A HACK. Temporary.
                             x=player_spec['x'],
                             y=player_spec['y'],
                             direction=player_spec['d'],
                             speed=player_spec['s'],
                             )  # PyCharm FALSE WARNING HERE (AbstractGroup)
    players.append(player)  # Although considered for removal in lieu of sprite groups, I see reasons to keep such lists.

# INSTANITATE WEAPONS/PROJECTILES - TEMPORARY/EXPERIMENTAL - THIS WILL CHANGE TO 'FIRING' (DYNAMIC INSTANTIATION)
# weapons: list[Weapon] = []
# for i, weapon_spec in enumerate(weapon_specs):
#     weapon_spec['instance_id'] = i
#     imgpath = os.path.join(ASSET_PATH, weapon_spec['img'])
#     weapon: Weapon = Weapon( groups=[all_sprites, all_weapons],
#                              spec=weapon_spec,
#                              x=weapon_spec['x'],
#                              y=weapon_spec['y'],
#                              direction=weapon_spec['d'],
#                              speed=weapon_spec['s'],
#                              )  # PyCharm FALSE WARNING HERE (AbstractGroup)
#     weapons.append(weapon)  # Although considered for removal in lieu of sprite groups, I see reasons to keep such lists.

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

# CUSTOM EVENTS - Random tumbleweeds
tumbleweed_event = pygame.event.custom_type()
pygame.time.set_timer(tumbleweed_event, 4500)


#   * * * * * * *    MAIN LOOP    * * * * * * *
while running:
    g_delta_time = clock.tick(TICKRATE) / 1000  # Seconds elapsed for a single frame (e.g. - 60 Frm/sec = 0.017 sec/Frm)


    # ##################################################    INPUT    ###################################################

    for event in pygame.event.get():  # Check all new events since the last main loop iteration
        if event.type == pygame.QUIT:
            running = False
        if event.type == tumbleweed_event:
            print(f"Look out! Here comes a tumbleweed!")


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
    all_weapons.update(g_delta_time, g_ephase_name)  # Must update Weapons AFTER Player since Player creates Weapons during Player update.
    # ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ THE BIG BUG FIX WAS HERE!!!!! SIMPLY HAD TO MOVE all_weapons.update()
    #                                                          TO --AFTER--  all_players.update()
    # This is because the Weapon is instantiated during the player update cycle .. BUT it has not had any update
    # of its own yet, and the update() is where the main surface is put in place (possibly for the first time).
    # Our error was basically (no surface yet!) .. so it made sense, we had done instantiation but NOT our first update
    # and then draw was getting called. This was happening when all_weapons.update was before all_players.update(),
    # but now that it is AFTER, everything works.
    # I considered another fix as well, similar .. and that is to put in a single bootstrapping call to Weapon.update()
    # inside of Player.update, right after instantiating the Weapon. That would most likely work as well and depending,
    # of the logic of what you want your first frame of the firing of a weapon to be, then you might choose one fix
    # over the other. For example, you might have some OTHER concern causing you to but all_players.update() LAST, no
    # matter what (its just hypothetical) BUT if that was the case (for whatever reason) THEN you might need to choose
    # the fix of calling the single Weapon.update() right after you have Player instantiate that Weapon.

    # This bug was a little tricky to figure out, but really it is totally logical (like most bugs ha ha, if not ALL
    # bugs lol) .. however since it was a timing issue and involved a bit of a hierarchy/sequence of actions, then
    # that is what added a little bit of the challenge to figuring it out. One can see that I added quite a lot of
    # print statements to help pinpoint the state of things at precise points of execution. Really this just helped
    # me think things thgough, because the right values/references were in fact ALWAYS there in the right place .. the
    # problem was simply one of chicken and egg, and when the update was called for the Weapon since it is the update
    # of the Player the even creates that Weapon to update in the first place.
    # Clearly, updating of the Weapon must come after the updating of Player (or the other fix) so that Surfaces are in
    # place for the DRAW calls we have st the end of every main loop.

    # REDRAW THE BACKGROUND
    if ACID_MODE is False:
        display_surface.blit(bg_surface, (0, 0))

    #   | | | | | |    MAIN DRAWING ACTIONS    | | | | | |
    all_props.draw(display_surface)
    all_npcs.draw(display_surface)
    all_weapons.draw(display_surface)
    all_players.draw(display_surface)

    pygame.display.flip()  # Similar to update but not entire screen. TODO: Clarify

#   * _ * _ * _ *    END MAIN LOOP    * _ * _ * _ *


pygame.quit()


##
#


# ###################################################    NOTES    ######################################################

# PYGMAE-CE DOCS:
# https://pyga.me/docs/

# Slightly-related and very interesting topic: Different methods of high-performance image storage and retrieval for
# Python (like LMDB, HDF5, filesystem etc.) I'm considering this topic as I prepare to write an image-loading and
# pre-processing function and so I was thinking what is the best way to store the image data. It will be used
# to instantiate surfaces, which will then be passed into the init of new entity instances. This is to prevent repeated
# unnecessary source-loading of image data and is a core concept to efficiently instantiating sprites.
# https://realpython.com/storing-images-in-python/

##
#

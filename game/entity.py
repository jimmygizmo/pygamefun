# entity.py

import sys
import pygame.math  # For pygame.math.Vector2 only.
from typing import TypedDict, Literal


# ###########################################    ENTITY SPECIFICATIONS    ##############################################

EnviroSpec = TypedDict('EnviroSpec',
    {
        'e_p': float,  # Enviro: Peace (speed)
        'e_r': float,  # Enviro: Rogue (speed)
        'e_c': float,  # Enviro: Chaos (speed)
        'e_f': float,  # Enviro: Frozen (speed)
    }
)  # EnviroSpec

EnviroKeys = Literal['e_p', 'e_r', 'e_c', 'e_f']


PlayerSpec = TypedDict('PlayerSpec',
    {
        'name': str,  # Player short name
        'instance_id': int,  # 0-based Int serial number unique to each instance of Player created. -1 means no instance created for this spec yet. (Jumping through MyPy hoops. Can't use None.) We are transitioning to OOP. This will all change.
        'img_filename': str,  # Filename of PNG (with transparency)
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
        'resize': bool,  # If True, image will be resized using resizer.alphonic_resize()
        'w': int,  # PNG pixel width
        'h': int,  # PNG pixel height
        'color': str,  # Debug mode color of rectangle
        'x': float,  # Initial position X value
        'y': float,  # Initial position Y value
        'd': pygame.math.Vector2,  # Direction
        's': float,  # Initial/default speed
        'a': float,  # Initial/default Angle
        'av': float,  # Initial/default Angular Velocity
        'e_p': float,  # Enviro: Peace (speed)
        'e_r': float,  # Enviro: Rogue (speed)
        'e_c': float,  # Enviro: Chaos (speed)
        'e_f': float,  # Enviro: Frozen (speed)
    }
)  # PlayerSpec

# PLAYER DATA - Initial state for a single player (usually) or possibly multiple players.
player_specs: list[PlayerSpec] = [
    {
        'name': 'buck',
        'instance_id': -1,
        'img_filename':  'rocket-200x252.png',
        'flip': False,
        'resize': True,
        'w': 100,
        'h': 126,
        'color': 'aqua',
        'x': 890.0,
        'y': 540.0,
        'd': pygame.math.Vector2((-0.994, -0.114)),  # placeholder instance (mypy)
        's': 780.0,
        'a': 0.0,
        'av': 0.0,
        'e_p': 590.0,
        'e_r': 1100.0,
        'e_c': 1700.0,
        'e_f': 2650.0,
    },
]  # player_specs: list[PlayerSpec]


WeaponSpec = TypedDict('WeaponSpec',
    {
        'name': str,  # Weapon/projectile short name
        'instance_id': int,  # 0-based Int serial number unique to each instance of Weapon created. -1 means no instance created for this spec yet. (Jumping through MyPy hoops. Can't use None.) We are transitioning to OOP. This will all change.
        'img_filename': str,  # Filename of PNG (with transparency)
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
        'resize': bool,  # If True, image will be resized using resizer.alphonic_resize()
        'w': int,  # PNG pixel width
        'h': int,  # PNG pixel height
        'color': str,  # Debug mode color of rectangle
        'x': float,  # Initial position X value
        'y': float,  # Initial position Y value
        'd': pygame.math.Vector2,  # Direction
        's': float,  # Initial/default speed
        'a': float,  # Initial/default Angle
        'av': float,  # Initial/default Angular Velocity
        'e_p': float,  # Enviro: Peace (speed)
        'e_r': float,  # Enviro: Rogue (speed)
        'e_c': float,  # Enviro: Chaos (speed)
        'e_f': float,  # Enviro: Frozen (speed)
    }
)  # WeaponSpec

# WEAPON/PROJECTILE DATA - Initial state for a weapon/projectile
weapon_specs: list[WeaponSpec] = [
    {
        'name': 'orb',
        'instance_id': -1,
        'img_filename':  'green-ball-140x140.png',
        'flip': False,
        'resize': True,
        'w': 70,
        'h': 70,
        'color': 'green3',
        'x': 890.0,
        'y': 260.0,
        'd': pygame.math.Vector2((0.0, -1.0)),  # placeholder instance (mypy)
        's': 134.0,
        'a': 0.0,
        'av': 0.0,
        'e_p': 98.0,
        'e_r': 122.0,
        'e_c': 840.0,
        'e_f': 2350.0,
    },
    {
        'name': 'meatball',
        'instance_id': -1,
        'img_filename':  'meatball-204x220.png',
        'flip': False,
        'resize': True,
        'w': 102,
        'h': 110,
        'color': 'brown',
        'x': 890.0,
        'y': 260.0,
        'd': pygame.math.Vector2((0.0, -1.0)),  # placeholder instance (mypy)
        's': 104.0,
        'a': 0.0,
        'av': 1.0,
        'e_p': 698.0,
        'e_r': 822.0,
        'e_c': 1640.0,
        'e_f': 3350.0,
    },
]  # weapon_specs: list[WeaponSpec]


NpcSpec = TypedDict('NpcSpec',
    {
        'name': str,  # NPC short name
        'instance_id': int,  # 0-based Int serial number unique to each instance of Entity created. -1 means no instance created for this spec yet. (Jumping through MyPy hoops. Can't use None.) We are transitioning to OOP. This will all change.
        'img_filename': str,  # Filename of PNG (with transparency)
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
        'resize': bool,  # If True, image will be resized using resizer.alphonic_resize()
        'w': int,  # PNG pixel width
        'h': int,  # PNG pixel height
        'color': str,  # Debug mode color of rectangle
        'x': float,  # Initial position X value
        'y': float,  # Initial position Y value
        'd': pygame.math.Vector2,  # Direction
        's': float,  # Initial/default speed
        'a': float,  # Initial/default Angle
        'av': float,  # Initial/default Angular Velocity
        'e_p': float,  # Enviro: Peace (speed)
        'e_r': float,  # Enviro: Rogue (speed)
        'e_c': float,  # Enviro: Chaos (speed)
        'e_f': float,  # Enviro: Frozen (speed)
    }
)  # NpcSpec

# NPC DATA - Initial state for a handful of NPCs that move, experience physics and interact. W/initial motion.
npc_specs: list[NpcSpec] = [
    {
        'name': 'red-flower-floaty',
        'instance_id': -1,
        'img_filename':  'red-flower-66x64.png',
        'flip': False,
        'resize': False,
        'w': 66,
        'h': 64,
        'color': 'red1',
        'x': 240.0,
        'y': 300.0,
        'd': pygame.math.Vector2((-0.624, 0.782)),  # placeholder instance (mypy)
        's': 100.0,
        'a': 0.0,
        'av': 3.0,
        'e_p': 100.0,
        'e_r': 100.0,
        'e_c': 350.0,
        'e_f': 2.0,
    },
    {
        'name': 'red-flower-drifty',
        'instance_id': -1,
        'img_filename':  'red-flower-66x64.png',
        'flip': True,
        'resize': False,
        'w': 66,
        'h': 64,
        'color': 'orangered',
        'x': 240.0,
        'y': 300.0,
        'd': pygame.math.Vector2((0.137, -0.991)),  # placeholder instance (mypy)
        's': 100.0,
        'a': 0.0,
        'av': -1.0,
        'e_p': 100.0,
        'e_r': 100.0,
        'e_c': 420.0,
        'e_f': 3.0,
    },
    {
        'name': 'goldie',
        'instance_id': -1,
        'img_filename': 'gold-retriever-160x142.png',
        'flip': True,
        'resize': False,
        'w': 160,
        'h': 142,
        'color': 'gold',
        'x': 500.0,
        'y': 300.0,
        'd': pygame.math.Vector2((1.0, 1.0)),  # placeholder instance (mypy)
        's': 141.0,
        'a': 0.0,
        'av': 11.0,
        'e_p': 160.0,
        'e_r': 880.0,
        'e_c': 1290.0,
        'e_f': 10.0,
    },
    {
        'name': 'grumpy',
        'instance_id': -1,
        'img_filename':  'grumpy-cat-110x120.png',
        'flip': True,
        'resize': True,
        'w': 220,
        'h': 240,
        'color': 'blanchedalmond',
        'x': 780.0,
        'y': 300.0,
        'd': pygame.math.Vector2((0.261, 0.966)),  # placeholder instance (mypy)
        's': 90.0,
        'a': 0.0,
        'av': 0.0,
        'e_p': 80.0,
        'e_r': 50.0,
        'e_c': 2170.0,
        'e_f': 40.0,
    },
    {
        'name': 'fishy',
        'instance_id': -1,
        'img_filename':  'goldfish-280x220.png',
        'flip': False,
        'resize': True,
        'w': 560,
        'h': 440,
        'color': 'darkgoldenrod1',
        'x': 840.0,
        'y': 300.0,
        'd': pygame.math.Vector2((-0.994, -0.114)),  # placeholder instance (mypy)
        's': 80.0,
        'a': 0.0,
        'av': -1.0,
        'e_p': 90.0,
        'e_r': 100.0,
        'e_c': 700.0,
        'e_f': 2850.0,
    },
]  # npc_specs: list[NpcSpec]


# TypedDict for PROP_TEMPLATE
PropTemplate = TypedDict('PropTemplate',
    {
        'name': str,
        'img_filename': str,
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
        'resize': bool,  # If True, image will be resized using resizer.alphonic_resize()
        'w': int,
        'h': int,
        'color': str,
        'x': float,
        'y': float,
        'a': float,  # Initial/default Angle
        'spray_count': int,
        'spray_radius': float,
    }
)  # PropTemplate

# PROP DATA - Initial state for a handful of non-moving props. Includes specs for random instantiation (spraying).
prop_templates: list[PropTemplate] = [
    {
        'name': 'red-flower',
        'img_filename':  'red-flower-66x64.png',
        'flip': False,
        'resize': False,
        'w': 66,
        'h': 64,
        'color': 'crimson',
        'x': 804.0,
        'y': 440.0,
        'a': 0.0,
        'spray_count': 60,
        'spray_radius': 780.0,
    },
    {
        'name': 'blue-flower',
        'img_filename':  'blue-flower-160x158.png',
        'flip': False,
        'resize': False,
        'w': 160,
        'h': 158,
        'color': 'darkturquoise',
        'x': 880.0,
        'y': 360.0,
        'a': 0.0,
        'spray_count': 18,
        'spray_radius': 680.0,
    },
]  # prop_templates: list[PropTemplate]

# TypedDict for PROP. Props are generated dynamically, when we "spray" props from their template.
PropSpec = TypedDict('PropSpec',
    {
        'name': str,
        'instance_id': int,  # 0-based Int serial number unique to each instance of Entity created. -1 means no instance created for this spec yet. (Jumping through MyPy hoops. Can't use None.) We are transitioning to OOP. This will all change.
        'img_filename': str,
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
        'resize': bool,  # If True, image will be resized using resizer.alphonic_resize()
        'w': int,
        'h': int,
        'color': str,
        'x': float,
        'y': float,
        'a': float,
    }
)  # PropSpec


if __name__ == '__main__':
    print("WARNING: PyGameFun entity.py has been run directly, however it is only meant to be imported.")
    sys.exit(1)


##
#

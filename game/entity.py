# entity.py

import sys
import pygame.math  # For pygame.math.Vector2 only.
from typing import TypedDict


# ###########################################    ENTITY SPECIFICATIONS    ##############################################

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
        'img_filename':  'rocket-200x252.png',
        'flip': False,
        'resize': True,
        'w': 100,
        'h': 126,
        'color': 'aqua',
        'x': 890.0,
        'y': 540.0,
        'd': pygame.math.Vector2((-0.994, -0.114)),  # placeholder instance (mypy)
        's': 480.0,
        'p': 590.0,
        'r': 1100.0,
        'c': 1700.0,
        'f': 2650.0,
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
        'img_filename':  'green-ball-140x140.png',
        'flip': False,
        'resize': True,
        'w': 70,
        'h': 70,
        'color': 'green3',
        'x': 890.0,
        'y': 260.0,
        'd': pygame.math.Vector2((0.0, -1.0)),  # placeholder instance (mypy)
        's': 334.0,
        'p': 98.0,
        'r': 122.0,
        'c': 840.0,
        'f': 2350.0,
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
        's': 734.0,
        'p': 698.0,
        'r': 822.0,
        'c': 1640.0,
        'f': 3350.0,
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
        'p': 100.0,
        'r': 100.0,
        'c': 350.0,
        'f': 2.0,
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
        'p': 100.0,
        'r': 100.0,
        'c': 420.0,
        'f': 3.0,
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
        'p': 160.0,
        'r': 880.0,
        'c': 1290.0,
        'f': 10.0,
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
        'p': 80.0,
        'r': 50.0,
        'c': 2170.0,
        'f': 40.0,
    },
    {
        'name': 'fishy',
        'instance_id': -1,
        'img_filename':  'goldfish-280x220.png',
        'flip': False,
        'resize': False,
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
        'img_filename': str,
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
        'resize': bool,  # If True, image will be resized using resizer.alphonic_resize()
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
        'img_filename':  'red-flower-66x64.png',
        'flip': False,
        'resize': False,
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
        'img_filename':  'blue-flower-160x158.png',
        'flip': False,
        'resize': False,
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
        'instance_id': int,  # 0-based Int serial number unique to each instance of Entity created. -1 means no instance created for this spec yet. (Jumping through MyPy hoops. Can't use None.) We are transitioning to OOP. This will all change.
        'img_filename': str,
        'flip': bool,  # If True, image will be flipped horizontally at the time of loading
        'resize': bool,  # If True, image will be resized using resizer.alphonic_resize()
        'w': int,
        'h': int,
        'color': str,
        'x': float,
        'y': float,
    }
)  # PropSpec


if __name__ == '__main__':
    print("WARNING: PyGameFun entity.py has been run directly, however it is only meant to be imported.")
    sys.exit(1)


##
#

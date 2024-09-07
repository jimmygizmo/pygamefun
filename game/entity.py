# entity.py

import sys
import pygame.math  # For pygame.math.Vector2 only.
from typing import TypedDict, Literal

# PHSYICS SPECIAL FEATURE VALUES - ALL ARE 4 DIGITS AND ALL START WITH 77__.0. DEFAULT NOOP (NON-SPECIFIC) IS 7700:
# Rotation: angular_vel av 7701.0: random angular_vel SLOW
# Rotation: angular_vel av 7702.0: random angular_vel MED
# Rotation: angular_vel av 7703.0: random angular_vel FAST
# Rotation: angular_vel av 7704.0: random angular_vel SLOW-TO-FAST (full range of rotation speeds)
# Speed: speed s 7711.0: random speed s SLOW
# Speed: Speed s 7712.0: random speed s MED
# Speed: speed s 7713.0: random speed s FAST
# Speed: speed s 7714.0: random speed s SLOW-TO-FAST (full range of speeds)
# Direction: direction d 7721.0: random direction d UP WIDE (180 degree range)
# Direction: direction d 7722.0: random direction d DOWN WIDE (180 degree range)
# Direction: direction d 7723.0: random direction d LEFT WIDE (180 degree range)
# Direction: direction d 7724.0: random direction d RIGHT WIDE (180 degree range)

# IMPORTANT: The Physics values are Float values. The .0 is required or at least very strongly advised as everything
# else in this program that would be a float would have .0 if anything else. Be consistent.

# ANIMATION SPECIAL FEATURE VALUES
# Repeat Count: repeat_count -1: repeat playing the animation in a loop, continuously forever - LOOP ANIMATION


# ###########################################    ENTITY SPECIFICATIONS    ##############################################


# TODO: Change ALL instance_id to TYPE: int | None and init to None, meaning no instance yet. Check all code for instance_id first.
#     Check for where it does anything related to -1 or < 0 etc. Generally, I think we can use TYPE | None a LOT more.
#     Using None to indicate some early/pre-initialization value or any special state/condition not like the 'normal' values,
#     this is EXTREMELY PYTHONIC and core to how you code Python and even to how many libraries operate, so it would make
#     no sense begin limiting the use of None as an optional/allowed init value, just to keep MyPy happy and to keep things
#     more strongly/simply typed. Barring some edge-case performance or other concern, I think we can use TYPE | None
#     all over the place, because it is: SEMANTICALLY GOOD, PYTHONIC, POWERFUL, COMPATIBLE, LOGICAL, FLEXIBLE, TRADITIONAL.
#     This thought process came out of a phase of trying to meet all MyPy recommendations explicitly and to try to do
#     relatively strong typing in Python. It was sort of an adventure. I mean there is nothing wrong with using a value
#     like -1 to mean not-yet-initialized .. but then you can't use -1 for -1 lol. There are MANY important reasons. I
#     like to re-explore the original principals and realities upon which I base my understandings and methods to keep
#     all of the up-to-date and optimal. I'm confident now on generally trying to meet MOST/NEARLY-ALL MyPy recommendations,
#     but I make exceptions in some areas or rather one might say, I am clarifying that not all MyPy recommendations apply
#     all the time, in fact, some of the might rarely be the best thing. One needs to assess every coding choice they make
#     from many intelligent perspectives and not just take mandates at face value. Don't be a sheep, be an adventurer,
#     but maybe your adventures will reveal that the sheep are doing 80% of the stuff right, but you know better about that
#     20%, because you take the time to assess everything you do based on the merits of the actions themselves.

# TODO: AnimSpec ?   Probably.  We will add an animation cache, ACACHE, similar to SCACHE.  There is a dir of images to
#     load instead of a single image. Width and Height are facts, not necessarily relevant. The animation will certainly
#     have multiple other specs, such as repeat, frame rate, etc.
#     So this logic concludes we will certainly be adding a new AnimationSpec or AnimSpec to organize all this information.


AnimSpec = TypedDict('AnimSpec',
    {
        'name': str,  # Animation short name
        'instance_id': int,  # 0-based Int serial number unique to each instance of Animation created. -1 means no instance created for this spec yet.
        'frames_dir': str,  # Name of the directory containing the sequentially-named frames. PNGs with transparency. Resides inside /assets/.
        'flip': bool,  # If True, all frames will be flipped horizontally at the time of loading
        'resize': bool,  # If True, all frames will be resized using resizer.alphonic_resize()
        'w': int,  # PNG pixel width
        'h': int,  # PNG pixel height
        'color': str,  # Debug mode color of rectangle
        'x': float,  # Initial position X value
        'y': float,  # Initial position Y value
        'frame_rate': float,  # Frame rate
        'repeat_count': int,  # Count to repeat. -1 to repeat continuously.
    }
)  # AnimSpec

# ANIMATION DATA - Initial state for animations.
anim_specs: list[AnimSpec] = [
    {
        'name': 'exp-elaborate',
        'instance_id': -1,
        'frames_dir':  'anim-exp-elaborate',
        'flip': False,
        'resize': False,
        'w': 512,
        'h': 512,
        'color': 'orangered2',
        'x': 890.0,
        'y': 540.0,
        'frame_rate': 32.0,  # TODO: Not used yet.
        'repeat_count': 1,
    },
]  # anim_specs: list[AnimSpec]


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
        'instance_id': int,  # 0-based Int serial number unique to each instance of Player created. -1 means no instance created for this spec yet.
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
        'instance_id': int,  # 0-based Int serial number unique to each instance of Weapon created. -1 means no instance created for this spec yet.
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
        'final_anim_spec': AnimSpec | None,
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
        'av': 6.0,
        'e_p': 98.0,
        'e_r': 122.0,
        'e_c': 840.0,
        'e_f': 2350.0,
        'final_anim_spec': None,
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
        'av': 7704.0,
        'e_p': 698.0,
        'e_r': 822.0,
        'e_c': 1640.0,
        'e_f': 3350.0,
        'final_anim_spec': None,
    },
]  # weapon_specs: list[WeaponSpec]


NpcSpec = TypedDict('NpcSpec',
    {
        'name': str,  # NPC short name
        'instance_id': int,  # 0-based Int serial number unique to each instance of Entity created. -1 means no instance created for this spec yet.
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
        'av': 7.0,
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
        'resize': False,
        'w': 220,
        'h': 240,
        'color': 'blanchedalmond',
        'x': 780.0,
        'y': 300.0,
        'd': pygame.math.Vector2((0.261, 0.966)),  # placeholder instance (mypy)
        's': 90.0,
        'a': 0.0,
        'av': -0.2,
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
        'resize': False,
        'w': 560,
        'h': 440,
        'color': 'darkgoldenrod1',
        'x': 840.0,
        'y': 300.0,
        'd': pygame.math.Vector2((-0.994, -0.114)),  # placeholder instance (mypy)
        's': 80.0,
        'a': 0.0,
        'av': 0.0,
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
        'instance_id': int,  # 0-based Int serial number unique to each instance of Entity created. -1 means no instance created for this spec yet.
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

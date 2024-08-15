import math  # config.py

import sys
import collections


# ###############################################    CONFIGURATION    ##################################################

SCREEN_WIDTH: int = 1640
SCREEN_HEIGHT: int = 860
SCOREBOARD: bool = True
SCORE_X: int = math.floor(SCREEN_WIDTH / 2)
SCORE_Y: int = math.floor(0.92 * SCREEN_HEIGHT)
SCORE_HEIGHT: int = 20
SCORE_WIDTH: int = 100
SCORE_FONT_PATH = 'assets/RabbidHighwaySignII-TTF.ttf'
SCORE_SYSTEM_FONT = 'freesansbold'
SCORE_FONT_SIZE: int = 40

TICKRATE: int = 60  # (frame rate) - 0/None gives maximum/unlimited. Depends on code but recently saw 500-1000 FPS.
GAME_TITLE: str = 'Goldfish Picnic'

BGCOLOR: str = 'olivedrab'
BGIMG: str = 'grass-field-med-1920x1249.jpg'  # 'grass-field-med-1920x1249.jpg'  # 'lawn-bg-dark-2560x1440.jpg'
ASSET_PATH: str = 'assets'  # Relative path with no trailing slash.
DEBUG: bool = False
ACID_MODE: bool = False  # Suppress background re-painting. This makes objects leave psychedelic trails for a fun effect.

LASER_COOLDOWN_DURATION: int = 100  # Milliseconds - minimum time between laser firing
PROJECTILE_MARGIN: int = 160  # Distane beyond wall on X or Y axis at which projectile/Weapon is "Finalized"
PLAYER_MAIN_WEAPON_INDEX: int = 0  # Index in weapon_specs of the weapon_spec item to use for the Player's main projectile.
# 0 = green ball    1 = meatball

PYGAME_FROMBYTES_IMAGE_LOAD_WORKAROUND_ENABLE: bool = True
MEATBALL_SPAWN_MARGIN: int = 60  # Meatballs can spawn this far slightly to the left/right and above the screen.
MEATBALL_SPAWN_TIME_MIN: int = 20  # They spawn no faster than this but a small random-in-range pause is added too.
MEATBALL_SPAWN_TIME_RANGE: int = 500  # Random from 0 to this range max is then ADDED TO THE MINIMUM.
# TODO: Meatball spawn time with current timer is only set randomly once at game start. MAKE IT VARY ALL THE TIME.

# List of tuples of the phase name and the phase duration in frames/iterations. collections.deque.popleft() is said
# to be efficient at popping from the left side of a list. I'm just giving it a try. There are many ways to rotate a list.
ENVIRO_PHASES: collections.deque = collections.deque([
     ('peace', 800),
     ('rogue', 160),
     ('chaos', 400),
     ('frozen', 60),
     ('rogue', 50),
     ('frozen', 110),
     ]
)  # The equivalent Spec keys for these phases are simply the first letters of the phase names: p, r, c, f


if __name__ == '__main__':
    print("WARNING: PyGameFun config.py has been run directly, however it is only meant to be imported.")
    sys.exit(1)


##
#


# NOTES:

# TODO: This looks like a cool way to apply type-hinting to literal enums like this (constant lists, dicts etc):
# PygameSurfaceFormatType = Union[
#     Literal["P"], Literal["RGB"], Literal["RGBX"], Literal["RGBA"], Literal["ARGB"]
# ]
# USAGE: format: PygameSurfaceFormatType = "RGBA"


##
#

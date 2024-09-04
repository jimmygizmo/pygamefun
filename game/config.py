# config.py

import math
import sys


# ###############################################    CONFIGURATION    ##################################################

SCREEN_WIDTH: int = 1640
SCREEN_HEIGHT: int = 860

TICKRATE: int = 60  # (frame rate) - 0/None gives maximum/unlimited. Depends on code but recently saw 500-1000 FPS.
GAME_TITLE: str = 'Goldfish Picnic'

BGCOLOR: str = 'olivedrab'
BGIMG: str = 'grass-field-med-1920x1249.jpg'  # 'grass-field-med-1920x1249.jpg'  # 'lawn-bg-dark-2560x1440.jpg'
ASSET_PATH: str = 'assets'  # Relative path with no trailing slash.
DEBUG: bool = False
ACID_MODE: bool = False  # Suppress background re-painting. This makes objects leave psychedelic trails for a fun effect.
WHITEOUT_MODE: bool = False  # White-out all objects in a demonstration of multiple Mask features.
ROTATION: bool = True  # Rotation is expensive in the initial implementation. TODO: Make rotation more efficient.

LASER_COOLDOWN_DURATION: int = 100  # Milliseconds - minimum time between laser firing
PROJECTILE_MARGIN: int = 160  # Distane beyond wall on X or Y axis at which projectile/Weapon is "Finalized"
PLAYER_MAIN_WEAPON_INDEX: int = 0  # Index in weapon_specs of the weapon_spec item to use for the Player's main projectile.
# 0 = green ball (orb)    1 = meatball

PYGAME_FROMBYTES_IMAGE_LOAD_WORKAROUND_ENABLE: bool = True
MEATBALL_SPAWN_MARGIN: int = 60  # Meatballs can spawn this far slightly to the left/right and above the screen.
MEATBALL_SPAWN_TIME_MIN: int = 20  # They spawn no faster than this but a small random-in-range pause is added too.
MEATBALL_SPAWN_TIME_RANGE: int = 500  # Random from 0 to this range max is then ADDED TO THE MINIMUM.
# TODO: Meatball spawn time with current timer is only set randomly once at game start. MAKE IT VARY ALL THE TIME.

ENVIRO_PHASES: list[tuple[str, int]] = [  # See related types: ent.EnviroSpec, ent.EnviroKeys
        ('peace', 800),
        ('rogue', 160),
        ('chaos', 400),
        ('frozen', 60),
        ('rogue', 50),
        ('frozen', 110),
    ] # See ent.EnviroKeys, a Literal type. Spec key convention: First letter of phase name, 'e_' prefix: e_p, e_r, e_c, e_f


# SCOREBOARD DESIGN - FONT, COLORS, POSITIONING, BORDER - (SCR prefix)
SCR: bool = True
SCR_X: int = math.floor(SCREEN_WIDTH / 2)
SCR_Y: int = math.floor(0.92 * SCREEN_HEIGHT)
SCR_WIDTH: int = 120
SCR_HEIGHT: int = 60
SCR_FONT_FILENAME = 'RabbidHighwaySignII-TTF.ttf'
SCR_SYSTEM_FONT = 'notosansbold'  # Only tested on Windows. Early font-validation, fallback, loading is still evolving.
SCR_FONT_FORCE_SYSTEM: bool = False  # Forces use of a common system font (Windows)
# TODO: Add a cascading load-font test to try for the most common font names based on pygame.font.get_fonts()
#      Survey this on Windows (already done for Win 11), MacOS and Linux (at least Ubuntu desktop.)
SCR_FONT_ADJUST_Y: int = -5  # Vertical position adjustment, affected by Font selection, size, platform, other factors.
SCR_FONT_SIZE: int = 40
SCR_FONT_COLOR: str = 'green'
SCR_BORDER_COLOR: str = 'black'
SCR_BORDER_THICKNESS: int = 8
SCR_BORDER_PAD_X: int = 32
SCR_BORDER_PAD_Y: int = 16
SCR_BORDER_RADIUS: int = 10


# RANDOM RANGE LIMITS
ROT_MIN: float = 0.01
ROT_SLOW_MAX: float = 1.0
ROT_MED_MIN: float = 1.01
ROT_MED_MAX: float = 2.0
ROT_FAST_MIN: float = 2.01
ROT_FAST_MAX: float = 8.0
ROT_MAX: float = 12.0


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

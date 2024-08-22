#! /usr/bin/env -vS python

import config as cfg
import entity as ent
import sys
import os.path
from typing import TypedDict
import pygame
import random
import resizer


# ###########################################    GLOBAL INITIALIZATION    ##############################################

# SURFACE CACHE - 'SCACHE'
# The Surface Cache SCACHE pre-loads images into surfaces. When sprites are instantiated, they will use this cache
# for surfaces and not need to load them from disk. This is important for dynamically/frequently spawned/destroyed sprites.
SurfCacheItem = TypedDict('SurfCacheItem',
    {
        'surface_l': pygame.Surface,  # Image as loaded and with 'flip' options and/or 'resize' options applied if True. Should be LEFT facing.
        'surface_r': pygame.Surface,  # Flipped (assumed to be RIGHT-facing) version of image. Generated by load_image()
        'mask_l': pygame.Mask,  # Mask from surface LEFT
        'mask_r': pygame.Mask,  # Mask from surface RIGHT
        'mask_surf_l': pygame.Surface,  # Mask Surface LEFT - TODO: These may be used later for special effects.
        'mask_surf_r': pygame.Surface,  # Mask Surface RIGHT - TODO: "
    }
)  # SurfCacheitem
SCACHE: dict[str, SurfCacheItem] = {}  # The Surface Cache. Key = filename, Value = SurfCacheItem.


# #############################################    CLASS DEFINITIONS    ################################################

class Entity(pygame.sprite.Sprite):
    base_instance_count: int = 0
    def __init__(self,
                groups: list[pygame.sprite.Group],
                img_filename: str,
                x: float,
                y: float,
                direction: pygame.math.Vector2,
                speed: float,
            ):
        self.base_instance_id: int = Entity.base_instance_count
        self.surface_l: pygame.Surface = SCACHE[img_filename]['surface_l']
        self.surface_r: pygame.Surface = SCACHE[img_filename]['surface_r']
        self.mask_l: pygame.Mask = SCACHE[img_filename]['mask_l']  # Mask from surface LEFT
        self.mask_r: pygame.Mask = SCACHE[img_filename]['mask_r']  # Mask from surface RIGHT
        self.mask_surf_l: pygame.Surface = SCACHE[img_filename]['mask_surf_l']  # TODO: These may be used later for special effects.
        self.mask_surf_r: pygame.Surface = SCACHE[img_filename]['mask_surf_r']  # TODO: "
        self.x: float = x
        self.y: float = y
        self.dir: pygame.math.Vector2 = direction  # Direction
        self.speed: float = speed  # Speed
        self.image: pygame.Surface = pygame.Surface((0, 0))  # Active image (depending on direction of motion). Placeholder.
        # self.mask: pygame.Mask = pygame.mask.from_surface(self.image)  # Placeholder (not very efficient. Maybe use type or|None.)
        self.mask: pygame.Mask | None = None  # Placeholder. Trying None for efficiency. TODO: Could do this in multiple other places.
        self.rect: pygame.FRect = pygame.FRect()
        super().__init__(groups)  # super.update() could be done first before setting all the self.* but for now I have them last.
        Entity.base_instance_count += 1
        self.rect = self.surface_l.get_frect(center=(self.x, self.y))

        if cfg.WHITEOUT_MODE:
            self.mask_surf_l.set_colorkey((0, 0, 0))  # Make the black transparent.
            self.mask_surf_r.set_colorkey((0, 0, 0))  # "
            self.surface_l = self.mask_surf_l  # White-out the object.
            self.surface_r = self.mask_surf_r  # "

    def update(self, delta_time: float, ephase_name: str):
        # NOTE: ephase_name ARG had to be added to places it is not actually used. (* PyCharm static analysis warning *)
        # Have not looked at this in weeks but I wanted to comment: This is related to the need to override update()
        # sometimes.

        delta_vector: pygame.math.Vector2 = self.dir * self.speed * delta_time
        # MYPY ERROR HERE - TRICKY ONE:
        # main.py:365: error: Incompatible types in assignment (expression has type "Vector2",
        #     variable has type "tuple[float, float]")  [assignment]
        self.rect.center += delta_vector
        # ***************************

        self.physics_outer_walls()  # Handle bouncing off walls. NOTE: Props override this and pass. Props ignore walls.
        # In fact, inside Props we override and pass update() too, so calling of physics_outer_walls() will never occur
        # here for props. To clarify, inside Prop, BOTH update() and physics_outer_walls() are overridden and passed.

        # Activate the correctly-facing image and mask, based on X direction.
        if self.dir.x < 0:
            self.image = self.surface_l
            self.mask = self.mask_l
        else:
            self.image = self.surface_r
            self.mask = self.mask_r

    def physics_outer_walls(self):
        # Bounce off LEFT wall in X Axis
        if self.rect.left <= 0:
            self.rect.left = 0
            self.dir.x *= -1

        # Bounce off RIGHT wall in X Axis
        if self.rect.right >= cfg.SCREEN_WIDTH:
            self.rect.right = cfg.SCREEN_WIDTH
            self.dir.x *= -1

        # Bounce off TOP wall in Y Axis
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dir.y *= -1

        # Bounce off BOTTOM wall in Y Axis
        if self.rect.bottom >= cfg.SCREEN_HEIGHT:
            self.rect.bottom = cfg.SCREEN_HEIGHT
            self.dir.y *= -1


class Player(Entity):
    instance_count: int = 0
    def __init__(self,
                groups: list[pygame.sprite.Group],
                img_filename: str,
                weapon_spec: ent.WeaponSpec,
                weapons_groups: list[pygame.sprite.Group],
                x: float,
                y: float,
                direction: pygame.math.Vector2,
                speed: float,
            ):
        self.instance_id: int = Player.instance_count
        self.weapon_spec = weapon_spec
        self.weapons_groups = weapons_groups
        self.can_shoot: bool = True
        self.laser_shoot_time: int = 0
        self.cooldown_duration: int = cfg.LASER_COOLDOWN_DURATION  # milliseconds
        super().__init__(groups, img_filename, x, y, direction, speed)  # super.update() could be done first before setting all the self.* but for now I have them last.
        Player.instance_count += 1

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
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            weapon_img_filename = self.weapon_spec['img_filename']
            projectile: Weapon = Weapon(
                    groups=self.weapons_groups,
                    img_filename=weapon_img_filename,
                    x=self.rect.midtop[0],
                    y=self.rect.midtop[1],
                    direction=self.weapon_spec['d'],
                    speed=self.weapon_spec['s'],
                )  # PyCharm FALSE WARNING HERE (AbstractGroup)
        self.laser_timer()
        # NOTE: WE UPDATE BASED ON INPUT --BEFORE-- WE CHECK FOR WALL COLLISION/BOUNCING (in super/Entity).
        super().update(delta_time, ephase_name)


class Weapon(Entity):
    instance_count: int = 0
    def __init__(self,
                groups: list[pygame.sprite.Group],
                img_filename: str,
                x: float,
                y: float,
                direction: pygame.math.Vector2,
                speed: float,
            ):
        self.instance_id: int = Weapon.instance_count
        super().__init__(groups, img_filename, x, y, direction, speed)  # super.update() could be done first before setting all the self.* but for now I have them last.
        Weapon.instance_count += 1

    def update(self, delta_time: float, ephase_name: str):
        enviro_influence(self, ephase_name)
        super().update(delta_time, ephase_name)

    def physics_outer_walls(self):  # Overrides Entity.physics_outer_walls().
        # Projectiles/weapons are deleted beyond some margin and do not bounce off the outer walls.
        if self.rect.left <= 0 - cfg.PROJECTILE_MARGIN:  # A little beyond LEFT wall in X Axis
            self.kill()
        if self.rect.right >= cfg.SCREEN_WIDTH + cfg.PROJECTILE_MARGIN:  # A little beyond RIGHT wall in X Axis
            self.kill()
        if self.rect.top <= 0 - cfg.PROJECTILE_MARGIN:  # A little beyond TOP wall in Y Axis
            self.kill()
        if self.rect.bottom >= cfg.SCREEN_HEIGHT + cfg.PROJECTILE_MARGIN:  # A little beyond BOTTOM wall in Y Axis
            self.kill()


class Npc(Entity):
    instance_count: int = 0
    def __init__(self,
                groups: list[pygame.sprite.Group],
                img_filename: str,
                x: float,
                y: float,
                direction: pygame.math.Vector2,
                speed: float,
            ):
        self.instance_id: int = Npc.instance_count
        super().__init__(groups, img_filename, x, y, direction, speed)  # super.update() can be done before or after setting any self.* but think about how it might matter! Maybe not at all.
        Npc.instance_count += 1

    def update(self, delta_time: float, ephase_name: str):
        enviro_influence(self, ephase_name)
        super().update(delta_time, ephase_name)


class Prop(Entity):
    instance_count: int = 0
    def __init__(self,
                groups: list[pygame.sprite.Group],
                img_filename: str,
                x: float,
                y: float,
            ):
        self.instance_id: int = Prop.instance_count
        prop_zero_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)  # Props special case direction, to init Entity.
        prop_zero_speed: float = 0.0  # Props special case speed, to init Entity.
        super().__init__(groups, img_filename, x, y, prop_zero_direction, prop_zero_speed)  # super.update() can be done before or after setting any self.* but think about how it might matter! Maybe not at all.
        Prop.instance_count += 1

    # I forgot that Entity.update() is where the surface itself is created based on direction L or R and thus we have
    # to call Entity.update() .. meaning super() from here.
    def update(self, delta_time: float, ephase_name: str):
        super().update(delta_time, ephase_name)
        # TRUE BUT WE CANNOT BYPASS Entity.update():
        # Props do not move. Update is for updating position and related actions. This suppresses Entity.update()
        # This is further argument for NOT subclassing Entity to make Props. Props are too different. we can make Prop it's
        # own class or even base-class since it might work well as that for many kinds of props.

    def physics_outer_walls(self):  # Overrides Entity.physics_outer_walls(), so we can disable that for Props.
        pass


# #############################################    FUNCTION DEFINITIONS    #############################################

# NOTE: Disabling enviro_influence temporarily for many reasons:    #### UPDATE: Now re-implementing. See UPDATE below.
# 1. I have removed spec from instances and this was where new enviro speeds are stored. I need to pass another way now.
# 2. I want to generalize so I need a tiny macro language to instruct enviro response changes to ANY ATTRIBUTE.
# 3. This macro system needs to be super simple and process efficiently OR just pass a simpler dict than spec.
# 4. Or use callbacks to little functions which implement the enviro responses.
# 5. When this is figured out I will re-enable the new form. None of this is in the tutorial anyhow.
# *** MyPy ERROR about PropSpec dict has no keys for p,r,c,f - BUT PropSpec WILL **NEVER** BE PASSED HERE !!! ???
# (UPDATE: I assume this error will return in a new form, complaining about e_p, e_r, e_c, e_f instead.)

#### UPDATE: Starting to re-implement with the enviro-phase-only stripped dict going back into the instances.
#            All enviro phase keys will not be prefixed with "e_"

def enviro_influence(xself: Player | Weapon | Npc, ephase_name: str) -> None:
    pass  # TEMPORARILY DISABLED PER THE ABOVE REASONS.
    # # ENVIRO PHASES - APPLICATION OF INFLUENCE OF CURRENT PHASE
    # if ephase_name == 'peace':
    #     xself.speed = xself.spec['e_p']
    # elif ephase_name == 'rogue':
    #     xself.speed = xself.spec['e_r']
    # elif ephase_name == 'chaos':
    #     xself.speed = xself.spec['e_c']
    # elif ephase_name == 'frozen':
    #     xself.speed = xself.spec['e_f']
    # else:
    #     raise ValueError(f"FATAL: Invalid ephase_name '{ephase_name}'. "
    #                      "Check values in ENVIRO_PHASES config.")

def load_image(
            filename: str,
            flip: bool,
            resize: bool,
            width: int | None,
            height: int | None,
        ) -> None:
    image_path = os.path.join(cfg.ASSET_PATH, filename)
    surface_l: pygame.Surface = pygame.Surface((0, 0))
    if resize:
        if width and height:
            with open(image_path, 'rb') as fh:
                img_bytes = fh.read()
            resized_png_bytes = resizer.alphonic_resize(
                    img_data=img_bytes,
                    width=width,
                    height=height,
                )
            # Output of this file was originally for validation, and now it is a workaround until frombytes() works.
            with open('load-image-temp-out-png.png', 'wb') as fh:
                fh.write(resized_png_bytes)
            # This image data is good! Proves problem is with pygame.image.frombytes()  (And then workaround was done.)
            new_size = (width, height)  # NOTE: This is the size of the already-resized image. No resizing occurs here.
            if cfg.PYGAME_FROMBYTES_IMAGE_LOAD_WORKAROUND_ENABLE:  # A BAD BUT VERY TEMPORARY HACK (which works great)
                # Obviously the following can have race conditions and is a very hackish hack and NOT a solution.
                filesystem_loaded_resized_surface_hack = pygame.image.load(
                    'load-image-temp-out-png.png'
                ).convert_alpha()
                surface_l = filesystem_loaded_resized_surface_hack  # For clarity
            else:
                alphonically_resized_surface = pygame.image.frombytes(
                        resized_png_bytes,
                        size=new_size,
                        format='RGBA',
                    ).convert_alpha()
                # ******************************************************************
                # PERSISTENT ERROR:
                #     fbtest = pygame.image.frombytes(img_bytes, size=(140, 140), format='RGBA').convert_alpha()
                #              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                # ValueError: Bytes length does not equal format and resolution size
                # ******************************************************************
                surface_l = alphonically_resized_surface
    else:
        surface_l = pygame.image.load(image_path).convert_alpha()

    if flip:
        surface_l = pygame.transform.flip(surface_l, True, False)

    # Mask mask_l made from surface_l regardless of resize or not, and must be done after possible flip (above):
    mask_l: pygame.Mask = pygame.mask.from_surface(surface_l)  # Mask from surface LEFT
    # And Mask Surface LEFT:
    mask_surf_l: pygame.Surface = mask_l.to_surface()  # Now a 'mask surface' from that (black & white silhouette)

    # Create RIGHT-facing surface and mask:
    surface_r: pygame.Surface = pygame.transform.flip(surface_l, True, False)
    mask_r: pygame.Mask = pygame.mask.from_surface(surface_r)  # Mask from surface RIGHT
    # And Mask Surface RIGHT:
    mask_surf_r: pygame.Surface = mask_r.to_surface()  # Now a 'mask surface' from that (black & white silhouette)

    # TODO: Mask Surfaces (not Masks) mask_surf_l and mask_surf_r MAY be used later for special effects.

    c_item: SurfCacheItem = {
            'surface_l': surface_l,
            'surface_r': surface_r,
            'mask_l': mask_l,
            'mask_r': mask_r,
            'mask_surf_l': mask_surf_l,
            'mask_surf_r': mask_surf_r,
        }
    SCACHE[filename] = c_item


def event_meatball(groups: list[pygame.sprite.Group]):
    meatball_spec = ent.weapon_specs[1]
    spawn_x = random.randint((0 - cfg.MEATBALL_SPAWN_MARGIN), (cfg.SCREEN_WIDTH + cfg.MEATBALL_SPAWN_MARGIN))
    spawn_y = random.randint((0 - 2 * cfg.MEATBALL_SPAWN_MARGIN), ( 0 - cfg.MEATBALL_SPAWN_MARGIN))
    projectile: Weapon = Weapon(
            groups=groups,
            img_filename=meatball_spec['img_filename'],
            x=spawn_x,
            y=spawn_y,
            direction=pygame.math.Vector2((0.0, 1.0)),  # Meatballs fall straight down.
            speed=meatball_spec['s'],
        )


def update_and_draw_scoreboard(
            arg_display_surface: pygame.display,
            arg_scoreboard_font: pygame.font.Font,
            score: int,
        ) -> None:
    # -------- SCOREBOARD TEXT
    score_text = str(score)
    scoreboard_surf: pygame.Surface = arg_scoreboard_font.render(
            text=score_text,
            antialias=True,
            color=cfg.SCR_FONT_COLOR,
            bgcolor=None,  # TODO: Should this arg just be left off?
        )
    scoreboard_rect: pygame.FRect = scoreboard_surf.get_frect(center=(cfg.SCR_X, cfg.SCR_Y))
    arg_display_surface.blit(scoreboard_surf, scoreboard_rect)

    # -------- SCORBOARD BORDER
    pygame.draw.rect(
            arg_display_surface,
            cfg.SCR_BORDER_COLOR,
            scoreboard_rect.inflate(cfg.SCR_BORDER_PAD_X, cfg.SCR_BORDER_PAD_Y)
                .move(0, cfg.SCR_FONT_ADJUST_Y),
            width=cfg.SCR_BORDER_THICKNESS,
            border_radius=cfg.SCR_BORDER_RADIUS,
        )


# ###############################################    INITIALIZATION    #################################################

pygame.init()

# # DEBUG/INFO-GATHER CODE
# system_fonts = pygame.font.get_fonts()
# for fontitem in system_fonts:
#     print(fontitem)

# INIT SCOREBOARD
if cfg.SCR_FONT_FORCE_SYSTEM:
    # TODO: Add a cascading load-font test to try for the most common font names based on pygame.font.get_fonts()
    # Each OS is going to have different fonts and issues with them, I am sure. Currently tested on Windows only.
    scoreboard_font = pygame.font.SysFont(cfg.SCR_SYSTEM_FONT, cfg.SCR_FONT_SIZE)
else:
    # Or we just use our included font. Probably a good default policy. This entire project is experimental, so we explore!
    scoreboard_font = pygame.font.Font(os.path.join(cfg.ASSET_PATH, cfg.SCR_FONT_FILENAME), cfg.SCR_FONT_SIZE)

# NOTE: If you request a bad System Font name, you get a warning and the PyGame still works. (some default font. cool.)
# "UserWarning: The system font 'notosansbold' couldn't be found. Did you mean: 'notosansmodi', 'notosanssymbols', 'notosansbuhid'?"
#     " ... Using the default font instead."


# INITIALIZE THE MAIN DISPLAY SURFACE (SCREEN / WINDOW)
display_surface = pygame.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
pygame.display.set_caption(cfg.GAME_TITLE)

# CREATE SPRITE GROUPS
all_sprites: pygame.sprite.Group = pygame.sprite.Group()
all_players: pygame.sprite.Group = pygame.sprite.Group()
all_weapons: pygame.sprite.Group = pygame.sprite.Group()  # TODO: Might go away. Need more specific groups.
all_meatballs: pygame.sprite.Group = pygame.sprite.Group()
all_greenballs: pygame.sprite.Group = pygame.sprite.Group()
all_npcs: pygame.sprite.Group = pygame.sprite.Group()
all_props: pygame.sprite.Group = pygame.sprite.Group()
all_colliders: pygame.sprite.Group = pygame.sprite.Group()

# GROUPS FOR DYNAMIC ENTITIES
new_greenballs_groups: list[pygame.sprite.Group] = [all_sprites, all_greenballs, all_colliders]
new_meatballs_groups: list[pygame.sprite.Group] = [all_sprites, all_meatballs, all_colliders]
# TODO: JUST NOTING HERE AGAIN AS IN OTHER PLACES. WE REALLY DON'T NEED all_sprites. And probably neither all_colliders


# GENERATE PROP SPECS - 'SPRAY' REPLICATED PROPS (randomly within specified radius, to specified count)
generated_prop_specs = []
for prop_t in ent.prop_templates:
    for index in range(prop_t['spray_count']):  # We will use the index for a unique prop name. Not critical.
        generated_prop_spec: ent.PropSpec = {
                'name': prop_t['name'] + str(index),  # Unique name of (sprayed) generated_prop_spec. (Compared to npc_spec which are hardcoded.)
                'instance_id': -1,  # -1 means instance not instantiated yet.
                'img_filename': prop_t['img_filename'],  # Copy the unchanging attributes from the template before handling dynamic ones.
                'flip': False,
                'resize': False,
                'w': prop_t['w'],
                'h': prop_t['h'],
                'color': prop_t['color'],
                'x': 0.0,  # placeholder (mpypy)
                'y': 0.0,  # placeholder (mpypy)
                }

        diameter = 2.0 * prop_t['spray_radius']  # This variable makes it easier to read/understand. Inline for perf.
        generated_prop_spec['name'] = prop_t['name'] + "-" + str(index)
        x_offset = random.uniform(0.0, diameter) - prop_t['spray_radius']  # uniform() gives a random float value
        y_offset = random.uniform(0.0, diameter) - prop_t['spray_radius']  # uniform() includes the limits
        generated_prop_spec['x'] = prop_t['x'] + x_offset
        generated_prop_spec['y'] = prop_t['y'] + y_offset

        generated_prop_specs.append(generated_prop_spec)


# ################################################    INSTANTIATION    #################################################

# TODO: See if we can move the prop spec (spraying/generation) code inside of prop instantiation. Probably can/should.


# INSTANITATE PLAYER SPRITE(S)
players: dict[str, Player] = {}
for i, player_spec in enumerate(ent.player_specs):
    player_spec['name'] = player_spec['name'] + str(i)
    player_spec['instance_id'] = i
    load_image(
            filename=player_spec['img_filename'],
            flip=player_spec['flip'],
            resize=player_spec['resize'],
            width=player_spec['w'],
            height=player_spec['h'],
        )
    player: Player = Player(
            groups=[all_sprites, all_players],
            img_filename=player_spec['img_filename'],
            weapon_spec=ent.weapon_specs[cfg.PLAYER_MAIN_WEAPON_INDEX],
            weapons_groups=new_greenballs_groups,
            x=player_spec['x'],
            y=player_spec['y'],
            direction=player_spec['d'],
            speed=player_spec['s'],
        )  # PyCharm FALSE WARNING HERE (AbstractGroup)
    players[player_spec['name']] = player  # Key off name or instance id. name should be unique

# INSTANITATE NPC SPRITES
npcs: dict[str, Npc] = {}
for i, npc_spec in enumerate(ent.npc_specs):
    npc_spec['instance_id'] = i
    load_image(
            filename=npc_spec['img_filename'],
            flip=npc_spec['flip'],
            resize=npc_spec['resize'],
            width=npc_spec['w'],
            height=npc_spec['h'],
        )
    npc: Npc = Npc(
            groups=[all_sprites, all_npcs, all_colliders],
            img_filename=npc_spec['img_filename'],
            x=npc_spec['x'],
            y=npc_spec['y'],
            direction=npc_spec['d'],
            speed=npc_spec['s'],
        )  # PyCharm FALSE WARNING HERE (AbstractGroup)
    npcs[npc_spec['name']] = npc  # Key off name or instance id. name should be unique

# INSTANITATE PROP SPRITES
props: dict[str, Prop] = {}
for i, generated_prop_spec in enumerate(generated_prop_specs):
    generated_prop_spec['instance_id'] = i
    load_image(
            filename=generated_prop_spec['img_filename'],
            flip=generated_prop_spec['flip'],
            resize=generated_prop_spec['resize'],
            width=generated_prop_spec['w'],
            height=generated_prop_spec['h'],
        )
    prop: Prop = Prop(
            groups=[all_sprites, all_props],
            img_filename=generated_prop_spec['img_filename'],
            x=generated_prop_spec['x'],
            y=generated_prop_spec['y'],
        )  # PyCharm FALSE WARNING HERE (AbstractGroup)
    props[generated_prop_spec['name']] = prop  # Key off name or instance id. name should be unique


# LOAD SURFACE CACHE WITH WEAPON DATA. (No Weapons have been instantiated at this point.)
for i, weapon_spec in enumerate(ent.weapon_specs):
    weapon_spec['instance_id'] = i
    load_image(
            filename=weapon_spec['img_filename'],
            flip=weapon_spec['flip'],
            resize=weapon_spec['resize'],
            width=weapon_spec['w'],
            height=weapon_spec['h'],
        )


# ###############################################    MAIN EXECUTION    #################################################

if not __name__ == '__main__':
    print("PyGameFun main.py has been imported. Some initialization has been performed. "
        "Main execution will not be started. Normally this file is executed as the app entry point and not imported.")
    sys.exit(0)

if cfg.DEBUG:
    bg_surface = pygame.Surface((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
    bg_surface.fill(cfg.BGCOLOR)
else:
    bg_surface = pygame.image.load(os.path.join(cfg.ASSET_PATH, cfg.BGIMG))

running: bool = True
ephase: dict[str, int] | None = None
g_ephase_name: str | None = None
g_score: int = 1776  # Normally 0. During development with continuous testing, starting at '1776'. Why 1776?
# The United States of America, the greatest nation on Earth, founded on freedom and the rights of the citizenry,
# formally came into existence in 1776 A.D., with the Declaration of Independence.

ephase_count: int = 0  # 0, not None since we will likly first/always do an arithmetic check on it, not an existence check.
clock = pygame.time.Clock()

# CUSTOM EVENTS - Random meatballs
meatball_event = pygame.event.custom_type()
pygame.time.set_timer(meatball_event, cfg.MEATBALL_SPAWN_TIME_MIN + cfg.MEATBALL_SPAWN_TIME_RANGE)
# TODO: Meatball spawn time with current timer is only set randomly once at game start. MAKE IT VARY ALL THE TIME.


#   * * * * * * * * * * * * * * * * * * * * * * * *
#   * * * * * * * *    MAIN LOOP    * * * * * * * *
#   * * * * * * * * * * * * * * * * * * * * * * * *
while running:
    g_delta_time = clock.tick(cfg.TICKRATE) / 1000  # Seconds elapsed for a single frame (e.g. - 60 Frm/sec = 0.017 sec/Frm)
    # TODO: I think I made this g_ early on because of shadowing warning that may no longer be an issue.
    #    Look into this again and maybe clarify further when/where/how I use g_ for either 1. limited and fully
    #    intentional use of a global variable or 2. to solve some shadowing issue usually with arguments or interior
    #    temp working vars. Seems like both issues can be solved in multiple ways so although I make VERY limited use
    #    of any global variables (almost always only constants, which is honestly a little different) .. but int fact
    #    alsmost NEVER --UPDATE-- a global variable from any interior namespace .. except now. In this case since we
    #    only have one score and one player possibly initiating changes to the score, we do not have any race condition
    #    concern. So in this case, updating the score (g_score) as a global variable feels just fine. No concerns.
    #    This is likely to change as I get more values I need to update centrally.


    # ##################################################    INPUT    ###################################################

    for event in pygame.event.get():  # Check all new events since the last main loop iteration
        if event.type == pygame.QUIT:
            running = False
        if event.type == meatball_event:
            event_meatball(groups=new_meatballs_groups)


    # #######################################    ENVIRONMENT PHASE PROCESSING    #######################################

    # ENVIRO_PHASES is a collections.deque instance and we popleft() the first/current 'phase'.
    #     Then we add the phase we removed from the left/start of the (deque) to the end (right side/last position).
    if ephase is None:
        ephase = cfg.ENVIRO_PHASES[0]
        g_ephase_name = ephase[0]
        ephase_count = ephase[1]
        cut_ephase = cfg.ENVIRO_PHASES.popleft()
        cfg.ENVIRO_PHASES.append(cut_ephase)
    else:
        ephase_count -= 1  # Decrement the counter for the current phase.
        if ephase_count < 1:
            ephase = None


    # #################################################    UPDATE    ###################################################

    all_props.update(g_delta_time, g_ephase_name)
    all_npcs.update(g_delta_time, g_ephase_name)
    all_players.update(g_delta_time, g_ephase_name)
    all_greenballs.update(g_delta_time, g_ephase_name)  # Must update GreenBalls (Weapons) AFTER Player since Player creates Weapons during Player update.
    all_meatballs.update(g_delta_time, g_ephase_name)


    # ###############################################    COLLISIONS    #################################################

    if players['buck0'].rect.collidepoint(pygame.mouse.get_pos()):  # Soon will likely use sprite collisions, not rect.
        print("BOINGGGGGGG!!")

    for greenball in all_greenballs:
        # greenball_col_sprites = pygame.sprite.spritecollide(greenball, all_meatballs, True)
        greenball_col_sprites = pygame.sprite.spritecollide(greenball, all_meatballs, True, pygame.sprite.collide_mask)
        if greenball_col_sprites:
            for col in greenball_col_sprites:
                g_score += 1  # g_ variable from outer scope. We do not need 'global' keyword. Limited use of these.
                print("                   *  *  *  BOOM!  *  *  *")
                greenball.kill()  # Meatball(s) was/were killed above in spritecollide(). Now greenball is killed too.


    # ##################################################    DRAW    ####################################################

    # REDRAW THE BACKGROUND
    if cfg.ACID_MODE is False:
        display_surface.blit(bg_surface, (0, 0))

    # IN ORDER OF DESIRED VISIBILITY-PRECEDENCE:
    all_props.draw(display_surface)
    all_npcs.draw(display_surface)
    all_meatballs.draw(display_surface)
    all_greenballs.draw(display_surface)

    # SCOREBOARD
    if cfg.SCR:
        update_and_draw_scoreboard(display_surface, scoreboard_font, g_score)

    # PLAYER(s)
    all_players.draw(display_surface)

    pygame.display.flip()  # Similar to update but not entire screen. TODO: Clarify
    # TODO: The tutorial has now gone back to using .update() at some point. Again, need to clarify and -> use best one.


#   - * - * - * - * - * - * - * - * - * - * - * - * -
#   - * - * - * -     END MAIN LOOP     - * - * - * -
#   - * - * - * - * - * - * - * - * - * - * - * - * -


pygame.quit()


##
#


# ###################################################    NOTES    ######################################################

# PYGAME-CE DOCS:
# https://pyga.me/docs/


##
#

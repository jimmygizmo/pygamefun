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

# TODO: Make into an Abstract Base Class using the ABC module.
class MapThing(pygame.sprite.Sprite):
    base_instance_count: int = 0
    def __init__(self,
                groups: list[pygame.sprite.Group],
                img_filename: str,
                x: float,
                y: float,
                angle: float,
            ):
        self.base_instance_id: int = MapThing.base_instance_count
        self.surface_l: pygame.Surface = SCACHE[img_filename]['surface_l']
        self.surface_r: pygame.Surface = SCACHE[img_filename]['surface_r']
        self.mask_l: pygame.Mask = SCACHE[img_filename]['mask_l']
        self.mask_r: pygame.Mask = SCACHE[img_filename]['mask_r']
        self.mask_surf_l: pygame.Surface = SCACHE[img_filename]['mask_surf_l']  # TODO: These may be used later for special effects.
        self.mask_surf_r: pygame.Surface = SCACHE[img_filename]['mask_surf_r']  # TODO: "
        self.x: float = x
        self.y: float = y
        self.angle: float = angle
        self.image: pygame.Surface | None = None  # Active image (depending on direction of motion).
        self.mask: pygame.Mask | None = None  # Active mask (depending on direction of motion).
        self.rect: pygame.FRect = pygame.FRect()
        super().__init__(groups)  # super.update() could be done first before setting all the self.* but for now I have them last.
        MapThing.base_instance_count += 1
        self.rect = self.surface_l.get_frect(center=(self.x, self.y))

        if cfg.WHITEOUT_MODE:
            self.mask_surf_l.set_colorkey((0, 0, 0))  # Make the black transparent.
            self.mask_surf_r.set_colorkey((0, 0, 0))  # "
            self.surface_l = self.mask_surf_l  # White-out the object.
            self.surface_r = self.mask_surf_r  # "

        # Props only use the LEFT side image and mask for everything, at this time.
        self.image = self.surface_l
        self.mask = self.mask_l

    # NOTICE: MapThing has no update(), no physics_outer_walls() like Entity has.


# TODO: Make into an Abstract Base Class using the ABC module.
class Entity(pygame.sprite.Sprite):
    base_instance_count: int = 0
    def __init__(self,
                groups: list[pygame.sprite.Group],
                img_filename: str,
                x: float,
                y: float,
                direction: pygame.math.Vector2,
                speed: float,
                angle: float,
                angular_vel: float,
                e_spec: ent.EnviroSpec | None = None,  # =None makes it optional. Prop has no e_spec. All others do.
            ):
        print(f"NEW ENTITY JUST CREATED WITH angular_vel: {angular_vel}")  #  *** DEBUG ***
        self.base_instance_id: int = Entity.base_instance_count
        self.surface_l: pygame.Surface = SCACHE[img_filename]['surface_l']
        self.surface_r: pygame.Surface = SCACHE[img_filename]['surface_r']
        self.mask_l: pygame.Mask = SCACHE[img_filename]['mask_l']
        self.mask_r: pygame.Mask = SCACHE[img_filename]['mask_r']
        self.mask_surf_l: pygame.Surface = SCACHE[img_filename]['mask_surf_l']  # TODO: These may be used later for special effects.
        self.mask_surf_r: pygame.Surface = SCACHE[img_filename]['mask_surf_r']  # TODO: "
        self.x: float = x
        self.y: float = y
        self.dir: pygame.math.Vector2 = direction
        self.speed: float = speed
        self.angle: float = angle
        self.angular_vel: float = angular_vel
        self.e_spec = e_spec
        self.image: pygame.Surface | None = None  # Active image (depending on direction of motion).
        self.mask: pygame.Mask | None = None  # Active mask (depending on direction of motion).
        self.rect: pygame.FRect = pygame.FRect()
        super().__init__(groups)  # super.update() could be done first before setting all the self.* but for now I have them last.
        Entity.base_instance_count += 1
        self.rect = self.surface_l.get_frect(center=(self.x, self.y))

        if cfg.WHITEOUT_MODE:
            self.mask_surf_l.set_colorkey((0, 0, 0))  # Make the black transparent.
            self.mask_surf_r.set_colorkey((0, 0, 0))  # "
            self.surface_l = self.mask_surf_l  # White-out the object.
            self.surface_r = self.mask_surf_r  # "

    def update(self, delta_time: float, ephase_name: str | None = None):
        delta_vector: pygame.math.Vector2 = self.dir * self.speed * delta_time
        # MYPY ERROR HERE - TRICKY ONE:
        # main.py:365: error: Incompatible types in assignment (expression has type "Vector2",
        #     variable has type "tuple[float, float]")  [assignment]
        self.rect.center += delta_vector
        # ***************************

        self.physics_outer_walls()  # Handle bouncing off walls. NOTE: Props override this and pass. Props ignore walls.
        # In fact, inside Props we override and pass update() too, so calling of physics_outer_walls() will never occur
        # here for props. To clarify, inside Prop, BOTH update() and physics_outer_walls() are overridden and passed.

        # Activate the correctly-facing image and mask, based on X direction. Use expensive rotation, if enabled.
        if cfg.ROTATION:
            self.angle += self.angular_vel  # ROTATE BY THE ANGULAR VELOCITY
            if self.angle >= 360:
                self.angle = 0.0
            if self.dir.x < 0:  # MOVING LEFT - ROTATION ENABLED
                self.image = pygame.transform.rotozoom(self.surface_l, self.angle, 1.0)
                self.mask = self.mask_l  # TODO: FIX THIS. WRONG MASK. NEEDS ROTATE.
            else:  # MOVING RIGHT - ROTATION ENABLED
                self.image = pygame.transform.rotozoom(self.surface_r, self.angle, 1.0)
                self.mask = self.mask_r  # TODO: FIX THIS. WRONG MASK. NEEDS ROTATE.
        else:  # No rotation:
            if self.dir.x < 0:  # MOVING LEFT
                self.image = self.surface_l
                self.mask = self.mask_l
            else:  # MOVING RIGHT
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

# TODO: IMPORTANT - RE BUG IN WHICH greenball spins not with its own angular_vel but with that for meatball. If we change the order
# in weapon_specs, the problem reverses. STRONG EVIDENCE SUGGESTS THAT THE BELOW "shadows name from outer scope" COULD VERY WELL
# BE OUR ISSUE. It is almost as if, we are using the LAST weapon_spec values .. well at leasst for AV. This bug has been tough.
# I'm not 100% sure. But confident that it is a good idea to try fixing that shadowing issue once and for all and then going
# from there.


class Player(Entity):
    instance_count: int = 0
    def __init__(self,
                groups: list[pygame.sprite.Group],
                img_filename: str,
                weapon_spec: ent.WeaponSpec,  # TODO: SOLVE THIS SHADOW ISSUE. REFER TO OTHER NOTES ON arg_ gr_ gw_ PREFIX IDEAS
                weapon_e_spec: ent.EnviroSpec,  # TODO: SOLVE THIS SHADOW ISSUE. REFER TO OTHER NOTES ON arg_ gr_ gw_ PREFIX IDEAS
                weapons_groups: list[pygame.sprite.Group],
                x: float,
                y: float,
                direction: pygame.math.Vector2,
                speed: float,
                angle: float,
                angular_vel: float,
                e_spec: ent.EnviroSpec | None = None,  # =None makes it optional. Don't pass e_spec and you get no enviro-behavior.
            ):
        self.instance_id: int = Player.instance_count
        self.weapon_spec = weapon_spec
        self.weapon_e_spec = weapon_e_spec
        self.weapons_groups = weapons_groups
        self.can_shoot: bool = True
        self.laser_shoot_time: int = 0
        self.cooldown_duration: int = cfg.LASER_COOLDOWN_DURATION  # milliseconds
        super().__init__(
            groups=groups,
            img_filename=img_filename,
            x=x,
            y=x,
            direction=direction,
            speed=speed,
            angle=angle,
            angular_vel=angular_vel,
            e_spec=e_spec)  # super.update() could be done first before setting all the self.* but for now I have them last.
        Player.instance_count += 1

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()  # Milliseconds since pygame.init() was called.
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, delta_time: float, ephase_name: str | None = None):
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
            print(f"NEW ORB (green-ball) WEAPON - ANGULAR VEL: {self.weapon_spec['av']}")  # *** DEBUG ***
            print(f"NEW ORB weapon_spec: {self.weapon_spec}")  # *** DEBUG ***  - NOTE: AV is correct in passed weapon_spec
            projectile: Weapon = Weapon(
                    groups=self.weapons_groups,
                    img_filename=weapon_img_filename,
                    x=self.rect.midtop[0],
                    y=self.rect.midtop[1],
                    direction=self.weapon_spec['d'],
                    speed=self.weapon_spec['s'],
                    angle=weapon_spec['a'],
                    angular_vel=weapon_spec['av'],
                    e_spec=self.weapon_e_spec,
                )
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
                angle: float,
                angular_vel: float,
                e_spec: ent.EnviroSpec | None = None,  # =None makes it optional. Don't pass e_spec and you get no enviro-behavior.
            ):
        debug_intermediate_angular_vel = angular_vel
        self.instance_id: int = Weapon.instance_count
        print(f"Weapon INIT for {img_filename} about to SUPER INIT. ANGULAR VELOCITY: {debug_intermediate_angular_vel}")  #  ***  DEBUG ***
        # IMPORTANT TROUBLESHOOTING CONCLUSION: For BOTH meatball and green-ball we are getting same AV, the value is only correct for meatball.
        # SO, green-ball is getting the AV for meatball at this point. Problem seems to be just before this point.
        # NOTE - IMPORTANT: In the FIRING CODE inside Player's update(), WE ARE PASSING THE CORRECT AV to Weapon() INIT.
        # Log output - - - - - - - - - - -
        # NEW WEAPON - ANGULAR VEL: 0.0
        # Weapon INIT for green-ball-140x140.png about to SUPER INIT. ANGULAR VELOCITY: 1.0
        # NEW WEAPON - ANGULAR VEL: 0.0
        # Weapon INIT for green-ball-140x140.png about to SUPER INIT. ANGULAR VELOCITY: 1.0
        # Weapon INIT for meatball-204x220.png about to SUPER INIT. ANGULAR VELOCITY: 1.0
        #                    *  *  *  BOOM!  *  *  *
        # End log output - - - - - - - - - -
        super().__init__(
            groups=groups,
            img_filename=img_filename,
            x=x,
            y=y,
            direction=direction,
            speed=speed,
            angle=angle,
            angular_vel=angular_vel,
            e_spec=e_spec)  # super.update() could be done first before setting all the self.* but for now I have them last.
        Weapon.instance_count += 1

    def update(self, delta_time: float, ephase_name: str | None = None):
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
                angle: float,
                angular_vel: float,
                e_spec: ent.EnviroSpec | None = None,  # =None makes it optional. Don't pass e_spec and you get no enviro-behavior.
            ):
        self.instance_id: int = Npc.instance_count
        super().__init__(
            groups=groups,
            img_filename=img_filename,
            x=x,
            y=y,
            direction=direction,
            speed=speed,
            angle=angle,
            angular_vel=angular_vel,
            e_spec=e_spec)  # super.update() could be done first before setting all the self.* but for now I have them last.

        Npc.instance_count += 1

    def update(self, delta_time: float, ephase_name: str | None = None):
        enviro_influence(self, ephase_name)
        super().update(delta_time, ephase_name)


class Prop(MapThing):
    instance_count: int = 0
    def __init__(self,
                groups: list[pygame.sprite.Group],
                img_filename: str,
                x: float,
                y: float,
                angle: float,
            ):
        self.instance_id: int = Prop.instance_count
        super().__init__(groups, img_filename, x, y, angle)  # super.update() can be done before or after setting any self.* but think about how it might matter! Maybe not at all.
        Prop.instance_count += 1


# #############################################    FUNCTION DEFINITIONS    #############################################

def enviro_influence(xself: Player | Weapon | Npc, ephase_name: str) -> None:
    if ephase_name == 'peace':
        xself.speed = xself.e_spec['e_p']
    elif ephase_name == 'rogue':
        xself.speed = xself.e_spec['e_r']
    elif ephase_name == 'chaos':
        xself.speed = xself.e_spec['e_c']
    elif ephase_name == 'frozen':
        xself.speed = xself.e_spec['e_f']
    else:
        raise ValueError(f"FATAL: Invalid ephase_name '{ephase_name}'. "
                         "Check values in ENVIRO_PHASES config.")


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

    mask_l: pygame.Mask = pygame.mask.from_surface(surface_l)  # Mask from surface LEFT. Done after possible flip and regardless of resize or not.
    mask_surf_l: pygame.Surface = mask_l.to_surface()  # Now a 'mask surface' from that (black & white silhouette)  # TODO: NOT USING THIS YET. Remove?

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


def event_meatball(groups: list[pygame.sprite.Group], e_spec_meatball: ent.EnviroSpec):
    meatball_spec = ent.weapon_specs[1]
    spawn_x = random.randint((0 - cfg.MEATBALL_SPAWN_MARGIN), (cfg.SCREEN_WIDTH + cfg.MEATBALL_SPAWN_MARGIN))
    spawn_y = random.randint((0 - 2 * cfg.MEATBALL_SPAWN_MARGIN), ( 0 - cfg.MEATBALL_SPAWN_MARGIN))
    # DUMMY_ANGLE: float = 0.0  # TODO: TEMPORARY, FIX THIS.
    # DUMMY_ANGULAR_VEL: float = 0.0  # TODO: TEMPORARY, FIX THIS.
    # print(meatball_spec)
    print(f"NEW MEATBALL - ANGULAR VEL: {meatball_spec['av']}")  # *** DEBUG ***
    projectile: Weapon = Weapon(
            groups=groups,
            img_filename=meatball_spec['img_filename'],
            x=spawn_x,
            y=spawn_y,
            direction=pygame.math.Vector2((0.0, 1.0)),  # Meatballs fall straight down.
            speed=meatball_spec['s'],
            angle=meatball_spec['a'],
            angular_vel=meatball_spec['av'],
            e_spec=e_spec_meatball,
        )


def update_and_draw_scoreboard(
            arg_display_surface: pygame.Surface,
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


def composed_enviro_spec(spec_in: ent.PlayerSpec | ent.WeaponSpec | ent.NpcSpec) -> ent.EnviroSpec:
    spec_out: ent.EnviroSpec = {  # Do we really need these bloated inits to keep PyCharm and MyPy type-hinting checks fully happy? NO.
            'e_p': -9999.9,  # Enviro: Peace (speed)
            'e_r': -9999.9,  # Enviro: Rogue (speed)
            'e_c': -9999.9,  # Enviro: Chaos (speed)
            'e_f': -9999.9,  # Enviro: Frozen (speed)
        }
    key: ent.EnviroKeys  # Must declare the type before the loop as we cannot do this in the for statement itself.
    for key in spec_in.keys():
        if key.startswith('e_'):
            spec_out[key] = spec_in[key]
    return spec_out


def template_generated_prop_specs():
    gen_prop_specs = []
    for prop_t in ent.prop_templates:
        for index in range(prop_t['spray_count']):  # We will use the index for a unique prop name. Not critical.
            gen_prop_spec: ent.PropSpec = {
                'name': prop_t['name'] + str(index),
                # Unique name of (sprayed) gen_prop_spec. (Compared to npc_spec which are hardcoded.)
                'instance_id': -1,  # -1 means instance not instantiated yet.
                'img_filename': prop_t['img_filename'],
                # Copy the unchanging attributes from the template before handling dynamic ones.
                'flip': False,
                'resize': False,
                'w': prop_t['w'],
                'h': prop_t['h'],
                'color': prop_t['color'],
                'x': 0.0,  # placeholder (mpypy)
                'y': 0.0,  # placeholder (mpypy)
                'a': prop_t['a'],
            }

            diameter = 2.0 * prop_t['spray_radius']  # Makes it easier to read/understand. Inline this for performance.
            gen_prop_spec['name'] = prop_t['name'] + "-" + str(index)
            x_offset = random.uniform(0.0, diameter) - prop_t['spray_radius']  # uniform() gives a random float value
            y_offset = random.uniform(0.0, diameter) - prop_t['spray_radius']  # uniform() includes the limits
            gen_prop_spec['x'] = prop_t['x'] + x_offset
            gen_prop_spec['y'] = prop_t['y'] + y_offset

            gen_prop_specs.append(gen_prop_spec)
    return gen_prop_specs


# ###############################################    INITIALIZATION    #################################################

pygame.init()

# INIT SCOREBOARD
if cfg.SCR_FONT_FORCE_SYSTEM:
    scoreboard_font = pygame.font.SysFont(cfg.SCR_SYSTEM_FONT, cfg.SCR_FONT_SIZE)
else:
    scoreboard_font = pygame.font.Font(os.path.join(cfg.ASSET_PATH, cfg.SCR_FONT_FILENAME), cfg.SCR_FONT_SIZE)


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
all_colliders: pygame.sprite.Group = pygame.sprite.Group()  # TODO: Might go away. We'll likely always be more specific.

# GROUPS FOR DYNAMIC ENTITIES
new_greenballs_groups: list[pygame.sprite.Group] = [all_sprites, all_greenballs, all_colliders]
new_meatballs_groups: list[pygame.sprite.Group] = [all_sprites, all_meatballs, all_colliders]
# TODO: JUST NOTING HERE AGAIN AS IN OTHER PLACES. WE REALLY DON'T NEED all_sprites. And probably neither all_colliders

generated_prop_specs = template_generated_prop_specs()


# ################################################    INSTANTIATION    #################################################

# Experimantal naming convention for variables at the global level which may have shadowing issues becuase their name
# is one likely to also be used in inner scopes. This is a system of a few prefixes to use on variable names, with
# a rough meaning:
# gr_    Lives in global scope and is intended for READ ONLY. Some bugs are still possible.
# gw_    Lives in global scope and may be written to. Many kinds of bugs possible if care is not taken.
# TODO: See notes, I had a third prefix I was considering.

# INSTANITATE PLAYER SPRITE(S)
players: dict[str, Player] = {}
for i, gr_player_spec in enumerate(ent.player_specs):
    gr_player_spec['name'] = gr_player_spec['name'] + str(i)
    gr_player_spec['instance_id'] = i
    load_image(
            filename=gr_player_spec['img_filename'],
            flip=gr_player_spec['flip'],
            resize=gr_player_spec['resize'],
            width=gr_player_spec['w'],
            height=gr_player_spec['h'],
        )
    gr_e_spec = composed_enviro_spec(gr_player_spec)
    gr_weapon_spec = ent.weapon_specs[cfg.PLAYER_MAIN_WEAPON_INDEX]
    gr_weapon_e_spec = composed_enviro_spec(gr_weapon_spec)  # TODO: This call COULD be done inside Player. Then we would not pass it to Player().
    player: Player = Player(
            groups=[all_sprites, all_players],
            img_filename=gr_player_spec['img_filename'],
            weapon_spec=gr_weapon_spec,
            weapon_e_spec=gr_weapon_e_spec,
            weapons_groups=new_greenballs_groups,
            x=gr_player_spec['x'],
            y=gr_player_spec['y'],
            direction=gr_player_spec['d'],
            speed=gr_player_spec['s'],
            angle=gr_player_spec['a'],
            angular_vel=gr_player_spec['av'],
            e_spec=gr_e_spec,
        )
    players[gr_player_spec['name']] = player  # Key off name or instance id. name should be unique

# INSTANITATE NPC SPRITES
npcs: dict[str, Npc] = {}
for i, gr_npc_spec in enumerate(ent.npc_specs):
    gr_npc_spec['instance_id'] = i
    load_image(
            filename=gr_npc_spec['img_filename'],
            flip=gr_npc_spec['flip'],
            resize=gr_npc_spec['resize'],
            width=gr_npc_spec['w'],
            height=gr_npc_spec['h'],
        )
    gr_e_spec = composed_enviro_spec(gr_npc_spec)
    npc: Npc = Npc(
            groups=[all_sprites, all_npcs, all_colliders],
            img_filename=gr_npc_spec['img_filename'],
            x=gr_npc_spec['x'],
            y=gr_npc_spec['y'],
            direction=gr_npc_spec['d'],
            speed=gr_npc_spec['s'],
            angle=gr_npc_spec['a'],
            angular_vel=gr_npc_spec['av'],
            e_spec=gr_e_spec,
        )
    npcs[gr_npc_spec['name']] = npc  # Key off name or instance id. name should be unique

# INSTANITATE PROP SPRITES
props: dict[str, Prop] = {}
for i, generated_prop_spec in enumerate(generated_prop_specs):
    generated_prop_spec['instance_id'] = i  # The instance id inside the class is totally different. ? Yes. TODO: Clarify.
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
            angle=generated_prop_spec['a'],
        )
    props[generated_prop_spec['name']] = prop  # Key off name or instance id. name should be unique


# LOAD SURFACE CACHE WITH WEAPON DATA. (No Weapons have been instantiated at this point. Just loading the cache.)
for i, gr_weapon_spec in enumerate(ent.weapon_specs):
    gr_weapon_spec['instance_id'] = i
    load_image(
            filename=gr_weapon_spec['img_filename'],
            flip=gr_weapon_spec['flip'],
            resize=gr_weapon_spec['resize'],
            width=gr_weapon_spec['w'],
            height=gr_weapon_spec['h'],
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
ephase: tuple[str, int] | None = None
g_ephase_name: str | None = None
g_score: int = 1776  # Normally 0. During development with continuous testing, starting at '9876'.


ephase_count: int = 0  # 0, not None since we will likly first/always do an arithmetic check on it, not an existence check.
clock = pygame.time.Clock()

# CUSTOM EVENTS - Random meatballs
meatball_event = pygame.event.custom_type()
pygame.time.set_timer(meatball_event, cfg.MEATBALL_SPAWN_TIME_MIN + cfg.MEATBALL_SPAWN_TIME_RANGE)
# TODO: Meatball spawn time with current timer is only set randomly once at game start. MAKE IT VARY ALL THE TIME.
e_spec_meatball = composed_enviro_spec(ent.weapon_specs[cfg.PLAYER_MAIN_WEAPON_INDEX])

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
            event_meatball(groups=new_meatballs_groups, e_spec_meatball=e_spec_meatball)


    # #######################################    ENVIRONMENT PHASE PROCESSING    #######################################

    # TODO: CHANGING TO LIST OF TUPLES, NOT COLLECTIONS.DEQUEUE.
    # ENVIRO_PHASES is a collections.deque instance and we popleft() the first/current 'phase'.
    #     Then we add the phase we removed from the left/start of the (deque) to the end (right side/last position).
    if ephase is None:
        ephase = cfg.ENVIRO_PHASES[0]
        g_ephase_name = ephase[0]
        ephase_count = ephase[1]
        cut_ephase = cfg.ENVIRO_PHASES.pop(0)  # Pop one off the left.
        cfg.ENVIRO_PHASES.append(cut_ephase)  # Stick it back on the right, and we'll use it for its specified duration.
    else:
        ephase_count -= 1  # Decrement the counter for the current ephase while we use it for its specified duration.
        if ephase_count < 1:
            ephase = None


    # #################################################    UPDATE    ###################################################

    all_props.update(g_delta_time, g_ephase_name)
    all_npcs.update(g_delta_time, g_ephase_name)
    all_players.update(g_delta_time, g_ephase_name)
    all_greenballs.update(g_delta_time, g_ephase_name)  # Must update GreenBalls (Weapons) AFTER Player since Player creates Weapons during Player update.
    all_meatballs.update(g_delta_time, g_ephase_name)


    # ###############################################    COLLISIONS    #################################################

    if players['buck0'].rect.collidepoint(pygame.mouse.get_pos()):  # Rect collision example. Mainly we will use sprite collisions, often using collide_mask.
        print("BOINGGGGGGG!!")

    for greenball in all_greenballs:
        # PyCharm Warning, POSSIBLY FALSE, on: "pygame.sprite.collide_mas" callback argument.
        # Expected type '(_SpriteSupportsGroup | Any, _TSprite2) -> Any | None'
        # (matched generic type '(_TSprite ≤: _SpriteSupportsGroup, _TSprite2 ≤: _SpriteSupportsGroup) -> Any | None'),
        # got '(left: _HasImageAndRect | _HasMaskAndRect, right: _HasImageAndRect | _HasMaskAndRect) -> tuple[int, int] | None' instead
        # NOTE: MyPy does not complain about this, only PyCharm. I have had other false warnings like this and some went away with PyCharm upgrades.
        greenball_col_sprites = pygame.sprite.spritecollide(greenball, all_meatballs, True, pygame.sprite.collide_mask)
        if greenball_col_sprites:
            for col in greenball_col_sprites:
                g_score += 1  # g_ variable from outer scope. We do not need 'global' keyword. Limited use of these.
                print("                   *  *  *  BOOM!  *  *  *")
                greenball.kill()


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

# Abstract Base Classes - Geeks Article:
# https://www.geeksforgeeks.org/abstract-classes-in-python/

# Abstract Base Classes - Python.Org:
# https://docs.python.org/3/library/abc.html


##
#

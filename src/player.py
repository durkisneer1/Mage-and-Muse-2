import pygame as pg
import math as m
from support import import_folder
from constants import WIN_WIDTH, WIN_HEIGHT


class Player:
    def __init__(self):
        self.anim_states = {
            "run": import_folder("../res/mage/run"),
            "fall": import_folder("../res/mage/fall"),
            "hit": import_folder("../res/mage/hit"),
            "jump": import_folder("../res/mage/jump"),
            "idle": import_folder("../res/mage/idle"),
        }

        self.status = "idle"
        self.frame_list = self.anim_states[self.status]
        self.current_frame = 0
        self.img = self.frame_list[self.current_frame]
        self.y_offset = 27  # Train top offset
        self.pos = pg.Vector2(
            WIN_WIDTH / 2, WIN_HEIGHT - self.img.get_height() - self.y_offset
        )
        self.rect = self.img.get_rect(midtop=self.pos)

        self.grav = -12
        self.on_ground = True
        self.direction = pg.Vector2(0, 0)

        self.speed = 10
        self.facing_right = True

        self.dash_time = 0
        self.dashed = False
        self.dash_scalar = 1

        self.on_cooldown = False
        self.hit_time = 0
        self.in_air = False
        self.air_time = 0

    def animate(self, dt: float):
        self.current_frame += dt * 0.8
        if self.current_frame >= len(self.frame_list):
            self.current_frame = 0

        if self.facing_right:
            self.img = self.frame_list[int(self.current_frame)]
        else:
            self.img = pg.transform.flip(
                self.frame_list[int(self.current_frame)], True, False
            )

    def jump(self, scalar: float = 1):
        self.direction.y = 36 * scalar
        self.on_ground = False

    def update(self, dt: float, keys: list[bool]):
        # Timer Setup
        current_time = pg.time.get_ticks()
        if self.on_cooldown and current_time - self.hit_time > 1000:
            self.on_cooldown = False
        if self.in_air and current_time - self.air_time > 400:
            self.in_air = False

        # Vertical Movement
        if self.on_ground:
            if keys[pg.K_SPACE]:
                self.jump()
        else:
            self.direction.y += self.grav * dt
            self.pos.y -= self.direction.y * dt

        # Horizontal Movement
        if keys[pg.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pg.K_d]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0
        self.dash_scalar = 10 if self.dashed else 1
        self.pos.x += self.direction.x * self.speed * self.dash_scalar * dt

        # Dashing
        if (
            keys[pg.K_LSHIFT]
            and not self.dashed
            and current_time - self.dash_time > 500
        ):
            self.dash_time = pg.time.get_ticks()
            self.dashed = True
        if self.dashed and current_time - self.dash_time > 50:
            self.dashed = False

        # Horizontal Bounding
        self.pos.x = min(max(self.pos.x, 0), WIN_WIDTH - self.img.get_width())

        # Vertical Bounding
        if self.pos.y > WIN_HEIGHT - self.img.get_height() - self.y_offset:
            self.pos.y = WIN_HEIGHT - self.img.get_height() - self.y_offset
            self.on_ground = True

        # Hitbox Alignment
        self.rect.midtop = self.pos

        self.update_status()
        self.animate(dt)

    def update_status(self):
        if self.on_ground:
            self.status = "idle" if self.direction.x == 0 else "run"
        else:
            if self.direction.y > 0:
                self.status = "hit" if self.in_air else "jump"
            else:
                self.status = "fall"
        self.frame_list = self.anim_states[self.status]

    def hit(self):
        hit_time = pg.time.get_ticks()
        self.jump(scalar=0.75)
        self.on_cooldown = True
        self.in_air = True
        self.hit_time = hit_time
        self.air_time = hit_time

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, "green", self.rect)
        screen.blit(self.img, self.rect)


class Wand:
    def __init__(self):
        raw_img = pg.image.load("../res/misc/wand/Wand.png").convert_alpha()
        self.img = pg.transform.rotate(raw_img, -135)
        self.rot_img = self.img
        self.rect = self.rot_img.get_rect()

    def rotate(self, mouse_pos: tuple[int, int]):
        rad = m.atan2(
            mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        )
        self.rot_img = pg.transform.rotate(self.img, m.degrees(rad))

    def update(self, player_pos: tuple, mouse_pos: tuple[int, int]):
        self.rotate(mouse_pos)
        self.rect = self.rot_img.get_rect(center=(player_pos[0], player_pos[1] + 5))

    def draw(self, screen: pg.Surface):
        screen.blit(self.rot_img, self.rect)

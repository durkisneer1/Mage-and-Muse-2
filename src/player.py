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
        self.rect = self.img.get_rect(topleft=self.pos)

        self.grav = -12
        self.on_ground = True
        self.direction = pg.Vector2(0, 0)

        self.speed = 10
        self.facing_right = True

        self.dash_time = 0
        self.dashed = False
        self.dash_scalar = 1

        self.stunned = False
        self.hit_time = 0
        self.on_cooldown = False

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

        self.rect = self.img.get_rect()

    def jump(self, scalar: float = 1):
        self.direction.y = 36 * scalar
        self.on_ground = False

    def movement(self, dt: float, keys: pg.key.get_pressed):
        current_time = pg.time.get_ticks()
        self.rect.topleft = self.pos

        if self.pos.y > WIN_HEIGHT - self.img.get_height() - self.y_offset:
            self.pos.y = WIN_HEIGHT - self.img.get_height() - self.y_offset
            self.on_ground = True

        if self.on_ground:
            self.stunned = False
            if keys[pg.K_SPACE]:
                self.jump()
        else:
            self.direction.y += self.grav * dt
            self.pos.y -= self.direction.y * dt

        if keys[pg.K_a]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pg.K_d]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0

        if keys[pg.K_LSHIFT] and not self.dashed and current_time - self.dash_time > 500:
            self.dash_time = pg.time.get_ticks()
            self.dashed = True
        self.dash_scalar = 10 if self.dashed else 1
        if self.dashed and current_time - self.dash_time > 50:
            self.dashed = False

        self.pos.x += self.direction.x * self.speed * self.dash_scalar * dt
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > WIN_WIDTH - self.img.get_width():
            self.pos.x = WIN_WIDTH - self.img.get_width()

        if current_time - self.hit_time > 1000 and self.on_cooldown:
            self.on_cooldown = False

    def get_status(self):
        if self.on_ground:
            self.status = "idle" if self.direction.x == 0 else "run"
        else:
            if self.direction.y > 0 and not self.stunned:
                self.status = "jump"
            # elif self.direction.y > 0 and self.stunned:
            #     self.status = "hit"
            else:
                self.status = "fall"
        self.frame_list = self.anim_states[self.status]

    def hit(self):
        self.jump(scalar=0.75)
        self.hit_time = pg.time.get_ticks()
        self.stunned = True
        self.on_cooldown = True

    def draw(self, screen: pg.Surface):
        self.get_status()
        screen.blit(self.img, self.pos)


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

    def update_pos(self, player_pos: tuple):
        self.rect = self.rot_img.get_rect(center=(player_pos[0], player_pos[1] + 5))

    def draw(self, screen: pg.Surface):
        screen.blit(self.rot_img, self.rect)

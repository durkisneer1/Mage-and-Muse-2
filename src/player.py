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

        self.frame_list = self.anim_states["idle"]
        self.img = self.anim_states["idle"][0]
        self.y_offset = 27  # Train top offset
        self.pos = pg.Vector2(
            WIN_WIDTH / 2, WIN_HEIGHT - self.img.get_height() - self.y_offset
        )
        self.rect = self.img.get_rect(topleft=self.pos)
        self.mask = pg.mask.from_surface(self.img)

        self.jump_vel = 0
        self.grav = -12
        self.on_ground = True

        self.speed = 10
        self.facing_right = True
        self.current_frame = 0

    def animate(self, dt):
        self.current_frame += dt * 0.8
        if self.current_frame > len(self.frame_list):
            self.current_frame = 0
        else:
            if self.facing_right:
                self.img = self.frame_list[int(self.current_frame)]
            else:
                self.img = pg.transform.flip(
                    self.frame_list[int(self.current_frame)], True, False
                )

        self.rect = self.img.get_rect()
        self.mask = pg.mask.from_surface(self.img)

    def bound(self):
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > WIN_WIDTH - self.img.get_width():
            self.pos.x = WIN_WIDTH - self.img.get_width()

    def movement(self, dt, keys):
        self.rect.topleft = self.pos

        if self.pos.y > WIN_HEIGHT - self.img.get_height() - self.y_offset:
            self.pos.y = WIN_HEIGHT - self.img.get_height() - self.y_offset
            self.on_ground = True

        if self.on_ground:
            self.frame_list = self.anim_states["idle"]
            if keys[pg.K_SPACE]:
                self.jump_vel = 36
                self.on_ground = False
        else:
            self.pos.y -= self.jump_vel * dt
            self.jump_vel += self.grav * dt
            if self.jump_vel > 0:
                self.frame_list = self.anim_states["jump"]
            else:
                self.frame_list = self.anim_states["fall"]

        if keys[pg.K_a]:
            self.pos.x -= self.speed * dt
            self.facing_right = False
            if self.on_ground:
                self.frame_list = self.anim_states["run"]
        if keys[pg.K_d]:
            self.pos.x += self.speed * dt
            self.facing_right = True
            if self.on_ground:
                self.frame_list = self.anim_states["run"]

        self.bound()

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)


class Wand:
    def __init__(self):
        raw_img = pg.image.load("../res/misc/wand/Wand.png").convert_alpha()
        self.img = pg.transform.rotate(raw_img, -135)
        self.rot_img = self.img
        self.rect = self.rot_img.get_rect()

    def rotate(self, mouse_pos):
        radians = m.atan2(
            mouse_pos[0] - self.rect.centerx, mouse_pos[1] - self.rect.centery
        )
        degrees = radians * (180 / m.pi)

        self.rot_img = pg.transform.rotate(self.img, degrees)

    def update_pos(self, player_pos: tuple):
        self.rect = self.rot_img.get_rect(center=(player_pos[0], player_pos[1] + 5))

    def draw(self, screen: pg.Surface):
        screen.blit(self.rot_img, self.rect)

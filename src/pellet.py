import pygame as pg
import math as m
import random as rand
from constants import *


class Pellet(pg.sprite.Sprite):
    def __init__(
            self,
            groups: pg.sprite.Group,
            spawn_pos: tuple,
            img: pg.Surface,
            mouse_pos: tuple,
    ):
        super().__init__(groups)

        self.speed = 20
        self.pos = pg.Vector2(
            spawn_pos[0] - img.get_width() / 2,
            (spawn_pos[1] + 5) - img.get_height() / 2,
        )
        self.img = img
        self.rect = self.img.get_rect(topleft=self.pos)
        self.vel = pg.Vector2(self.direction(mouse_pos))

        self.turn_tick = 0

    def rotate(self, dt):
        self.turn_tick += dt
        if self.turn_tick > 1:
            self.img = pg.transform.rotate(self.img, 90)
            self.turn_tick = 0

    def direction(self, mouse_pos) -> tuple[float, float]:
        radians = m.atan2((self.pos.y - mouse_pos[1]), (self.pos.x - mouse_pos[0]))
        x_vel = m.cos(radians) * self.speed
        y_vel = m.sin(radians) * self.speed
        return x_vel, y_vel

    def bound_check(self) -> bool:
        return (
                self.pos.x < 0
                or self.pos.x > WIN_WIDTH
                or self.pos.y < 0
                or self.pos.y > WIN_HEIGHT
        )

    def movement(self, dt):
        self.pos -= self.vel * dt
        self.rect.topleft = self.pos

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)
        if self.bound_check():
            self.kill()


class PelletExplode(pg.sprite.Sprite):
    def __init__(self, groups: pg.sprite.Group, spawn_pos, anim_frames):
        super().__init__(groups)

        self.anim_frames = anim_frames
        self.img = self.anim_frames[0]

        offset_pos = (rand.randint(-4, 4), rand.randint(-4, 4))
        new_spawn = (spawn_pos[0] + offset_pos[0], spawn_pos[1] + offset_pos[1])
        self.pos = pg.Vector2(new_spawn)

        self.current_frame = 0

    def animate(self, dt):
        self.current_frame += dt * 2
        if self.current_frame > len(self.anim_frames):
            self.kill()
        else:
            self.img = self.anim_frames[int(self.current_frame)]

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)

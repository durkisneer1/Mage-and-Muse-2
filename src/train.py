import math

import pygame as pg
from src.constants import *


class Train:
    def __init__(self, image: pg.Surface):
        self.img = image

        x_offset = -8
        self.pos = pg.Vector2(x_offset, WIN_HEIGHT - self.img.get_height())
        self.speed = 250
        self.angle = 0
        self.step = 90

        positions_list = []
        for deg in range(0, 360, self.step):
            rad = math.radians(deg)
            x_pos = math.sin(rad) + x_offset
            positions_list.append(x_pos)
        self.positions = tuple(positions_list)

    def update(self, dt: float):
        index = int(self.angle / self.step)
        self.pos.x = self.positions[index]
        self.angle += dt * self.speed
        self.angle %= 360

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)


class TrainFire(pg.sprite.Sprite):
    def __init__(
        self,
        group: pg.sprite.Group,
        fire_frames: list[pg.Surface],
        x_offset: int,
    ):
        super().__init__(group)

        self.max_frames = len(fire_frames)
        self.frame_list = fire_frames
        self.current_frame = 0
        self.anim_speed = 1.5
        self.fire_img = self.frame_list[self.current_frame]
        fire_size = self.fire_img.get_size()

        self.pos = pg.Vector2(
            x_offset - fire_size[0] / 2, WIN_HEIGHT - fire_size[1] - 28
        )
        self.hitbox = pg.FRect(
            (self.pos.x, self.pos.y + fire_size[1] * 2 / 3),
            (fire_size[0], fire_size[1] / 3),
        )

        self.loops = 0

    def update(self, dt: float):
        if self.current_frame >= self.max_frames:
            self.current_frame = 0
            self.loops += 1
        self.fire_img = self.frame_list[int(self.current_frame)]
        self.current_frame += self.anim_speed * dt

        if self.loops > 4:
            self.kill()

    def draw(self, screen: pg.Surface):
        screen.blit(self.fire_img, self.pos)

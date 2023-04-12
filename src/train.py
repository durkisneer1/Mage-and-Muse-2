import math

import pygame as pg
from src.constants import *


class Train:
    def __init__(self):
        self.img = pg.image.load("./res/train/Train.png").convert_alpha()
        img_height = self.img.get_height()

        x_offset = -8
        self.pos = pg.Vector2(x_offset, WIN_HEIGHT - img_height)
        self.speed = 250
        self.angle = 0

        positions_list = []
        for deg in range(0, 360):
            rad = math.radians(deg)
            x_pos = math.sin(rad) + x_offset
            positions_list.append((x_pos, WIN_HEIGHT - img_height))
        self.positions = tuple(positions_list)

    def update(self, dt: float):
        index = int(self.angle)
        self.pos.x = self.positions[index][0]
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
        self.hitbox = pg.FRect(self.pos, fire_size)

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
        # pg.draw.rect(screen, (255, 0, 0), self.hitbox)

import pygame as pg
import random

from src.constants import *


class Bull(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, anim_frames: list[pg.Surface]):
        super().__init__(group)
        self.side = random.choice(["left", "right"])

        self.frame_list = (
            [pg.transform.flip(i, True, False) for i in anim_frames]
            if self.side == "right"
            else anim_frames
        )
        self.max_frames = len(self.frame_list)
        self.img = self.frame_list[0]

        start_x = -self.img.get_width() if self.side == "left" else WIN_WIDTH
        self.pos = pg.Vector2(start_x, WIN_HEIGHT - self.img.get_height() - 25)
        self.pos_offset = (12, 5)
        hitbox_size = (
            self.img.get_width() - self.pos_offset[0],
            self.img.get_height() - self.pos_offset[1],
        )
        self.rect = pg.FRect(self.pos, hitbox_size)
        self.hitbox = self.rect

        self.speed = 14 if self.side == "left" else -14
        self.current_frame = 0
        self.anim_speed = 1.4

        self.health = 2

    def animate(self, dt: float):
        self.current_frame %= self.max_frames
        self.img = self.frame_list[int(self.current_frame)]
        self.current_frame += self.anim_speed * dt

    def hit(self):
        self.health -= 1
        if self.health == 0:
            self.kill()

    def update(self, dt: float, *args) -> None:
        self.animate(dt)

        if self.side == "left":
            self.rect.topleft = (
                self.pos.x + self.pos_offset[0],
                self.pos.y + self.pos_offset[1],
            )
        elif self.side == "right":
            self.rect.topleft = (self.pos.x, self.pos.y + self.pos_offset[1])
        self.pos.x += self.speed * dt

        self.hitbox = self.rect

        if -self.img.get_width() - 1 <= self.pos.x <= WIN_WIDTH:
            return
        self.kill()

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)

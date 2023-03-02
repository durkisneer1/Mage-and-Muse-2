import pygame as pg
import math as m
from constants import *
from support import import_folder


class Skull(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group):
        super().__init__(group)

        self.img = pg.image.load("../res/skull/idle.png").convert_alpha()
        self.x_offset, self.y_offset = (WIN_WIDTH / 2, WIN_HEIGHT / 2 - 17)
        self.pos = pg.Vector3(self.x_offset, self.y_offset, 0)
        self.rect = self.img.get_rect(center=self.pos.xy)

        self.flower_frames = import_folder("../res/skull/flower")
        self.shadow_frames = import_folder("../res/skull/shadow")
        self.flower_pos = [
            pg.Vector2(self.x_offset - 19, self.y_offset),
            pg.Vector2(self.x_offset + 19, self.y_offset),
        ]
        self.current_frame = 0
        self.current_flower = self.flower_frames[int(self.current_frame)]
        self.current_shadow = self.shadow_frames[int(self.current_frame)]
        self.max_frames = len(self.flower_frames)

        self.angle = 0
        self.speed = 12

    def animate(self, dt):
        if self.current_frame >= self.max_frames:
            self.current_frame = 0
        self.current_flower = self.flower_frames[int(self.current_frame)]
        self.current_shadow = self.shadow_frames[int(self.current_frame)]
        self.current_frame += dt

    def update(self, dt: float):
        self.animate(dt)

        self.pos.y = (m.sin(m.radians(self.angle)) * 15) + self.y_offset
        self.rect.center = self.pos.xy
        self.angle += self.speed * dt

        for pos in self.flower_pos:
            pos.y = self.pos.y - 3

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.rect)
        for pos in self.flower_pos:
            shadow_rect = self.current_shadow.get_rect(center=(pos.x - 1, pos.y + 1))
            flower_rect = self.current_flower.get_rect(center=pos)
            screen.blit(self.current_shadow, shadow_rect)
            screen.blit(self.current_flower, flower_rect)

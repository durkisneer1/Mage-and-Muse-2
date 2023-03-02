import pygame as pg
import math as m
from constants import *


class Skull(pg.sprite.Group):
    def __init__(self, group: pg.sprite.Group):
        super().__init__(group)
        self.img = pg.image.load("../res/skull/idle.png").convert_alpha()
        self.pos_offset = (WIN_WIDTH / 2, WIN_HEIGHT / 2)
        self.pos = pg.Vector2(self.pos_offset)
        self.rect = self.img.get_rect(center=self.pos)

        self.angle = 0
        self.speed = 10

    def move(self, dt: float):
        self.pos.y = (m.sin(m.radians(self.angle)) * 25) + self.pos_offset[1]
        self.rect.center = self.pos
        self.angle += self.speed * dt

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.rect)
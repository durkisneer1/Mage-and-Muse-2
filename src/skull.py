import pygame as pg
import math as m
from constants import *


class Skull(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group):
        super().__init__(group)

        self.img = pg.image.load("../res/skull/idle.png").convert_alpha()
        self.x_offset, self.y_offset = (WIN_WIDTH / 2, WIN_HEIGHT / 2 - 17)
        self.pos = pg.Vector3(self.x_offset, self.y_offset, 0)
        self.rect = self.img.get_rect(center=self.pos.xy)

        self.angle = 0
        self.speed = 12

    def update(self, dt: float):
        self.pos.y = (m.sin(m.radians(self.angle)) * 15) + self.y_offset
        self.rect.center = self.pos.xy
        self.angle += self.speed * dt

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.rect)

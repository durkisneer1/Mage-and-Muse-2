import pygame as pg
import random

from src.constants import *


class Rain(pg.sprite.Sprite):
    template = pg.Surface((1, 4))
    rain_colors = (
        (55, 148, 110),
        (50, 60, 57),
        (63, 63, 116),
        (48, 96, 130),
        (91, 110, 225),
        (99, 155, 255),
        (95, 205, 228),
        (132, 126, 135),
        (105, 106, 106),
        (89, 86, 82),
    )  # Blue-Green-Gray Colors

    def __init__(
        self,
        group: pg.sprite.Group,
    ):
        super().__init__(group)

        self.img = self.template.copy()
        self.img.fill(random.choice(self.rain_colors))
        self.rect = self.img.get_frect()
        self.pos = pg.Vector2(random.randint(-150, 800), 0)
        self.speed = random.randint(15, 30)
        self.momentum = 9 - self.speed / 5

    def update(self, dt: float):
        self.pos.y += self.speed * dt
        self.pos.x += self.momentum * dt
        if self.pos.y > WIN_HEIGHT or self.pos.x > WIN_WIDTH:
            self.kill()

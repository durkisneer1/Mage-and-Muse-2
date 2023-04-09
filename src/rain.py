import pygame as pg
import random

from src.constants import *


class Rain(pg.sprite.Sprite):
    def __init__(
        self,
        group: pg.sprite.Group,
        rain_surface: pg.Surface,
        colors: tuple[tuple[int, int, int], ...],
    ):
        super().__init__(group)

        self.img = rain_surface.copy()
        self.img.fill(random.choice(colors))
        self.rect = pg.FRect(self.img.get_rect())
        self.pos = pg.Vector2(random.randint(-150, 800), 0)
        self.speed = 30  # random.randint(10, 20)
        self.momentum = 6

    def update(self, dt: float):
        self.pos.y += self.speed * dt
        self.pos.x += self.momentum * dt
        if self.pos.y > WIN_HEIGHT or self.pos.x > WIN_WIDTH:
            self.kill()

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)

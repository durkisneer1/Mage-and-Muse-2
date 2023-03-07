import pygame as pg
import random
import math as m
from constants import *


class Taco(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, img: pg.Surface):
        super().__init__(group)

        self.img = img
        self.rot_img = self.img
        self.side = random.choice(["left", "right"])
        if self.side == "right":
            self.img = pg.transform.flip(self.img, True, False)

        self.size = self.img.get_size()
        start_x = (
            -self.size[0] if self.side == "left" else WIN_WIDTH + (self.size[0] / 2)
        )
        self.pos = pg.Vector2(start_x, self.size[1])
        self.rect = self.rot_img.get_rect(center=self.pos)

        self.speed = 14 if self.side == "left" else -14
        self.health = 2
        self.angle = 0

    def hit(self):
        self.health -= 1
        if self.health == 0:
            self.kill()

    def update(self, dt) -> bool:
        self.pos.x += self.speed * dt
        self.angle += dt * 100
        self.angle %= 360

        rad = m.radians(self.angle)
        pivot = m.sin(rad) * 30

        self.rot_img = pg.transform.rotate(self.img, pivot)
        self.rect = self.rot_img.get_rect(center=self.pos)

        return self.rect.right < -self.size[0] or self.rect.left > WIN_WIDTH

    def draw(self, screen: pg.Surface):
        screen.blit(self.rot_img, self.rect)

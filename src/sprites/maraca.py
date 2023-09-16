import functools
import math

import pygame as pg
from src.constants import WIN_WIDTH, WIN_HEIGHT
from src.utils import import_folder


class Maraca(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, brother: bool):
        super().__init__(group)
        self.anim_states = {
            "idle": import_folder("./res/maraca"),
            "hit": import_folder("./res/maraca", highlight=True),
        }

        self.frame_list = self.anim_states["idle"]
        self.current_frame = 0
        self.img = self.anim_states["idle"][self.current_frame]  # pg.Surface
        self.img_width = self.img.get_width()
        self.rect = self.img.get_frect()
        self.pos = pg.Vector3(0, WIN_HEIGHT - self.img.get_height(), 0)

        self.angle = 0
        self.current_frame = 0
        self.multiplier = 1 if brother else -1
        self.speed = 6 * self.multiplier
        self.health = 5  # Default 50

        self.hit_time = 0
        self.animate_death = False

    @staticmethod
    @functools.cache
    def cache_scaled(img: pg.Surface, factor: float) -> pg.Surface:
        return pg.transform.scale_by(img, factor)

    def hit(self):
        self.health -= 1
        self.hit_time = pg.time.get_ticks()
        self.frame_list = self.anim_states["hit"]

    def animate(self, dt: float):
        if pg.time.get_ticks() - self.hit_time > 80:
            self.frame_list = self.anim_states["idle"]

        self.current_frame %= len(self.frame_list)
        self.img = self.frame_list[int(self.current_frame)]
        self.current_frame += dt * 0.8

    def update(self, dt: float):
        self.animate(dt)

        if self.animate_death:
            self.speed *= 1 + dt / 4
            self.pos.y -= dt * abs(self.speed) / 4
            if self.pos.y < -self.img.get_height():
                self.kill()

        self.angle += dt * self.speed
        self.angle %= 360
        rad = math.radians(self.angle)

        self.pos.x = (math.sin(rad) * 125) + (WIN_WIDTH / 2) - (self.img_width / 3)
        self.pos.z = math.cos(rad) * self.multiplier

        self.img = Maraca.cache_scaled(self.img, ((self.pos.z / 4) + 0.75))

    def draw_collider(self):
        box_height = self.img.get_height() / 3
        box_width = self.img_width - (self.img_width / 5)
        x_offset = self.pos.x + (box_width / 8)
        y_offset = self.pos.y + (box_height / 8)
        self.rect.topleft = x_offset, y_offset
        self.rect.size = box_width, box_height

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos.xy)
        self.draw_collider()

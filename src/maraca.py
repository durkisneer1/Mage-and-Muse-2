import functools
import math

import pygame as pg
from src.constants import WIN_WIDTH, WIN_HEIGHT
from src.support import import_folder


class Maraca(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, brother: bool):
        super().__init__(group)
        self.anim_states = {"idle": import_folder("./res/maraca/idle")}

        self.frame_list = self.anim_states["idle"]
        self.current_frame = 0
        self.img = self.anim_states["idle"][self.current_frame]  # pg.Surface
        self.rect = pg.FRect(self.img.get_rect())
        self.pos = pg.Vector3(0, WIN_HEIGHT - self.img.get_height(), 0)

        # start_x = 0 if brother else WIN_WIDTH - self.img.get_width()

        self.angle = 0
        self.current_frame = 0
        self.speed = 6
        self.health = 50  # Default 50

        multiplier = 1 if brother else -1
        positions_list = []
        for deg in range(0, 360):
            rad = math.radians(deg * multiplier)
            x = math.sin(rad) * 125 + (WIN_WIDTH / 2) - (self.img.get_width() / 3)
            z = math.cos(rad) * multiplier
            positions_list.append((x, z))
        self.positions = tuple(positions_list)
        print(len(self.positions))

    @staticmethod
    @functools.cache
    def cache_scaled(img: pg.Surface, factor: float):
        return pg.transform.scale_by(img, factor)

    def animate(self, dt: float):
        self.current_frame %= len(self.frame_list)
        self.img = self.frame_list[int(self.current_frame)]
        self.current_frame += dt * 0.8

    def update(self, dt: float):
        self.animate(dt)

        index = int(self.angle)
        self.pos.x = self.positions[index][0]
        self.pos.z = self.positions[index][1]
        self.angle += dt * self.speed
        self.angle %= 360

        self.img = Maraca.cache_scaled(self.img, ((self.pos.z / 4) + 0.75))

    def draw_collider(self):
        box_height = self.img.get_height() / 3
        box_width = self.img.get_width() - (self.img.get_width() / 5)
        x_offset = self.pos.x + (box_width / 8)
        y_offset = self.pos.y + (box_height / 8)
        self.rect.topleft = x_offset, y_offset
        self.rect.size = box_width, box_height

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos.xy)
        self.draw_collider()

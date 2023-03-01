import pygame as pg
from constants import WIN_WIDTH, WIN_HEIGHT
from support import import_folder
import math as m


class Maraca(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, brother: bool):
        super().__init__(group)
        self.anim_states = {"idle": import_folder("../res/maraca/idle")}

        self.frame_list = self.anim_states["idle"]
        self.img = self.anim_states["idle"][0]  # pg.Surface
        self.rect = self.img.get_rect()

        start_x = 0 if brother else WIN_WIDTH - self.img.get_width()
        self.pos = pg.Vector3(start_x, WIN_HEIGHT - self.frame_list[0].get_height(), 0)

        self.speed = 6
        self.multiplier = 1 if brother else -1
        self.current_frame = 0
        self.angle = 0
        self.z_pos = 0

    def animate(self, dt: float):
        self.current_frame += dt * 0.8
        if self.current_frame >= len(self.frame_list):
            self.current_frame = 0
        self.img = self.frame_list[int(self.current_frame)]

    def movement(self, dt: float):
        self.angle += dt * self.speed * self.multiplier
        rad = m.radians(self.angle)
        self.pos.z = m.cos(rad) * self.multiplier
        self.pos.x = (m.sin(rad) * 125) + (WIN_WIDTH / 2) - (self.img.get_width() * 0.5)

        self.img = pg.transform.scale_by(self.img, ((self.pos.z / 4) + 0.75))

    def hitbox(self):
        box_height = self.img.get_height() / 3
        box_width = self.img.get_width() - (self.img.get_width() / 5)
        x_offset = self.pos.x + (box_width / 8)
        y_offset = self.pos.y + (box_height / 8)
        self.rect.topleft = x_offset, y_offset
        self.rect.size = box_width, box_height

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos.xy)
        self.hitbox()

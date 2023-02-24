import pygame as pg
from constants import WIN_WIDTH, WIN_HEIGHT
from support import import_folder


class Maraca(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, brother: bool):
        super().__init__(group)
        self.anim_states = {"idle": import_folder("../res/maraca/idle")}

        self.frame_list = self.anim_states["idle"]
        self.img = self.anim_states["idle"][0]  # pg.Surface
        self.rect = self.img.get_rect()

        start_x = 0 if brother else WIN_WIDTH - self.img.get_width()
        self.pos = pg.Vector2(start_x, WIN_HEIGHT - self.frame_list[0].get_height())

        self.speed = 7 if brother else -7
        self.current_frame = 0

    def animate(self, dt):
        self.current_frame += dt * 0.8
        if self.current_frame > len(self.frame_list):
            self.current_frame = 0
        else:
            self.img = self.frame_list[int(self.current_frame)]

    def movement(self, dt):
        self.pos.x += self.speed * dt
        if self.pos.x < 0:
            self.pos.x = 0
            self.speed *= -1
        elif self.pos.x > WIN_WIDTH - self.img.get_width():
            self.pos.x = WIN_WIDTH - self.img.get_width()
            self.speed *= -1

    def draw_hitbox(self):
        box_height = self.img.get_height() / 3
        box_width = self.img.get_width() - (self.img.get_width() / 5)
        x_offset = self.pos.x + (box_width / 8)
        y_offset = self.pos.y + (box_height / 8)
        self.rect = pg.Rect((x_offset, y_offset), (box_width, box_height))

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)
        self.draw_hitbox()

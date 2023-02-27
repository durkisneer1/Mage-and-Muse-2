import pygame as pg
import random
from constants import *


class Bull(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, anim_frames):
        super().__init__(group)

        self.frame_list = anim_frames
        self.max_frames = len(self.frame_list)
        self.img = self.frame_list[0]  # pg.Surface
        self.rect = self.img.get_rect()
        self.mask = pg.mask.from_surface(self.img)

        self.side = random.choice(["left", "right"])
        start_x = -self.img.get_width() if self.side == "left" else WIN_WIDTH
        self.pos = pg.Vector2(
            start_x, WIN_HEIGHT - self.frame_list[0].get_height() - 25
        )

        self.speed = 14 if self.side == "left" else -14
        self.current_frame = 0
        self.anim_speed = 1.4

        self.health = 2

    def animate(self, dt):
        self.current_frame += self.anim_speed * dt
        if self.current_frame >= self.max_frames:
            self.current_frame = 0

        if self.side == "left":
            self.img = self.frame_list[int(self.current_frame)]
        else:
            self.img = pg.transform.flip(
                self.frame_list[int(self.current_frame)], True, False
            )

        self.rect = self.img.get_rect()
        self.mask = pg.mask.from_surface(self.img)

    def update(self, dt) -> bool:
        self.rect.topleft = self.pos
        self.pos.x += self.speed * dt

        return self.pos.x < -self.img.get_width() or self.pos.x > WIN_WIDTH

    def hit(self):
        self.health -= 1
        if self.health < 0:
            self.kill()

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.pos)

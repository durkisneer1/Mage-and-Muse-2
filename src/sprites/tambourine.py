import pygame as pg
from random import choice
from src.constants import WIN_WIDTH


class Tambourine(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, image: pg.Surface, dest_pos: tuple[float, float]):
        super().__init__(group)

        self.left = choice([True, False])
        self.rot_direction = -1 if self.left else 1
        self.pos = pg.Vector2(0 if self.left else WIN_WIDTH, 0)
        self.velocity = (pg.Vector2(dest_pos) - self.pos).normalize() * 18
        self.image = image
        self.rot_image = image.copy()
        self.rect = self.image.get_frect(center=self.pos)
        self.hitbox = self.rect.inflate(-8, -8)
        self.angle = 0
        self.health = 2

    def hit(self):
        self.health -= 1
        if self.health == 0:
            self.kill()

    def rotate(self, dt):
        self.angle += dt * 50 * self.rot_direction
        self.angle %= 360
        self.rot_image = pg.transform.rotate(self.image, self.angle)

    def update(self, dt):
        self.rotate(dt)

        self.pos += self.velocity * dt
        self.rect = self.rot_image.get_frect(center=self.pos)
        self.hitbox.center = self.rect.center = self.pos

    def draw(self, screen: pg.Surface):
        screen.blit(self.rot_image, self.rect)

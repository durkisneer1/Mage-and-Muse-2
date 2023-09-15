import pygame as pg
from random import choice
from src.constants import WIN_WIDTH


class Trumpet(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, image: pg.Surface, dest_pos: tuple[float, float]):
        super().__init__(group)

        self.left = choice([True, False])
        self.pos = pg.Vector2(0 if self.left else WIN_WIDTH, 0)
        self.velocity = (pg.Vector2(dest_pos) - self.pos).normalize() * 10
        self.angle = -self.velocity.as_polar()[1]
        self.image = pg.transform.rotate(
            pg.transform.flip(image, False, not self.left),
            self.angle,
        )
        self.rect = self.image.get_rect(center=self.pos)
        self.hitbox = self.rect

    def update(self, dt):
        self.pos += self.velocity * dt
        self.hitbox.center = self.rect.center = self.pos

    def draw(self, screen: pg.Surface):
        screen.blit(self.image, self.rect)

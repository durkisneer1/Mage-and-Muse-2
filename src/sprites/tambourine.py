import pygame as pg
from random import choice
from src.constants import WIN_WIDTH, WIN_HEIGHT


class Tambourine(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, image: pg.Surface):
        super().__init__(group)

        self.left = choice([True, False])
        self.rot_direction = -1 if self.left else 1
        self.pos = pg.Vector2(0 if self.left else WIN_WIDTH, 0)

        self.direction = pg.Vector2(-self.rot_direction, 1).normalize()

        self.velocity = 18
        self.max_angle_change = 40

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

    def rotate(self, dt: float):
        self.angle += dt * 50 * self.rot_direction
        self.angle %= 360
        self.rot_image = pg.transform.rotate(self.image, self.angle)

    def update(self, dt: float, player_pos: pg.Vector2):
        self.rotate(dt)

        angle_to_player = (player_pos - self.pos).as_polar()[1] - self.direction.as_polar()[1]

        if self.pos.y < WIN_HEIGHT / 2:
            if abs(angle_to_player) > (a := self.max_angle_change * dt):
                angle_to_player = a if angle_to_player > 0 else -a
            self.direction.rotate_ip(angle_to_player)

        self.pos += self.direction * self.velocity * dt
        self.rect = self.rot_image.get_frect(center=self.pos)
        self.hitbox.center = self.rect.center = self.pos

        if not (-self.rect.w < self.rect.top < WIN_WIDTH + self.rect.w and
                -self.rect.h < self.rect.top < WIN_HEIGHT):
            self.kill()

    def draw(self, screen: pg.Surface):
        screen.blit(self.rot_image, self.rect)

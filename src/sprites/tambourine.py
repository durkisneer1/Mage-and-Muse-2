import pygame as pg
from random import choice
from src.constants import WIN_WIDTH


class Tambourine(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, image: pg.Surface):
        super().__init__(group)

        self.left = choice([True, False])
        self.rot_direction = -1 if self.left else 1
        self.pos = pg.Vector2(0 if self.left else WIN_WIDTH, 0)
        
        self.direction = pg.Vector2(1, 0)
        self.velocity = 18
        self.turn_decay = 0

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

        # move the tambourine to the player
        angle_to_player = (player_pos - self.pos).as_polar()[1] - self.direction.as_polar()[1]
        angle_delta = angle_to_player - (angle_to_player * self.turn_decay)
        self.direction.rotate_ip(angle_delta)
        self.pos += self.direction * self.velocity * dt
        self.turn_decay = min(self.turn_decay + dt / 10, 1)

        self.rect = self.rot_image.get_frect(center=self.pos)
        self.hitbox.center = self.rect.center = self.pos

    def draw(self, screen: pg.Surface):
        screen.blit(self.rot_image, self.rect)

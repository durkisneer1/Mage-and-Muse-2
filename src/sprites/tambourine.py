import pygame as pg
from random import choice
from src.constants import WIN_WIDTH


class Tambourine(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, image: pg.Surface):
        super().__init__(group)

        self.left = choice([True, False])
        self.rot_direction = -1 if self.left else 1
        self.pos = pg.Vector2(0 if self.left else WIN_WIDTH, 0)

        self.velocity = 18
        self.direction = pg.Vector2(1, 0)
        self.turning_speed = 1

        self.image = image
        self.rot_image = image.copy()
        self.rect = self.image.get_frect(center=self.pos)
        self.hitbox = self.rect.inflate(-8, -8)
        self.angle = 0
        self.health = 2

        self.track_timer = 0

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

        # angle_to_player = (player_pos - self.pos).as_polar()[1]
        # angle_delta = angle_to_player - self.direction.as_polar()[1]
        # angle_delta = max(angle_delta, 30)
        #
        # turning = 0
        # if angle_delta > 0:
        #     turning = -1
        # elif angle_delta < 0:
        #     turning = 1
        #
        # self.direction.rotate_ip(angle_delta * turning * self.turning_speed * dt)
        # self.pos += self.direction * self.velocity * dt

        self.track_timer += dt
        if self.track_timer < 10:
            self.pos.move_towards_ip(player_pos, self.velocity * dt)
            if vec := player_pos - self.pos:
                self.direction = vec.normalize()
        else:
            self.pos += self.direction * self.velocity * dt

        self.rect = self.rot_image.get_frect(center=self.pos)
        self.hitbox.center = self.rect.center = self.pos

    def draw(self, screen: pg.Surface):
        screen.blit(self.rot_image, self.rect)

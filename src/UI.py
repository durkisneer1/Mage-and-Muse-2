import pygame as pg
from src.constants import *


class HealthBar(pg.sprite.Sprite):
    def __init__(
        self,
        group: pg.sprite.Group,
        pos: tuple[int, int],
        format_side: str,
        target_obj: any,
    ):
        super().__init__(group)

        self.target = target_obj
        self.original_health = target_obj.health
        self.original_width = 160

        self.format_side = format_side
        self.pos = pos

        self.rect = pg.Rect(self.pos, (self.original_width, 3))
        self.update(target_obj)
        self.bg_rect = pg.Rect((self.rect.x, 0), (WIN_WIDTH / 2, 4))

    def update(self, target_obj: any):
        new_health = target_obj.health
        factor = new_health / self.original_health
        self.rect.width = self.original_width * factor
        if self.format_side == "left":
            self.rect.topleft = self.pos
        elif self.format_side == "right":
            self.rect.topright = self.pos

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, DARK_RED, self.bg_rect)
        pg.draw.rect(screen, RED, self.rect)


class PlayerHealth(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, target_obj: any):
        super().__init__(group)

        self.target = target_obj
        self.heart_img = pg.image.load("./res/interface/heart.png").convert_alpha()
        self.heart_rect = self.heart_img.get_rect(bottomleft=(4, WIN_HEIGHT - 4))
        self.font = pg.font.Font("./res/fonts/rainy_hearts.ttf", 16)

        self.text_pos = pg.Vector2(self.heart_rect.topright[0] + 2, self.heart_rect.topright[1] + 1)
        self.offset_vec = pg.Vector2()
        self.text_surf = self.font.render(
            f"{self.target.health}", False, BLACK
        )
        self.text_shadow = self.font.render(
            f"{self.target.health}", False, "white"
        )

    def update(self, target_obj: any):
        self.text_surf = self.font.render(
            f"{self.target.health}", False, BLACK
        )
        self.text_shadow = self.font.render(
            f"{self.target.health}", False, "white"
        )

    def draw(self, screen: pg.Surface):
        for i in range(-1, 2):
            for j in range(-1, 2):
                self.offset_vec.xy = (i, j)
                screen.blit(
                    self.text_shadow,
                    self.text_pos + self.offset_vec
                )
        screen.blit(self.text_surf, self.text_pos)
        screen.blit(self.heart_img, self.heart_rect)

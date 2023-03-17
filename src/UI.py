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

        self.img = pg.image.load("./res/interface/bar.png").convert()
        self.scaled_img = self.img
        self.rect = self.scaled_img.get_rect()

        self.format_side = format_side
        self.pos = pos
        self.update(target_obj)

        self.bg_rect = pg.Rect((self.rect.x, 0), (WIN_WIDTH / 2, 4))

    def update(self, target_obj: any):
        new_health = target_obj.health
        factor = new_health / self.original_health
        self.scaled_img = pg.transform.scale_by(self.img, (factor, 1))
        self.rect = self.scaled_img.get_rect()
        if self.format_side == "left":
            self.rect.topleft = self.pos
        elif self.format_side == "right":
            self.rect.topright = self.pos

    def draw(self, screen: pg.Surface):
        pg.draw.rect(screen, (69, 40, 60), self.bg_rect)
        screen.blit(self.scaled_img, self.rect)


class PlayerHealth(pg.sprite.Sprite):
    def __init__(self, group: pg.sprite.Group, target_obj: any):
        super().__init__(group)

        self.target = target_obj
        self.img = pg.Surface((62, 18))
        self.img.fill("black")
        self.rect = self.img.get_rect(bottomleft=(0, WIN_HEIGHT))

        self.font = pg.font.Font("./res/fonts/rainyhearts.ttf", 16)
        self.text_surf = self.font.render(
            f"Health: {self.target.health}", False, "white"
        )
        self.text_rect = self.text_surf.get_rect(
            center=(self.rect.centerx - 1, self.rect.centery)
        )

    def update(self, target_obj: any):
        self.text_surf = self.font.render(
            f"Health: {target_obj.health}", False, "white"
        )
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen: pg.Surface):
        screen.blit(self.img, self.rect)
        screen.blit(self.text_surf, self.text_rect)

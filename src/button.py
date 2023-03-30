import pygame as pg


class Button:
    def __init__(
        self,
        pos: tuple[int, int] | pg.Vector2,
        text: str,
        font: pg.font.Font,
        scale_factor: float = 1.0,
    ):
        self.pos = pg.Vector2(pos) if isinstance(pos, tuple) else pos
        offset = pg.Vector2(-1, 1)
        self.text_top = pg.transform.scale_by(
            font.render(text, False, "white"), scale_factor
        )
        self.text_bottom = pg.transform.scale_by(
            font.render(text, False, "black"), scale_factor
        )
        self.rect_top = self.text_top.get_rect(center=self.pos)
        self.rect_bottom = self.text_bottom.get_rect(center=self.pos + offset)

    def check_collision(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect_top.collidepoint(mouse_pos)

    def draw(self, screen: pg.Surface, *args):
        screen.blit(self.text_bottom, self.rect_bottom)
        screen.blit(self.text_top, self.rect_top)

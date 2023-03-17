import pygame as pg
import random
from src.constants import *
from src.support import import_folder
from src.decor import Background, Train
from src.enums import AttackType, Images
from src.player import Player, Wand
from src.maraca import Maraca
from src.bull import Bull
from src.pellet import Pellet, PelletExplode
from src.skull import Skull
from src.taco import Taco
from src.UI import HealthBar, PlayerHealth


class Gameplay:
    def __init__(self):
        # Level Setup Setup
        self.player = Player()
        self.wand = Wand()
        self.background = Background()
        self.train = Train()

        # Maraca Setup
        self.boss_group = pg.sprite.Group()
        maraca_1 = Maraca(self.boss_group, True)
        maraca_2 = Maraca(self.boss_group, False)
        Skull(self.boss_group)

        # Bull Attack Setup
        self.ATTACK_EVENT = pg.event.custom_type()
        pg.time.set_timer(self.ATTACK_EVENT, 2000)
        self.attack_group = pg.sprite.Group()
        self.bull_frames = import_folder(Images.bull_frames.value)
        self.taco_img = pg.image.load(Images.taco_img.value).convert_alpha()

        # Pellet Setup
        self.max_delay = 2.5
        self.pellet_delay = self.max_delay
        self.hit_explosion_group = pg.sprite.Group()
        self.pellet_group = pg.sprite.Group()
        self.pellet_img = pg.image.load(Images.pellet_img.value).convert()
        self.pellet_frames = import_folder(Images.pellet_frames.value)

        self.UI_group = pg.sprite.Group()
        HealthBar(self.UI_group, (0, 0), "left", maraca_1)  # Maraca Health
        HealthBar(self.UI_group, (WIN_WIDTH, 0), "right", maraca_2)  # Maraca Health
        PlayerHealth(self.UI_group, self.player)  # Player Health

    def user_input(
        self,
        mouse_click: tuple[bool, bool, bool],
        mouse_pos: tuple[int, int],
        dt: float,
    ):
        self.pellet_delay += dt
        if self.pellet_delay >= self.max_delay:
            self.pellet_delay = self.max_delay

        if mouse_click[0] and self.pellet_delay >= self.max_delay:
            Pellet(
                self.pellet_group,
                self.player.rect.center,
                self.pellet_img,
                mouse_pos,
            )
            self.pellet_delay = 0

    def adjust_ui(self, target_obj: any):
        target_obj.health -= 1
        for UI in self.UI_group:
            if target_obj.health <= 0 and hasattr(target_obj, "kill"):
                target_obj.kill()
                UI.kill()
                return
            if UI.target == target_obj:
                UI.update(target_obj)

    def collision(self):
        for boss in self.boss_group:
            for pellet in self.pellet_group:
                if boss.rect.colliderect(pellet.rect) and boss.pos.z > 0:
                    PelletExplode(
                        pellet,
                        self.hit_explosion_group,
                        pellet.pos.copy(),
                        self.pellet_frames,
                    )
                    self.adjust_ui(boss)
        for attack in self.attack_group:
            if (
                attack.hitbox.colliderect(self.player.rect)
                and not self.player.on_cooldown
                and not self.player.dashed
            ):
                self.player.hit()
                self.adjust_ui(self.player)
            for pellet in self.pellet_group:
                if attack.rect.colliderect(pellet.rect):
                    PelletExplode(
                        pellet,
                        self.hit_explosion_group,
                        pellet.pos.copy(),
                        self.pellet_frames,
                    )
                    attack.hit()

    def update(
        self,
        screen: pg.Surface,
        keys: pg.key.get_pressed,
        mouse_pos: tuple[int, int],
        events: pg.event.get,
        dt: float,
    ):
        self.collision()
        for ev in events:
            if ev.type == self.ATTACK_EVENT:
                attack_type = random.choice(list(AttackType))
                if attack_type == AttackType.BULL:
                    Bull(self.attack_group, self.bull_frames)
                elif attack_type == AttackType.TACO:
                    Taco(self.attack_group, self.taco_img)

        # Background Update
        self.background.update(dt)
        self.background.draw(screen)

        # Maraca/Skull Update
        if self.boss_group:
            sorted_bosses = sorted(self.boss_group.sprites(), key=lambda m: m.pos.z)
            for boss in sorted_bosses:
                boss.update(dt)
                boss.draw(screen)

        # Player Update
        self.player.update(dt, keys)
        self.player.draw(screen)

        # Wand Update
        self.wand.update(self.player.rect.center, mouse_pos)
        self.wand.draw(screen)

        # Train Update
        self.train.update(dt)
        self.train.draw(screen)

        # Bull Update
        for attack in self.attack_group:
            if attack.update(dt):
                attack.kill()
            attack.draw(screen)

        # Pellet Update
        for pellet in self.pellet_group:
            pellet.update(dt)
            pellet.draw(screen)
        for expl in self.hit_explosion_group:
            expl.update(dt)
            expl.draw(screen)

        for UI in self.UI_group:
            UI.draw(screen)

import pygame as pg
import random

from src.constants import *
from src.background import Background
from src.train import Train, TrainFire
from src.enums import LevelOneAttack, LevelTwoAttack
from src.pellet import Pellet, PelletExplode
from src.UI import HealthBar, PlayerHealth
from src.rain import Rain

from src.sprites.player import Player, Wand
from src.sprites.maraca import Maraca
from src.sprites.bull import Bull
from src.sprites.skull import Skull
from src.sprites.taco import Taco
from src.sprites.tambourine import Tambourine


class Gameplay:
    def __init__(self, main):
        # Main Setup
        self.main = main

        # Level Setup Setup
        self.player = Player()
        self.wand = Wand()
        self.background = Background()
        self.train = Train(main.tex.train_img)

        # Tint Setup
        self.tint_surf = pg.Surface(WIN_SIZE, pg.SRCALPHA)
        self.tint_surf.fill((0, 0, 0, 135))

        # Rain Setup
        self.rain_group = pg.sprite.Group()
        self.RAIN_EVENT = pg.event.custom_type()
        pg.time.set_timer(self.RAIN_EVENT, 50)

        # Maraca Setup
        self.boss_group = pg.sprite.Group()
        maraca_left = Maraca(self.boss_group, True)
        maraca_right = Maraca(self.boss_group, False)

        # Skull Setup
        Skull(self.boss_group, main.tex.idle_skull_img, main.tex.flower_frames, 15, 3)
        self.active_skull = Skull(
            None, main.tex.active_skull_img, main.tex.fire_eye_frames, 12, 20, True
        )

        # Attacks Setup
        self.ATTACK_EVENT = pg.event.custom_type()
        self.attack_group = pg.sprite.Group()
        pg.time.set_timer(self.ATTACK_EVENT, 2000)

        # Pellet Setup
        self.max_delay = 2.5
        self.pellet_delay = self.max_delay
        self.hit_explosion_group = pg.sprite.Group()
        self.pellet_group = pg.sprite.Group()

        # UI Setup
        self.UI_group = pg.sprite.Group()
        HealthBar(self.UI_group, (0, 0), "left", maraca_left)  # Maraca Health
        HealthBar(self.UI_group, (WIN_WIDTH, 0), "right", maraca_right)  # Maraca Health
        PlayerHealth(self.UI_group, self.player)  # Player Health

        # Game State
        self.first_level = True

    def user_input(self) -> str:
        for ev in self.main.events:
            if ev.type == pg.KEYDOWN and ev.key == pg.K_ESCAPE:
                return "pause"
        if self.player.health <= 0:
            return "exit"

        self.pellet_delay += self.main.dt
        self.pellet_delay = min(self.pellet_delay, self.max_delay)

        if self.main.mouse_click[0] and self.pellet_delay >= self.max_delay:
            Pellet(
                self.pellet_group,
                self.player.rect.center,
                self.main.tex.pellet_img,
                self.main.mouse_pos,
            )
            self.pellet_delay = 0

    def adjust_ui(self, target_obj: any) -> None:
        target_obj.hit()
        for UI in self.UI_group:
            if UI.target == target_obj:
                if (
                    target_obj.health <= 0
                    and hasattr(target_obj, "animate_death")
                    and not target_obj.animate_death
                ):
                    target_obj.animate_death = True
                    UI.kill()
                    return
                UI.update(target_obj)

    def collision(self) -> None:
        for boss in self.boss_group:
            for pellet in self.pellet_group:
                if boss.rect.colliderect(pellet.rect) and boss.pos.z > 0 and pellet.name == "player":
                    PelletExplode(
                        pellet,
                        self.hit_explosion_group,
                        pellet.pos.copy(),
                        self.main.tex.pellet_frames,
                    )
                    self.adjust_ui(boss)

        for attack in self.attack_group:
            if (
                attack.hitbox.colliderect(self.player.rect)
                and not self.player.on_cooldown
                and not self.player.dashed
            ):
                self.adjust_ui(self.player)
            if attack.rect is None:
                return
            for pellet in self.pellet_group:
                if attack.rect.colliderect(pellet.rect) and pellet.name == "player":
                    PelletExplode(
                        pellet,
                        self.hit_explosion_group,
                        pellet.pos.copy(),
                        self.main.tex.pellet_frames,
                    )
                    attack.hit()

    def queue_attacks(self):
        for ev in self.main.events:
            if ev.type == self.ATTACK_EVENT:
                if self.first_level:  # Level One Queue
                    attack_type = random.choice(list(LevelOneAttack))
                    if attack_type == LevelOneAttack.BULL:
                        Bull(self.attack_group, self.main.tex.bull_frames)
                    elif attack_type == LevelOneAttack.TACO:
                        Taco(self.attack_group, self.main.tex.taco_img, self.main.tex.cheese_img)
                    elif attack_type == LevelOneAttack.TAMBOURINE:
                        Tambourine(self.attack_group, self.main.tex.tambourine_img)
                else:  # Level Two Queue
                    attack_type = random.choice(list(LevelTwoAttack))
                    if attack_type == LevelTwoAttack.FIREBALL:
                        fireball_spawn = (
                            self.active_skull.rect.centerx,
                            self.active_skull.rect.centery + 24,
                        )
                        target_position = random.choice((20, 95, 175, 240)) + 24  # Center target
                        Pellet(
                            self.pellet_group,
                            fireball_spawn,
                            self.main.tex.fireball_img,
                            target_position,
                            turn_speed=2,
                            move_method="parabolic",
                            name="fireball",
                        )  # Fireball
                    else:
                        pass

            elif ev.type == self.RAIN_EVENT and not self.first_level:  # Rain Particles
                for i in range(50):
                    Rain(self.rain_group)

    def update(self):
        self.collision()
        self.queue_attacks()

        dt = self.main.dt
        screen = self.main.screen
        keys = self.main.keys
        mouse_pos = self.main.mouse_pos

        # Background Update
        self.background.update(dt)
        self.background.draw(screen, self.first_level)

        # Maraca/Skull Update
        if self.first_level:
            sorted_bosses = sorted(self.boss_group.sprites(), key=lambda m: m.pos.z)
            for boss in sorted_bosses:
                boss.update(dt)
                boss.draw(screen)

                # Start Level Two
                if len(self.boss_group) == 1:
                    boss.kill()
                    self.first_level = False
                    pg.time.set_timer(self.ATTACK_EVENT, 1500)
                    self.boss_group.add(self.active_skull.heart)
                    HealthBar(self.UI_group, (0, 0), "left", self.active_skull.heart, width=WIN_WIDTH)
        else:
            screen.blit(self.tint_surf, (0, 0))

            # Active Skull Update
            self.active_skull.update(dt)
            self.active_skull.draw(screen)

            # Rain Update
            for rain in self.rain_group:
                rain.update(dt)
            screen.fblits([(rain.img, rain.pos) for rain in self.rain_group])

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
            attack.update(dt, self.player.pos)
            attack.draw(screen)

        # Pellet Update
        for pellet in self.pellet_group:
            if pellet.move_method == "linear":
                pellet.linear_update(dt)
            elif pellet.move_method == "parabolic":
                if pellet.parabolic_update(dt):
                    TrainFire(self.attack_group, self.main.tex.ground_fire_frames, pellet.pos.x)
        screen.fblits([(pellet.img, pellet.pos) for pellet in self.pellet_group])

        # Hit Explosion Update
        for expl in self.hit_explosion_group:
            expl.update(dt)
        screen.fblits([(expl.img, expl.pos) for expl in self.hit_explosion_group])

        # UI Update
        for UI in self.UI_group:
            UI.draw(screen)

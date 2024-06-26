import pygame as pg

from src.constants import *
from src.states.gameplay import Gameplay
from src.states.pause import Pause
from src.states.title import Title
from src.states.controls import Controls
from src.textures import Textures
from src.enums import States


class Main:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(WIN_SIZE, pg.SCALED | pg.FULLSCREEN)  # pg.FULLSCREEN
        self.clock = pg.Clock()
        self.font = pg.Font("res/fonts/arcade_in.ttf", 32)
        self.tex = Textures()
        self.running = True

        self.game_states = {
            States.TITLE: Title(self),
            States.CONTROLS: Controls(self),
            States.GAMEPLAY: None,  # Gameplay(screen, font)
            States.PAUSE: Pause(self),
            States.LOSE: None,
            States.WIN: None,
        }

        self.dt = 0
        self.keys = ()
        self.mouse_click = ()
        self.mouse_pos = ()
        self.events = ()

        pg.display.set_caption("Mage and Muse 2")

    def end_game(self, fps_tracker: dict):
        print("\n")
        total = sum(v for v in fps_tracker.values())
        for k in sorted(fps_tracker.keys()):
            print(f"FPS: {k}\t{100 * fps_tracker[k] / total:.2f}%")
        self.running = False

    def update(self):
        self.dt = self.clock.tick() / 100
        self.keys = pg.key.get_pressed()
        self.mouse_click = pg.mouse.get_pressed()
        self.mouse_pos = pg.mouse.get_pos()
        self.events = pg.event.get()

    def run(self) -> None:
        current_state = self.game_states[States.TITLE]
        fps_tracker = {}
        while self.running:
            self.update()

            if current_state == self.game_states[States.GAMEPLAY]:
                fps = int(self.clock.get_fps())
                fps_tracker[fps] = fps_tracker.setdefault(fps, 0) + 1

            for ev in self.events:
                if ev.type == pg.QUIT:
                    self.end_game(fps_tracker)
                    return

                state = current_state.user_input(ev)
                if state is not None:
                    if state == States.EXIT:
                        self.end_game(fps_tracker)
                        return

                    if state == States.GAMEPLAY and current_state == self.game_states[States.TITLE]:
                        self.game_states[state] = Gameplay(self)

                    current_state = self.game_states[state]
                    if state == States.PAUSE or state == States.CONTROLS:
                        current_state.last_frame = self.screen.copy()

            current_state.update()
            pg.display.flip()


if __name__ == "__main__":
    game = Main()
    game.run()

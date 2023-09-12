import pygame as pg

from src.constants import *
from src.states.gameplay import Gameplay
from src.states.pause import Pause
from src.states.title import Title
from src.states.controls import Controls


class Main:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode(WIN_SIZE, pg.SCALED)  # pg.FULLSCREEN
        self.clock = pg.time.Clock()
        self.font = pg.Font("res/fonts/arcade_in.ttf", 32)

        self.game_states = {
            "title": Title(self.font),
            "controls": Controls(self.font),
            "gameplay": None,  # Gameplay(screen, font)
            "pause": Pause(self.font),
            "lose": None,
            "win": None,
        }

        self.dt = 0
        self.keys = []
        self.mouse_click = []
        self.mouse_pos = ()
        self.events = []

        pg.display.set_caption("Mage and Muse 2")

    @staticmethod
    def end_game(fps_tracker: dict):
        print("\n")
        total = sum(v for v in fps_tracker.values())
        for k in sorted(fps_tracker.keys()):
            print(f"FPS: {k}\t{100 * fps_tracker[k] / total:.2f}%")
        pg.quit()

    def run(self) -> None:
        current_state = self.game_states["title"]
        fps_tracker = {}
        while True:
            self.dt = self.clock.tick() / 100
            self.keys = pg.key.get_pressed()
            self.mouse_click = pg.mouse.get_pressed()
            self.mouse_pos = pg.mouse.get_pos()
            self.events = pg.event.get()

            if current_state == self.game_states["gameplay"]:
                fps = int(self.clock.get_fps())
                fps_tracker[fps] = fps_tracker.setdefault(fps, 0) + 1

            for ev in self.events:
                if ev.type == pg.QUIT:
                    Main.end_game(fps_tracker)
                    return

            if s := current_state.user_input(
                self.events, self.mouse_click, self.mouse_pos, self.dt, self.mouse_click
            ):
                if s == "exit":
                    Main.end_game(fps_tracker)
                    return

                if s == "gameplay" and current_state == self.game_states["title"]:
                    self.game_states[s] = Gameplay()
                current_state = self.game_states[s]
                if s == "pause" or s == "controls":
                    current_state.last_frame = self.screen.copy()

            current_state.update(self.screen, self.keys, self.mouse_pos, self.events, self.dt)
            pg.display.flip()


if __name__ == "__main__":
    game = Main()
    game.run()

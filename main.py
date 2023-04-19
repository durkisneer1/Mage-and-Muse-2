import pygame as pg

from src.constants import *
from src.states.gameplay import Gameplay
from src.states.pause import Pause
from src.states.title import Title
from src.states.controls import Controls


pg.init()

screen = pg.display.set_mode(WIN_SIZE, pg.SCALED)
pg.display.set_caption("Mage and Muse 2")
clock = pg.time.Clock()
font = pg.Font("res/fonts/arcade_in.ttf", 32)

game_states = {
    "title": Title(font),
    "controls": Controls(font),
    "gameplay": None,  # Gameplay(screen, font),
    "pause": Pause(font),
    "lose": None,
    "win": None,
}


def end_game(fps_tracker: dict):
    print("\n")
    total = sum(v for v in fps_tracker.values())
    for k in sorted(fps_tracker.keys()):
        print(f"FPS: {k}\t{100 * fps_tracker[k] / total:.2f}%")
    pg.quit()


def main() -> None:
    current_state = game_states["title"]
    fps_tracker = {}
    while True:
        dt = clock.tick() / 100
        keys = pg.key.get_pressed()
        mouse_click = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        events = pg.event.get()

        if current_state == game_states["gameplay"]:
            fps = int(clock.get_fps())
            fps_tracker[fps] = fps_tracker.setdefault(fps, 0) + 1

        for ev in events:
            if ev.type == pg.QUIT:
                end_game(fps_tracker)
                return

        if s := current_state.user_input(
            events, mouse_click, mouse_pos, dt, mouse_click
        ):
            if s == "exit":
                end_game(fps_tracker)
                return

            if s == "gameplay" and current_state == game_states["title"]:
                game_states[s] = Gameplay()
            current_state = game_states[s]
            if s == "pause" or s == "controls":
                current_state.last_frame = screen.copy()

        current_state.update(screen, keys, mouse_pos, events, dt)
        pg.display.flip()


if __name__ == "__main__":
    main()

import pygame as pg
from src.constants import *
from src.states.level import Gameplay
from src.states.pause import Pause
from src.states.title import Title
from src.states.controls import Controls

pg.init()

screen = pg.display.set_mode(WIN_SIZE, pg.SCALED)
pg.display.set_caption("Mage and Muse 2")
clock = pg.time.Clock()
letter_font = pg.font.Font("res/fonts/arcade_in.ttf", 32)

game_states = {
    "title": Title(letter_font),
    "controls": Controls(letter_font),
    "gameplay": None,
    "pause": Pause(screen.copy(), letter_font),
    "lose": None,
    "win": None,
}


def main():
    current_state = game_states["title"]
    fps_tracker = {}
    run = True
    while run:
        dt = clock.tick() / 100
        fps = int(clock.get_fps())
        fps_tracker[fps] = fps_tracker.setdefault(fps, 0) + 1

        keys = pg.key.get_pressed()
        mouse_click = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        events = pg.event.get()

        for ev in events:
            if ev.type == pg.QUIT:
                run = False
                total = sum(v for v in fps_tracker.values())
                for k in sorted(fps_tracker.keys()):
                    print(f"FPS: {k}\t{100 * fps_tracker[k] / total:.2f}%")
            if ev.type == pg.KEYDOWN:
                if ev.key == pg.K_ESCAPE:
                    if current_state == game_states["gameplay"]:
                        current_state = game_states["pause"]
                        current_state.last_frame = screen.copy()
                    elif current_state == game_states["pause"]:
                        current_state = game_states["gameplay"]

        if s := current_state.user_input(
            events, mouse_click, mouse_pos, dt, mouse_click
        ):
            if s == "gameplay":
                game_states[s] = Gameplay()
            current_state = game_states[s]
        current_state.update(screen, keys, mouse_pos, events, dt)

        pg.display.flip()


if __name__ == "__main__":
    main()

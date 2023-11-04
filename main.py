from pygame import (
    init,
    display,
    time,
    event,
    mouse,
    QUIT,
    quit,
    FULLSCREEN as FS,
    KEYDOWN,
    K_ESCAPE,
)
from sys import exit

from settings import *
from src.level import Level


class Game:
    def __init__(self) -> None:
        init()
        self.screen = (FULLSCREEN and display.set_mode((0, 0), FS)) or display.set_mode(
            (WIDTH, HEIGHT)
        )
        display.set_caption("Shadowfell")
        mouse.set_visible(False)
        self.clock = time.Clock()
        self.delta_time = 1
        self.frames = FPS

        self.level = Level(self)

    def run(self) -> None:
        while True:
            for e in event.get():
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    quit()
                    exit()

            self.screen.fill((113, 221, 238))
            self.level.run()
            display.update()
            self.delta_time = self.clock.tick(FPS)
            self.frames = self.frames * self.delta_time / 1000


if __name__ == "__main__":
    game = Game()
    game.run()

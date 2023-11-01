from pygame import display, sprite
from settings import *

from src.tile import Tile
from src.player import Player


class Level:
    def __init__(self) -> None:
        self.display_surface = display.get_surface()
        self.visible_sprites = sprite.Group()
        self.obstacle_sprites = sprite.Group()

        self.create_map()

    def run(self) -> None:
        self.visible_sprites.draw(self.display_surface)

    def create_map(self) -> None:
        for i, row in enumerate(WORLD_MAP):
            for j, tile in enumerate(row):
                x, y = j * TILE_SIZE, i * TILE_SIZE
                if tile == "x":
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif tile == "p":
                    Player((x, y), [self.visible_sprites])

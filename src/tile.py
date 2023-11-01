from pygame import sprite, image
from settings import *


class Tile(sprite.Sprite):
    def __init__(self, pos, groups) -> None:
        super().__init__(groups)
        self.image = image.load("assets/test/rock.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

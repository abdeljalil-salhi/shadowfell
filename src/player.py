from pygame import sprite, image
from settings import *


class Player(sprite.Sprite):
    def __init__(self, pos, groups) -> None:
        super().__init__(groups)
        self.image = image.load("assets/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

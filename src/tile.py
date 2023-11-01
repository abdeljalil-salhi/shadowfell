from pygame import sprite, image, Surface

from settings import *


class Tile(sprite.Sprite):
    def __init__(
        self, pos, groups, sprite_type, surface=Surface((TILE_SIZE, TILE_SIZE))
    ) -> None:
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)

        # Create a hitbox that is smaller than the tile
        self.hitbox = self.rect.inflate(0, -10)

from pygame import display, sprite, math

from settings import *
from src.tile import Tile
from src.player import Player
from debug import debug


class Level:
    def __init__(self) -> None:
        self.display_surface = display.get_surface()
        self.visible_sprites = FollowingCameraGroup()
        self.obstacle_sprites = sprite.Group()

        self.create_map()

    def run(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        debug(self.player.direction)

    def create_map(self) -> None:
        for i, row in enumerate(WORLD_MAP):
            for j, tile in enumerate(row):
                x, y = j * TILE_SIZE, i * TILE_SIZE
                if tile == "x":
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites])
                elif tile == "p":
                    self.player = Player(
                        (x, y), [self.visible_sprites], self.obstacle_sprites
                    )


class FollowingCameraGroup(sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = math.Vector2(0, 0)

    def custom_draw(self, player) -> None:
        # Offset the camera so that the player is always in the center of the screen
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        # Draw the sprites with the offset
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset)

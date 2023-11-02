from pygame import display, sprite, math, image
from random import choice

from settings import *
from debug import debug
from src.tile import Tile
from src.player import Player
from src.weapon import Weapon
from src.utils import import_csv_layout, import_folder


class Level:
    def __init__(self, game) -> None:
        self.game = game

        self.display_surface = display.get_surface()
        self.visible_sprites = FollowingCameraGroup()
        self.obstacle_sprites = sprite.Group()
        self.current_attack = None

        self.create_map()

    def run(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

        if DEBUG:
            debug(f"VECTOR: {self.player.direction}")
            debug(f"STATE: {self.player.state}", y=30)
            debug(f"FPS: {str(int(self.game.clock.get_fps()))}", y=50)

    def create_map(self) -> None:
        layouts = {
            "boundary": import_csv_layout("map/floor_blocks.csv"),
            "grass": import_csv_layout("map/grass_blocks.csv"),
            "object": import_csv_layout("map/object_blocks.csv"),
        }
        assets = {
            "grass": import_folder("assets/grass"),
            "objects": import_folder("assets/objects", True),
        }
        for style, layout in layouts.items():
            for i, row in enumerate(layout):
                for j, tile in enumerate(row):
                    if tile != "-1":
                        x, y = j * TILE_SIZE, i * TILE_SIZE
                        if style == "boundary":
                            Tile(
                                (x, y),
                                [self.obstacle_sprites],
                                "invisible",
                            )
                        elif style == "grass":
                            random_grass = choice(assets["grass"])
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "grass",
                                random_grass,
                            )
                        elif style == "object":
                            object_surface = assets["objects"][int(tile)]
                            Tile(
                                (x, y),
                                [self.visible_sprites, self.obstacle_sprites],
                                "object",
                                object_surface,
                            )
        self.player = Player(
            (2000, 1430),
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack,
        )

    def create_attack(self) -> None:
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self) -> None:
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None


class FollowingCameraGroup(sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.display_surface = display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = math.Vector2(0, 0)

        self.floor_surface = image.load("assets/tilemap/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player) -> None:
        # Offset the camera so that the player is always in the center of the screen
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw the floor with the offset
        floor_offset = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset)

        # Draw the sprites with the offset
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            offset = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset)

from pygame import display, sprite, math, image
from random import choice
from json import dump, load
from os import path

from settings import *
from debug import debug
from src.tile import Tile
from src.gui import GUI
from src.player import Player
from src.weapon import Weapon
from src.utils import import_csv_layout, import_folder


class Level:
    def __init__(self, game) -> None:
        self.game = game

        if not path.exists("data/player.json"):
            with open("data/player.json", "w") as file:
                self.player_data = {
                    "position": (2000, 1430),
                    "weapon_selected": 0,
                    "spell_selected": 0,
                    "health": 100,
                    "mana": 100,
                    "stamina": 100,
                    "armor": 0,
                    "attack_damage": 10,
                    "ability_power": 4,
                    "speed": 0.4,
                    "experience": 0,
                }
                dump(
                    self.player_data,
                    file,
                )
        else:
            with open("data/player.json", "r") as file:
                self.player_data = load(file)

        self.display_surface = display.get_surface()
        self.visible_sprites = FollowingCameraGroup()
        self.obstacle_sprites = sprite.Group()
        self.current_attack = None

        self.gui = GUI()
        self.create_map()

    def run(self) -> None:
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.gui.display(self.player)

        if DEBUG:
            width = self.display_surface.get_width()
            debug(f"VECTOR: {self.player.direction}", x=width - 200, y=10)
            debug(f"STATE: {self.player.state}", x=width - 200, y=30)
            debug(
                f"FPS: {str(int(self.game.clock.get_fps()))}",
                x=width - 200,
                y=50,
            )

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
            self.game,
            self.player_data["position"],
            [self.visible_sprites],
            self.obstacle_sprites,
            self.create_attack,
            self.destroy_attack,
            self.create_spell,
        )

    def create_attack(self) -> None:
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self) -> None:
        if self.current_attack:
            self.current_attack.kill()
            self.current_attack = None

    def create_spell(self, spell: str, efficiency: int, cost: int) -> None:
        pass


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

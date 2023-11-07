from pygame import math, display, mixer
from random import randint

from settings import *


class Spells:
    def __init__(self, game, animation_player) -> None:
        self.game = game
        self.animation_player = animation_player
        self.display_surface = display.get_surface()
        self.sounds = {
            "heal": mixer.Sound("assets/sounds/heal.wav"),
            "flame": mixer.Sound("assets/sounds/flame.wav"),
        }

    def heal(self, player, efficiency, cost, groups) -> None:
        if (
            player.stats["mana"] < cost
            or player.stats["health"] == player.initial_stats["health"]
        ):
            self.game.level.gui.display_tooltip(
                "Not enough mana" if player.stats["mana"] < cost else "Health is full",
                self.display_surface.get_width() // 2,
                self.display_surface.get_height() - 100,
            )
            return
        player.stats["mana"] -= cost
        if not MUTE:
            self.sounds["heal"].play()

        player.stats["health"] += efficiency
        if player.stats["health"] > player.initial_stats["health"]:
            player.stats["health"] = player.initial_stats["health"]

        self.animation_player.spawn_particles(
            self.game,
            "aura",
            player.rect.center,
            groups,
        )
        self.animation_player.spawn_particles(
            self.game,
            "heal",
            player.rect.center + math.Vector2(0, -40),
            groups,
        )

    def flame(self, player, cost, groups) -> None:
        if player.stats["mana"] < cost:
            self.game.level.gui.display_tooltip(
                "Not enough mana",
                self.display_surface.get_width() // 2,
                self.display_surface.get_height() - 100,
            )
            return
        player.stats["mana"] -= cost
        if not MUTE:
            self.sounds["flame"].play()

        state = player.state.split("_")[0]
        if state == "right":
            direction = math.Vector2(1, 0)
        elif state == "left":
            direction = math.Vector2(-1, 0)
        elif state == "up":
            direction = math.Vector2(0, -1)
        elif state == "down":
            direction = math.Vector2(0, 1)

        for i in range(1, 6):
            rand = randint(-TILE_SIZE // 3, TILE_SIZE // 3)

            # Horizontal flame particles
            if direction.x:
                offset_x = (direction.x * i) * TILE_SIZE
                self.animation_player.spawn_particles(
                    self.game,
                    "flame",
                    (player.rect.centerx + offset_x + rand, player.rect.centery + rand),
                    groups,
                )

            # Vertical flame particles
            elif direction.y:
                offset_y = (direction.y * i) * TILE_SIZE
                self.animation_player.spawn_particles(
                    self.game,
                    "flame",
                    (player.rect.centerx + rand, player.rect.centery + offset_y + rand),
                    groups,
                )

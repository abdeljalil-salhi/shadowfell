from pygame import math, time

from settings import *
from src.entity import Entity
from src.utils import import_folder


class Enemy(Entity):
    def __init__(self, game, groups, obstacle_sprites, position, name) -> None:
        super().__init__(groups, game)
        self.game = game

        self.name = name
        self.sprite_type = "enemy"
        self.state = "idle"
        self.import_enemy_assets(self.name)

        self.obstacle_sprites = obstacle_sprites

        self.image = self.animations[self.state][self.frame]
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -10)

        # Enemy stats

        data = ENEMY[self.name]
        self.health = data["health"]
        self.experience = data["experience"]
        self.attack = data["attack"]
        self.attack_damage = data["attack_damage"]
        self.speed = data["speed"]
        self.resistance = data["resistance"]
        self.attack_radius = data["attack_radius"]
        self.notice_radius = data["notice_radius"]

        # Player interactions

        self.able_to_attack = True
        self.attack_cooldown = 400
        self.attack_timer = None

    def update(self) -> None:
        self.move(self.speed)
        self.animate()
        self.cooldown()

    def animate(self) -> None:
        animation = self.animations[self.state]
        self.frame += self.animation_speed * self.game.delta_time
        if self.frame >= len(animation):
            if self.state == "attack":
                self.able_to_attack = False
            self.frame = 0
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def import_enemy_assets(self, name) -> None:
        path = f"assets/enemies/{name}/"
        self.animations = {
            "idle": [],
            "move": [],
            "attack": [],
        }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(path + animation)

    def actions(self, player) -> None:
        if self.state == "attack":
            self.attack_timer = time.get_ticks()
        elif self.state == "move":
            self.direction = self.get_player_direction(player)[1]
        else:
            self.direction = math.Vector2(0, 0)

    def get_player_direction(self, player) -> tuple:
        enemy_vector = math.Vector2(self.rect.center)
        player_vector = math.Vector2(player.rect.center)
        distance = (player_vector - enemy_vector).magnitude()
        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = math.Vector2(0, 0)
        return (distance, direction)

    def get_state(self, player) -> None:
        distance = self.get_player_direction(player)[0]
        if distance <= self.attack_radius and self.able_to_attack:
            if self.state != "attack":
                self.frame = 0
            self.state = "attack"
        elif distance <= self.notice_radius:
            self.state = "move"
        else:
            self.state = "idle"

    def enemy_update(self, player) -> None:
        self.get_state(player)
        self.actions(player)

    def cooldown(self) -> None:
        if not self.able_to_attack:
            if time.get_ticks() - self.attack_timer >= self.attack_cooldown:
                self.able_to_attack = True

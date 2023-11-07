from pygame import math, time

from settings import *
from src.entity import Entity
from src.utils import import_folder


class Enemy(Entity):
    def __init__(
        self,
        game,
        groups,
        obstacle_sprites,
        position,
        name,
        damage_player: callable,
        spawn_death_particles: callable,
        gain_experience: callable,
    ) -> None:
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

        self.damage_player = damage_player
        self.spawn_death_particles = spawn_death_particles
        self.gain_experience = gain_experience

        # Fight logic

        self.able_to_attack = True
        self.attack_cooldown = 400
        self.attack_timer = None

        self.can_be_attacked = True
        self.attacked_cooldown = 500
        self.attacked_timer = None

    def update(self) -> None:
        self.attacked()
        self.move(self.speed)
        self.animate()
        self.cooldown()
        self.check_death()

    def animate(self) -> None:
        animation = self.animations[self.state]

        self.frame += self.animation_speed * self.game.delta_time
        if self.frame >= len(animation):
            if self.state == "attack":
                self.able_to_attack = False
            self.frame = 0

        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.can_be_attacked:
            self.image.set_alpha(self.wave_value())
        else:
            self.image.set_alpha(255)

    def import_enemy_assets(self, name) -> None:
        self.animations = {
            "idle": [],
            "move": [],
            "attack": [],
        }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(
                f"assets/enemies/{name}/{animation}"
            )

    def actions(self, player) -> None:
        if self.state == "attack":
            self.attack_timer = time.get_ticks()
            self.damage_player(self.attack_damage, self.attack)
            player.needs_save = True

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

    def take_damage(self, player, attack_type) -> None:
        if not self.can_be_attacked:
            return

        self.direction = self.get_player_direction(player)[1]

        if attack_type == "weapon":
            self.health -= player.get_attack_damage()
        elif attack_type == "spell":
            self.health -= player.get_ability_power()

        self.attacked_timer = time.get_ticks()
        self.can_be_attacked = False

    def check_death(self) -> None:
        if self.health <= 0:
            self.kill()
            self.spawn_death_particles(self.rect.center, self.name)
            self.gain_experience(self.experience)

    def attacked(self) -> None:
        if not self.can_be_attacked:
            self.direction *= -self.resistance

    def enemy_update(self, player) -> None:
        self.get_state(player)
        self.actions(player)

    def cooldown(self) -> None:
        current_time = time.get_ticks()

        if not self.able_to_attack:
            if current_time - self.attack_timer >= self.attack_cooldown:
                self.able_to_attack = True

        if not self.can_be_attacked:
            if current_time - self.attacked_timer >= self.attacked_cooldown:
                self.can_be_attacked = True

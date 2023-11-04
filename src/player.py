from pygame import (
    sprite,
    image,
    math,
    key,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_LSHIFT,
    K_q,
    K_w,
    K_e,
    transform,
    time,
)
from json import dump, load

from settings import *
from src.utils import import_folder


class Player(sprite.Sprite):
    def __init__(
        self,
        game,
        position,
        groups,
        obstacle_sprites,
        create_attack: callable,
        destroy_attack: callable,
        create_spell: callable,
    ) -> None:
        super().__init__(groups)
        self.game = game
        self.image = transform.scale(
            image.load("assets/init/player.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE),
        )
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(0, -26)
        self.needs_save = False

        with open("data/player.json", "r") as file:
            data = load(file)

        self.obstacle_sprites = obstacle_sprites

        self.import_player_assets()
        self.state = "down_idle"
        self.frame = 0
        self.animation_speed = 0.01

        # Player stats
        self.direction = math.Vector2(0, 0)

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_timer = None

        self.health, self.max_health = data["health"] * 0.5, data["health"]
        self.mana, self.max_mana = data["mana"] * 0.8, data["mana"]
        self.stamina, self.max_stamina = data["stamina"] * 0.9, data["stamina"]
        self.armor, self.initial_armor = data["armor"], data["armor"]
        self.attack_damage, self.initial_attack_damage = (
            data["attack_damage"],
            data["attack_damage"],
        )
        self.ability_power, self.initial_ability_power = (
            data["ability_power"],
            data["ability_power"],
        )
        self.speed, self.initial_speed = data["speed"], data["speed"]
        self.experience = 0

        # Weapon stats
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_selected = data["weapon_selected"]
        self.weapon = list(WEAPON.keys())[self.weapon_selected]
        self.able_to_switch_weapon = True
        self.weapon_switch_timer = None
        self.weapon_switch_cooldown = 200

        # Spell stats
        self.create_spell = create_spell
        self.spell_selected = data["spell_selected"]
        self.spell = list(SPELL.keys())[self.spell_selected]
        self.able_to_switch_spell = True
        self.spell_switch_timer = None
        self.spell_switch_cooldown = 200

    def update(self) -> None:
        self.input()
        self.cooldown()
        self.get_state()
        self.animate()
        self.move(self.speed)
        self.save()

    def save(self) -> None:
        if self.needs_save:
            with open("data/player.json", "w") as file:
                dump(
                    {
                        "position": self.rect.topleft,
                        "weapon_selected": self.weapon_selected,
                        "spell_selected": self.spell_selected,
                        "health": self.health,
                        "mana": self.mana,
                        "stamina": self.stamina,
                        "armor": self.armor,
                        "attack_damage": self.attack_damage,
                        "ability_power": self.ability_power,
                        "speed": self.speed,
                        "experience": self.experience,
                    },
                    file,
                )
                self.needs_save = False

    def animate(self) -> None:
        animation = self.animations[self.state]
        self.frame += self.animation_speed * self.game.delta_time
        if self.frame >= len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def import_player_assets(self) -> None:
        path = "assets/player/"
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "up_idle": [],
            "down_idle": [],
            "left_idle": [],
            "right_idle": [],
            "up_attack": [],
            "down_attack": [],
            "left_attack": [],
            "right_attack": [],
        }

        for animation in self.animations.keys():
            self.animations[animation] = import_folder(path + animation)

    def input(self) -> None:
        if self.attacking:
            return

        keys = key.get_pressed()

        # Move the player
        if keys[K_UP]:
            self.direction.y, self.state = -1, "up"
        elif keys[K_DOWN]:
            self.direction.y, self.state = 1, "down"
        else:
            self.direction.y = 0
        if keys[K_LEFT]:
            self.direction.x, self.state = -1, "left"
        elif keys[K_RIGHT]:
            self.direction.x, self.state = 1, "right"
        else:
            self.direction.x = 0

        # Sprint if the player is holding shift
        if keys[K_LSHIFT]:
            self.speed = self.initial_speed * 1.5
        else:
            self.speed = self.initial_speed

        # Attack if the player is holding space
        if keys[K_SPACE]:
            self.attacking = True
            self.attack_timer = time.get_ticks()
            self.create_attack()

        # Cast a spell if the player is holding Q
        if keys[K_q]:
            self.attacking = True
            self.attack_timer = time.get_ticks()
            self.create_spell(
                list(SPELL.keys())[self.spell_selected],
                list(SPELL.values())[self.spell_selected]["efficiency"]
                + self.ability_power,
                list(SPELL.values())[self.spell_selected]["cost"],
            )

        if keys[K_w] and self.able_to_switch_weapon:
            self.able_to_switch_weapon = False
            self.weapon_switch_timer = time.get_ticks()
            self.weapon_selected = (self.weapon_selected + 1) % len(WEAPON)
            self.weapon = list(WEAPON.keys())[self.weapon_selected]
            self.needs_save = True

        if keys[K_e] and self.able_to_switch_spell:
            self.able_to_switch_spell = False
            self.spell_switch_timer = time.get_ticks()
            self.spell_selected = (self.spell_selected + 1) % len(SPELL)
            self.spell = list(SPELL.keys())[self.spell_selected]
            self.needs_save = True

    def get_state(self) -> None:
        # Idle if the player is not moving
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.state and not "attack" in self.state:
                self.state += "_idle"
                self.needs_save = True

        # Attack if the player is attacking
        if self.attacking:
            self.direction.x, self.direction.y = 0, 0
            if not "attack" in self.state:
                if "idle" in self.state:
                    self.state = self.state.replace("_idle", "_attack")
                else:
                    self.state += "_attack"
        else:
            if "attack" in self.state:
                self.state = self.state.replace("_attack", "")

    def move(self, speed: int) -> None:
        # Normalize the direction vector to prevent faster diagonal movement
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Move the player horizontally and check for collisions
        self.hitbox.x += self.direction.x * speed * self.game.delta_time
        self.collide("horizontal")
        # Move the player vertically and check for collisions
        self.hitbox.y += self.direction.y * speed * self.game.delta_time
        self.collide("vertical")

        self.rect.center = self.hitbox.center

    def collide(self, direction) -> None:
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                # Prevent the player from overlapping with the obstacle
                if sprite.hitbox.colliderect(self.hitbox):
                    # If the player is moving right, set the player's right side to the left side of the object it hit
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    # If the player is moving left, set the player's left side to the right side of the object it hit
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
        elif direction == "vertical":
            for sprite in self.obstacle_sprites:
                # Prevent the player from overlapping with the obstacle
                if sprite.hitbox.colliderect(self.hitbox):
                    # If the player is moving down, set the player's bottom side to the top side of the object it hit
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    # If the player is moving up, set the player's top side to the bottom side of the object it hit
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldown(self) -> None:
        current_time = time.get_ticks()

        if self.attacking:
            if current_time - self.attack_timer >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.able_to_switch_weapon:
            if current_time - self.weapon_switch_timer >= self.weapon_switch_cooldown:
                self.able_to_switch_weapon = True

        if not self.able_to_switch_spell:
            if current_time - self.spell_switch_timer >= self.spell_switch_cooldown:
                self.able_to_switch_spell = True

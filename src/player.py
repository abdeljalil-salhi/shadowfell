from pygame import (
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
    K_a,
    K_w,
    K_z,
    K_e,
    transform,
    time,
    mixer,
)
from json import dump, load

from settings import *
from src.utils import import_folder
from src.entity import Entity


class Player(Entity):
    def __init__(
        self,
        game,
        groups,
        position,
        obstacle_sprites,
        create_attack: callable,
        destroy_attack: callable,
        create_spell: callable,
    ) -> None:
        super().__init__(groups, game)
        self.game = game

        self.image = transform.scale(
            image.load("assets/init/player.png").convert_alpha(),
            (TILE_SIZE, TILE_SIZE),
        )
        self.rect = self.image.get_rect(topleft=position)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET["player"])
        self.needs_save = False

        with open("data/player.json", "r") as file:
            data = load(file)

        self.obstacle_sprites = obstacle_sprites

        self.import_player_assets()
        self.state = "down_idle"

        # Player stats

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_timer = None

        self.level = data["level"]
        self.experience, self.max_experience = data["experience"], 100 * self.level
        self.stats = {
            "health": data["health"],
            "mana": data["mana"],
            "stamina": data["stamina"],
            "armor": data["armor"],
            "attack_damage": data["attack_damage"],
            "ability_power": data["ability_power"],
            "speed": data["speed"],
        }
        self.initial_stats = {
            "health": PLAYER["health"],
            "mana": PLAYER["mana"],
            "stamina": PLAYER["stamina"],
            "armor": PLAYER["armor"],
            "attack_damage": PLAYER["attack_damage"],
            "ability_power": PLAYER["ability_power"],
            "speed": PLAYER["speed"],
        }
        self.upgrade_costs = {
            "health": 100,
            "mana": 100,
            "stamina": 100,
            "armor": 100,
            "attack_damage": 100,
            "ability_power": 100,
            "speed": 100,
        }

        # Weapon stats

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_selected = data["weapon_selected"]
        self.weapon = list(WEAPON.keys())[self.weapon_selected]
        self.able_to_switch_weapon = True
        self.weapon_switch_timer = None
        self.weapon_switch_cooldown = 200
        self.weapon_attack_sound = mixer.Sound("assets/sounds/sword.wav")
        self.weapon_attack_sound.set_volume(0.4)

        # Spell stats

        self.create_spell = create_spell
        self.spell_selected = data["spell_selected"]
        self.spell = list(SPELL.keys())[self.spell_selected]
        self.able_to_switch_spell = True
        self.spell_switch_timer = None
        self.spell_switch_cooldown = 200

        # Fight logic

        self.can_be_attacked = True
        self.attacked_cooldown = 800
        self.attacked_timer = None

    def update(self) -> None:
        self.input()
        self.cooldown()
        self.get_state()
        self.animate()
        self.move(self.stats["speed"])
        self.regeneration()
        self.save()

    def save(self) -> None:
        if self.needs_save:
            with open("data/player.json", "w") as file:
                dump(
                    {
                        "position": self.rect.topleft,
                        "weapon_selected": self.weapon_selected,
                        "spell_selected": self.spell_selected,
                        "level": self.level,
                        "health": self.stats["health"],
                        "mana": self.stats["mana"],
                        "stamina": self.stats["stamina"],
                        "armor": self.stats["armor"],
                        "attack_damage": self.stats["attack_damage"],
                        "ability_power": self.stats["ability_power"],
                        "speed": self.stats["speed"],
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

        if not self.can_be_attacked:
            self.image.set_alpha(self.wave_value())
        else:
            self.image.set_alpha(255)

    def import_player_assets(self) -> None:
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
            self.animations[animation] = import_folder(
                f"assets/player/{animation}", forceTransform=True
            )

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
        if (
            keys[K_LSHIFT]
            and self.stats["stamina"] > 0
            and self.direction.magnitude() != 0
        ):
            self.stats["speed"] = self.initial_stats["speed"] * 1.5
            self.stats["stamina"] -= 0.1
        else:
            self.stats["speed"] = self.initial_stats["speed"]

        # Attack if the player is holding space
        if keys[K_SPACE]:
            self.attacking = True
            self.attack_timer = time.get_ticks()
            self.create_attack()
            if not MUTE:
                self.weapon_attack_sound.play()

        # Cast a spell if the player is holding Q or A (layout dependent)
        if QWERTY and keys[K_q] or not QWERTY and keys[K_a]:
            self.attacking = True
            self.attack_timer = time.get_ticks()
            self.create_spell(
                list(SPELL.keys())[self.spell_selected],
                list(SPELL.values())[self.spell_selected]["efficiency"]
                + self.stats["ability_power"],
                list(SPELL.values())[self.spell_selected]["cost"],
            )

        if (
            QWERTY and keys[K_w] or not QWERTY and keys[K_z]
        ) and self.able_to_switch_weapon:
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

    def get_attack_damage(self) -> int:
        return self.stats["attack_damage"] + WEAPON[self.weapon]["damage"]

    def get_ability_power(self) -> int:
        return self.stats["ability_power"] + SPELL[self.spell]["efficiency"]

    def regeneration(self) -> None:
        if self.stats["mana"] < self.initial_stats["mana"]:
            self.stats["mana"] += 0.007 * self.stats["ability_power"]
        else:
            self.stats["mana"] = self.initial_stats["mana"]

        if self.stats["stamina"] < self.initial_stats["stamina"]:
            self.stats["stamina"] += 0.02 * (
                self.stats["armor"] == 0 and 1 or self.stats["armor"]
            )
        else:
            self.stats["stamina"] = self.initial_stats["stamina"]

    def cooldown(self) -> None:
        current_time = time.get_ticks()

        if self.attacking:
            if (
                current_time - self.attack_timer
                >= self.attack_cooldown + WEAPON[self.weapon]["cooldown"]
            ):
                self.attacking = False
                self.destroy_attack()

        if not self.able_to_switch_weapon:
            if current_time - self.weapon_switch_timer >= self.weapon_switch_cooldown:
                self.able_to_switch_weapon = True

        if not self.able_to_switch_spell:
            if current_time - self.spell_switch_timer >= self.spell_switch_cooldown:
                self.able_to_switch_spell = True

        if not self.can_be_attacked:
            if current_time - self.attacked_timer >= self.attacked_cooldown:
                self.can_be_attacked = True

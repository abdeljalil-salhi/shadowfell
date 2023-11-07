# Game settings

WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False

FPS = 120
TILE_SIZE = 64

DEBUG = True

# Player settings

PLAYER = {
    "health": 100,
    "mana": 100,
    "stamina": 50,
    "armor": 0,
    "attack_damage": 10,
    "ability_power": 4,
    "speed": 0.4,
}

MAX_STATS = {
    "health": 300,
    "mana": 250,
    "stamina": 80,
    "armor": 30,
    "attack_damage": 50,
    "ability_power": 40,
    "speed": 1,
}

UPGRADE_COST = {
    "health": 100,
    "mana": 100,
    "stamina": 100,
    "armor": 100,
    "attack_damage": 100,
    "ability_power": 100,
    "speed": 100,
}

WEAPON = {
    "sword": {
        "cooldown": 100,
        "damage": 15,
        "asset": "assets/weapons/sword/full.png",
    },
    "lance": {
        "cooldown": 400,
        "damage": 30,
        "asset": "assets/weapons/lance/full.png",
    },
    "axe": {
        "cooldown": 300,
        "damage": 20,
        "asset": "assets/weapons/axe/full.png",
    },
    "rapier": {
        "cooldown": 50,
        "damage": 8,
        "asset": "assets/weapons/rapier/full.png",
    },
    "sai": {
        "cooldown": 80,
        "damage": 10,
        "asset": "assets/weapons/sai/full.png",
    },
}

SPELL = {
    "flame": {
        "cost": 20,
        "efficiency": 5,
        "asset": "assets/particles/flame/full.png",
    },
    "heal": {
        "cost": 30,
        "efficiency": 20,
        "asset": "assets/particles/heal/full.png",
    },
}

HITBOX_OFFSET = {"player": -26, "object": -40, "grass": -10, "invisible": 0}

# GUI settings

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 300
MANA_BAR_WIDTH = 250
STAMINA_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
GUI_FONT_FAMILY = "assets/fonts/joystix.ttf"
GUI_FONT_SIZE = 18

WATER_COLOR = (113, 221, 238)
GUI_BACKGROUND_COLOR = "#222222"
GUI_BORDER_COLOR = "#000000"
GUI_TEXT_COLOR = "#eeeeee"
GUI_TEXT_COLOR_SELECTED = "#ffea00"

HEALTH_BAR_COLOR = "#d50000"
MANA_BAR_COLOR = "#304ffe"
STAMINA_BAR_COLOR = "#00c853"
GUI_BORDER_COLOR_ACTIVE = "#ffea00"

BAR_COLOR = "#eeeeee"
BAR_COLOR_SELECTED = "#ffea00"
UPGRADE_BG_COLOR_SELECTED = "#eeeeee"

# Enemy settings

ENEMY = {
    "squid": {
        "health": 100,
        "experience": 5,
        "attack": "slash",
        "attack_damage": 20,
        "attack_sound": "assets/sounds/attack/slash.wav",
        "speed": 0.18,
        "resistance": 3,
        "attack_radius": 80,
        "notice_radius": 360,
    },
    "raccoon": {
        "health": 300,
        "experience": 20,
        "attack": "claw",
        "attack_damage": 40,
        "attack_sound": "assets/sounds/attack/claw.wav",
        "speed": 0.1,
        "resistance": 3,
        "attack_radius": 120,
        "notice_radius": 400,
    },
    "spirit": {
        "health": 100,
        "experience": 8,
        "attack": "thunder",
        "attack_damage": 8,
        "attack_sound": "assets/sounds/attack/fireball.wav",
        "speed": 0.25,
        "resistance": 3,
        "attack_radius": 60,
        "notice_radius": 300,
    },
    "bamboo": {
        "health": 70,
        "experience": 7,
        "attack": "leaf_attack",
        "attack_damage": 6,
        "attack_sound": "assets/sounds/attack/slash.wav",
        "speed": 0.15,
        "resistance": 3,
        "attack_radius": 60,
        "notice_radius": 150,
    },
}

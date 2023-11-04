# Game settings

WIDTH = 1280
HEIGHT = 720
FULLSCREEN = False

FPS = 120
TILE_SIZE = 64

DEBUG = True

# Player settings

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

MAGIC = {
    "flame": {
        "cost": 20,
        "efficience": 5,
        "asset": "assets/particles/flame/full.png",
    },
    "heal": {
        "cost": 30,
        "efficience": 20,
        "asset": "assets/particles/heal/full.png",
    },
}

# GUI settings

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 300
MANA_BAR_WIDTH = 250
STAMINA_BAR_WIDTH = 200
ITEM_BOX_SIZE = 80
GUI_FONT_FAMILY = "assets/fonts/joystix.ttf"
GUI_FONT_SIZE = 18

WATER_COLOR = "#0d47a1"
GUI_BACKGROUND_COLOR = "#222222"
GUI_BORDER_COLOR = "#000000"
GUI_TEXT_COLOR = "#eeeeee"

HEALTH_BAR_COLOR = "#d50000"
MANA_BAR_COLOR = "#304ffe"
STAMINA_BAR_COLOR = "#00c853"
GUI_BORDER_COLOR_ACTIVE = "#ffea00"

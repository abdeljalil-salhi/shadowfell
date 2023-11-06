from pygame import display, font, Rect, draw, image, time

from settings import *


class GUI:
    def __init__(self) -> None:
        self.display_surface = display.get_surface()
        self.font = font.Font(GUI_FONT_FAMILY, GUI_FONT_SIZE)

        # Bar settings
        self.health_bar_rect = Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.mana_bar_rect = Rect(
            10, self.health_bar_rect.bottom + 3, MANA_BAR_WIDTH, BAR_HEIGHT
        )
        self.stamina_bar_rect = Rect(
            10, self.mana_bar_rect.bottom + 3, STAMINA_BAR_WIDTH, BAR_HEIGHT
        )

        # Weapon overlay settings
        self.weapon_assets = []
        for weapon in WEAPON.values():
            self.weapon_assets.append(
                image.load(weapon["asset"]).convert_alpha(),
            )

        # Spell overlay settings
        self.spell_assets = []
        for spell in SPELL.values():
            self.spell_assets.append(
                image.load(spell["asset"]).convert_alpha(),
            )

        # Tooltip settings
        self.tooltip_display = False
        self.tooltip_timer = None
        self.tooltip_duration = 1000
        self.tooltip_text = None
        self.tooltip_position = None

    def display(self, player) -> None:
        self.display_bar(
            player.health,
            player.max_health,
            self.health_bar_rect,
            HEALTH_BAR_COLOR,
        )
        self.display_bar(
            player.mana, player.max_mana, self.mana_bar_rect, MANA_BAR_COLOR
        )
        self.display_bar(
            player.stamina,
            player.max_stamina,
            self.stamina_bar_rect,
            STAMINA_BAR_COLOR,
        )

        self.display_experience(player.experience)

        self.weapon_overlay(player.weapon_selected, not player.able_to_switch_weapon)
        self.spell_overlay(player.spell_selected, not player.able_to_switch_spell)

        if self.tooltip_display:
            self.display_tooltip(
                self.tooltip_text,
                *self.tooltip_position,
            )
            if time.get_ticks() - self.tooltip_timer >= self.tooltip_duration:
                self.tooltip_display = False
                self.tooltip_text = None

    def display_bar(self, current, max_amount, background_rect, color) -> None:
        draw.rect(
            self.display_surface,
            GUI_BACKGROUND_COLOR,
            background_rect,
        )
        draw.rect(
            self.display_surface,
            color,
            (
                background_rect.x,
                background_rect.y,
                background_rect.width * (current / max_amount),
                background_rect.height,
            ),
        )
        draw.rect(
            self.display_surface,
            GUI_BORDER_COLOR,
            background_rect,
            3,
        )

    def display_experience(self, experience) -> None:
        text_surface = self.font.render(f"{int(experience)} EXP", False, GUI_TEXT_COLOR)
        text_rect = text_surface.get_rect(
            bottomright=(
                self.display_surface.get_width() - 20,
                self.display_surface.get_height() - 20,
            )
        )
        draw.rect(
            self.display_surface,
            GUI_BACKGROUND_COLOR,
            text_rect.inflate(20, 10),
        )
        self.display_surface.blit(text_surface, text_rect)
        draw.rect(
            self.display_surface,
            GUI_BORDER_COLOR,
            text_rect.inflate(20, 10),
            3,
        )

    def display_tooltip(self, text: str, x: int, y: int) -> None:
        if self.tooltip_text != text:
            self.tooltip_timer = time.get_ticks()
            self.tooltip_text = text
            self.tooltip_position = (x, y)
            self.tooltip_display = True

        text_surface = self.font.render(text, False, GUI_TEXT_COLOR)
        text_rect = text_surface.get_rect(
            center=(x, y),
        )
        draw.rect(
            self.display_surface,
            GUI_BACKGROUND_COLOR,
            text_rect.inflate(20, 10),
        )
        self.display_surface.blit(text_surface, text_rect)
        draw.rect(
            self.display_surface,
            GUI_BORDER_COLOR,
            text_rect.inflate(20, 10),
            3,
        )

    def display_item_box(self, left, top, has_switched: bool) -> Rect:
        background_rect = Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        draw.rect(
            self.display_surface,
            GUI_BACKGROUND_COLOR,
            background_rect,
        )
        if has_switched:
            draw.rect(
                self.display_surface,
                GUI_BORDER_COLOR_ACTIVE,
                background_rect,
                3,
            )
        else:
            draw.rect(
                self.display_surface,
                GUI_BORDER_COLOR,
                background_rect,
                3,
            )
        return background_rect

    def weapon_overlay(self, weapon_selected: int, has_switched: bool) -> None:
        background_rect = self.display_item_box(
            10,
            self.display_surface.get_height() - ITEM_BOX_SIZE - 10,
            has_switched,
        )
        weapon_surface = self.weapon_assets[weapon_selected]
        weapon_rect = weapon_surface.get_rect(
            center=background_rect.center,
        )
        self.display_surface.blit(weapon_surface, weapon_rect)

    def spell_overlay(self, spell_selected: int, has_switched: bool) -> None:
        background_rect = self.display_item_box(
            ITEM_BOX_SIZE,
            self.display_surface.get_height() - ITEM_BOX_SIZE - 5,
            has_switched,
        )
        spell_surface = self.spell_assets[spell_selected]
        spell_rect = spell_surface.get_rect(
            center=background_rect.center,
        )
        self.display_surface.blit(spell_surface, spell_rect)

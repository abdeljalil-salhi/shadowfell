from pygame import display, key, font, time, K_RIGHT, K_LEFT, K_SPACE, Rect, draw, math

from settings import *


class Upgrade:
    def __init__(self, player) -> None:
        self.display_surface = display.get_surface()
        self.player = player
        self.font = font.Font(GUI_FONT_FAMILY, GUI_FONT_SIZE)

        # PLayer statistics
        self.stats = player.stats
        self.stats_length = len(self.stats)
        self.stats_names = list(self.stats.keys())
        self.max_values = list(MAX_STATS.values())

        # Selection settings
        self.selection = 0
        self.selection_timer = None
        self.able_to_move = True

        # Item settings
        self.height = self.display_surface.get_height() * 0.8
        self.width = self.display_surface.get_width() // (self.stats_length + 1)
        self.item_list = []
        self.create_items()

    def display(self) -> None:
        self.input()
        self.cooldown()

        for index, item in enumerate(self.item_list):
            item.display(
                self.display_surface,
                self.selection,
                self.stats_names[index],
                list(self.player.stats.values())[index],
                self.max_values[index],
                list(self.player.upgrade_costs.values())[index],
            )

    def input(self) -> None:
        keys = key.get_pressed()

        if not self.able_to_move:
            return

        if keys[K_RIGHT]:
            self.selection += 1
            if self.selection >= self.stats_length:
                self.selection = 0
            self.able_to_move = False
            self.selection_timer = time.get_ticks()
        elif keys[K_LEFT]:
            self.selection -= 1
            if self.selection < 0:
                self.selection = self.stats_length - 1
            self.able_to_move = False
            self.selection_timer = time.get_ticks()

        elif keys[K_SPACE]:
            self.able_to_move = False
            self.selection_timer = time.get_ticks()
            self.item_list[self.selection].trigger(self.player)

    def create_items(self) -> None:
        for item, index in enumerate(range(self.stats_length)):
            increment = self.display_surface.get_width() // self.stats_length
            left = (item * increment) + (increment - self.width) // 2
            top = self.display_surface.get_height() * 0.1
            self.item_list.append(
                Item(left, top, self.width, self.height, index, self.font)
            )

    def cooldown(self) -> None:
        if not self.able_to_move:
            if time.get_ticks() - self.selection_timer >= 300:
                self.able_to_move = True


class Item:
    def __init__(self, left, top, width, height, index, font) -> None:
        self.rect = Rect(left, top, width, height)
        self.index = index
        self.font = font

    def display(self, surface, selection, name, value, max_value, cost) -> None:
        if selection == self.index:
            draw.rect(
                surface,
                GUI_BACKGROUND_COLOR,
                self.rect,
            )
            draw.rect(
                surface,
                GUI_BORDER_COLOR_ACTIVE,
                self.rect,
                4,
            )
        else:
            draw.rect(
                surface,
                GUI_BACKGROUND_COLOR,
                self.rect,
            )
            draw.rect(
                surface,
                GUI_BORDER_COLOR,
                self.rect,
                4,
            )
        self.display_names(surface, name, cost, selection == self.index)
        self.display_bar(surface, value, max_value, selection == self.index)

    def display_names(self, surface, name: str, cost, selected) -> None:
        words = name.split("_")
        lines, line = [], ""

        color = GUI_TEXT_COLOR_SELECTED if selected else GUI_TEXT_COLOR

        for word in words:
            current_line = f"{line} {word}".strip()
            current_line_width = self.font.size(current_line)[0]
            if current_line_width > self.rect.width:
                lines.append(line)
                line = word
            else:
                line = current_line

        lines.append(line)

        for index, line in enumerate(lines):
            text_surface = self.font.render(line, False, color)
            text_rect = text_surface.get_rect(
                center=(
                    self.rect.centerx,
                    self.rect.centery + (index * 20) - self.rect.height // 2 + 20,
                ),
            )
            surface.blit(text_surface, text_rect)

        if cost == 0:
            cost_surface = self.font.render("MAX", False, color)
        else:
            cost_surface = self.font.render(f"{int(cost)} EXP", False, color)
        cost_rect = cost_surface.get_rect(
            midbottom=(self.rect.midbottom - math.Vector2(0, 20),),
        )
        surface.blit(cost_surface, cost_rect)

    def display_bar(self, surface, value, max_value, selected) -> None:
        top = self.rect.midtop + math.Vector2(0, 60)
        bottom = self.rect.midbottom - math.Vector2(0, 60)
        color = BAR_COLOR_SELECTED if selected else BAR_COLOR

        try:
            full_height = bottom.y - top.y
            current_height = full_height * (value / max_value)
        except ZeroDivisionError:
            current_height = 0
        value_rect = Rect(
            top.x - 15,
            bottom.y - current_height,
            30,
            10,
        )

        draw.line(surface, color, top, bottom, 5)
        draw.rect(surface, color, value_rect)

    def trigger(self, player) -> None:
        upgrade_attribute = list(player.stats.keys())[self.index]
        if (
            player.experience >= player.upgrade_costs[upgrade_attribute]
            and player.stats[upgrade_attribute] < MAX_STATS[upgrade_attribute]
        ):
            player.experience -= player.upgrade_costs[upgrade_attribute]
            player.upgrade_costs[upgrade_attribute] *= 1.2
            player.stats[upgrade_attribute] *= 1.07
            player.needs_save = True

        if player.stats[upgrade_attribute] >= MAX_STATS[upgrade_attribute]:
            player.stats[upgrade_attribute] = MAX_STATS[upgrade_attribute]
            player.upgrade_costs[upgrade_attribute] = 0

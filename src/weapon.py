from pygame import sprite, image, math

from src.player import Player


class Weapon(sprite.Sprite):
    def __init__(self, player: Player, groups) -> None:
        super().__init__(groups)
        direction = player.state.split("_")[0]
        self.image = image.load(
            f"assets/weapons/{player.weapon}/{direction}.png"
        ).convert_alpha()

        if direction == "up":
            self.rect = self.image.get_rect(
                midbottom=player.rect.midtop + math.Vector2(-10, 0)
            )
        elif direction == "down":
            self.rect = self.image.get_rect(
                midtop=player.rect.midbottom + math.Vector2(-10, 0)
            )
        elif direction == "right":
            self.rect = self.image.get_rect(
                midleft=player.rect.midright + math.Vector2(0, 16)
            )
        else:
            self.rect = self.image.get_rect(
                midright=player.rect.midleft + math.Vector2(0, 16)
            )

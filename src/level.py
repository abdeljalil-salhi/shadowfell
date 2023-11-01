from pygame import sprite


class Level:
    def __init__(self) -> None:
        self.visible_sprites = sprite.Group()
        self.obstacle_sprites = sprite.Group()

    def run(self) -> None:
        pass

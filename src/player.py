from pygame import sprite, image, math, key, K_w, K_a, K_s, K_d

from settings import *


class Player(sprite.Sprite):
    def __init__(self, pos, groups) -> None:
        super().__init__(groups)
        self.image = image.load("assets/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)

        self.direction = math.Vector2(0, 0)
        self.speed = 5

    def update(self) -> None:
        self.input()
        self.move(self.speed)

    def input(self) -> None:
        keys = key.get_pressed()
        if keys[K_w]:
            self.direction.y = -1
        elif keys[K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[K_a]:
            self.direction.x = -1
        elif keys[K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed: int) -> None:
        # Normalize the direction vector to prevent faster diagonal movement
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        # Move the player in the direction of the vector
        self.rect.center += self.direction * speed

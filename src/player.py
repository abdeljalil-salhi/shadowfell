from pygame import sprite, image, math, key, K_w, K_a, K_s, K_d

from settings import *


class Player(sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites) -> None:
        super().__init__(groups)
        self.image = image.load("assets/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.obstacle_sprites = obstacle_sprites

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
        # Move the player horizontally and check for collisions
        self.rect.x += self.direction.x * speed
        self.collide("horizontal")
        # Move the player vertically and check for collisions
        self.rect.y += self.direction.y * speed
        self.collide("vertical")

    def collide(self, direction) -> None:
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                # Prevent the player from overlapping with the obstacle
                if sprite.rect.colliderect(self.rect):
                    # If the player is moving right, set the player's right side to the left side of the object it hit
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    # If the player is moving left, set the player's left side to the right side of the object it hit
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right
        elif direction == "vertical":
            for sprite in self.obstacle_sprites:
                # Prevent the player from overlapping with the obstacle
                if sprite.rect.colliderect(self.rect):
                    # If the player is moving down, set the player's bottom side to the top side of the object it hit
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    # If the player is moving up, set the player's top side to the bottom side of the object it hit
                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

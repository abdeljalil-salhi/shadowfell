from pygame import sprite, math, time
from math import sin


class Entity(sprite.Sprite):
    def __init__(self, groups, game) -> None:
        super().__init__(groups)
        self.game = game

        self.frame = 0
        self.animation_speed = 0.01
        self.direction = math.Vector2(0, 0)

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

    def wave_value(self) -> int:
        if sin(time.get_ticks()) >= 0:
            return 255
        else:
            return 0

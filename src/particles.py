from pygame import sprite, transform
from random import choice

from src.utils import import_folder


class ParticleEffect(sprite.Sprite):
    def __init__(self, game, position, frames, groups) -> None:
        super().__init__(groups)
        self.game = game

        self.frame = 0
        self.animation_speed = 0.01
        self.frames = frames
        self.image = self.frames[self.frame]
        self.rect = self.image.get_rect(center=position)

    def update(self) -> None:
        self.animate()

    def animate(self) -> None:
        self.frame += self.animation_speed * self.game.delta_time
        if self.frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame)]


class AnimationPlayer:
    def __init__(self) -> None:
        self.frames = {
            # Spells
            "flame": import_folder("assets/particles/flame/frames", isParticle=True),
            "aura": import_folder("assets/particles/aura", isParticle=True),
            "heal": import_folder("assets/particles/heal/frames", isParticle=True),
            # Physical attacks
            "claw": import_folder("assets/particles/claw", isParticle=True),
            "slash": import_folder("assets/particles/slash", isParticle=True),
            "sparkle": import_folder("assets/particles/sparkle", isParticle=True),
            "leaf_attack": import_folder(
                "assets/particles/leaf_attack", isParticle=True
            ),
            "thunder": import_folder("assets/particles/thunder", isParticle=True),
            # Enemies deaths
            "squid": import_folder("assets/particles/smoke_orange", isParticle=True),
            "raccoon": import_folder("assets/particles/raccoon", isParticle=True),
            "spirit": import_folder("assets/particles/nova", isParticle=True),
            "bamboo": import_folder("assets/particles/bamboo", isParticle=True),
            # Leafs
            "leaf": (
                import_folder("assets/particles/leaves/leaf1", isParticle=True),
                import_folder("assets/particles/leaves/leaf2", isParticle=True),
                import_folder("assets/particles/leaves/leaf3", isParticle=True),
                import_folder("assets/particles/leaves/leaf4", isParticle=True),
                import_folder("assets/particles/leaves/leaf5", isParticle=True),
                import_folder("assets/particles/leaves/leaf6", isParticle=True),
                self.reflect_frames(
                    import_folder("assets/particles/leaves/leaf1", isParticle=True)
                ),
                self.reflect_frames(
                    import_folder("assets/particles/leaves/leaf2", isParticle=True)
                ),
                self.reflect_frames(
                    import_folder("assets/particles/leaves/leaf3", isParticle=True)
                ),
                self.reflect_frames(
                    import_folder("assets/particles/leaves/leaf4", isParticle=True)
                ),
                self.reflect_frames(
                    import_folder("assets/particles/leaves/leaf5", isParticle=True)
                ),
                self.reflect_frames(
                    import_folder("assets/particles/leaves/leaf6", isParticle=True)
                ),
            ),
        }

    def reflect_frames(self, frames) -> list:
        reflected_frames = []
        for frame in frames:
            reflected_frames.append(transform.flip(frame, True, False))
        return reflected_frames

    def spawn_grass_particles(self, game, position, groups) -> None:
        frames = choice(self.frames["leaf"])
        ParticleEffect(game, position, frames, groups)

    def spawn_particles(self, game, type: str, position, groups) -> None:
        frames = self.frames[type]
        ParticleEffect(game, position, frames, groups)

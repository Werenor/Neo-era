import pygame
from neoera.render.animation.animation_queue import AnimationQueue
from neoera.render.animation.animation import Animation
from neoera.render.animation.tween import Tween
from neoera.core.resource_manager import RESOURCE_MANAGER


class SpriteObject:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.surface = RESOURCE_MANAGER.load_image(name)
        self.x = x
        self.y = y
        self.scale = 1.0
        self.alpha = 255
        self.animations = AnimationQueue()

    def draw(self, screen):
        if not self.surface:
            return

        surf = self.surface.copy()
        surf.set_alpha(int(self.alpha))

        if self.scale != 1.0:
            w, h = surf.get_size()
            surf = pygame.transform.scale(
                surf,
                (int(w * self.scale), int(h * self.scale))
            )

        screen.blit(surf, (self.x, self.y))


class SpriteManager:
    def __init__(self):
        self.sprites = {}

    # -----------------------------------------------------
    # Basic show/hide
    # -----------------------------------------------------
    def show(self, name, x, y):
        self.sprites[name] = SpriteObject(name, x, y)

    def hide(self, name):
        if name in self.sprites:
            del self.sprites[name]

    # -----------------------------------------------------
    # Animations
    # -----------------------------------------------------
    def move(self, name, x, y, duration):
        if name not in self.sprites:
            return
        sp = self.sprites[name]

        tw_x = Tween(sp, "x", sp.x, x, duration)
        tw_y = Tween(sp, "y", sp.y, y, duration)
        anim = Animation([tw_x, tw_y])
        sp.animations.push(anim)

    def fade_in(self, name, duration):
        if name not in self.sprites:
            return
        sp = self.sprites[name]
        sp.alpha = 0
        tw = Tween(sp, "alpha", 0, 255, duration)
        anim = Animation([tw])
        sp.animations.push(anim)

    def fade_out(self, name, duration):
        if name not in self.sprites:
            return
        sp = self.sprites[name]
        tw = Tween(sp, "alpha", sp.alpha, 0, duration)
        anim = Animation([tw])
        sp.animations.push(anim)

    def scale(self, name, scale, duration):
        if name not in self.sprites:
            return
        sp = self.sprites[name]
        tw = Tween(sp, "scale", sp.scale, scale, duration)
        anim = Animation([tw])
        sp.animations.push(anim)

    # -----------------------------------------------------
    # Update + Draw
    # -----------------------------------------------------
    def update(self, dt):
        for sp in self.sprites.values():
            sp.animations.update(dt)

    def draw(self, screen):
        for sp in self.sprites.values():
            sp.draw(screen)

    # -----------------------------------------------------
    # Animation state check (for WAIT_ANIMATION)
    # -----------------------------------------------------
    def animating(self):
        return any(sp.animations.active() for sp in self.sprites.values())

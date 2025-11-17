import pygame
from neoera.core.resource_manager import RESOURCE_MANAGER


class SpriteManager:
    """
    管理立绘：
    - 支持任意数量
    - 每个立绘有：pos / alpha / scale
    """

    def __init__(self, screen_width, screen_height):
        self.sprites = {}  # key=path, value=dict(...)
        self.w = screen_width
        self.h = screen_height

    def show_sprite(self, path, pos="center", alpha=255, scale=1.0):
        img = RESOURCE_MANAGER.load_image(path)
        if img is None:
            print(f"[SpriteManager] Cannot load {path}")
            return

        w = img.get_width() * scale
        h = img.get_height() * scale
        img = pygame.transform.smoothscale(img, (int(w), int(h)))

        if pos == "left":
            x = self.w * 0.15
        elif pos == "right":
            x = self.w * 0.85 - w
        else:
            x = (self.w - w) // 2

        y = self.h - h - 50

        self.sprites[path] = {
            "img": img,
            "x": x,
            "y": y,
            "alpha": alpha,
            "target_alpha": alpha,
            "path": path,
        }

        img.set_alpha(alpha)

    def hide_sprite(self, path):
        if path in self.sprites:
            del self.sprites[path]

    def update(self, dt):
        # alpha 过渡（简单版）
        for sp in self.sprites.values():
            current = sp["alpha"]
            target = sp["target_alpha"]
            if current != target:
                if current < target:
                    current += dt * 255 / 0.3
                    if current > target:
                        current = target
                else:
                    current -= dt * 255 / 0.3
                    if current < target:
                        current = target
                sp["alpha"] = int(current)
                sp["img"].set_alpha(sp["alpha"])

    def draw(self, screen):
        for sp in self.sprites.values():
            screen.blit(sp["img"], (sp["x"], sp["y"]))

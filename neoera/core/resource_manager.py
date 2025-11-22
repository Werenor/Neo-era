import pygame
from neoera.core.config import CONFIG


class ResourceManager:
    def __init__(self):
        self.images = {}
        self.fonts = {}
        self.bgms = {}

    # ---- Image ----
    def load_image(self, path):
        if path in self.images:
            return self.images[path]

        try:
            img = pygame.image.load(path).convert_alpha()
            self.images[path] = img
            return img
        except Exception as e:
            print(f"[ResourceManager] Failed to load image {path}: {e}")
            return None

    # ---- Font ----
    def load_font(self, path=None, size=24):
        if path is None:
            path = CONFIG.FONT_PATH

        key = (path, size)
        if key not in self.fonts:
            try:
                self.fonts[key] = pygame.font.Font(path, size)
            except Exception as e:
                print(f"[ResourceManager] Failed to load font {path}: {e}")
                self.fonts[key] = pygame.font.Font(None, size)

        return self.fonts[key]

    # ---- BGM ----
    def load_bgm(self, path):
        return path  # pygame mixer 使用路径即可


RESOURCE_MANAGER = ResourceManager()

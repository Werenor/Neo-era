import pygame
from neoera.core.config import CONFIG


class ResourceManager:
    """
    加载图片、BGM、字体等资源。
    内部自动走缓存，避免重复 load。
    """

    def __init__(self):
        self.images = {}
        self.bgm_loaded = {}
        self.fonts = {}

    def load_image(self, path):
        if path in self.images:
            return self.images[path]

        try:
            img = pygame.image.load(path)
            self.images[path] = img
            return img
        except Exception as e:
            print(f"[ResourceManager] 无法加载图片 {path}: {e}")
            return None

    def load_bgm(self, path):
        return path  # pygame 直接用路径播放，不需要提前缓存

    def load_font(self, size=24):
        key = (CONFIG.FONT_PATH, size)
        if key not in self.fonts:
            self.fonts[key] = pygame.font.Font(CONFIG.FONT_PATH, size)
        return self.fonts[key]


RESOURCE_MANAGER = ResourceManager()

import os


class Config:
    def __init__(self):
        self.RESOLUTION = (1280, 720)
        self.WIDTH = self.RESOLUTION[0]
        self.HEIGHT = self.RESOLUTION[1]
        self.FPS = 60

        # 全局路径
        self.ASSETS_BASE = "assets"
        self.FONT_PATH = os.path.join(self.ASSETS_BASE, "fonts", "NotoSansSC-Regular.ttf")
        self.BG_PATH = os.path.join(self.ASSETS_BASE, "bg")
        self.SPRITE_PATH = os.path.join(self.ASSETS_BASE, "sprite")
        self.BGM_PATH = os.path.join(self.ASSETS_BASE, "bgm")

    def set_resolution(self, w, h):
        self.RESOLUTION = (w, h)


CONFIG = Config()

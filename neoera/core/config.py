import os


class Config:
    """
    全局配置中心：
    - 分辨率
    - 字体路径
    - 资源目录
    """

    def __init__(self):
        self.RESOLUTION = (1920, 1080)
        self.FPS = 60

        # 全局资源路径
        self.ASSETS_BASE = "assets"
        self.FONT_PATH = os.path.join(self.ASSETS_BASE, "fonts", "NotoSansSC-Regular.ttf")
        self.BGM_PATH = os.path.join(self.ASSETS_BASE, "bgm")
        self.BG_PATH = os.path.join(self.ASSETS_BASE, "bg")
        self.SPRITE_PATH = os.path.join(self.ASSETS_BASE, "sprite")

    def get_font_path(self):
        return self.FONT_PATH

    def set_resolution(self, width, height):
        self.RESOLUTION = (width, height)


CONFIG = Config()

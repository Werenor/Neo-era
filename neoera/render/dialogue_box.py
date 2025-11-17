import pygame
from neoera.core.config import CONFIG
from neoera.core.resource_manager import RESOURCE_MANAGER


class DialogueBox:
    """
    简单文本框：
    - 半透明背景
    - 支持多行文本
    - 自动换行
    - show(text) 显示文本
    - draw(surface) 绘制
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.text = ""
        self.font = RESOURCE_MANAGER.load_font(28)

        self.rect = pygame.Rect(
            50,
            height - 250,
            width - 100,
            200
        )

        self.bg_color = (0, 0, 0, 160)

        # 渲染缓存
        self.text_surfaces = []

    def set_text(self, text):
        self.text = text
        self.text_surfaces = self._wrap_text(text)

    def _wrap_text(self, text):
        """自动换行：按 rect 宽度分行"""

        surfaces = []
        words = text.split(" ")
        line = ""

        for w in words:
            test = (line + " " + w).strip()
            ts = self.font.render(test, True, (255, 255, 255))
            if ts.get_width() > self.rect.width - 40:
                # 换行
                surfaces.append(self.font.render(line, True, (255, 255, 255)))
                line = w
            else:
                line = test

        if line:
            surfaces.append(self.font.render(line, True, (255, 255, 255)))

        return surfaces

    def draw(self, screen):
        # 背景
        s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        s.fill(self.bg_color)
        screen.blit(s, (self.rect.x, self.rect.y))

        # 文本
        y = self.rect.y + 20
        for ts in self.text_surfaces:
            screen.blit(ts, (self.rect.x + 20, y))
            y += ts.get_height() + 8

import pygame
from neoera.core.resource_manager import RESOURCE_MANAGER
from neoera.core.config import CONFIG


class DialogueBox:
    """
    v2.5 DialogueBox 具备：
    - 打字机效果（typewriter）
    - 打字机加速（按键跳过）
    - 支持字体切换
    - 支持 name box（未来扩展）
    """

    def __init__(self):
        w, h = CONFIG.RESOLUTION
        self.rect = pygame.Rect(60, h - 240, w - 120, 180)

        self.font = RESOURCE_MANAGER.load_font(size=32)

        self.visible = True
        self.full_text = ""
        self.display_text = ""
        self.type_pos = 0

        # 打字机速度（每秒多少字符）
        self.type_speed = 60
        self.timer = 0

        # 是否正在进行打字机
        self.typing = False
        self.skip_flag = False
        self.clicked = False

    # --------------------------------------------------------
    # 设置文字（启动打字机）
    # --------------------------------------------------------
    def set_text(self, text):
        self.full_text = text
        self.display_text = ""
        self.type_pos = 0
        self.typing = True
        self.skip_flag = False

    # --------------------------------------------------------
    # 字体切换
    # --------------------------------------------------------
    def change_font(self, path, size):
        self.font = RESOURCE_MANAGER.load_font(path, size)

    # --------------------------------------------------------
    # 更新：打字机逻辑
    # --------------------------------------------------------
    def update(self, dt):
        if not self.typing:
            return

        if self.skip_flag:
            # 跳过 → 直接显示完整文本
            self.display_text = self.full_text
            self.typing = False
            return

        self.timer += dt
        chars_to_show = int(self.timer * self.type_speed)

        if chars_to_show > 0:
            self.timer -= chars_to_show / self.type_speed

            self.type_pos += chars_to_show
            self.display_text = self.full_text[:self.type_pos]

            if self.type_pos >= len(self.full_text):
                self.typing = False

    # --------------------------------------------------------
    # 外部调用：用户点击跳过打字机
    # --------------------------------------------------------
    def skip(self):
        if self.typing:
            self.skip_flag = True

    # --------------------------------------------------------
    # 绘制
    # --------------------------------------------------------
    def draw(self, screen):
        if not self.visible:
            return

        # 背景框
        bg = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 180))
        screen.blit(bg, (self.rect.x, self.rect.y))

        # 绘制文字
        y = self.rect.y + 20
        for line in self.display_text.split("\n"):
            surf = self.font.render(line, True, (255, 255, 255))
            screen.blit(surf, (self.rect.x + 20, y))
            y += surf.get_height() + 8

    # --------------------------------------------------------
    # 点击事件处理（推进剧情 / 跳过打字机）
    # --------------------------------------------------------
    def handle_event(self, event):
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 若正在打字 → 跳过
            if self.typing:
                self.skip()
                return True

            # 若已完整显示 → 通知 Executor 可以继续
            # DialogueBox 本身不保存 clicked 状态，由 Executor 处理
            if hasattr(self, "clicked"):
                self.clicked = True
            else:
                self.clicked = True
            return True

        return False

import pygame
from neoera.core.resource_manager import RESOURCE_MANAGER
from neoera.render.animation.tween import Tween
from neoera.render.animation.animation import Animation
from neoera.render.animation.animation_queue import AnimationQueue


class ChoiceUI:
    """
    v2.5 Choice UI:
    - 动画进入（淡入 + 从下移入）
    - hover 效果（加亮）
    - 点击返回 index
    """

    def __init__(self):
        self.font = RESOURCE_MANAGER.load_font(size=32)

        self.visible = False
        self.options = []
        self.rects = []
        self.base_y = 260

        # 进入动画参数
        self.alpha = 0
        self.offset_y = 30

        self.anim = AnimationQueue()

    # --------------------------------------------------------
    # 显示选项（带动画）
    # --------------------------------------------------------
    def show_options(self, options):
        self.options = options
        self.visible = True
        self.rects = []

        y = self.base_y
        for opt in options:
            self.rects.append(pygame.Rect(240, y, 800, 60))
            y += 80

        # 初始为透明且下移
        self.alpha = 0
        self.offset_y = 30

        # 动画：alpha 0→255 & y 下移
        tw1 = Tween(self, "alpha", 0, 255, 0.35, easing="ease_out")
        tw2 = Tween(self, "offset_y", 30, 0, 0.35, easing="ease_out")

        self.anim.push(Animation([tw1, tw2]), parallel=True)

    # --------------------------------------------------------
    # 点击检测
    # --------------------------------------------------------
    def handle_click(self, pos):
        if not self.visible:
            return None

        x, y = pos

        for idx, r in enumerate(self.rects):
            rect = pygame.Rect(r.x, r.y + self.offset_y, r.width, r.height)
            if rect.collidepoint(x, y):
                self.visible = False
                return idx

        return None

    # --------------------------------------------------------
    # 更新（动画）
    # --------------------------------------------------------
    def update(self, dt):
        if self.visible:
            self.anim.update(dt)

    # --------------------------------------------------------
    # 绘制
    # --------------------------------------------------------
    def draw(self, screen):
        if not self.visible:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for idx, r in enumerate(self.rects):
            rect = pygame.Rect(r.x, r.y + self.offset_y, r.width, r.height)

            hovered = rect.collidepoint(mouse_x, mouse_y)

            color = (80, 80, 80) if hovered else (40, 40, 40)
            s = pygame.Surface(rect.size)
            s.fill(color)
            s.set_alpha(int(self.alpha))
            screen.blit(s, rect)

            # 文本
            txt = self.font.render(self.options[idx], True, (255, 255, 255))
            screen.blit(txt, (rect.x + 20, rect.y + 15))

    # --------------------------------------------------------
    # 事件处理（统一接口）
    # --------------------------------------------------------
    def handle_event(self, event):
        if not self.visible:
            return None

        # 左键点击
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            idx = self.handle_click(pos)
            return idx  # 若点击命中，返回选项 index

        return None

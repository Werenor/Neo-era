import pygame
from neoera.core.resource_manager import RESOURCE_MANAGER
from neoera.render.animation.tween import Tween
from neoera.render.animation.animation import Animation
from neoera.render.animation.animation_queue import AnimationQueue
from neoera.core.config import CONFIG


class BackgroundLayerObject:
    """
    单个背景层对象（多层背景支持）
    """
    def __init__(self, img, alpha=255, offset=(0, 0)):
        self.img = img
        self.alpha = alpha
        self.offset = offset


class Background:
    """
    v2.5 Background:
    - 支持淡入淡出
    - 支持 crossfade
    - 支持多层背景
    - 支持未来 slide/zoom 过渡
    """

    def __init__(self):
        self.layers = []        # 可扩展为多背景层
        self.current = None     # 当前背景图像
        self.next_bg = None     # 下一个背景
        self.transitioning = False

        self.animations = AnimationQueue()

    def set(self, path, fade=True, duration=0.6):
        """
        切换背景：
        fade = True → 淡出淡入
        fade = False → 直接切换
        """
        img = RESOURCE_MANAGER.load_image(path)
        if img is None:
            print("[Background] Failed to load:", path)
            return

        if self.current is None or not fade:
            # 无需渐变
            self.current = img
            return

        # 启动 crossfade
        self.next_bg = img
        self.transitioning = True

        # 动画：current.alpha 255 → 0
        #       next_bg.alpha   0 → 255
        self.current_alpha = 255
        self.next_alpha = 0

        tw1 = Tween(self, "current_alpha", 255, 0, duration, easing="ease_out")
        tw2 = Tween(self, "next_alpha", 0, 255, duration, easing="ease_in")

        self.animations.push(Animation([tw1, tw2]), parallel=True)

    # --------------------------------------------------------
    # 更新
    # --------------------------------------------------------
    def update(self, dt):
        if self.transitioning:
            self.animations.update(dt)
            if not self.animations.active():
                # 完成
                self.current = self.next_bg
                self.next_bg = None
                self.transitioning = False

    # --------------------------------------------------------
    # 绘制
    # --------------------------------------------------------
    def draw(self, screen):
        if self.current:
            surf = self.current.copy()
            surf.set_alpha(255)
            screen.blit(surf, (0, 0))

        if self.transitioning and self.next_bg:
            # 绘制 old（淡出）
            old = self.current.copy()
            old.set_alpha(int(self.current_alpha))
            screen.blit(old, (0, 0))

            # 绘制 new（淡入）
            new = self.next_bg.copy()
            new.set_alpha(int(self.next_alpha))
            screen.blit(new, (0, 0))
